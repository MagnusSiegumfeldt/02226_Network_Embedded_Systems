from collections import deque
from Topology.Topology import Topology

class ShortestPathManager:
    def __init__(self, topology : Topology):
        end_systems = topology.get_end_systems()
        self.distance_table = {}
        self.routes_table = {}
        
        for es in end_systems:
            self.distance_table[es.name], self.routes_table[es.name] = self.__bfs(topology, es)

    def __bfs(self, topology : Topology, start):
        visited = { start.name: True }
        distances = { start.name: 0}
        routes = { start.name: [start]}
        

        queue = deque([start])

        while queue:
            node = queue.popleft()
            for adj in node.ports:
                if adj != None and adj.name not in visited:
                    queue.append(adj)
                    
                    distances[adj.name] = distances[node.name] + 1
                    routes[adj.name] = routes[node.name].copy() + [adj]
                    visited[adj.name] = True
        return distances, routes

    def get_distance(self, ep1_name, ep2_name):
        return self.distance_table[ep1_name][ep2_name]

    def get_route(self, ep1_name, ep2_name):
        return self.routes_table[ep1_name][ep2_name]

