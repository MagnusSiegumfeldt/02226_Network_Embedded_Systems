from Topology.Topology import Topology

class TopologyParser:
    def parse(self, file_name):
        topology = Topology()
        with open(file_name) as file:
            for line in file:
                entries = line.strip().split(",")

                type = entries[0]
                if type == "SW":
                    name, ports, domain = entries[1], int(entries[2]), int(entries[3]) if entries[3] != '' else -1
                    topology.add_switch(name, ports, domain)
                    
                elif type == "ES":
                    name, ports, domain = entries[1], int(entries[2]), int(entries[3]) if entries[3] != '' else None
                    topology.add_end_system(name, ports, domain)

                elif type == "LINK":
                    name, ep1, port1, ep2, port2, domain = entries[1], entries[2], int(entries[3]), entries[4], int(entries[5]), int(entries[6]) if entries[6] != '' else None
                    topology.add_link(name, ep1, port1, ep2, port2, domain)
            return topology