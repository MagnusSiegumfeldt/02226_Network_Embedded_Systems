
import sys
from itertools import pairwise

from Parser.TopologyParser import TopologyParser
from Parser.StreamParser import StreamParser

from ShortestPathManager import ShortestPathManger

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

    print(streams)

    for s in streams:
        route = shortest_path_manager.get_route(s.src, s.dest)
        for hop_pair in pairwise(route):
            pass

    



















if __name__ == "__main__":
    main()