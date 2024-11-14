from Parser.TopologyParser import TopologyParser
from Parser.StreamParser import StreamParser


# Verifies that topology is parsed correctly
def test_parse_topology_1():
    parser = TopologyParser()

    topology = parser.parse("./tests/inputs/simple_topology.csv")    
    assert(len(topology.devices) == 4)
    assert(len(topology.links) == 3)
    

# TODO: Implement further tests
def test_parse_topology_2():
    pass
    """
    parser = TopologyParser()

    topology = parser.parse("./examples/small_topology2.csv")    
    print(topology.devices)
    assert(len(topology.devices) == 328)
    assert(len(topology.links) == 409)
    """


# Verifies that streams are parsed correctly.
def test_parse_streams_1():
    parser = StreamParser()

    streams = parser.parse("./tests/inputs/simple_streams.csv")    
    assert(len(streams) == 6)
    