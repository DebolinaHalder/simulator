import pandas as pd


def gen_malleable(x, df):
    total_jobs = len(df)
    malleable_count = (total_jobs * x) // 100


def main():
    dataframe = pd.read_csv("workload_final.csv")
    gen_malleable(8, dataframe)


if __name__ == '__main__':
    main()
