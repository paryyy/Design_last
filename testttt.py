from sympy.abc import x
from sympy import Eq, solve
import numpy as np
import math
def Entrainment():
    from sympy.abc import x
    Horizontal_parameter = np.log(0.0622)
    VntoVf = 0.8
    VntoVf_list = [[0.3, Eq(-0.3707 * Horizontal_parameter - 7.2003, x)],
                   [0.35, Eq(-0.5005 * Horizontal_parameter -7.0611, x)],
                   [0.4, Eq(-0.6286 * Horizontal_parameter -7.0323, x)],
                   [0.45, Eq(-0.7449 * Horizontal_parameter -6.9309, x)],
                   [0.5, Eq(-0.8953 * Horizontal_parameter -7.0127, x)],
                   [0.6, Eq(-0.9957 * Horizontal_parameter -6.9485, x)],
                   [0.7, Eq(-1.0439 * Horizontal_parameter -6.5051, x)],
                   [0.8, Eq(-1.0817 * Horizontal_parameter - 6.2877, x)],
                   [0.9, Eq(-1.0578 * Horizontal_parameter -5.8211, x)],
                   [0.95, Eq(-1.0182 * Horizontal_parameter -5.0749, x)]]
    # for i in range(10):
    E11 = 0
    for i in range(10):
        if VntoVf_list[i][0] == VntoVf:
            Eqq = VntoVf_list[i][1]
            E11 = solve(Eqq)
            E11 = round(math.exp(E11[0]),4)
            return E11
        if VntoVf_list[i][0] != VntoVf:
            for t in range(9):
                if VntoVf_list[t][0] < VntoVf < VntoVf_list[t + 1][0]:
                    Eqq1 = VntoVf_list[t][1]
                    Eqq2 = VntoVf_list[t + 1][1]
                    E1 = solve(Eqq1)
                    E2 = solve(Eqq2)
                    x0 = VntoVf_list[t][0]
                    x1 = VntoVf_list[t + 1][0]
                    y0 = E1[0]
                    y1 = E2[0]
                    x = VntoVf
                    E11 = (((y0) * (x1 - x)) + ((y1) * (x - x0))) / (x1 - x0)
                    E11 = round(math.exp(E11),4)
                    return E11

E = Entrainment()
print(E)

if E > 0.075:
    context['Ewarning'] = 'Warning Entrainment: E is more than 0.075'
    context['E'] = E
elif E < 0.075:
    context['E'] = E