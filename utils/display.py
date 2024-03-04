import logging
import pandas as pd
from pyvis.network import Network
import networkx as nx

from utils.dataclasses import DetectorResult


def generate_xlsx(results: DetectorResult):
    logging.info("")
    logging.info(
        f"Generating the output.xlsx file for a graph with {len(results.groups)} groups..."
    )

    with pd.ExcelWriter("output.xlsx", engine="xlsxwriter") as writer:
        # writing the groups with group labels to the first sheet of the document
        groupHeaders = [f"group{i}" for i in range(len(results.groups))]
        df = pd.DataFrame(results.groups)
        df = df.transpose()
        df.columns = groupHeaders
        logging.info(f'  Creating the "groups" sheet...')
        df.to_excel(writer, sheet_name="groups", index=False)

        for i, row in enumerate(results.graphs):
            logging.info(f'  Creating the "group{i}_edges" sheet...')
            df = pd.DataFrame(row)
            df.columns = ["node1", "node2", "weight"]
            df.to_excel(writer, sheet_name=f"group{i}_edges", index=False)


def generate_html(results: DetectorResult):
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
