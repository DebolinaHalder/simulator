import pandas as pd
import random

rigid = 1
malleable = 2
evolving = 3


def gen_malleable(m, e, k, df, y):
    sorted_df = df.sort_values(by='Total_cost', ascending=False)
    number = len(sorted_df) * (m+e+k)//100
    df1 = sorted_df.iloc[:number,:]
    print(len(df1))
    #df2 = sorted_df.iloc[:, number:]
    modified_df = df1.sample(frac=(m+e)/100, replace=False, random_state=1)
    malleable_df = modified_df.sample(frac=m/(m+e), replace=False, random_state=1)
    evolving_df = modified_df[~modified_df.isin(malleable_df)].dropna()
    for index in df.index:
        if df.loc[index, 'id'] in malleable_df.id:
            df.loc[index, 'type'] = malleable
            df.loc[index, 'Max_resource'] = int(df.loc[index, 'Processors'] * (1 + y/ 100))
            df.loc[index, 'Min_resource'] = int(df.loc[index, 'Processors'] * (1 - y / 100))
    for index in df.index:
        if df.loc[index, 'id'] in evolving_df.id:
            df.loc[index, 'type'] = evolving
            df.loc[index, 'Max_resource'] = int(df.loc[index, 'Processors'] * (1 + y / 100))
            df.loc[index, 'Min_resource'] = int(df.loc[index, 'Processors'] * (1 - y / 100))
    return df


def main():
    dataframe = pd.read_csv("workload_final.csv")
    #print(len(dataframe))
    dataframe = dataframe.iloc[:100:]
    dataframe = gen_malleable(10, 10, 100, dataframe, 25)
    #dataframe = dataframe.sort_values(by='Processors', ascending=False)

    dataframe.to_csv('workload_mal_evol.csv', index=False)


if __name__ == '__main__':
    main()
