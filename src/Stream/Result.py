class Result:
    def __init__(self):
        self.stream = []
        self.source = []  
        self.dest = []
        self.app_index = []  
        self.local_port = []
        self.mean_delay = [] 

    def add_result(self, stream, source, dest, local_port):
        self.stream.append(stream)
        self.source.append(source)
        self.app_index.append(None)
        self.dest.append(dest)
        self.local_port.append(local_port) 
        self.mean_delay.append(None) 

    def add_delay(self, index, delay):
        self.mean_delay[index] = round(float(delay) * (10 ** 6), 3)
        
    def add_app_index(self, index, app_index):
        self.app_index[index] = app_index
        
    def __iter__(self):
        return iter(zip(self.stream, self.source, self.dest, self.app_index, self.local_port, self.mean_delay))
        
    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self):
        return "\n".join([
            f"Stream: {stream}, Source: {source}, Dest: {dest}, App Index: {app_index}, Mean Delay: {mean_delay}"
            for stream, source, dest, app_index, mean_delay in zip(
                self.stream, self.source, self.dest, self.app_index, self.mean_delay
            )
        ])
        
    def create_mapping(self):
        self.mapping = {}
        for index, (stream, source, dest, app_index, local_port, mean_delay) in enumerate(self):
            if app_index is not None and dest is not None:
                self.mapping[(app_index, dest)] = index