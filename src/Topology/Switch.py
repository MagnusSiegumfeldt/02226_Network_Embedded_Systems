from copy import deepcopy
from Constants import *

# TODO: add shaped queues, such that an added stream with its priority and *next hop* will be translated to the according shaped queue

class Switch: 
    def __init__(self, name : str, ports : int, domain : int):
        self.name = name
        self.ports = [None for _ in range(ports)]
        self.domain = domain
        self.streams = [[] for _ in range(NUM_PRIOS)]
        self.shaped_queues: dict = {}
    
    def add_stream(self, stream):
        self.streams[stream.pcp].append(stream)
        """shaped_queues_for_dst = self.shaped_queues.get(dst)
        if shaped_queues_for_dst is None:
            self.shaped_queues[dst] = {stream.pcp: [stream]}
        else: 
            shaped_queues_for_dst.get(dst).get(stream.pcp).append(stream)"""
    
    def get_all_shaped_queues(self):
        return deepcopy(self.shaped_queues)
    
    def get_shaped_queue_for_dst(self, dst):
        return deepcopy(self.shaped_queues.get(dst))

    def get_streams(self):
        return [s for level in self.streams for s in level]
    
    def get_streams_with_higher_prio(self, prio):
        streams_with_higher_prio = []
        for i in range(prio + 1, NUM_PRIOS):
            streams_with_higher_prio += self.streams[i]
        return streams_with_higher_prio

    def get_streams_with_higher_prio_and_same_dst(self, prio, dst):
        streams_with_higher_prio = []
        for i in range(prio + 1, NUM_PRIOS):
            streams_with_higher_prio += self.shaped_queues.get(dst).get(i)
        return streams_with_higher_prio
    
    def get_all_other_streams_with_same_prio_and_same_dst(self, stream, dst):
        filter(lambda s: s != stream, self.shaped_queues.get(dst).get(stream.pcp))

    def __repr__(self):
        return self.name