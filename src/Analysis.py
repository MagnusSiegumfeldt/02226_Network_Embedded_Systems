
import sys

from Topology.Topology import Topology
from ShortestPathManager import ShortestPathManger

def main():
    if len(sys.argv) != 3:
        print("Usage: python analysis.py [topology.csv] [streams.csv]")
    topology_file_name = sys.argv[1]
    streams_file_name = sys.argv[2]

    topology = Topology()

    topology_file = open(topology_file_name, "r") 
    for line in topology_file:
        entries = line.split(",")
        type = entries[0]
        if type == "SW":
            name, ports, domain = entries[1], int(entries[2]), int(entries[3])
            topology.add_switch(name, ports, domain)
            
        elif type == "ES":
            name, ports, domain = entries[1], int(entries[2]), int(entries[3])
            topology.add_end_system(name, ports, domain)

        elif type == "LINK":
            name, ep1, port1, ep2, port2, domain = entries[1], entries[2], int(entries[3]), entries[4], int(entries[5]), int(entries[6])
            topology.add_link(name, ep1, port1, ep2, port2, domain)
            
    shortest_path_manager = ShortestPathManger(topology)
    print(shortest_path_manager.get_distance("ES_54", "ES_110"))
    print(shortest_path_manager.get_route("ES_54", "ES_110"))
    print(shortest_path_manager.get_distance("ES_110", "ES_54"))
    print(shortest_path_manager.get_route("ES_110", "ES_54"))
    topology_file.close()





    streams_file = open(streams_file_name, "r") 
    for line in streams_file:
        entries = line.split(",")
























if __name__ == "__main__":
    main()