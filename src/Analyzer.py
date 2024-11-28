
import sys
from itertools import pairwise



from ShortestPathManager import ShortestPathManager

from Topology import Switch
from Stream import Stream
from Topology import Link

from Constants import *


class Analyzer:
    def analyse(self, topology, streams):
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

        delays = {}
        for s in streams:
            stream_delay = 0
            route = shortest_path_manager.get_route(s.src, s.dest)
            for hop_pair in pairwise(route):

                hop_delay = compute_hop_delay(topology, *hop_pair, s)
                stream_delay += hop_delay

            d = round(stream_delay * 10 ** 6, 3)
            delays[s.name] = d
        return delays

def compute_hop_delay(topology, src : Switch, dst : Switch, stream : Stream):
    link = topology.get_link(src, dst)

    H = list(filter(lambda x: x.pcp > stream.pcp, link.get_streams()))
    L = list(filter(lambda x: x.pcp < stream.pcp, link.get_streams()))

    bH = sum(x.size for x in H) # Sum size of high prio streams out of src
    rH = sum(x.rate for x in H) # Sum rate of high prio streams out of src
    lL = max([x.size for x in L], default=0)

    
    r = link.rate

    I = list(filter(lambda x: x.pcp == stream.pcp, link.get_streams()))
    max_delay = 0
    for j in I:
        bj = j.size
        lj = j.size

        Cj = list(filter(lambda x: x != j, I))
        bCj = sum(x.size for x in Cj)

        delay = (((bH + bCj + (bj - lj) + lL) / (r - rH)) + (lj / r))
        max_delay = max(delay, max_delay)

    return max_delay

