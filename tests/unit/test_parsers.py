from Parser.TopologyParser import TopologyParser
from Parser.StreamParser import StreamParser
from Topology.EndSystem import EndSystem
from Topology.Switch import Switch


def check_device(topology, n, t):
    return any(type(topology.devices[k]) is t and n == topology.devices[k].name for k in topology.devices.keys())

def check_link(topology, e1, e2):
    return any((e1 == a and e2 == b) or (e1 == b and e2 == a) for (a, b) in topology.links.keys())

def test_parse_topology_1():
    parser = TopologyParser()

    topology = parser.parse("./tests/inputs/simple_topology.csv")    
    assert(len(topology.devices) == 4)
    assert(len(topology.links) == 3)
    
    # Check Topology
    assert(check_device(topology, "A", EndSystem))
    assert(check_device(topology, "B", Switch))
    assert(check_device(topology, "C", EndSystem))
    assert(check_device(topology, "D", EndSystem))

    assert(check_link(topology, "A", "B"))
    assert(check_link(topology, "B", "C"))
    assert(check_link(topology, "B", "D"))

    # Check nothing non-defined exists
    assert(not check_device(topology, "A", Switch))
    assert(not check_device(topology, "B", EndSystem))
    assert(not check_link(topology, "A", "C"))
    assert(not check_link(topology, "A", "D"))
    assert(not check_link(topology, "C", "D"))


def test_routing_topology_2():
    parser = TopologyParser()

    topology = parser.parse("./tests/inputs/medium_topology.csv")    
    assert(len(topology.devices) == 8)
    assert(len(topology.links) == 8)
    
    # Check Topology
    assert(check_device(topology, "A", EndSystem))
    assert(check_device(topology, "B", EndSystem))
    assert(check_device(topology, "C", EndSystem))
    assert(check_device(topology, "D", Switch))
    assert(check_device(topology, "E", Switch))
    assert(check_device(topology, "F", Switch))
    assert(check_device(topology, "G", EndSystem))
    assert(check_device(topology, "H", Switch))

    assert(check_link(topology, "A", "D"))
    assert(check_link(topology, "B", "D"))
    assert(check_link(topology, "C", "D"))
    assert(check_link(topology, "C", "F"))
    assert(check_link(topology, "D", "E"))
    assert(check_link(topology, "E", "G"))
    assert(check_link(topology, "F", "H"))
    assert(check_link(topology, "G", "H"))

    # Check nothing non-defined exists
    assert(not check_device(topology, "A", Switch))
    assert(not check_device(topology, "B", Switch))
    assert(not check_device(topology, "C", Switch))
    assert(not check_device(topology, "D", EndSystem))

    assert(not check_device(topology, "null", Switch))
    assert(not check_device(topology, "null", EndSystem))

    assert(not check_link(topology, "A", "C"))
    assert(not check_link(topology, "A", "E"))
    assert(not check_link(topology, "G", "F"))


def check_stream(streams, str, src, dst, sz, prd):
    return any(str == stream.name and src == stream.src and dst == stream.dest and sz == stream.size and prd == stream.period for stream in streams)

def test_parse_streams_1():
    parser = StreamParser()

    streams = parser.parse("./tests/inputs/simple_streams.csv")    
    assert(len(streams) == 6)
    
    assert(check_stream(streams, "F0", "A", "C", 80, 20000))
    assert(check_stream(streams, "F1", "A", "C", 80, 20000))
    assert(check_stream(streams, "F2", "D", "C", 80, 20000))
    assert(check_stream(streams, "F3", "D", "C", 80, 20000))

    