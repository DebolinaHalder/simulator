import pandas as pd
import random

rigid = 1
malleable = 2
evolving = 3


def gen_malleable(m, e, k, df, exp, shrk):
    sorted_df = df.sort_values(by='Total_cost', ascending=False)
    total_num = len(sorted_df) * k//100
    mal_num = len(sorted_df) * m//100
    evol_num = len(sorted_df) * e//100
    df1 = sorted_df.iloc[:total_num,:]
    print(len(df1))
    #df2 = sorted_df.iloc[:, number:]
    modified_df = df1.sample(frac=(mal_num + evol_num)/total_num, replace=False, random_state=1)
    malleable_df = modified_df.sample(frac=mal_num/(mal_num+evol_num), replace=False, random_state=1)
    evolving_df = modified_df[~modified_df.isin(malleable_df)].dropna()
    for index in df.index:
        if df.loc[index, 'id'] in malleable_df.id:
            df.loc[index, 'type'] = malleable
            df.loc[index, 'Max_resource'] = int(df.loc[index, 'Processors'] * (1 + exp/ 100))
            df.loc[index, 'Min_resource'] = int(df.loc[index, 'Processors'] * (1 - shrk / 100))
    for index in df.index:
        if df.loc[index, 'id'] in evolving_df.id:
            df.loc[index, 'type'] = evolving
            df.loc[index, 'Max_resource'] = int(df.loc[index, 'Processors'] * (1 + exp / 100))
            df.loc[index, 'Min_resource'] = int(df.loc[index, 'Processors'] * (1 -  shrk/ 100))
    return df


def main():
    dataframe = pd.read_csv("workload_final.csv")
    #print(len(dataframe))
    dataframe = dataframe.iloc[:100:]
    dataframe = gen_malleable(20, 10, 40, dataframe, 25, 10)
    #dataframe = dataframe.sort_values(by='Processors', ascending=False)

    dataframe.to_csv('workload_mal_evol.csv', index=False)


if __name__ == '__main__':
    main()
