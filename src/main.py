import sys
import timeit
import statistics

from Parser.TopologyParser import TopologyParser
from Parser.StreamParser import StreamParser
from Analyzer import Analyzer
from Output import OutputGenerator

from Parser.ResultParser import ResultParser
def main():
    if len(sys.argv) not in [4, 5]:
        print("Usage: python main.py [topology.csv] [streams.csv] [output.csv] ([omnet_simulation.rca])")
        return
    topology_file_name = sys.argv[1]
    streams_file_name = sys.argv[2]
    output_file_path = sys.argv[3]
    
    if len(sys.argv) == 5:
        simulation_res_file_name = sys.argv[4]
        res_parser = ResultParser()
        res_parser.parse(simulation_res_file_name)

    start = timeit.default_timer()
    topology_parser = TopologyParser()
    topology = topology_parser.parse(topology_file_name)
    
    stream_parser = StreamParser()
    streams = stream_parser.parse(streams_file_name)

    
    analyzer = Analyzer()
    delays, routes = analyzer.analyse(topology, streams)
    stop = timeit.default_timer()
    elapsed_time = stop - start
    mean_e2e = statistics.mean(delays.values())
    data = []
    for s in streams:
        data.append({"flowname": s.name, "max_e2e": delays[s.name], "route": routes[s.name], "deadline": s.deadline})
    OutputGenerator.write_csv_to_file(output_file_path, ["flowname", "max_e2e", "route", "deadline"], data, elapsed_time, mean_E2E=mean_e2e)
    #print(delays)




if __name__ == "__main__":
    main()