import numpy as np
from collections import defaultdict
from dataclasses import dataclass

class LECD:
    def __init__(self, edgeList: np.ndarray) -> None:
        """
        Leading Eigenvector Community Detector.\n 
        Create an instance by passing it an adjacency matrix and call LECD.split() to perform a split
        """
        self.graphWeight = 0
        self.edgeList = edgeList
        self.nodeMap = defaultdict(int)
        self.nodeList = self._getNodelist()
        self.matrix = self._getMatrix()
        self.modMatrix = self._getModularityMatrix()

    def split(self):
        """
        Performs the split using the leading eigenvector of the modularity matrix generated on initialization.\n
        """
        _, eigenvectors = np.linalg.eig(self.modMatrix)
        resultVector = eigenvectors.T[0]
        groups = [[], []]
        graphs = [[], []]

        for i, val in enumerate(resultVector):
            if val < 0:
                for tar in groups[0]:
                    tarIndex = self.nodeMap[tar]

                    if self.matrix[i][tarIndex] > 0:
                        graphs[0].append([self.nodeList[i], tar, self.matrix[i][tarIndex]])

                groups[0].append(self.nodeList[i])
            else:
                for tar in groups[1]:
                    tarIndex = self.nodeMap[tar]

                    if self.matrix[i][tarIndex] > 0:
                        graphs[1].append([self.nodeList[i], tar, self.matrix[i][tarIndex]])

                groups[1].append(self.nodeList[i])

        # had to add this correction since in some cases it would just swap the nodes from one
        # group to another and report an extremely small positive modularity, now if the split 
        # does not result in two non-empty groups, the delta is set to 0 as it should
        delta = self.getDelta(resultVector) if len(groups[0]) > 0 and len(groups[1]) > 0 else 0

        # if the split is not an improvement, return the unmodified communities
        if delta > 0:
            return Split(groups, graphs, delta, resultVector)
        else:
            return Split([self.nodeList, []], [self.edgeList, []], 0, [0] * len(self.nodeList))


    def getDelta(self, splitVector):
        firstProd = np.matmul(splitVector.T, self.modMatrix)
        finalProd = np.matmul(firstProd, splitVector)

        return (finalProd) / (4 * self.graphWeight)
        

    # generates the list of nodes and maps the nodes to an integer index
    def _getNodelist(self):
        """Return the list of unique nodes of the graph"""
        seen = set()
        nodeList = []

        counter = 0

        for edge in self.edgeList:
            self.graphWeight += edge[2]

            if edge[0] not in seen:
                nodeList.append(edge[0])
                seen.add(edge[0])
                self.nodeMap[edge[0]] = counter
                counter += 1

            if edge[1] not in seen:
                nodeList.append(edge[1])
                seen.add(edge[1])
                self.nodeMap[edge[1]] = counter
                counter += 1

        return nodeList
    
    
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
        matrix = np.zeros((len(self.nodeList), len(self.nodeList)))

        for edge in self.edgeList:
            node1Index = self.nodeMap[edge[0]]
            node2Index = self.nodeMap[edge[1]]
            matrix[node1Index][node2Index] = edge[2]
            matrix[node2Index][node1Index] = edge[2]

        return matrix

@dataclass
class Split:
    """
    Split.groups contains two lists, where each list has the members by labels of each group.\n
    Split.graphs contains two lists, where each list contains all the edges of each group.\n
    Split.delta contains the change in modularity after performing this split.\n
    Split._splitVector contains the vector that was used to split the group.
    """
    groups: list[list[str]]
    graphs: list[list]
    delta: float
    _splitVector: list[float]

    def __str__(self) -> str:
        return f"group1: {self.groups[0]}\ngroup2: {self.groups[1]}\ndelta: {self.delta}"
