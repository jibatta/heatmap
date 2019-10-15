import subprocess
from utils import log

def get_measure(model):
    if model is 'MacOS':
        measure = subprocess.run(['airport', '-s'], stdout=subprocess.PIPE)
    elif model is 'Raspi':
        measure = subprocess.run(['airport', '-s'], stdout=subprocess.PIPE)
    else:
        log('heatmap','ERROR','System not recognized.')
    measure_list = bash_to_list(str(measure.stdout).encode().decode('unicode_escape'))
    print(measure_list)

def bash_to_list(measure):
    measure_list = []
    for wifi_measure in measure.splitlines():
        wifi_measure_element = wifi_measure.split()
        # find returns -1 when there's no match
        if (wifi_measure_element[-2].find('WPA') != -1):
            del wifi_measure_element[-4:-2]
        else:
            del wifi_measure_element[-3:-1]
        measure_list.append(wifi_measure_element)
    del measure_list[0]
    del measure_list[-1]
    return measure_list
