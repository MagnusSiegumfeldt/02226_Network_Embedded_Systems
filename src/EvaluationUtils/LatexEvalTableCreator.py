import csv
import sys

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
  \\tcentering
  \\caption{{Simulated worst-case delays}}
  \\begin{{tabular}}{{|c|c|c|}}
    \\hline
    \\textbf{{Stream number}} & \\textbf{{Calculated Worst-case delay}} & \\textbf{{Simulated Worst-case delay}} \\\\ \\hline \n""" 
        for stream_name, calcs in stream_to_delays.items():
            latex_string += f"""    {stream_name} & {calcs["wcd"]}\\(\\mu\\text{{s}}\\)& {calcs["omnetpp"]}\\(\\mu\\text{{s}}\\) \\\\ \\hline \n"""

        latex_string += f"""  \\end{{tabular}}
    \\label{{tab:example1}}
\\end{{table}}

% Graph using the same data
\\begin{{figure}}[H]
  \\centering
  \\begin{{tikzpicture}}
  \\begin{{axis}}[
    width=12cm,
    height=8cm,
    ylabel={{Worst-case delay (\\(\\mu\\text{{s}}\\))}},
    xlabel={{Graph type}},
    xtick=data,
    xticklabels={{Mesh, Path, Ring, Random geometric, Binomial, Expected ND}},
    grid=both,
    legend pos=north east,
    x tick label style={{
        rotate=30, % Rotate labels slightly for better spacing
        anchor=north east, % Align labels to avoid overlap
        font=\\small, % Adjust label font size
        yshift=-3pt % Add spacing between labels and axis
    }},
    xlabel style={{
        at={{(axis description cs:0.5,-0.25)}}, % Move xlabel further down
        font=\\small 
    }},
    enlarge x limits=0.1 % Add horizontal spacing on both sides of the x-axis
    ]

      % Plot Simulated Data
      \\addplot[color=blue, mark=*] table[x expr=\\coordindex, y=Simulated] {{\\mydata}};
      \\addlegendentry{{Simulated worst-case delay}}

      % Plot Calculated Data
      \\addplot[color=red, mark=square*] table[x expr=\\coordindex, y=Calculated] {{\\mydata}};
      \\addlegendentry{{Calculated worst-case delay}}

      \\end{{axis}}
    \\end{{tikzpicture}}
    \\caption{{Graph of simulated and calculated worst-case delays for different graph types}}
\\end{{figure}}"""


        return latex_string

          

def main():
    if len(sys.argv) != 3:
        print("Usage: LatexEvalTableCreator.py [wcd_analysis_file.csv] [omnetpp-file.sca]")
        return
    latexETC = LatexEvalTableCreator()
    latex_string = latexETC.create_table(sys.argv[1], sys.argv[2])
    print(latex_string)


if __name__ == "__main__":
    main()