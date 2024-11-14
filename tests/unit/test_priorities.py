import pytest


from Parser.TopologyParser import TopologyParser
from Parser.StreamParser import StreamParser

from Analyzer import Analyzer

def test_priorities_small():
    topology_parser = TopologyParser()
    topology = topology_parser.parse("./tests/inputs/small_topology.csv")    

    stream_parser = StreamParser()
    streams = stream_parser.parse("./tests/inputs/small_streams.csv")    

    analyzer = Analyzer()
    delays = analyzer.analyse(topology, streams)
    
    assert(delays["F0"] <= delays["F1"] <= delays["F2"])
    