from typing import Union, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy import inexact, ndarray


def draw_plot(dataframeFlex, dataframeRigid):
    flexible = np.array(dataframeFlex['Exe_time'])
    rigid = np.array(dataframeRigid['Exe_time'])
    expansion = np.array(dataframeFlex['No_of_expansion'])
    shrinkage = np.array(dataframeFlex['No_of_shrinkage'])
    id = np.array(dataframeFlex['id'])
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    #ax.scatter(id, rigid, label="rigid")
    #ax.scatter(id, flexible, color = 'r', label="flexible", alpha = 0.5)
    ax.scatter(id, expansion, label="expansion", alpha=0.5)
    ax.scatter(id, shrinkage, label="shrinkage", alpha=0.5)
    ax.legend(frameon=False)
    #ax.plot(id, flexible, linestyles = "dashed", marker=".", color='r', markersize=14, label="flexible")
    name = "synthetic/result10/plots/no80expansion.png"
    plt.savefig(name)
    #plt.show()

    return





def main():
    dataframe = pd.read_csv("synthetic/result10/expansion/mal/mal80.csv")
    daraframeRigid = pd.read_csv("synthetic/result10/expansion/rigid/rigid.csv")
    dataframe = dataframe.iloc[0:1000:]
    daraframeRigid = daraframeRigid.iloc[0:1000:]
    draw_plot(dataframe, daraframeRigid)


if __name__ == '__main__':
    main()
