import numpy as np

# ---- Параметры батареи из даташита ----
Q_NOM_MAH   = 137.0        # номинальная ёмкость, мА·ч
R_LOAD_OHM  = 68000.0      # нагрузка для кривой 68 кΩ
N_POINTS    = 200          # сколько точек писать в файл


def build_ocv_dod_file(
    t_anchor_h,
    V_anchor_V,
    output_file="ocv_dod.txt",
    n_points=N_POINTS,
    q_nom_mah=Q_NOM_MAH,
    r_load_ohm=R_LOAD_OHM,
):
    """
    Преобразует опорные точки (t, V) с графика разряда
    в таблицу (DOD_%, OCV_V) и пишет её в txt-файл.

    DOD считается кулоновским интегрированием:
        I(t) = V(t) / R        [А]
        q(t) = ∫ I dt          [мА·ч]
        DOD  = q(t) / Q_nom    [доля 0..1]
    """

    # 1. Регулярная сетка по времени
    t = np.linspace(t_anchor_h[0], t_anchor_h[-1], n_points)

    # 2. Интерполяция напряжения на эту сетку
    V = np.interp(t, t_anchor_h, V_anchor_V)

    # 3. Ток в мА (V в В, R в Ом → I в А; ×1000 → мА)
    I_mA = V / r_load_ohm * 1000.0

    # 4. Кулоновское интегрирование
    dt = np.diff(t, prepend=t[0])          # шаг по времени, ч
    charge_mah = np.cumsum(I_mA * dt)      # мА·ч

    # 5. DOD в процентах
    DOD_pct = charge_mah / q_nom_mah * 100.0

    # 6. Запись в файл
    with open(output_file, "w") as f:
        f.write("DOD_%,OCV_V\n")
        for d, v in zip(DOD_pct, V):
            f.write(f"{d:.3f},{v:.3f}\n")

    return DOD_pct, V


def read_ocv_dod(file_path="ocv_dod.txt"):
    """
    Читает txt со структурой DOD_%,OCV_V.
    Возвращает два массива numpy: DOD_pct, OCV_V.
    """
    data = np.loadtxt(file_path, delimiter=",", skiprows=1)
    DOD_pct = data[:, 0]
    OCV_V   = data[:, 1]
    return DOD_pct, OCV_V


def ocv_from_dod(dod_pct_current, DOD_table, OCV_table):
    """
    Интерполяция OCV по текущему DOD.
    Внутри модели вы работаете с x1 = DOD как долей (0..1),
    поэтому перед вызовом умножьте x1 на 100.
    """
    return np.interp(dod_pct_current, DOD_table, OCV_table)

t_anchor = np.array([0, 200, 500, 1000, 1500, 2000, 2300,
                     2500, 2700, 2850, 2950, 3050, 3150, 3250, 3300])
V_anchor = np.array([3.00, 2.98, 2.96, 2.94, 2.91, 2.88, 2.85,
                     2.80, 2.70, 2.55, 2.40, 2.25, 2.10, 2.00, 1.95])

build_ocv_dod_file(t_anchor, V_anchor, output_file="../data/datasheet/ocv_dod.txt")