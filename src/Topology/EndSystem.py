from Constants import *

class EndSystem: 
    def __init__(self, name : str, ports : int, domain : int):
        self.name = name
        self.ports = [None for _ in range(ports)]
        self.domain = domain
        self.streams = [[] for _ in range(NUM_PRIOS)]
    
    def add_stream(self, stream):
        self.streams[stream.pcp].append(stream)

    def get_streams(self):
        return [s for level in self.streams for s in level]
    def __repr__(self):
        return self.name