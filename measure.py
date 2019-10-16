import subprocess
from utils import log

def get_measure(model):
    if model is 'MacOS':
        measure = subprocess.run(['airport', '-s'], stdout=subprocess.PIPE)
    elif model is 'Raspi':
        measure = subprocess.run(['airport', '-s'], stdout=subprocess.PIPE)
    else:
        log('heatmap','ERROR','System not recognized.')
    return bash_to_list(measure.stdout.decode('utf-8'))

def bash_to_list(measure):
    measure_list = []
    for wifi_measure in measure.splitlines():
        wifi_measure_element = wifi_measure.split()
        for text in wifi_measure_element:
            if ':' in text and wifi_measure_element.index(text) != 1:
                for i in reversed(range(1, wifi_measure_element.index(text))):
                    wifi_measure_element[i-1] = wifi_measure_element[i-1] + ' ' + wifi_measure_element.pop(i)
                break
        # find returns -1 when there's no match
        if (wifi_measure_element[-2].find('WPA') != -1):
            del wifi_measure_element[-4:-2]
            wifi_measure_element[-1] = wifi_measure_element.pop(-2) + ' ' + wifi_measure_element[-1] 
        else:
            del wifi_measure_element[-3:-1]
        measure_list.append(wifi_measure_element)
    del measure_list[0]
    return measure_list
