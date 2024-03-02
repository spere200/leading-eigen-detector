import pandas as pd
import numpy as np
from pyvis.network import Network
import networkx as nx

from dataclasses import dataclass
import logging
import time

from LECD import LECD


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

        results = DetectorResult(groups, graphs)

        if xlsx:
            logging.info("")
            logging.info(
                f"Generating the output.xlsx file for a graph with {len(groups)} groups..."
            )

            with pd.ExcelWriter("output.xlsx", engine="xlsxwriter") as writer:
                # writing the groups with group labels to the first sheet of the document
                groupHeaders = [f"group{i}" for i in range(len(groups))]
                df = pd.DataFrame(groups)
                df = df.transpose()
                df.columns = groupHeaders
                logging.info(f'  Creating the "groups" sheet...')
                df.to_excel(writer, sheet_name="groups", index=False)

                for i, row in enumerate(graphs):
                    logging.info(f'  Creating the "group{i}_edges" sheet...')
                    df = pd.DataFrame(row)
                    df.columns = ["node1", "node2", "weight"]
                    df.to_excel(writer, sheet_name=f"group{i}_edges", index=False)

        if visualize:
            logging.info(f"")
            logging.info(f"Creating the output.html file for the visualization")

            nxGraph = nx.Graph()

            groupID = 0

            for group in results.groups:
                for node in group:
                    nxGraph.add_node(
                        node,
                        size=15,
                        title=f"group {groupID}",
                        label=node,
                        group=groupID,
                    )

                groupID += 1

            for graph in results.graphs:
                nxGraph.add_weighted_edges_from(graph)

            net = Network()
            net.from_nx(nxGraph)
            net.show_buttons(filter_=["physics"])

            net.barnes_hut(
                gravity=-500,
                central_gravity=0.3,
                spring_length=90,
                spring_strength=0.04,
                damping=0.09,
                overlap=0,
            )

            net.toggle_physics(False)
            net.show("output.html", notebook=False)

        logging.info(f"")
        logging.info(f"Done after {(time.time() - processStartTime):.6f} seconds.")

        return results


@dataclass
class DetectorResult:
    """
    Wrapper dataclass for the results, it just includes the list of groups and the list of edges for each group of nodes.
    """

    groups: list[list[str]]
    graphs: list[list]

    def __str__(self) -> str:
        return str(self.groups)
