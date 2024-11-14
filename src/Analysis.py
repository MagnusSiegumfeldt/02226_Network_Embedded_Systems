
import sys
from itertools import pairwise

from Parser.TopologyParser import TopologyParser
from Parser.StreamParser import StreamParser

from ShortestPathManager import ShortestPathManager

from Topology import Switch
from Stream import Stream
from Topology import Link

MAX_PRIO = 8
BANDWIDTH = (10 ** 9) / 8 # in bits
# TODO: WE ARE NOT USING BANDWIDTH

    
def main():
    if len(sys.argv) != 3:
        print("Usage: python analysis.py [topology.csv] [streams.csv]")
        return
    
    topology_file_name = sys.argv[1]
    streams_file_name = sys.argv[2]


    topology_parser = TopologyParser()
    topology = topology_parser.parse(topology_file_name)
    
    stream_parser = StreamParser()
    streams = stream_parser.parse(streams_file_name)

    shortest_path_manager = ShortestPathManager(topology)

    for s in streams:
        route = shortest_path_manager.get_route(s.src, s.dest)
        for device in route[1:-1]:
            device.add_stream(s)


    for s in streams:
        route = shortest_path_manager.get_route(s.src, s.dest)
        for (src, dst) in pairwise(route):
            src.add_stream(s)
            link = topology.get_link(src, dst)
            link.add_stream(s)

    for s in streams:
        stream_delay = 0
        route = shortest_path_manager.get_route(s.src, s.dest)
        print(list(pairwise(route)))
        for hop_pair in pairwise(route):

            hop_delay = compute_hop_delay(topology, *hop_pair, s)
            stream_delay += hop_delay

        print(s, "Delay:", round(stream_delay * 10 ** 6, 3), "\t", route)


def compute_hop_delay(topology, src : Switch, dst : Switch, stream : Stream):
    link = topology.get_link(src, dst)

    H = filter(lambda x: x.pcp > stream.pcp, link.get_streams())
    L = filter(lambda x: x.pcp < stream.pcp, link.get_streams())

    bH = sum(x.size for x in H) # Sum size of high prio streams out of src
    rH = sum(x.rate for x in H) # Sum rate of high prio streams out of src
    lL = max([x.size for x in L], default=0)

       
    r = link.rate

    I = filter(lambda x: x.pcp == stream.pcp, link.get_streams())
    max_delay = 0
    for j in I:
        bj = j.size
        lj = j.size

        Cj = filter(lambda x: x.pcp == stream.pcp and x != j, link.get_streams())
        bCj = sum(x.size for x in Cj)

        delay = (((bH + bCj + (bj - lj) + lL) / (r - rH)) + (lj / r))
        max_delay = max(delay, max_delay)

    return max_delay

if __name__ == "__main__":
    main()