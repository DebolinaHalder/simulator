from typing import Union, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
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
    name = "shrinked/result4/plots2/" + name + ".png"
    plt.savefig(name)
    return

def calculate_time(dataframe):
    length = len(dataframe) - 2000
    dataframe = dataframe.iloc[2000:length:]
    W_time = dataframe['Wait_time']
    Turn_time = dataframe['Turn_around_time']
    C_time = dataframe['Completion']
    A_time = dataframe['Arrival']
    E_time = dataframe['Exe_time']
    avg_w_time = W_time.mean()
    avg_t_time = Turn_time.mean()
    avg_e_time = E_time.mean()
    span = C_time.max() - A_time.min()
    return avg_w_time, avg_t_time, span, avg_e_time



def main():
    wait_time = []
    turn_around_time = []
    spn = []
    utilization = []
    exe = []
    wait_time_evol = []
    turn_around_time_evol = []
    span_evol = []
    utilization_evol = []
    exe_evol = []
    rigid = pd.read_csv("shrinked/result4/rigid/rigid_Unilu_15k.csv")
    w_time, t_time, span, exe_time = calculate_time(rigid)
    wait_time_rigid = w_time
    turn_around_time_rigid = t_time
    span_rigid = span
    exe_rigid = exe_time

    for i in range(10, 110, 10):
        malleable = pd.read_csv("shrinked/result4/mal/" + "mal" + str(i) +"_Unilu_15k.csv")
        w_time, t_time, span, exe_time = calculate_time(malleable)
        wait_time.append(w_time)
        turn_around_time.append(t_time)
        spn.append(span)
        exe.append(exe_time)
    for i in range(10, 110, 10):
        evolving = pd.read_csv("shrinked/result4/mal_evol/" + "mal_evol" + str(i) +"_Unilu_15k.csv")
        w_time, t_time, span, exe_time = calculate_time(evolving)
        wait_time_evol.append(w_time)
        turn_around_time_evol.append(t_time)
        span_evol.append(span)
        exe_evol.append(exe_time)
    draw_plot(turn_around_time, turn_around_time_evol, turn_around_time_rigid, "Average Turnaround Time","Turnaround time")
    draw_plot(wait_time, wait_time_evol, wait_time_rigid, "Average wait Time",
              "wait time")
    draw_plot(spn, span_evol, span_rigid, "Span",
              "span")
    draw_plot(exe, exe_evol, exe_rigid, "Average Execution Time",
              "execution")


if __name__ == '__main__':
    main()
