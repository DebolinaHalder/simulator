from typing import Union, Tuple

import matplotlib.pyplot as plt
import numpy as np
from numpy import inexact, ndarray


def draw_plot(malleable, rigid, label, name):
    difference = []
    for i in malleable:
        difference.append(i)
    y = np.array(difference)
    x = np.linspace(10, 100, 10)
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    ax.plot(x, y, linewidth=3, marker=".", markersize=14)
    ax.set_xticks(range(10, 110, 10))
    ax.set_xlabel('percentage of malleable')
    ax.set_ylabel(label)
    #ax.hlines(rigid, 0, 100, colors='gray', linestyles='dashed', linewidth=1.5)
    right_side = ax.spines["right"]
    right_side.set_visible(False)
    top_side = ax.spines["top"]
    top_side.set_visible(False)
    #plt.show()
    name = "result/plots/" + name + ".pdf"
    plt.savefig(name)
    return





def main():
    wait_time = []
    turn_around_time = []
    span = []
    rigid = open(r"result/rigid/average_2016_25k.txt", "r")
    lines = rigid.read()
    lines = lines.split('(')
    lines = lines[1].split(')')
    lines = lines[0].split(',')
    wait_time_rigid = float(lines[0])
    turn_around_time_rigid = float(lines[1])
    span_rigid = float(lines[2])
    print(wait_time_rigid, turn_around_time_rigid, span_rigid)
    for i in range(10, 110, 10):
        filename = "result/flexible/average_mal"+str(i)+"_2016_25k.txt"
        print(filename)
        flexible = open(filename, "r")
        lines = flexible.read()
        lines = lines.split('(')
        lines = lines[1].split(')')
        lines = lines[0].split(',')
        wait_time.append(float(lines[0]))
        turn_around_time.append(float(lines[1]))
        span.append(float(lines[2]))
    draw_plot(wait_time, wait_time_rigid, "avg_wait_time (rigid) - average_wait_time (x% malleable)", "wait_time")
    draw_plot(turn_around_time, turn_around_time_rigid,
              "avg_turnaround_time (rigid) - average_turnaround_time (x%malleable)", "turnaround_time")

if __name__ == '__main__':
    main()
