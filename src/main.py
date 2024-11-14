import sys
from Parser.TopologyParser import TopologyParser
from Parser.StreamParser import StreamParser
from Analyzer import Analyzer


def main():
    if len(sys.argv) != 3:
        print("Usage: python main.py [topology.csv] [streams.csv]")
    
    topology_file_name = sys.argv[1]
    streams_file_name = sys.argv[2]


    topology_parser = TopologyParser()
    topology = topology_parser.parse(topology_file_name)
    
    stream_parser = StreamParser()
    streams = stream_parser.parse(streams_file_name)

    
    analyzer = Analyzer()
    analyzer.analyse(topology, streams)



if __name__ == "__main__":
    main()