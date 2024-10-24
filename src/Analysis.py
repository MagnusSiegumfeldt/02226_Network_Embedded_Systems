
import sys
from itertools import pairwise

from Parser.TopologyParser import TopologyParser
from Parser.StreamParser import StreamParser

from ShortestPathManager import ShortestPathManger

from Topology import Switch
from Stream import Stream
from Topology import Link

MAX_PRIO = 8
BANDWIDTH = 10 ** 9 # in bytes

    


def main():
    if len(sys.argv) != 3:
        print("Usage: python analysis.py [topology.csv] [streams.csv]")
    
    topology_file_name = sys.argv[1]
    streams_file_name = sys.argv[2]


    topology_parser = TopologyParser()
    topology = topology_parser.parse(topology_file_name)
    
    stream_parser = StreamParser()
    streams = stream_parser.parse(streams_file_name)

    shortest_path_manager = ShortestPathManger(topology)

    for s in streams:
        
        route = shortest_path_manager.get_route(s.src, s.dest)
        print(route)
        for device in route[1:-1]:
            
            device.add_stream(s)


    for s in streams:
        route = shortest_path_manager.get_route(s.src, s.dest)
        for (src, dst) in pairwise(route):
            link = topology.get_link(src, dst)
            link.add_stream(s)

    r = BANDWIDTH
    for s in streams:
        stream_delay = 0
        route = shortest_path_manager.get_route(s.src, s.dest)
        for hop_pair in pairwise(route):
            hop_delay = compute_hop_delay(topology, *hop_pair, s)
            stream_delay += hop_delay

        print("Stream:", s, "Delay", round(stream_delay * 10 ** 6, 3), route)

def compute_hop_delay(topology, src : Switch, dst : Switch, stream : Stream):
    
    priority = stream.pcp
    link = topology.get_link(src, dst)
    
    streams_through_link = link.get_streams()
    
    max_delay = 0
    I = filter(lambda x: x is not None, [s if s.pcp == priority else None for s in streams_through_link])
    for j in I:
    
        bj = j.size
        lj = j.size

        r = link.rate

        bH = sum([s.size if s.pcp > priority else 0 for s in streams_through_link])
        bCj = sum([s.size if (s.pcp == j.pcp and s != stream) else 0 for s in streams_through_link])
        lL = max([s.size if s.pcp < priority else 0 for s in streams_through_link])
        rhat_H = sum([s.rate if s.pcp > priority else 0 for s in streams_through_link])
        
        # with j in I. I defined as all streams with same link and same priority
        delay = (((bH + bCj + (bj - lj) + lL) / (r - rhat_H)) + (lj / r))
        max_delay = max(max_delay, delay)
        
    return max_delay


            

    



















if __name__ == "__main__":
    main()