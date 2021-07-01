import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def gen_plot(key, name):
    df = pd.read_csv("final_test/result4/result_application/result_mal_evol.csv")
    perc = np.linspace(10, 100, 10)
    value_adaptation_med = []
    value_adaptation_25_quantile = []
    value_adaptation_75_quantile = []
    value_expansion_med = []
    value_expansion_25_quantile = []
    value_expansion_75_quantile = []
    value_gain_med = []
    value_gain_25_quantile = []
    value_gain_75_quantile = []
    value_resource_med = []
    value_resource_25_quantile = []
    value_resource_75_quantile = []
    value_time_med = []
    value_time_25_quantile = []
    value_time_75_quantile = []

    for p in perc:
        col = "adp_" + key
        res_adp = df[col][df['perc'] == p]
        value_adaptation_med.append(np.median(res_adp))
        value_adaptation_25_quantile.append(np.quantile(res_adp, [.25])[0])
        value_adaptation_75_quantile.append(np.quantile(res_adp, [.75])[0])

        col = "exp_" + key
        res_adp = df[col][df['perc'] == p]
        value_expansion_med.append(np.median(res_adp))
        value_expansion_25_quantile.append(np.quantile(res_adp, [.25])[0])
        value_expansion_75_quantile.append(np.quantile(res_adp, [.75])[0])

        col = "gain_" + key
        res_adp = df[col][df['perc'] == p]
        value_gain_med.append(np.median(res_adp))
        value_gain_25_quantile.append(np.quantile(res_adp, [.25])[0])
        value_gain_75_quantile.append(np.quantile(res_adp, [.75])[0])

        col = "resr_" + key
        res_adp = df[col][df['perc'] == p]
        value_resource_med.append(np.median(res_adp))
        value_resource_25_quantile.append(np.quantile(res_adp, [.25])[0])
        value_resource_75_quantile.append(np.quantile(res_adp, [.75])[0])

        col = "time_" + key
        res_adp = df[col][df['perc'] == p]
        value_time_med.append(np.median(res_adp))
        value_time_25_quantile.append(np.quantile(res_adp, [.25])[0])
        value_time_75_quantile.append(np.quantile(res_adp, [.75])[0])

    fig, ax = plt.subplots(1, 1, figsize=(8, 8))

    ax.plot(perc, value_adaptation_med, c="r", label='Adaptation')
    ax.plot(perc, value_expansion_med, c="g", label='Expansion')
    ax.plot(perc, value_gain_med, c="b", label='Gain')
    ax.plot(perc, value_resource_med, c="k", label='Resource')
    ax.plot(perc, value_time_med, c="y", label='Time')
    #ax.fill_between(perc, value_adaptation_25_quantile, value_adaptation_75_quantile, facecolor='r', alpha=.3)
    #ax.fill_between(perc, value_expansion_25_quantile, value_expansion_75_quantile, facecolor='g', alpha=.3)
    #ax.fill_between(perc, value_gain_25_quantile, value_gain_75_quantile, facecolor='b', alpha=.3)
    #ax.fill_between(perc, value_resource_25_quantile, value_resource_75_quantile, facecolor='k', alpha=.3)
    #ax.fill_between(perc, value_time_25_quantile, value_time_75_quantile, facecolor='y', alpha=.3)
    #ax.fill_between(sample_size, dist_rf_25_quantile, dist_rf_75_quantile, facecolor='k', alpha=.3)

    ax.set_xticks(range(10, 110, 10))
    ax.set_xlabel('Percentage of elasticity')
    ax.set_ylabel(name)
    ax.legend(loc='upper left', fontsize=10, frameon=False)
    right_side = ax.spines["right"]
    right_side.set_visible(False)
    top_side = ax.spines["top"]
    top_side.set_visible(False)
    plt.show()
    # plt.savefig('plots/sim_res_spherical.pdf')


def main():
    gen_plot("util", "average turn")


if __name__ == '__main__':
    main()




