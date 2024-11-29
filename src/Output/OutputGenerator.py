import csv 


def write_csv_to_file(path, field_names, analysis_dic, runtime_in_sec, mean_E2E):
    with open(path, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(analysis_dic)
        csv_file.write(f"\nMean E2E: {mean_E2E}\nRuntime in Seconds: {runtime_in_sec}")

