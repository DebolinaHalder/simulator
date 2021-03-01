import pandas as pd
import random
import math

rigid = 1
malleable = 2
evolving = 3


def gen_malleable(m, e, k, df, exp, shrk):
    df_order = df.drop(df[df.Processors < 10].index)
    sorted_df = df_order.sort_values(by='Total_cost', ascending= False)
    total_num = len(sorted_df) * k//100
    mal_num = len(sorted_df) * m//100
    evol_num = len(sorted_df) * e//100
    df1 = sorted_df.iloc[:total_num,:]
    print(total_num, mal_num, evol_num)
    #df2 = sorted_df.iloc[:, number:]
    modified_df = df1.sample(frac=(mal_num + evol_num)/total_num, replace=False, random_state=1)
    print(len(modified_df))
    malleable_df = modified_df.sample(frac=mal_num/(mal_num+evol_num), replace=False, random_state=1)
    evolving_df = modified_df[~modified_df.isin(malleable_df)].dropna()
    for index in df.index:
        if df.loc[index, 'id'] in malleable_df.id:
            df.loc[index, 'type'] = malleable
            df.loc[index, 'Max_resource'] = math.ceil(df.loc[index, 'Processors'] * (1 + exp/ 100))
            df.loc[index, 'Min_resource'] = math.ceil(df.loc[index, 'Processors'] * (1 - shrk / 100))
    for index in df.index:
        if df.loc[index, 'id'] in evolving_df.id:
            df.loc[index, 'type'] = evolving
            df.loc[index, 'Max_resource'] = math.ceil(df.loc[index, 'Processors'] * (1 + exp / 100))
            df.loc[index, 'Min_resource'] = math.ceil(df.loc[index, 'Processors'] * (1 -  shrk/ 100))
    return df


def main():
    dataframe = pd.read_csv("workload_final_2016.csv")
    #print(len(dataframe))
    dataframe = dataframe.iloc[10000:35000:]
    dataframe = gen_malleable(10, 0, 10, dataframe, 25, 10)
    #dataframe = dataframe.sort_values(by='Processors', ascending=False)

    dataframe.to_csv('workload/flexible/workload_mal10_2016_25k.csv', index=False)
    #dataframe.to_csv('sample.csv', index=False)


if __name__ == '__main__':
    main()
