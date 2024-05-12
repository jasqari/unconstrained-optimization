import math
import numpy as np
from Utils import visualize


def f(x):
    return (1 - x[0]) ** 2 + 5 * (x[1] - x[0] ** 2) ** 2


def gradient(x):
    dx0 = (20 * x[0] ** 3) - (20 * x[0] * x[1]) + (2 * x[0]) - 2
    dx1 = (10 * x[1]) - (10 * x[0] ** 2)
    return np.array([dx0, dx1], dtype=np.float64)


def Armijo(x, p, alpha, c, rho):
    x_i = x
    p_i = p
    alpha_i = alpha
    armijo = f(x_i + alpha_i * p_i) <= f(x_i) + c * alpha_i * np.dot(gradient(x_i), p_i)
    while not armijo:
        alpha_i = rho * alpha_i
        armijo = f(x_i + alpha_i * p_i) <= f(x_i) + c * alpha_i * np.dot(gradient(x_i), p_i)
    return alpha_i


def Wolfe(x, p, alpha, c1, c2):
    x_i = x
    p_i = p
    alpha_i = alpha
    alpha_min = 0
    alpha_max = math.inf
    while True:
        armijo = f(x_i + alpha_i * p_i) <= f(x_i) + c1 * alpha_i * np.dot(gradient(x_i), p_i)
        curvature = np.dot(gradient(x_i + alpha_i * p_i), p_i) >= c2 * np.dot(gradient(x_i), p_i)
        if not armijo:
            alpha_max = alpha_i
            alpha_i = 0.1 * (alpha_min + alpha_max)
        elif not curvature:
            alpha_min = alpha_i
            if alpha_max == math.inf:
                alpha_i = 2 * alpha_i
            else:
                alpha_i = 0.1 * (alpha_min + alpha_max)
        else:
            break
    return alpha_i


x0 = np.array([-2, -2])
num_iterations = 10000
tolerance = 0.00001
alpha = 1

x_i = x0
alpha_i = alpha
g_i = gradient(x0)
p_i = -1 * g_i
iteration = 0
x_path = [x_i]
f_path = [f(x_i)]
while iteration < num_iterations and np.linalg.norm(g_i) > tolerance:
    x_i_prev = x_i
    g_i_prev = g_i
    p_i_prev = p_i

    alpha_i = Wolfe(x_i_prev, p_i, alpha_i, 10 ^ -4, 0.1)
    x_i = x_i_prev + alpha_i * p_i_prev
    g_i = gradient(x_i)
    # beta_i = np.dot(g_i, g_i) / np.dot(g_i_prev, g_i_prev) # Fletcher–Reeves
    beta_i = np.dot(g_i, (g_i - g_i_prev)) / np.dot(g_i_prev, g_i_prev)  # Polak–Ribière
    p_i = -1 * g_i + beta_i * p_i_prev

    x_path.append(x_i)
    f_path.append(f(x_i))
    iteration += 1

print("x0:", x0)
print("f(x0):", f(x0))
print("\nNumber of iterations:", iteration)
print("\nx*:", x_i)
print("f(x*):", f(x_i))

visualize.contour_plot(np.array(x_path), np.array(f_path), "Conjugate Gradient")
