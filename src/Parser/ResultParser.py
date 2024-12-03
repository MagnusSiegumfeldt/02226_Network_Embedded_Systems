import re
import sys
from Stream.Result import Result

class ResultParser:
    def parse(self, file_name):
        
        result = Result()
            
        localPort_pattern = r'config \*\.(ES_\d+)\.app\[(\d+)\]\.io\.destPort (\d+)'
        config_pattern = r'config \*\.(ES_\d+)\.app\[(\d+)\]\.io\.destAddress "\\"(ES_\d+)\\""'
        
        with open(file_name, "r") as file:
            lines = file.readlines()
            stream_number = 1
            for i, line in enumerate(lines):
                if config_match := re.search(config_pattern, line):
                    stream = f"Stream_{stream_number}"
                    source_es = config_match[1]
                    dest_es = config_match[3]

                    app_line = lines[i + 1]           
                    if localPort_match := re.search(localPort_pattern, app_line):
                        local_port = localPort_match[3]
                                   
                    result.add_result(stream, source_es, dest_es, local_port)
                    stream_number += 1
             
        pattern = r"TSN_Network\.(ES_\d+)\.app\[(\d+)\]\.sink meanBitLifeTimePerPacket:histogram"
        mean_pattern = r"field mean ([\d.e+-]+)"     
        app_index_pattern = r"config \*\.(ES_\d+)\.app\[(\d+)\]\.io\.localPort (\d+)"    
        
        with open(file_name, "r") as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                if app_index_match := re.search(app_index_pattern, line):
                    app_index = app_index_match[2]
                    local_port_of_app_index = app_index_match[3]
                    
                    result.add_app_index(int(local_port_of_app_index) - 1, app_index)    
                
        result.create_mapping()  
        
        with open(file_name, "r") as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                if pattern_match := re.search(pattern, line):
                    dest_es = pattern_match[1]
                    app_index_check = pattern_match[2]

                    index = result.mapping.get((app_index_check, dest_es))
                    if index is not None:
                        mean_line = lines[i + 2]
                        if mean_match := re.search(mean_pattern, mean_line):
                            mean_delay = float(mean_match[1])
                            result.add_delay(index, mean_delay)
                    else:
                        print(f"No entry found for app index={app_index_check}, dest={dest_es}")
        
        # Print final results
        #for stream in result:
            #print(stream)

        return result

def main():
    if len(sys.argv) != 2:
        print("Usage: ResultParser.py path/to/file.sca")
        return
    rp = ResultParser()
    rp.parse(sys.argv[1])
    

if __name__ =="__main__":
    main()
