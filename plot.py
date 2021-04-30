from typing import Union, Tuple

import matplotlib.pyplot as plt
import numpy as np
from numpy import inexact, ndarray


def draw_plot(malleable1, malleable2, malleable3, rigid, label, name):
    malleable1 = np.array(malleable1)
    malleable2 = np.array(malleable2)
    malleable3 = np.array(malleable3)
    perc = np.linspace(10, 100, 10)
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    ax.plot(perc, malleable1, linewidth=3, marker=".", markersize=14, label="remaining resources")
    ax.plot(perc, malleable2, linewidth=3, marker=".", markersize=14, color='r', label="no_of_expansion")
    ax.plot(perc, malleable3, linewidth=3, marker=".", markersize=14, label="remaining time")
    ax.set_xticks(range(10, 110, 10))
    ax.set_xlabel('Percentage of elasticity')
    ax.set_ylabel(label)
    ax.hlines(rigid, 0, 100, colors='gray', linestyles='dashed', linewidth=1.5, label="rigid")
    ax.legend(loc='upper left', fontsize=10, frameon=False)
    right_side = ax.spines["right"]
    right_side.set_visible(False)
    top_side = ax.spines["top"]
    top_side.set_visible(False)
    #plt.show()
    name = "shrinked/result5/plots_evol/" + name + ".png"
    plt.savefig(name)
    return





def main():
    wait_time = []
    turn_around_time = []
    span = []
    utilization = []
    exe = []
    wait_time2 = []
    turn_around_time2 = []
    span2 = []
    utilization2 = []
    exe2 = []
    wait_time3 = []
    turn_around_time3 = []
    span3 = []
    utilization3 = []
    exe3 = []
    rigid = open(r"shrinked/result5/resource/rigid/average_rigid_2016_1k.txt", "r")
    lines = rigid.readlines()
    wait_time_rigid = float(lines[0])
    turn_around_time_rigid = float(lines[1])
    span_rigid = float(lines[2])
    utilization_rigid = float(lines[3])
    exe_rigid = float(lines[4])
    for i in range(10, 110, 10):
        location = "shrinked/result5/resource/mal_evol/" + "average_mal_evol" + str(i) +"_2016_1k.txt"
        malleable = open(location, "r")
        lines = malleable.readlines()
        wait_time.append(float(lines[0]))
        turn_around_time.append(float(lines[1]))
        span.append(float(lines[2]))
        utilization.append(float(lines[3]))
        exe.append(float(lines[4]))
    for i in range(10, 110, 10):
        location = "shrinked/result5/expansion/mal_evol/" + "average_mal_evol" + str(i) +"_2016_1k.txt"
        evol = open(location, "r")
        lines = evol.readlines()
        wait_time2.append(float(lines[0]))
        turn_around_time2.append(float(lines[1]))
        span2.append(float(lines[2]))
        utilization2.append(float(lines[3]))
        exe2.append(float(lines[4]))
    for i in range(10, 110, 10):
        location = "shrinked/result5/time/mal_evol/" + "average_mal_evol" + str(i) +"_2016_1k.txt"
        evol = open(location, "r")
        lines = evol.readlines()
        wait_time3.append(float(lines[0]))
        turn_around_time3.append(float(lines[1]))
        span3.append(float(lines[2]))
        utilization3.append(float(lines[3]))
        exe3.append(float(lines[4]))
    draw_plot(turn_around_time, turn_around_time2, turn_around_time3, turn_around_time_rigid, "Average Turnaround Time","Turnaround time")
    draw_plot(wait_time, wait_time2, wait_time3, wait_time_rigid, "Average wait Time",
              "wait time")
    draw_plot(span, span2, span3, span_rigid, "Span",
              "span")
    draw_plot(utilization, utilization2, utilization3, utilization_rigid, "Utilization",
              "utilization")
    draw_plot(exe, exe2, exe3, exe_rigid, "Average Execution Time",
              "execution")

if __name__ == '__main__':
    main()
