import pandas as pd
import random
import math

rigid = 1
malleable = 2
evolving = 3

#random.seed(123)
def gen_malleable_random(m, e, k, df, exp_m, shrk_m, exp_e, shrk_e):
    modified_df = df.sample(frac=(m + e) / 100, replace=False, random_state=1)
    malleable_df = modified_df.sample(frac=m / (m + e), replace=False, random_state=1)
    evolving_df = modified_df[~modified_df.isin(malleable_df)].dropna()
    for index in df.index:
        if df.loc[index, 'id'] in malleable_df.id:
            df.loc[index, 'type'] = malleable
            df.loc[index, 'Max_resource'] = math.ceil(df.loc[index, 'Processors'] * (1 + exp_m / 100))
            df.loc[index, 'Min_resource'] = math.ceil(df.loc[index, 'Processors'] * (1 - shrk_m / 100))
    for index in df.index:
        if df.loc[index, 'id'] in evolving_df.id:
            df.loc[index, 'type'] = evolving
            df.loc[index, 'Max_resource'] = math.ceil(df.loc[index, 'Processors'] * (1 + exp_e / 100))
            df.loc[index, 'Min_resource'] = math.ceil(df.loc[index, 'Processors'] * (1 - shrk_e / 100))
    return df

def gen_malleable(m, e, k, df, exp_m, shrk_m, exp_e, shrk_e):
    #df_order = df.drop(df[df.Processors < 10].index)
    sorted_df = df.sort_values(["Processors", "R_time"], ascending=(False, False))
    #sorted_df = df
    total_num = len(sorted_df) * k//100
    mal_num = len(sorted_df) * m//100
    evol_num = len(sorted_df) * e//100
    df1 = sorted_df.iloc[:total_num:]
    print(total_num, mal_num, evol_num)
    #df2 = sorted_df.iloc[:, number:]
    modified_df = df1.sample(frac=(mal_num + evol_num)/total_num, replace=False, random_state=1)
    malleable_df = modified_df.sample(frac=mal_num/(mal_num+evol_num), replace=False, random_state=1)
    evolving_df = modified_df[~modified_df.isin(malleable_df)].dropna()
    for index in df.index:
        if df.loc[index, 'id'] in malleable_df.id:
            df.loc[index, 'type'] = malleable
            df.loc[index, 'Max_resource'] = math.ceil(df.loc[index, 'Processors'] * (1 + exp_m/ 100))
            df.loc[index, 'Min_resource'] = math.ceil(df.loc[index, 'Processors'] * (1 - shrk_m / 100))

        if df.loc[index, 'id'] in evolving_df.id:
            df.loc[index, 'type'] = evolving
            df.loc[index, 'Max_resource'] = math.ceil(df.loc[index, 'Processors'] * (1 + exp_e / 100))
            df.loc[index, 'Min_resource'] = math.ceil(df.loc[index, 'Processors'] * (1 - shrk_e / 100))

    return df


def main():
    dataframe = pd.read_csv("synthetic/synthetic2.csv")
    #dataframe.to_csv('synthetic/workload12/rigid/workload_synthetic_rigid.csv', index=False)
    #print(len(dataframe))
    #dataframe = dataframe.iloc[15000:40000:]
    #dataframe = dataframe.iloc[15000:40000:]
    dataframe.to_csv('final_test/workload4/rigid/workload_rigidsynthetic1.csv')
    #dataframe = dataframe[dataframe['Processors'] != -1]
    #dataframe = dataframe[dataframe['Processors'] <= 9216]
    #dataframe = dataframe.iloc[5000:15000]
    #dataframe.to_csv('final_test/workload2/rigid/workload_rigidLLNL.csv', index=False)
    for i in range(10, 110, 10):
        #df = gen_malleable(i/2, i/2, i, dataframe, 35, 40, 60, 20)
        df = gen_malleable(i/2, i/2, i, dataframe, 60, 30, 60, 20)
        name = 'final_test/workload4/mal_evol/workload_mal_evol'+str(i)+'synthetic1.csv'
        df.to_csv(name, index=False)
    #dataframe = gen_malleable(20, 0, 20, dataframe, 35, 40, 60, 20)
    #dataframe = dataframe.sort_values(by='Processors', ascending=False)


    #dataframe.to_csv('sample.csv', index=False)


if __name__ == '__main__':
    main()
