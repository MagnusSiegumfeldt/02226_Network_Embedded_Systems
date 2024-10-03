from Topology.Switch import Switch
from Topology.EndSystem import EndSystem
from Topology.Link import Link

class Topology:
    def __init__(self):
        self.devices = {}
        self.links = {}

    def add_end_system(self, name, ports, domain):
        self.devices[name] = EndSystem(name, ports, domain)

    def add_switch(self, name, ports, domain):
        self.devices[name] = Switch(name, ports, domain)

    def add_link(self, name, ep1, port1, ep2, port2, domain):
        self.links[name] = Link(name, ep1, port1 - 1, ep2, port2 - 1, domain)
        self.devices[ep1].ports[port1 - 1] = self.devices[ep2]
        self.devices[ep2].ports[port2 - 1] = self.devices[ep1]

    def get_end_systems(self):
        l = []
        for d in self.devices.values():
            if isinstance(d, EndSystem):
                l.append(d)
        return l