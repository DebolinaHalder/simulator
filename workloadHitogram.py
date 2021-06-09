import pandas as pd
import matplotlib.pyplot as plt

def plot(name,dest):
    dataframe = pd.read_csv(name)
    ser1 = pd.Series(dataframe['Processors'])
    ser1.plot.hist(grid=True, bins=20, rwidth=0.9,
                       color='#607c8e')
    plt.title('Workload Histogram')
    plt.xlabel('Processors')
    plt.ylabel('Count')
    plt.grid(axis='y', alpha=0.75)
    plt.savefig(dest)

def main():
    name = "shrinked/workload5/rigid/workload_rigid_2016_1k.csv"
    dest = "unshrinked/plots1/workload.png"
    plot(name,dest)


main()