import pandas as pd

reps = 10
source = "final_test/result4/result_application/"
dest = source + "result_mal_evol.csv"


def get_value(filename):
    malleable = open(filename, "r")
    lines = malleable.readlines()
    wait_time = float(lines[0])
    turn_around_time = float(lines[1])
    utilization = float(lines[3])
    return wait_time, turn_around_time, utilization


def main():
    df = pd.DataFrame(
        columns=['adp_res', 'adp_turn', 'adp_util', 'exp_res', 'exp_turn', 'exp_util', 'gain_res', 'gain_turn',
                 'gain_util',
                 'resr_res', 'resr_turn', 'resr_util', 'time_res', 'time_turn', 'time_util', 'reps', 'perc'])
    for i in range(10, 110, 10):
        for j in range(1, reps + 1, 1):
            fileadp = source + "adaptation/mal_evol/" + "average_mal_evol" + str(i) + str(j) + ".txt"
            fileexp = source + "expansion/mal_evol/" + "average_mal_evol" + str(i) + str(j) + ".txt"
            filegain = source + "gain/mal_evol/" + "average_mal_evol" + str(i) + str(
                j) + ".txt"
            fileres = source + "resource/mal_evol/" + "average_mal_evol" + str(i) + str(
                j) + ".txt"
            filetime = source + "time/mal_evol/" + "average_mal_evol" + str(i) + str(
                j) + ".txt"
            adp_res, adp_turn, adp_util = get_value(fileadp)
            exp_res, exp_turn, exp_util = get_value(fileexp)
            gain_res, gain_turn, gain_util = get_value(filegain)
            resr_res, resr_turn, resr_util = get_value(fileres)
            time_res, time_turn, time_util = get_value(filetime)
            df = df.append({'adp_res': adp_res, 'adp_turn': adp_turn, 'adp_util': adp_util, 'exp_res': exp_res,
                            'exp_turn': exp_turn, 'exp_util': exp_util,
                            'gain_res': gain_res, 'gain_turn': gain_turn, 'gain_util': gain_util, 'resr_res': resr_res,
                            'resr_turn': resr_turn, 'resr_util': resr_util,
                            'time_res': time_res, 'time_turn': time_turn, 'time_util': time_util, 'reps': j, 'perc': i},
                           ignore_index=True)

    df.to_csv(dest)

main()