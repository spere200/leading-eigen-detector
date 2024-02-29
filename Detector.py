import pandas as pd
import numpy as np
from dataclasses import dataclass
import logging
import time

from LECD import LECD

class Detector:
    def __init__(self, edgeList, log=False) -> None:
        if log:
            logging.basicConfig(level=logging.INFO, format='INFO: %(message)s')

        self.edgeList = edgeList

    def getLECommunities(self, xls=True):
        groups = []
        graphs = []

        processStartTime = time.time()

        def dfs(currEdgeList):
            logging.info(f"Splitting a graph with {len(currEdgeList)} edges...")
            start = time.time()

            splitResults = LECD(currEdgeList).split()

            logging.info(f"  Done after {(time.time() - start):.6f} seconds.")

            if splitResults.delta <= 0:
                groups.append(splitResults.groups[0])
                graphs.append(splitResults.graphs[0])
                logging.info(f"    No good split found, group {len(groups)} created.")
            else:
                resultGraph1 = splitResults.graphs[0]
                resultGraph2 = splitResults.graphs[1]

                logging.info(f"    Found a possible split.")

                if len(resultGraph1) > 0:
                    dfs(resultGraph1)

                if len(resultGraph2) > 0:
                    dfs(resultGraph2)

        dfs(self.edgeList)

        if xls:
            logging.info("")
            logging.info(f"Generating the output .xlsx file for a graph with {len(groups)} groups...")

            with pd.ExcelWriter("output_groups.xlsx", engine='xlsxwriter') as writer:
                # writing the groups with group labels to the first sheet of the document
                groupHeaders = [f"group{i}" for i in range(len(groups))]
                df = pd.DataFrame(groups)
                df = df.transpose()
                df.columns = groupHeaders
                logging.info(f"  Creating the \"groups\" sheet...")
                df.to_excel(writer, sheet_name="groups", index=False)

                for i, row in enumerate(graphs):
                    logging.info(f"  Creating the \"group{i}_edges\" sheet...")
                    df = pd.DataFrame(row)
                    df.columns = ["node1", "node2", "weight"]
                    df.to_excel(writer, sheet_name=f"group{i}_edges", index=False)

        logging.info(f"")
        logging.info(f"Done after {(time.time() - processStartTime):.6f} seconds.")

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
