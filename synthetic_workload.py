import pandas as pd


def make_csv():
    dataframe = pd.read_csv("synthetic/output1.csv")
    dataframe = dataframe.iloc[0:1000:]
    dataframe = dataframe[['S_ime', 'R_time', 'Processors', 'Sigma']]
    dataframe.insert(4, 'id', dataframe.index + 1)
    dataframe.insert(5, "type", 1)
    dataframe.insert(6, "Max_resource", dataframe['Processors'])
    dataframe.insert(7, "Min_resource", dataframe['Processors'])
    dataframe.insert(8, "Total_cost", dataframe['Processors'] * dataframe['R_time'])
    print(dataframe.head())
    dataframe.to_csv("synthetic/synthetic1.csv", index=False)


if __name__ == '__main__':
    make_csv()