from Parser.TopologyParser import TopologyParser
from Parser.StreamParser import StreamParser
from Topology.EndSystem import EndSystem
from Topology.Switch import Switch

# Verifies that topology is parsed correctly
def test_parse_topology_1():
    parser = TopologyParser()

    topology = parser.parse("./tests/inputs/simple_topology.csv")    
    assert(len(topology.devices) == 4)
    assert(len(topology.links) == 3)

    check_device = lambda n, t: any(type(topology.devices[k]) is t and n == topology.devices[k].name for k in topology.devices.keys())
    check_link =   lambda e1, e2: any((e1 == a and e2 == b) or (e1 == b and e2 == a) for (a, b) in topology.links.keys())
    
    # Check Topology
    assert(check_device("A", EndSystem))
    assert(check_device("B", Switch))
    assert(check_device("C", EndSystem))
    assert(check_device("D", EndSystem))

    assert(check_link("A", "B"))
    assert(check_link("B", "C"))
    assert(check_link("B", "D"))

    # Wrong checks
    assert(not check_device("A", Switch))
    assert(not check_device("B", EndSystem))
    assert(not check_link("A", "C"))
    assert(not check_link("A", "D"))
    assert(not check_link("C", "D"))


def test_parse_topology_2():
    pass
    """
    parser = TopologyParser()

    topology = parser.parse("./tests/inputs/simple_topology.csv")    
    print(topology.devices)
    assert(len(topology.devices) == 328)
    assert(len(topology.links) == 409)
    """ 


# Verifies that streams are parsed correctly.
def test_parse_streams_1():
    parser = StreamParser()

    streams = parser.parse("./tests/inputs/simple_streams.csv")    
    assert(len(streams) == 6)
    