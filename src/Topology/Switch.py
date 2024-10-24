from Constants import *

class Switch: 
    def __init__(self, name : str, ports : int, domain : int):
        self.name = name
        self.ports = [None for _ in range(ports)]
        self.domain = domain
        self.streams = [[] for _ in range(NUM_PRIOS)]
    
    def add_stream(self, stream):
        self.streams[stream.pcp].append(stream)

    def get_streams_with_higher_prio(self, prio):
        streams_with_higher_prio = []
        for i in range(prio + 1, NUM_PRIOS):
            streams_with_higher_prio += self.streams[i]
        return streams_with_higher_prio

    def get_streams_with_prop_excluding(self, prio, stream):
        return filter()

    def __repr__(self):
        return self.name