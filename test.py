from typing import Dict
import random
import pandas as pd


def modify(tel):
    tel['guido'] = 4127
    del tel['sape']

def discard_white_space(old, new):
    file = open(old, "r")
    file_mod = open(new, "w")
    for line in file:
        line = ' '.join(line.split())
        file_mod.write(line)
        file_mod.write("\n")
    file.close()
    file_mod.close()
    return

def put_comma(old, new):
    file = open(old, "r")
    file_mod = open(new, "w")
    for line in file:
        line = line.replace(" ", ",")
        file_mod.write(line)
        file_mod.write("\n")
    file.close()
    file_mod.close()
    return


def convert_to_csv(old,new):
    text = pd.read_csv(old, header=None)
    text.columns = ['id', 'S_ime', 'W_time', 'R_time', 'Processors', 'Avg_CPU', 'Memory', 'Req_proc', 'Req_time'
                    , 'Req_mem', 'Status', 'U_id', 'G_id', 'Exe_num', 'Q_num', 'Part_num', 'Proc_job_no', 'Irre']
    text.to_csv(new, index=None)
    return


def main():
    discard_white_space("modified.txt", "workload_wspace.txt")
    put_comma("workload_wspace.txt", "workload_final.txt")
    convert_to_csv("workload_final.txt", "workload_all_2016.csv")
    dataframe = pd.read_csv("workload_all_2016.csv")
    dataframe = dataframe[['S_ime', 'W_time', 'R_time', 'Processors']]
    dataframe.insert(4, 'id', dataframe.index+1)
    dataframe.insert(5, "type", 1)
    dataframe.insert(6, "Max_resource", dataframe['Processors'])
    dataframe.insert(7, "Min_resource", dataframe['Processors'])
    dataframe.insert(8, "Total_cost", dataframe['Processors']*dataframe['R_time'])
    print(dataframe.head())
    dataframe.to_csv('workload_final_2016.csv', index=False)









main()