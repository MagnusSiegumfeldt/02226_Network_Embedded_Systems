import sys
from Parser.TopologyParser import TopologyParser
from Parser.StreamParser import StreamParser
from Analyzer import Analyzer
from Parser.ResultParser import ResultParser

def main():
    if len(sys.argv) not in [3, 4]:
        print("Usage: python main.py [topology.csv] [streams.csv]")
        print("or usage: python main.py [topology.csv] [streams.csv] [simulation.sca]")
        return
    
    topology_file_name = sys.argv[1]
    streams_file_name = sys.argv[2]
    
    if len(sys.argv) == 4:
        simulation_res_file_name = sys.argv[3]
        res_parser = ResultParser()
        res_parser.parse(simulation_res_file_name)
    
    topology_parser = TopologyParser()
    topology = topology_parser.parse(topology_file_name)
    
    stream_parser = StreamParser()
    streams = stream_parser.parse(streams_file_name)

    
    analyzer = Analyzer()
    delays = analyzer.analyse(topology, streams)
    
    for k in delays.keys():
        print(k + ":\t", delays[k])
    



if __name__ == "__main__":
    main()