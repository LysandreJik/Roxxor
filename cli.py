import numpy as np
from datetime import datetime, timedelta


def display_progress(n, length, times, cmd_size=100):
    mean = np.mean(times)
    progress = int(n / length * cmd_size)

    output = '['
    output += "=" * progress
    output += ">"
    output += "_" * (cmd_size - progress - 1)
    output += '] '
    output += str(n) + "/" + str(length)
    output += " Avg. " + str(int(mean)) + "s. "
    output += "ETA. " + "%dd %dh %dm %ds" % display_hours_and_minutes(int((length - n) * mean)) + "s."

    print('\r' + output, end='')


def display_hours_and_minutes(n):
    """
    Convert number of seconds into days, hours, minutes and seconds
    :param n:
    :return:
    """
    d = datetime(1, 1, 1) + timedelta(seconds=n)
    return d.day - 1, d.hour, d.minute, d.second
