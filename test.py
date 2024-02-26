import numpy as np
import pandas as pd
from Detector import Detector

# used for testing
if __name__ == "__main__":
    edgeList = np.array(pd.read_csv('data/small.csv'))
    detector = Detector(edgeList)
    results = detector.getLECommunities(xls=False)

    for row in results.groups:
        print(row)
