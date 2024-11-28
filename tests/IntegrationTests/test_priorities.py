from Parser.TopologyParser import TopologyParser
from Parser.StreamParser import StreamParser

from Analyzer import Analyzer

# Verifies that higher priority streams have lower delays than lower priority streams.
def test_priorities_small():
    topology_parser = TopologyParser()
    topology = topology_parser.parse("./tests/inputs/topologies/t_small.csv")    

    stream_parser = StreamParser()
    streams = stream_parser.parse("./tests/inputs/streams/s_small.csv")    

    analyzer = Analyzer()
    delays = analyzer.analyse(topology, streams)

    assert(delays["F0"] <= delays["F1"] <= delays["F2"])
    assert(delays["F0"] <= delays["F1"] <= delays["F3"])
    
# Verifies that more conflicting streams results in higher delays.
def test_priorities_compare():
    topology_parser = TopologyParser()
    topology = topology_parser.parse("./tests/inputs/topologies/t_small.csv")    

    stream_parser = StreamParser()
    s1 = stream_parser.parse("./tests/inputs/streams/s_delay1.csv")
    s2 = stream_parser.parse("./tests/inputs/streams/s_delay2.csv")    

    analyzer = Analyzer()
    d1 = analyzer.analyse(topology, s1)
    d2 = analyzer.analyse(topology, s2)

    assert(d1["F0"] < d2["F0"])

    assert(d1["F1"] == d1["F2"])
    assert(d2["F1"] == d2["F2"] == d2["F3"] == d2["F4"] == d2["F5"] == d2["F6"])

    assert(d1["F1"] < d2["F2"])

def test_priorities_simple_1():
    topology_parser = TopologyParser()
    topology = topology_parser.parse("./tests/inputs/topologies/t_simple.csv")    

    stream_parser = StreamParser()
    streams = stream_parser.parse("./tests/inputs/streams/s_simple1.csv")
    
    analyzer = Analyzer()
    wcd = analyzer.analyse(topology, streams)
    
    assert(wcd["S1"] >= wcd["S2"])
    assert(wcd["S1"] > wcd["S3"])

def test_priorities_simple_2():
    topology_parser = TopologyParser()
    topology = topology_parser.parse("./tests/inputs/topologies/t_simple.csv")    

    stream_parser = StreamParser()
    streams = stream_parser.parse("./tests/inputs/streams/s_simple2.csv")
    
    analyzer = Analyzer()
    wcd = analyzer.analyse(topology, streams)
    
    
    assert(wcd["S5"] < wcd["S4"] == wcd["S3"] < wcd["S2"] == wcd["S1"])



def test_priorities_simple_3():
    topology_parser = TopologyParser()
    topology = topology_parser.parse("./tests/inputs/topologies/t_simple.csv")    

    stream_parser = StreamParser()
    streams = stream_parser.parse("./tests/inputs/streams/s_simple3.csv")
    
    analyzer = Analyzer()
    wcd = analyzer.analyse(topology, streams)
    
    assert(wcd["S1"] == wcd["S2"])
    assert(wcd["S3"] == wcd["S4"] == wcd["S5"])
    assert(wcd["S7"] == wcd["S8"])
    assert(wcd["S9"] == wcd["S10"] == wcd["S11"])
    
    assert(wcd["S1"] > wcd["S3"] > wcd["S6"])
    assert(wcd["S7"] > wcd["S9"] > wcd["S12"])