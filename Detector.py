import logging
import time

from LeadingEigenvector.LECD import LECD

import utils.display
from utils.dataclasses import DetectorResult
from utils.functions import getUnconnectedComponents


class Detector:
    def __init__(self, edgeList) -> None:
        self.edgeList = edgeList

    def getLECommunities(self, xlsx=True, visualize=False, log=False):
        if log:
            logging.basicConfig(level=logging.INFO, format="INFO: %(message)s")

        groups = []
        graphs = []

        processStartTime = time.time()

        def dfs(currEdgeList):
            logging.info(f"Splitting a graph with {len(currEdgeList)} edges...")
            start = time.time()

            splitResults = LECD(currEdgeList).split()

            logging.info(f"  Done after {(time.time() - start):.6f} seconds.")

            if splitResults.delta <= 0:
                # since the algorithm may place very small unconnected graphs in the same group for very large input graphs
                # this step is performed to make sure that any generated groups are made up of connected graphs
                unconnectedResults = getUnconnectedComponents(splitResults.graphs[0])

                for group in unconnectedResults[0]:
                    groups.append(group)

                for graph in unconnectedResults[1]:
                    graphs.append(graph)

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

        results = DetectorResult(groups, graphs)

        if xlsx:
            utils.display.generate_xlsx(results)

        if visualize:
            utils.display.generate_html(results)

        logging.info(f"")
        logging.info(f"Done after {(time.time() - processStartTime):.6f} seconds.")

        return results
