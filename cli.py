from time import sleep
import numpy as np


def display_progress(n, length, times, cmd_size=100):
    mean = np.mean(times)
    progress = int(n / length * cmd_size)

    output = '['
    output += "=" * progress
    output += ">"
    output += "_" * (cmd_size - progress - 1)
    output += '] '
    output += str(n) + "/" + str(length)
    output += " Avg. " + str(mean) + "s. "
    output += "ETA. " + str((length - n) * mean) + "s."

    print('\r' + output, end='')

for i in range(400):
    display_progress(i, 4000, np.array([0.2, 0.2, 0.2, 0.2]))
    sleep(0.2)