from Parser.TopologyParser import TopologyParser
from Parser.StreamParser import StreamParser

from Analyzer import Analyzer

# Verifies that higher priority streams have lower delays than lower priority streams.
def test_priorities_small():
    topology_parser = TopologyParser()
    topology = topology_parser.parse("./tests/inputs/small_topology.csv")    

    stream_parser = StreamParser()
    streams = stream_parser.parse("./tests/inputs/small_streams.csv")    

    analyzer = Analyzer()
    delays = analyzer.analyse(topology, streams)

    assert(delays["F0"] <= delays["F1"] <= delays["F2"])
    assert(delays["F0"] <= delays["F1"] <= delays["F3"])
    
# Verifies that more conflicting streams results in higher delays.
def test_priorities():
    topology_parser = TopologyParser()
    topology = topology_parser.parse("./tests/inputs/small_topology.csv")    

    stream_parser = StreamParser()
    s1 = stream_parser.parse("./tests/inputs/delay1.csv")
    s2 = stream_parser.parse("./tests/inputs/delay2.csv")    

    analyzer = Analyzer()
    d1 = analyzer.analyse(topology, s1)
    d2 = analyzer.analyse(topology, s2)

    assert(d1["F0"] < d2["F0"])

    assert(d1["F1"] == d1["F2"] == d1["F3"])
    assert(d2["F1"] == d2["F2"] == d2["F3"] == d2["F4"] == d2["F5"] == d2["F6"])

    assert(d1["F1"] < d2["F2"])


