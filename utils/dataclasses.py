from dataclasses import dataclass


@dataclass
class DetectorResult:
    """
    Wrapper dataclass for the results, it just includes the list of groups and the list of edges for each group of nodes.
    """

    groups: list[list[str]]
    graphs: list[list]

    def __str__(self) -> str:
        return str(self.groups)


@dataclass
class SplitResult:
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
        return (
            f"group1: {self.groups[0]}\ngroup2: {self.groups[1]}\ndelta: {self.delta}"
        )
