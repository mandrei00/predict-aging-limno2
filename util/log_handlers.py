import csv
import numpy as np
import datetime

import re

from pathlib import Path

def read_temperature_log(path_to_log: str) -> tuple[np.ndarray, np.ndarray]:
    times_list = []
    temps_list = []

    with open(path_to_log, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')

        for row in reader:
            times_list.append(float(row["timestamp"]))
            temps_list.append(float(row["temperature"]))

    times = np.array(times_list)
    temps = np.array(temps_list)
    return times, temps


import numpy as np


def read_voltage_log(path_to_log: str) -> tuple[np.ndarray, np.ndarray]:
    with open(path_to_log, 'r', encoding='utf-8') as f:
        header = f.readline().strip().split(',')

    time_idx = header.index("timestamp")
    voltage_idx = header.index("voltage_V")

    data = np.loadtxt(
        path_to_log,
        delimiter=',',
        skiprows=1,
        usecols=(time_idx, voltage_idx)
    )

    return data[:, 0], data[:, 1]


def read_current_log(path_to_log: str) -> tuple[np.ndarray, np.ndarray]:
    file_name = Path(path_to_log).stem
    match = re.search(r"(\d{8}T\d{6})", file_name)
    if not match:
        raise ValueError(
            f"Не удалось найти штамп даты/времени в имени файла: {file_name}"
        )

    date_str = match.group(1)
    dt_utc = datetime.datetime.strptime(date_str, "%Y%m%dT%H%M%S").replace(
        tzinfo=datetime.timezone.utc
    )
    dt = dt_utc.timestamp()

    with open(path_to_log, "r", encoding="utf-8") as f:
        header = f.readline().strip().split(",")

    time_idx = header.index("Timestamp(ms)")
    current_idx = header.index("Current(uA)")

    data = np.loadtxt(
        path_to_log,
        delimiter=",",
        skiprows=1,
        usecols=(time_idx, current_idx),
    )

    times_s = data[:, 0] * 1e-3 + dt
    currents_a = data[:, 1] * 1e-6

    return times_s, currents_a



if __name__ == "__main__":
    path_to_logs_temp = [
        r"C:\Users\User\Desktop\my-mcs-work\predict-aging-limno2\logs\temp\2026-10-11_18-48-38_temp\data.csv",
        r"C:\Users\User\Desktop\my-mcs-work\predict-aging-limno2\logs\temp\2026-10-15_09-09-43_temp\data.csv"
    ]
    times, temps = read_temperature_log(path_to_log=path_to_logs_temp[0])

