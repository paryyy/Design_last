from sympy.abc import x
from sympy import Eq, solve
import numpy as np
import math


def DeltaP():
    from sympy.abc import x

    Table_list = [
        [50, Eq((-0.0721 * (Horizontal_parameter_Fig6_34 ** 2)) - (0.6359 * Horizontal_parameter_Fig6_34) - 5.6494, x)],
        [100, Eq((-0.0945 * Horizontal_parameter_Fig6_34 ** 2) - (0.7361 * Horizontal_parameter_Fig6_34) - 4.9607, x)],
        [200, Eq((-0.1024 * Horizontal_parameter_Fig6_34 ** 2) - (0.8044 * Horizontal_parameter_Fig6_34) - 4.4764, x)],
        [400, Eq((-0.1027 * Horizontal_parameter_Fig6_34 ** 2) - (0.8363 * Horizontal_parameter_Fig6_34) - 4.0548, x)],
        [800, Eq((-0.1194 * Horizontal_parameter_Fig6_34 ** 2) - (0.9476 * Horizontal_parameter_Fig6_34) - 3.7313, x)],
        [1200, Eq((-0.128 * Horizontal_parameter_Fig6_34 ** 2) - (0.9886 * Horizontal_parameter_Fig6_34) - 3.5525, x)]]
    # for i in range(10):

    Verticalup = solve(Table_list[5][1])
    Verticalup = Verticalup[0]
    Verticalup = math.exp(Verticalup)
    Verticaldown = solve(Table_list[0][1])
    Verticaldown = Verticaldown[0]
    Verticaldown = math.exp(Verticaldown)
    print(Verticaldown)
    if math.exp(Vertical_parameter_Fig6_34) > Verticalup:
        context['Approximate flooding'] = 'Approximate flooding'
    elif math.exp(Vertical_parameter_Fig6_34) < Verticaldown:
        context['Pressure Drop'] = 'Gas Pressure Drop is under 50 [pa]'

    for i in range(5):
        Vertical_list1 = solve(Table_list[i][1])
        Vertical_list2 = solve(Table_list[i + 1][1])
        Vertical_list1 = Vertical_list1[0]
        Vertical_list2 = Vertical_list2[0]
        if Vertical_list1 <= Vertical_parameter_Fig6_34 <= Vertical_list2:
            x0 = math.exp(Vertical_list1)
            x1 = math.exp(Vertical_list2)
            y0 = Table_list[i][0]
            y1 = Table_list[i + 1][0]
            x = math.exp(Vertical_parameter_Fig6_34)
            Delta_P = round((((y0) * (x1 - x)) + ((y1) * (x - x0))) / (x1 - x0), 3)
            return Delta_P
            # print(Delta_P)


Delta_P = DeltaP()
print(Delta_P)
print(context)
