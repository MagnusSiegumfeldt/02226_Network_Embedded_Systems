class EndSystem: 
    def __init__(self, name : str, ports : int, domain : int):
        self.name = name
        self.ports = [None for _ in range(ports)]
        self.domain = domain
    def __repr__(self):
        return self.name