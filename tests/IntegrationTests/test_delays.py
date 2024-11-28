from Parser.TopologyParser import TopologyParser
from Parser.StreamParser import StreamParser

from Constants import *

from Analyzer import Analyzer

# Verifies that simple per hop delays are calculated correctly
def test_delay_calculation_1():
    topology_parser = TopologyParser()
    topology = topology_parser.parse("./tests/inputs/topologies/t_small.csv")    

    stream_parser = StreamParser()
    streams = stream_parser.parse("./tests/inputs/streams/s_delay1.csv")    

    analyzer = Analyzer()
    delays = analyzer.analyse(topology, streams)

    expected = {}
    expected["F0"] = round(((240000 / (BANDWIDTH - (160000 / 4000 + 80000 / 3000))) + (320000/BANDWIDTH)) * 10 ** 6, 3)
    expected["F1"] = round((400000 / (BANDWIDTH) + 160000/BANDWIDTH) * 10 ** 6, 3)
    expected["F2"] = round((400000 / (BANDWIDTH) + 160000/BANDWIDTH) * 10 ** 6, 3)
    
    
    assert(delays["F0"] == expected["F0"])
    assert(delays["F1"] == expected["F1"])
    assert(delays["F2"] == expected["F2"])
    
    

def test_delay_calculation_2():
    topology_parser = TopologyParser()
    topology = topology_parser.parse("./tests/inputs/topologies/t_simple.csv")    

    stream_parser = StreamParser()
    streams = stream_parser.parse("./tests/inputs/streams/s_simple1.csv")    

    analyzer = Analyzer()
    delays = analyzer.analyse(topology, streams)

    expected = {}

    expected["S1"] = round(10 ** 6 * (((80 + 80) / (BANDWIDTH - (80/20000))) + 80/BANDWIDTH + 80 / (BANDWIDTH - (80/20000)) + 80/BANDWIDTH), 3)
    expected["S2"] = round(10 ** 6 * (80/BANDWIDTH + 80/BANDWIDTH + 80/BANDWIDTH + 80/BANDWIDTH), 3)
    expected["S3"] = round(10 ** 6 * (((80 + 80) / (BANDWIDTH - (80/20000))) + 80/BANDWIDTH + 80/BANDWIDTH), 3)
    
    assert(delays["S1"] == expected["S1"])
    assert(delays["S2"] == expected["S2"])
    assert(delays["S3"] == expected["S3"])

def test_delay_calculation_3():
    topology_parser = TopologyParser()
    topology = topology_parser.parse("./tests/inputs/topologies/t_small.csv")    

    stream_parser = StreamParser()
    streams = stream_parser.parse("./tests/inputs/streams/s_small.csv")    

    analyzer = Analyzer()
    delays = analyzer.analyse(topology, streams)

    expected = {}
    expected["F0"] = round(10 ** 6 * (3200/BANDWIDTH + 2400/BANDWIDTH), 3)
    expected["F1"] = round(10 ** 6 * ((2400 + 3200)/BANDWIDTH + 1600/BANDWIDTH), 3)
    expected["F2"] = round(10 ** 6 * max(((2400 + 1600 + 3200)/(BANDWIDTH - (2400/2000 + 1600/2000)) + 800/BANDWIDTH),((2400 + 1600 + 800)/(BANDWIDTH - (2400/2000 + 1600/2000)) + 3200/BANDWIDTH)), 3)
    expected["F3"] = round(10 ** 6 * max(((2400 + 1600 + 3200)/(BANDWIDTH - (2400/2000 + 1600/2000)) + 800/BANDWIDTH),((2400 + 1600 + 800)/(BANDWIDTH - (2400/2000 + 1600/2000)) + 3200/BANDWIDTH)), 3)
    
    assert(delays["F0"] == expected["F0"])
    assert(delays["F1"] == expected["F1"])
    assert(delays["F2"] == expected["F2"])
    assert(delays["F3"] == expected["F3"])