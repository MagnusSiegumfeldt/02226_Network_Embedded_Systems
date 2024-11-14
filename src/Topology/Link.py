class Link: 
    def __init__(self, name : str, ep1 : str, port1 : int, ep2, port2 : int, domain : int):
        self.name = name
        self.ep1 = ep1
        self.port1 = port1
        self.ep2 = ep2
        self.port2 = port2
        self.domain = domain
        self.rate = 10**9 / 8
        self.streams = []

    def add_stream(self, stream):
        self.streams.append(stream)
    
    def get_streams(self):
        return self.streams