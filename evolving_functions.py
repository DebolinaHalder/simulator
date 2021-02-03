import random
import numpy as np
from Class import Phase

max_no_of_phase = 4
min_no_of_phase = 1
max_time = 80
min_time = 10
max_cores = 5
min_cores = 2
exp_probability = 0.6
expansion_event = 1
shrinkage_event = 2


def create_phases():
    no_of_phase = random.randint(1, 4)
    phase = []
    for i in range(no_of_phase):
        s = np.random.binomial(1, exp_probability)
        time = random.randint(min_time, max_time)
        cores = random.randint(min_cores, max_cores)
        if s == 1:
            p = Phase(expansion_event, cores, time)
        else:
            p = phase(shrinkage_event, cores, time)
        phase.append(p)
    return phase




create_phases()