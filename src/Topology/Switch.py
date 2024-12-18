from Constants import *

# TODO: add shaped queues, such that an added stream with its priority and *next hop* will be translated to the according shaped queue

class Switch: 
    def __init__(self, name : str, ports : int, domain : int):
        self.name = name
        self.ports = [None for _ in range(ports)]
        self.domain = domain
        self.streams = [[] for _ in range(NUM_PRIOS)]
    
    def add_stream(self, stream):
        self.streams[stream.pcp].append(stream)

    def get_streams(self):
        return [s for level in self.streams for s in level]
    def get_streams_with_higher_prio(self, prio):
        streams_with_higher_prio = []
        for i in range(prio + 1, NUM_PRIOS):
            streams_with_higher_prio += self.streams[i]
        return streams_with_higher_prio

    def __repr__(self):
        return self.name