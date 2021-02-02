import pandas as pd
import random

rigid = 1
malleable = 2
evolving = 3


def gen_malleable(m, e, df, y):
    modified_df = df.sample(frac=(m+e)/100, replace=False, random_state=1)
    malleable_df = modified_df.sample(frac=m/(m+e), replace=False, random_state=1)
    evolving_df = modified_df[~modified_df.isin(malleable_df)].dropna()
    for index in df.index:
        if df.loc[index, 'id'] in malleable_df.id:
            df.loc[index, 'type'] = malleable
            df.loc[index, 'Max_resource'] = int(df.loc[index, 'Processors'] * (1 + y/100))
            df.loc[index, 'Min_resource'] = int(df.loc[index, 'Processors'] * (1 - y /100))
    for index in df.index:
        if df.loc[index, 'id'] in evolving_df.id:
            df.loc[index, 'type'] = evolving
    return df


def main():
    dataframe = pd.read_csv("workload_final1.csv")
    print(len(dataframe))
    dataframe = gen_malleable(8, 10, dataframe, 25)
    dataframe.to_csv('workload_mal_evol.csv', index=False)


if __name__ == '__main__':
    main()
