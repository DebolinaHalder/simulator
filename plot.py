from typing import Union, Tuple

import matplotlib.pyplot as plt
import numpy as np
from numpy import inexact, ndarray


def draw_plot(malleable, evolving, rigid, label, name):
    malleable = np.array(malleable)
    evolving = np.array(evolving)
    perc = np.linspace(10, 100, 10)
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    ax.plot(perc, malleable, linewidth=3, marker=".", markersize=14, label="malleable")
    ax.plot(perc, evolving, linewidth=3, marker=".", markersize=14, color='r', label="malleable and evolving")
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
    name = "synthetic/result4/plots/" + name + ".png"
    plt.savefig(name)
    return





def main():
    wait_time = []
    turn_around_time = []
    span = []
    utilization = []
    exe = []
    wait_time_evol = []
    turn_around_time_evol = []
    span_evol = []
    utilization_evol = []
    exe_evol = []
    rigid = open(r"synthetic/result4/rigid/average_rigid_synthetic4_256.txt", "r")
    lines = rigid.readlines()
    wait_time_rigid = float(lines[0])
    turn_around_time_rigid = float(lines[1])
    span_rigid = float(lines[2])
    utilization_rigid = float(lines[3])
    exe_rigid = float(lines[4])
    for i in range(10, 110, 10):
        location = "synthetic/result4/mal/" + "average_mal" + str(i) +"_synthetic4_256.txt"
        malleable = open(location, "r")
        lines = malleable.readlines()
        wait_time.append(float(lines[0]))
        turn_around_time.append(float(lines[1]))
        span.append(float(lines[2]))
        utilization.append(float(lines[3]))
        exe.append(float(lines[4]))
    for i in range(10, 110, 10):
        location = "synthetic/result4/mal_evol/" + "average_mal_evol" + str(i) +"_synthetic4_256.txt"
        evol = open(location, "r")
        lines = evol.readlines()
        wait_time_evol.append(float(lines[0]))
        turn_around_time_evol.append(float(lines[1]))
        span_evol.append(float(lines[2]))
        utilization_evol.append(float(lines[3]))
        exe_evol.append(float(lines[4]))
    draw_plot(turn_around_time, turn_around_time_evol, turn_around_time_rigid, "Average Turnaround Time","Turnaround time")
    draw_plot(wait_time, wait_time_evol, wait_time_rigid, "Average wait Time",
              "wait time")
    draw_plot(span, span_evol, span_rigid, "Span",
              "span")
    draw_plot(utilization, utilization_evol, utilization_rigid, "Utilization",
              "utilization")
    draw_plot(exe, exe_evol, exe_rigid, "Average Execution Time",
              "execution")

if __name__ == '__main__':
    main()
