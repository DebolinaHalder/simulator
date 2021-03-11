from typing import Union, Tuple

import matplotlib.pyplot as plt
import numpy as np
from numpy import inexact, ndarray


def draw_plot(malleable, rigid, label, name):
    y = np.array(malleable)
    x = np.linspace(10, 100, 10)
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    ax.plot(x, y, linewidth=3, marker=".", markersize=14)
    ax.set_xticks(range(10, 110, 10))
    ax.set_xlabel('Percentage of Malleable')
    ax.set_ylabel(label)
    ax.hlines(rigid, 0, 100, colors='gray', linestyles='dashed', linewidth=1.5)
    right_side = ax.spines["right"]
    right_side.set_visible(False)
    top_side = ax.spines["top"]
    top_side.set_visible(False)
    #plt.show()
    name = "result3/plots/" + name + ".png"
    plt.savefig(name)
    return





def main():
    wait_time = []
    turn_around_time = []
    span = []
    utilization = []
    rigid = open(r"result3/rigid/average_rigid_2016_15k_40k.txt", "r")
    lines = rigid.readlines()
    wait_time_rigid = float(lines[0])
    turn_around_time_rigid = float(lines[1])
    span_rigid = float(lines[2])
    utilization_rigid = float(lines[3])
    for i in range(10, 110, 10):
        location = "result3/mal/" + "average_mal" + str(i) +"_2016_15k_40k.txt"
        malleable = open(location, "r")
        lines = malleable.readlines()
        wait_time.append(float(lines[0]))
        turn_around_time.append(float(lines[1]))
        span.append(float(lines[2]))
        utilization.append(float(lines[3]))
    draw_plot(wait_time, wait_time_rigid, "Average Wait Time", "wait time")

if __name__ == '__main__':
    main()
