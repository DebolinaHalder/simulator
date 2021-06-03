from typing import Union, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy import inexact, ndarray


def draw_plot(dataframeFlex, dataframeRigid):
    flexible = np.array(dataframeFlex['Start'])
    rigid = np.array(dataframeRigid['Start'])
    id = np.array(dataframeFlex['id'])
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    ax.scatter(id, rigid, label="rigid")
    ax.scatter(id, flexible, color = 'r', label="rigid", alpha = 0.5)
    #ax.plot(id, flexible, linestyles = "dashed", marker=".", color='r', markersize=14, label="flexible")
    name = "unshrinked/plots1/start.png"
    plt.savefig(name)

    return





def main():
    dataframe = pd.read_csv("unshrinked/result1/resource/mal/mal100_2016_1k.csv")
    daraframeRigid = pd.read_csv("unshrinked/result1/resource/rigid/rigid_2016_1k.csv")
    #dataframe = dataframe.iloc[0:1000:]
    #daraframeRigid = daraframeRigid.iloc[900:1000:]
    draw_plot(dataframe, daraframeRigid)


if __name__ == '__main__':
    main()
