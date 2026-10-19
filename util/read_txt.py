
import numpy as np

def read_dod_ocv(path_to_txt):
    """
    Читает txt-файл с колонками DOD_% и OCV_V.

    Возвращает:
        dod (np.ndarray): значения DOD_%
        ocv (np.ndarray): значения OCV_V
    """
    data = np.loadtxt(path_to_txt, delimiter=',', skiprows=1)
    return data[:, 0], data[:, 1]
