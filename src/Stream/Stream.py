
class Stream:

    def __init__(self, pcp, stream_name, stream_type, source_node, destination_node, size, period, deadline):
        self.pcp = int(pcp)
        self.name = stream_name
        self.type = stream_type
        self.src = source_node
        self.dest = destination_node
        self.size = float(size)
        self.period = float(period)
        self.deadline = float(deadline)

        self.burst = self.size
        self.rate = self.size / self.period

    def __str__(self) -> str:
        return f"Name: {self.name}, PCP: {self.pcp}"
    def __repr__(self) -> str:
        return self.__str__()