from Parser.TopologyParser import TopologyParser
from Parser.StreamParser import StreamParser

from Constants import *

from Analyzer import Analyzer

# Verifies that simple per hop delays are calculated correctly
def test_delay_calculation():
    topology_parser = TopologyParser()
    topology = topology_parser.parse("./tests/inputs/small_topology.csv")    

    stream_parser = StreamParser()
    streams = stream_parser.parse("./tests/inputs/delay1.csv")    

    analyzer = Analyzer()
    delays = analyzer.analyse(topology, streams)

    expected = {}
    expected["F0"] = round(((240000 / (BANDWIDTH - (160000 / 4000 + 80000 / 3000))) + (320000/BANDWIDTH)) * 10 ** 6, 3)
    expected["F1"] = round((400000 / (BANDWIDTH) + 160000/BANDWIDTH) * 10 ** 6, 3)
    expected["F2"] = round((400000 / (BANDWIDTH) + 160000/BANDWIDTH) * 10 ** 6, 3)
    
    
    assert(delays["F0"] == expected["F0"])
    assert(delays["F1"] == expected["F1"])
    assert(delays["F2"] == expected["F2"])
    
    

def test_delay_calculation_4_streams_2_ES_1_Switch():
    topology_parser = TopologyParser()
    topology = topology_parser.parse("./tests/inputs/2_ES_1_Switch_4_Streams/topology.csv")

    stream_parser = StreamParser()
    streams = stream_parser.parse("./tests/inputs/2_ES_1_Switch_4_Streams/streams.csv")

    analyzer = Analyzer()
    delays = analyzer.analyse(topology, streams)

    expected = {}
    expected["F0"] = round((778 + 783) / 10**9 + 878 / 10**9)
    assert(delays["F0"] == expected["F0"])
