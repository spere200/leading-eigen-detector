import numpy as np
import pandas as pd
from collections import defaultdict

class LECD:
    def __init__(self, edgeList: np.ndarray) -> None:
        """Leading Eigenvector Community Detector.\n 
        Create an instance by passing it an adjacency matrix and call LECD.split() to perform a split"""
        self.edgeList = edgeList
        self.nodeMap = defaultdict(int)
        self.nodeList = self._getNodelist()
        self.matrix = self._getMatrix()

        print(self.matrix)

    # generates the list of nodes and maps the nodes to an integer index
    def _getNodelist(self):
        """Return the list of unique nodes of the graph"""
        nodeList = set()

        counter = 0

        for edge in self.edgeList:
            if edge[0] not in nodeList:
                nodeList.add(edge[0])
                self.nodeMap[edge[0]] = counter
                counter += 1

            if edge[1] not in nodeList:
                nodeList.add(edge[1])
                self.nodeMap[edge[1]] = counter
                counter += 1

        return np.array(list(nodeList))

    def _getMatrix(self):
        """Return the adjacency matrix of the graph"""
        matrix = np.zeros((self.nodeList.size, self.nodeList.size))

        for edge in self.edgeList:
            node1Index = self.nodeMap[edge[0]]
            node2Index = self.nodeMap[edge[1]]
            matrix[node1Index][node2Index] = edge[2]
            matrix[node2Index][node1Index] = edge[2]

        return matrix



if __name__ == "__main__":
    edgeList = np.array(pd.read_csv('small.csv'))
    test = LECD(edgeList)
