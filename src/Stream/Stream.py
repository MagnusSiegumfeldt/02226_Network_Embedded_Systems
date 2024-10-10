
class Stream:

    def __init__(self, pcp, stream_name, stream_type, source_node, destination_node, size, period, deadline):
        self.pcp = pcp
        self.name = stream_name
        self.type = stream_type
        self.src = source_node
        self.dest = destination_node
        self.size = size
        self.period = period
        self.deadline = deadline

    def __str__(self) -> str:
        return f"Name: {self.name}, PCP: {self.pcp}"
    def __repr__(self) -> str:
        return self.__str__()