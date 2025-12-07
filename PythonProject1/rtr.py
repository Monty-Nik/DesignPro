import numpy as np
import matplotlib.pyplot as plt

# --- Константы и параметры ---
T_HALF = 40.2  # Период полураспада, часы
Y0 = 1.0  # Начальное количество вещества, кг

# Постоянная распада: lambda = ln(2) / T_HALF
LAMBDA = np.log(2) / T_HALF

# Интервал времени для моделирования (5 периодов полураспада)
T_MAX = 5 * T_HALF
# Шаг интегрирования (h), чем меньше, тем точнее
H = 0.5
N_STEPS = int(T_MAX / H)


# --- Функция ОДУ (y' = f(t, y)) ---
def f(t, y):
    """Правая часть ОДУ: y' = -lambda * y"""
    return -LAMBDA * y


# --- Метод Рунге-Кутты 2-го порядка (РК2, метод средней точки) ---
def runge_kutta_2(f, y0, t_start, t_end, h):
    """
    Численное решение ОДУ методом РК2.
    """
    t_points = np.arange(t_start, t_end + h, h)
    y_points = np.zeros(len(t_points))
    y_points[0] = y0

    for i in range(len(t_points) - 1):
        t_i = t_points[i]
        y_i = y_points[i]

        # 1. Вычисление k1
        k1 = h * f(t_i, y_i)

        # 2. Вычисление k2 (используется средняя точка)
        k2 = h * f(t_i + h / 2, y_i + k1 / 2)

        # 3. Обновление y
        y_points[i + 1] = y_i + k2

    return t_points, y_points


# --- Аналитическое решение (для сравнения) ---
def y_analytic(t, y0, lambd):
    """Точное решение y(t) = y0 * exp(-lambda * t)"""
    return y0 * np.exp(-lambd * t)


# --- Запуск программы ---
T, Y_RK2 = runge_kutta_2(f, Y0, 0, T_MAX, H)
Y_ANALYTIC = y_analytic(T, Y0, LAMBDA)
# --- Построение графика ---
plt.figure(figsize=(10, 6))

# График аналитического решения
plt.plot(T, Y_ANALYTIC, label='Аналитическое решение', color='blue', linewidth=2)

# График численного решения РК2
plt.plot(T, Y_RK2, label=f'Рунге-Кутта 2-го порядка ($h={H}$ ч)', color='red', linestyle='--', linewidth=1.5)

# Отметки периода полураспада
plt.axvline(T_HALF, color='gray', linestyle=':', label='$T_{1/2}$')
plt.axhline(0.5, color='gray', linestyle=':', label='$y(T_{1/2}) = 0.5$ кг')

plt.title(f'Радиоактивный распад изотопа $^{140}La$ ($\lambda \\approx {LAMBDA:.5f}$)', fontsize=14)
plt.xlabel('Время $t$, ч')
plt.ylabel('Количество вещества $y(t)$, кг')
plt.grid(True)
plt.legend()
plt.show()