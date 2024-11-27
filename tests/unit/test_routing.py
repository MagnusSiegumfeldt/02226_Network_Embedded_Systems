from Parser.TopologyParser import TopologyParser
from Parser.StreamParser import StreamParser
from Topology.EndSystem import EndSystem
from Topology.Switch import Switch
from ShortestPathManager import ShortestPathManager

def check_route(route, res):
    return all(x.name == y for x, y in zip(route, res))

# Verifies that topology is parsed correctly
def test_routing_1():
    parser = TopologyParser()

    topology = parser.parse("./tests/inputs/simple_topology.csv")    
    spm = ShortestPathManager(topology)
    assert(check_route(spm.get_route("A", "B"), ["A", "B"]))
    assert(check_route(spm.get_route("A", "C"), ["A", "B", "C"]))
    assert(check_route(spm.get_route("A", "D"), ["A", "B", "D"]))
    assert(check_route(spm.get_route("C", "D"), ["C", "B", "D"]))

def test_routing_2():
    parser = TopologyParser()

    topology = parser.parse("./tests/inputs/medium_topology.csv")    
    spm = ShortestPathManager(topology)
    
    assert(check_route(spm.get_route("C", "G"), ["C", "D", "E", "G"]) or check_route(spm.get_route("C", "G"), ["C", "F", "H", "G"]))
    assert(check_route(spm.get_route("G", "B"), ["G", "E", "D", "B"]))
    assert(check_route(spm.get_route("C", "B"), ["C", "D", "B"]))
    assert(check_route(spm.get_route("B", "C"), ["B", "D", "C"]))
    assert(check_route(spm.get_route("A", "B"), ["A", "D", "B"]))
    assert(check_route(spm.get_route("B", "A"), ["B", "D", "A"]))    