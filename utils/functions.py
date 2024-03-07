from collections import defaultdict

def getUnconnectedComponents(edgeList):
    resGroup = []
    resGraph = []
    adj = defaultdict(list)

    for n1, n2, w in edgeList:
        adj[n1].append([n2, w])
        adj[n2].append([n1, w])

    visited = set()
    addedEdges = set()

    def dfs(currNode, currGroup):
        if currNode not in visited:
            resGroup[currGroup].append(currNode)
            visited.add(currNode)
     
            for tar, weight in adj[currNode]:
                if (currNode, tar) not in addedEdges and (tar, currNode) not in addedEdges:
                    resGraph[currGroup].append([currNode, tar, weight])
                    addedEdges.add((currNode, tar))
                    dfs(tar, currGroup)

    groupID = 0
    for node in adj:
        if node not in visited:
            resGroup.append([])
            resGraph.append([])
            dfs(node, groupID)
            groupID += 1

    return [resGroup, resGraph]



if __name__ == "__main__":
    edgeList = [
        ['a', 'b', 1],
        ['e', 'f', 1],
        ['d', 'a', 1],
        ['d', 'b', 1],
        # ['c', 'd', 1],
        ['b', 'c', 1],
    ]

    res = getUnconnectedComponents(edgeList)

    print(res)