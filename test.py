import numpy as np
import pandas as pd
# import networkx as nx
# import matplotlib.pyplot as plt

from Detector import Detector

# used for testing
if __name__ == "__main__":
    edgeList = np.array(pd.read_csv("data/small.csv"))

    # # this was only used to generate the sample graph for the .md file, feel  
    # # free to add it back in if you want but you'll have to install matplotlib 
    # # networkx, and scipy, and it's extremely impractical for very large graphs
    # G = nx.Graph()
    # G.add_weighted_edges_from(edgeList)

    # pos = nx.spring_layout(G)
    # nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=700, font_size=14)
    # edge_labels = nx.get_edge_attributes(G, 'weight')
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12)

    # plt.show()

    detector = Detector(edgeList)
    results = detector.getLECommunities()

    for row in results.groups:
        print(row)
