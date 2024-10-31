from Stream.Stream import Stream

class StreamParser:
    def parse(self, file_name):
        stream_arr = []
        with open(file_name) as csv_file:
            for line in csv_file:
                entries = line.strip().split(',')
                stream_arr.append(Stream(entries[0], entries[1], entries[2], entries[3], entries[4], entries[5], entries[6], entries[7]))
        return stream_arr
    