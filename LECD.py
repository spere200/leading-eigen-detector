import numpy as np
import pandas as pd

class LECD:
    def __init__(self, matrix: np.ndarray) -> None:
        """Leading Eigenvector Community Detector.\n 
        Create an instance by passing it an adjacency matrix and call LECD.split() to perform a split"""
        self.matrix = matrix

if __name__ == "__main__":
    matrix = np.array(pd.read_csv('COAD.csv'))
    test = LECD(matrix)
