import pandas as pd
import numpy as np
from dataclasses import dataclass
from LECD import LECD

class Detector:
    def __init__(self, edgeList) -> None:
        self.edgeList = edgeList

    def getLECommunities(self, xls=False):
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


# used for testing
if __name__ == "__main__":
    edgeList = np.array(pd.read_csv('small.csv'))
    detector = Detector(edgeList)
    results = detector.getLECommunities(xls=True)

    # for row in results.groups:
    #     print(row)
