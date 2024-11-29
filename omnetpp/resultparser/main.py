import sys
import json
import pprint
import re

def main():
    if len(sys.argv) != 4:
        print("Usage: main.py [setup.ini] [res.json] [streams.csv]")
    ini_path = sys.argv[1]
    res_path = sys.argv[2]
    str_path = sys.argv[3]
    
    res = open(res_path, "r")

    bad_stream_name_to_end_point = {}
    for line in res:    
        if "module" in line:
            stream = line.split(" : ")[1].replace("\"", "").strip()
            end = stream.replace("TSN_Network.", "").replace(".sink,", "")
            bad_stream_name_to_end_point[stream] = end
    

    endpoint_to_local_port = {}
    ini = open(ini_path, "r")
    for line in ini:
        if "localPort" in line:
            ep, port = line.strip().replace("*.", "").split(".io.localPort = ")
            endpoint_to_local_port[ep] = int(port)
    ini.close()
    dest_port_to_endpoint = {}
    ini = open(ini_path, "r")
    for line in ini:
        if "destPort" in line and "bridging" not in line:
            ep, port = line.strip().replace("*.", "").split(".io.destPort = ")
            dest_port_to_endpoint[int(port)] = ep
    ini.close()

    res = {}
    for bad_name in bad_stream_name_to_end_point:
        dst_point = bad_stream_name_to_end_point[bad_name]
        port = endpoint_to_local_port[dst_point]
        src_point = dest_port_to_endpoint[port]
        res[bad_name] = (src_point, dst_point)

    out1 = {}
    for k in res.keys():
        src, dest = res[k]
        out1[k] = (re.sub(r'.app\[\d\]', "", src), re.sub(r'.app\[\d\]', "", dest))

    out = {}
    for k in out1.keys():
        str = open(str_path, "r")
        src, dst = out1[k]
        for line in str:
            if src in line and dst in line:
                stream_name = line.split(",")[1]
                out[k] = stream_name
        str.close()
    print(out)




if __name__ == "__main__":
    main()