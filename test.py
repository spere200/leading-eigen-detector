import numpy as np
import pandas as pd

from Detector import Detector

# used for testing
if __name__ == "__main__":
    edgeList = np.array(pd.read_csv("sample_data/small.csv"))
    detector = Detector(edgeList)
    results = detector.getLECommunities(
        log=True, xlsx=True, visualize=True  # just delete all args to set all to false
    )

    # print(results.groups)
    # print(results.graphs)