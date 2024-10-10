import csv

def generate_ini_from_csv(input_csv, output_ini):
    # Read the CSV file
    file = open(input_csv, "r")

    stream_configs = []

        # Loop through each row in the CSV file
    for row in file:

            entries = row.split(',')
            # Extract each field from the CSV line using index positions
            pcp = entries[0]                # PCP is in the first column
            stream_name = entries[1]       # StreamName is in the second column
            stream_type = entries[2]       # StreamType is in the third column
            src_node = entries[3]          # SourceNode is in the fourth column
            dest_node = entries[4]         # DestinationNode is in the fifth column
            packet_size = int(entries[5])       # Size is in the sixth column
            period_ns = int(entries[6])     # Period is in the seventh column (in nanoseconds)
            deadline_ns = int(entries[7])   # Deadline is in the eighth column (in nanoseconds)

            # Generate INI content for each stream
            stream_config = f"""
# Configuration for {stream_name}
*.{src_node}.numApps += 1
*.{src_node}.app[*.{src_node}.numApps-1].typename = "TsnUdpSourceApp"
*.{src_node}.app[*.{src_node}.numApps-1].display-name = "{stream_name}"
*.{src_node}.app[*.{src_node}.numApps-1].io.destAddress = "{dest_node}"
*.{src_node}.app[*.{src_node}.numApps-1].io.destPort = {1000 + int(pcp)}
*.{src_node}.app[*.{src_node}.numApps-1].source.packetLength = {packet_size}B
*.{src_node}.app[*.{src_node}.numApps-1].source.productionInterval = {period_ns}us
*.{src_node}.app[*.{src_node}.numApps-1].source.deadline = {deadline_ns}us

# Ingress Filtering Configuration
*.{src_node}.bridging.streamIdentifier.identifier.mapping += [{{stream: "{stream_name}", packetFilter: expr(udp.destPort == {1000 + int(pcp)})}}]

# Egress Traffic Shaping Configuration
*.{src_node}.bridging.streamCoder.encoder.mapping += [{{stream: "{stream_name}", pcp: {pcp}, shapingRate: {packet_size / (period_ns / 1e6)}B/us}}]
            stream_configs.append(stream_config)
"""
            stream_configs.append(stream_config)
    # Write the INI configuration to the output file
    with open(output_ini, mode='w') as ini_file:
        ini_file.write("[General]\n")
        ini_file.write("network = inet.networks.tsn.TsnLinearNetwork\n")
        ini_file.write("sim-time-limit = 10s\n")
        ini_file.write("description = \"Generated INI file for TSN streams\"\n\n")
        for stream_config in stream_configs:
            ini_file.write(stream_config)


generate_ini_from_csv("test_streams.csv", "example.ini")