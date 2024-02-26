import pandas as pd
import numpy as np
from dataclasses import dataclass
from LECD import LECD

class Detector:
    def __init__(self, edgeList) -> None:
        self.edgeList = edgeList

    def getLECommunities(self, xls=True):
        groups = []
        graphs = []

        def dfs(currEdgeList):
            splitResults = LECD(currEdgeList).split()

            if splitResults.delta <= 0:
                groups.append(splitResults.groups[0])
                graphs.append(splitResults.graphs[0])
            else:
                resultGraph1 = splitResults.graphs[0]
                resultGraph2 = splitResults.graphs[1]

                if len(resultGraph1) > 0:
                    dfs(resultGraph1)

                if len(resultGraph2) > 0:
                    dfs(resultGraph2)

        dfs(self.edgeList)

        if xls:
            with pd.ExcelWriter("output_groups.xlsx", engine='xlsxwriter') as writer:
                # writing the groups with group labels to the first sheet of the document
                groupHeaders = [f"group{i}" for i in range(len(groups))]
                df = pd.DataFrame(groups)
                df = df.transpose()
                df.columns = groupHeaders
                df.to_excel(writer, sheet_name="groups", index=False)

                for i, row in enumerate(graphs):
                    df = pd.DataFrame(row)
                    df.columns = ["src", "tar", "weight"]
                    df.to_excel(writer, sheet_name=f"group{i}_edges", index=False)

        return DetectorResult(groups, graphs)


@dataclass
class DetectorResult:
    """
    Wrapper dataclass for the results, it just includes the list of groups and the list of edges for each group of nodes.
    """
    groups: list[list[str]]
    graphs: list[list]

    def __str__(self) -> str:
        return str(self.groups)
