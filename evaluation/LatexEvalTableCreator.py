import csv
import sys
import pyperclip

from Parser.ResultParser import ResultParser

"""
This class is responsible for parsing our calculated WCD and the simulated results, such that latex tables 
will be simply created that can then be copy pasted into the document.
"""

COL_NAME_FLOW = "flowname"
COL_NAME_MAX_E2E = "max_e2e"
COL_NAME_DEADLINE = "deadline"

#TODO: This might crash, if Streams are not actually named in the scheme "Stream_<number>" but something like "Flow_<number>"
class LatexEvalTableCreator():

    """
    This method will return the latex string for the overleaf document.
    """
    def create_table(self, wcd_file, sca_file) -> str:
        # dict that will hold streamname -> {wcd: <number in microseconds>, omnetpp: <number in microseconds>}
        stream_to_delays : dict = {}
        with open(wcd_file, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if not(row[COL_NAME_FLOW].startswith("Mean E2E") or row[COL_NAME_FLOW].startswith("Runtime in Seconds")): 
                    stream_to_delays[row[COL_NAME_FLOW]] = {"wcd": row[COL_NAME_MAX_E2E]}
                    #print(f"{row[COL_NAME_FLOW]}, wcd: {row[COL_NAME_MAX_E2E]}, deadline: {row[COL_NAME_DEADLINE]}")
        resultParser = ResultParser()
        results = resultParser.parse(sca_file)
        for res in results:
            stream_to_delays[res[0]]["omnetpp"] = res[5]

        latex_string = f"""
\\begin{{table}}[H]
  \\centering
  \\caption{{Simulated worst-case delays}}
  \\begin{{tabular}}{{|c|c|c|}}
    \\hline
    \\textbf{{Stream number}} & \\textbf{{Calculated Worst-case delay}} & \\textbf{{Simulated Worst-case delay}} \\\\ \\hline \n""" 
        for stream_name, calcs in stream_to_delays.items():
            latex_string += f"""    {stream_name.replace('_', '\\_')} & {calcs["wcd"]}\\(\\mu\\text{{s}}\\)& {calcs["omnetpp"]}\\(\\mu\\text{{s}}\\) \\\\ \\hline \n"""

        latex_string += f"""  \\end{{tabular}}
    \\label{{tab:example1}}
\\end{{table}}

% Define data for the graph
\\pgfplotstableread {{"StreamName   Calculated  Simulated\n"""
                      
        for stream_name, calc in stream_to_delays.items():
            latex_string += f"""{stream_name.replace("_", "\\_")}   {calc["wcd"]}   {calc["omnetpp"]}\n"""
        latex_string += f"""}}\\mydata\n"""


        latex_string += f"""% Graph using the same data
\\begin{{figure}}[H]
  \\centering
  \\begin{{tikzpicture}}
  \\begin{{axis}}[
    width=14cm,
    height=8cm,
    ylabel={{Delay in (\\(\\mu\\text{{s}}\\))}},
    xlabel={{Stream of stream.csv file}},
    xtick=data,
    xticklabels={{{','.join(str(stream_name.replace('Stream_', '')) for stream_name, _ in stream_to_delays.items())}}},
    grid=both,
    legend pos=north east,
    x tick label style={{
        rotate=45, % Rotate labels slightly for better spacing
        anchor=east, % Align labels to avoid overlap
        font=\\small, % Adjust label font size
        yshift=-3pt % Add spacing between labels and axis
    }},
    xlabel style={{
        font=\\small 
    }}
    ]

      % Plot Simulated Data
      \\addplot[color=blue, mark=*] table[x expr=\\coordindex, y=Simulated] {{\\mydata}};
      \\addlegendentry{{Simulated Mean Delays}}

      % Plot Calculated Data
      \\addplot[color=red, mark=square*] table[x expr=\\coordindex, y=Calculated] {{\\mydata}};
      \\addlegendentry{{Calculated Worst-Case Delays}}

      \\end{{axis}}
    \\end{{tikzpicture}}
    \\caption{{Graph of simulated mean and calculated worst-case delays}}
\\end{{figure}}"""


        return latex_string

          

def main():
    if len(sys.argv) != 3:
        print("Usage: LatexEvalTableCreator.py [wcd_analysis_file.csv] [omnetpp-file.sca]")
        return
    latexETC = LatexEvalTableCreator()
    latex_string = latexETC.create_table(sys.argv[1], sys.argv[2])
    pyperclip.copy(latex_string)
    print("latex text has been copied to your clipboard! :)")


if __name__ == "__main__":
    main()