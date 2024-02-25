import numpy as np
import pandas as pd
from collections import defaultdict

class LECD:
    def __init__(self, edgeList: np.ndarray) -> None:
        """Leading Eigenvector Community Detector.\n 
        Create an instance by passing it an adjacency matrix and call LECD.split() to perform a split"""
        self.graphWeight = 0
        self.edgeList = edgeList
        self.nodeMap = defaultdict(int)
        self.nodeList = self._getNodelist()
        self.matrix = self._getMatrix()
        self.modMatrix = self._getModularityMatrix()

        self.groups = defaultdict(list[str])
        splitVector = self.split()

        for g, v in self.groups.items():
            print(g, v)

        print(f"Delta: {self.getDelta(splitVector)}")


    def split(self):
        _, eigenvectors = np.linalg.eig(self.modMatrix)
        resultVector = eigenvectors.T[0]

        for i, val in enumerate(resultVector):
            if val < 0:
                self.groups[0].append(self.nodeList[i])
            else:
                self.groups[1].append(self.nodeList[i])

        return resultVector


    def getDelta(self, splitVector):
        firstProd = np.matmul(splitVector.T, self.modMatrix)
        finalProd = np.matmul(firstProd, splitVector)

        return (finalProd) / (4 * self.graphWeight)

        # delta = (splitVector.T * ) / (4 * self.graphWeight)
        

    # generates the list of nodes and maps the nodes to an integer index
    def _getNodelist(self):
        """Return the list of unique nodes of the graph"""
        nodeList = set()

        counter = 0

        for edge in self.edgeList:
            self.graphWeight += edge[2]

            if edge[0] not in nodeList:
                nodeList.add(edge[0])
                self.nodeMap[edge[0]] = counter
                counter += 1

            if edge[1] not in nodeList:
                nodeList.add(edge[1])
                self.nodeMap[edge[1]] = counter
                counter += 1

        return np.array(list(nodeList))
    
    
    def _getModularityMatrix(self):
        """Return the modularity matrix of the graph"""
        modMatrix = np.zeros(self.matrix.shape)
        
        for i in range(len(modMatrix)):
            for j in range(len(modMatrix)):
                deg1 = np.sum(self.matrix[:,[i]])
                deg2 = np.sum(self.matrix[:,[j]])

                modMatrix[i][j] = self.matrix[i][j] - ((deg1 * deg2) / (2 * self.graphWeight))

        return modMatrix


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
