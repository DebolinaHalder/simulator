import matplotlib.pyplot as plt
import numpy as np
import pandas as pd




def main():
    rigid = pd.read_csv('result3/rigid/processor_rigid_2016_15k_40k.csv')
    malleable10 = pd.read_csv('result3/mal/processor_mal100_2016_15k_40k.csv')
    mal_evol60 = pd.read_csv('result3/mal_evol/processor_malevol60_2016_15k_40k.csv')
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    ax.step(rigid['time'], rigid['cores']/rigid['running_job_len'], color = 'grey', where='post', alpha = 1)
    ax.step(malleable10['time'], malleable10['cores']/malleable10['running_job_len'], color='r', where='post', alpha = 0.5)
    plt.show()


main()
