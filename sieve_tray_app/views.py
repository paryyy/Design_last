from django.shortcuts import render
from .forms import give_data_form, give_data_packed_form
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
import math
import numpy as np
import pandas as pd
from sympy.abc import x
from sympy import Eq, solve

from django.http import HttpResponse


# create Home page
def Home_page_view(request):
    if request.method == 'POST':
        data = request.POST
        if data['method'] == 'Treybal' and data['types_tower'] == 'Sieve Tray':
            return redirect('/Home/sieveTray/')
        elif data['method'] == 'Treybal' and data['types_tower'] == 'Packed Tray':
            # return render(request, 'packedTray.html',{data['method']:'trybal', data['types_tower']: 'packed tray' })
            return redirect('/Home/packedtray/')
    return render(request, 'Home.html')


def packedTray_view(request):
    if request.method == "POST":
        form = give_data_packed_form(request.POST)
        if form.is_valid():
            context = {'form': form}
            Tower_Diam = float(form.cleaned_data['Tower_Diam'])
            Gas_Flowrate = float(form.cleaned_data['Gas_Flowrate'])
            Liq_Flowrate = float(form.cleaned_data['Liq_Flowrate'])
            Gas_density = float(form.cleaned_data['Gas_density'])  # 1.25[Kg/m^3]
            Liq_density = float(form.cleaned_data['Liq_density'])  # 1235 [kg/m^3]
            viscosity_sub_in_liq = float(form.cleaned_data['viscosity_sub_in_liq'])  # 0.0025 [Kg/m.s]
            Cf = float(form.cleaned_data['Cf'])
            Area = (math.pi * (Tower_Diam) ** 2) / 4
            G_prim = Gas_Flowrate / Area  # [Kg/m^2.s]
            Horizontal_parameter_Fig6_34 = round(
                (Liq_Flowrate / Gas_Flowrate) * (Gas_density / (Liq_density - Gas_density)) ** 0.5, 4)  # 0.125
            print('H:',Horizontal_parameter_Fig6_34)
            Horizontal_parameter_Fig6_34 = np.log(Horizontal_parameter_Fig6_34)
            Vertical_parameter_Fig6_34 = (G_prim ** 2 * Cf * (viscosity_sub_in_liq ** 0.1)) / (
                    Gas_density * (Liq_density - Gas_density))
            print( 'V: ',Vertical_parameter_Fig6_34)
            Vertical_parameter_Fig6_34 = np.log(Vertical_parameter_Fig6_34)


            def DeltaP():
                from sympy.abc import x

                Table_list = [
                    [50, Eq((-0.0721 * (Horizontal_parameter_Fig6_34 ** 2)) - (
                            0.6359 * Horizontal_parameter_Fig6_34) - 5.6494, x)],
                    [100, Eq((-0.0945 * Horizontal_parameter_Fig6_34 ** 2) - (
                            0.7361 * Horizontal_parameter_Fig6_34) - 4.9607, x)],
                    [200, Eq((-0.1024 * Horizontal_parameter_Fig6_34 ** 2) - (
                            0.8044 * Horizontal_parameter_Fig6_34) - 4.4764, x)],
                    [400, Eq((-0.1027 * Horizontal_parameter_Fig6_34 ** 2) - (
                            0.8363 * Horizontal_parameter_Fig6_34) - 4.0548, x)],
                    [800, Eq((-0.1194 * Horizontal_parameter_Fig6_34 ** 2) - (
                            0.9476 * Horizontal_parameter_Fig6_34) - 3.7313, x)],
                    [1200,
                     Eq((-0.128 * Horizontal_parameter_Fig6_34 ** 2) - (0.9886 * Horizontal_parameter_Fig6_34) - 3.5525,
                        x)]]
                # for i in range(10):

                Verticalup = solve(Table_list[5][1])
                Verticalup = Verticalup[0]
                Verticalup = math.exp(Verticalup)
                print('Verticalup= ', Verticalup)
                Verticaldown = solve(Table_list[0][1])
                Verticaldown = Verticaldown[0]
                Verticaldown = math.exp(Verticaldown)
                print('Verticaldown= ',Verticaldown)

                if math.exp(Vertical_parameter_Fig6_34) > Verticalup:
                    context['Approximate_flooding'] = 'Approximate flooding'
                elif math.exp(Vertical_parameter_Fig6_34) < Verticaldown:
                    context['Pressure_Drop'] = 'Gas Pressure Drop is under 50 [pa]'

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
            if Delta_P != None:
                if Delta_P > 400:
                    context['Pup400'] = 'Gas Pressure Drop> 400 [pa]'
                elif Delta_P < 200:
                    context['Pdown400'] = 'Gas Pressure Drop < 200 [pa]'
            context['Delta_P'] = Delta_P
            return render(request, 'packedTray/packedTray.html', context)
    else:
        form = give_data_packed_form()
        return render(request, 'packedTray/packedTray.html', {'form': form})


# Create your views here.
# create sieve tray page
def sieveTray_view(request, ):
    if request.method == "POST":
        data = request.POST


        try:
            f_2 = (data['f'])
            f_2 = float(f_2)
            print('yesssss')

        except :
            f_2 = None

        form = give_data_form(request.POST)
        if form.is_valid():

            Volumetric_flow_rate_G = float(form.cleaned_data['FlowRateVapor'])
            Volumetric_flow_rate_L = float(form.cleaned_data['FlowRateLiquid'])
            Pressure = float(form.cleaned_data['Pressure'])
            viscosity = float(form.cleaned_data['viscosity'])
            liquid_density = float(form.cleaned_data['liquid_density'])
            Gas_density = float(form.cleaned_data['Gas_density'])  # kg/m^3
            surface_tension = float(form.cleaned_data['surface_tension'])
            TowerDiameter = float(form.cleaned_data['TowerDiameter'])
            tray_spacing = float(form.cleaned_data['tray_spacing'])
            times_w_t = float(form.cleaned_data['times_w_t'])
            g = 9.807  # [m^2/s]
            gc = 1
            context = {'form': form}
            context['tray_spacing'] = tray_spacing
            # check material and Do
            material_design = form.cleaned_data['material_design']
            if material_design == 'Stainless steel':
                material_design_id = 1
            elif material_design == 'Carbon steel':
                material_design_id = 2
            Do = float(form.cleaned_data['Do'])

            # به دست آوردن نسبت ضخامت به قطر  L/Do  جدول 6.2 شماره 2
            def _ticknessToHoleDiameter_():
                Do_Stainless_Carbon_list = [[3, 0.65, 0.760], [4.5, 0.43, 0.702], [6.0, 0.32, 0.64],
                                            [9.0, 0.22, 0.5],
                                            [12.0, 0.16, 0.38], [15.0, 0.17, 0.3], [18.0, 0.11, 0.25]]
                df_Do_Stainless_Carbon_list = pd.DataFrame(Do_Stainless_Carbon_list,
                                                           columns='Hole_Diameter 1 2'.split())
                # دسترسی به شماره ایندکس ها
                ticknessToHoleDiameter = 0
                for i in range(7):
                    if Do_Stainless_Carbon_list[i][0] == Do:
                        ticknessToHoleDiameter = Do_Stainless_Carbon_list[i][material_design_id]
                if Do_Stainless_Carbon_list[i][0] != Do:
                    for i in range(6):
                        if Do_Stainless_Carbon_list[i][0] < Do < Do_Stainless_Carbon_list[i + 1][0]:
                            x0 = Do_Stainless_Carbon_list[i][0]
                            x1 = Do_Stainless_Carbon_list[i + 1][0]
                            y0 = Do_Stainless_Carbon_list[i][material_design_id]
                            y1 = Do_Stainless_Carbon_list[i + 1][material_design_id]
                            x = Do
                            ticknessToHoleDiameter = (((y0) * (x1 - x)) + ((y1) * (x - x0))) / (x1 - x0)
                return ticknessToHoleDiameter

            ticknessToHoleDiameter = _ticknessToHoleDiameter_()
            Times_dis_hol = float(form.cleaned_data['Times_dis_hol'])  # P'/Do

            P_prim = math.ceil(Times_dis_hol * Do)

            L = math.ceil(Do * ticknessToHoleDiameter)  # [mm]
            division_L_to_do = ticknessToHoleDiameter
            context['L'] = L

            # print('L is= ', L)
            # تابعی برای منطقی و رند کردن شعاع ها
            def _round_diameter(td):
                td = round(td, 2)
                t_tuple = math.modf(td)
                t_dec = t_tuple[0] * 100
                t_dec = round(t_dec)
                while t_dec % 5 != 0:
                    t_dec += 1
                td = t_tuple[1] + (t_dec / 100)
                return td

            division_AoToAa = round(0.907 * (Do ** 2 / P_prim ** 2), 4)
            #  print(Do)
            def _calc_vf_():
                #  {{ Calculation CF }}
                # ابتدا L'/G'(density_g/density_l)^0.5 که نامش را division_for_CF میگذاریم، را  محاسبه میکنیم
                division_for_cf = ((Volumetric_flow_rate_L * liquid_density) / (
                        Volumetric_flow_rate_G * Gas_density)) * (
                                          Gas_density / liquid_density) ** 0.5
                if 0.01 <= division_for_cf < 0.1 and division_AoToAa>0.1 :
                    division_for_cf = 0.1
                # Calculation alfa and beta for CF
                alfa = 0.0744 * tray_spacing + 0.01173
                beta = 0.0304 * tray_spacing + 0.015
                if division_AoToAa <= 0.1:  # question for >=
                    alfa = alfa * ((5 * division_AoToAa) + 0.5)
                    beta = beta * ((5 * division_AoToAa) + 0.5)
                #  Calc CF
                cf = (alfa * (math.log((1 / division_for_cf), 10)) + beta) * (surface_tension / 0.020) ** 0.2
                # print('CF= ', cf)
                # {{ Calc VF }}
                vf = cf * ((liquid_density - Gas_density) / Gas_density) ** 0.5

                return vf

            def _w_to_area_used_by_one_downspout_():
                division_ad_to_at_in_w_to_t_list = [[0.6, 5.257], [0.65, 6.899], [0.7, 8.808], [0.75, 11.255],
                                                    [0.8, 14.145]]

                for i in range(5):
                    if division_ad_to_at_in_w_to_t_list[i][0] == times_w_t:
                        w_to_area_used_by_one_downspout = division_ad_to_at_in_w_to_t_list[i][1]
                        return w_to_area_used_by_one_downspout
                    if division_ad_to_at_in_w_to_t_list[i][0] != times_w_t:
                        for t in range(5):
                            if division_ad_to_at_in_w_to_t_list[t][0] < times_w_t < \
                                    division_ad_to_at_in_w_to_t_list[t + 1][0]:
                                x0 = division_ad_to_at_in_w_to_t_list[t][0]
                                x1 = division_ad_to_at_in_w_to_t_list[t + 1][0]
                                y0 = division_ad_to_at_in_w_to_t_list[t][1]
                                y1 = division_ad_to_at_in_w_to_t_list[t + 1][1]
                                x = times_w_t
                                w_to_area_used_by_one_downspout = round(
                                    (((y0) * (x1 - x)) + ((y1) * (x - x0))) / (x1 - x0), 4)
                                return w_to_area_used_by_one_downspout

            w_to_area_used_by_one_downspout = _w_to_area_used_by_one_downspout_()

            # محاسبه مساحت ها
            def _calc_areas_(td):
                at = round(math.pi * td ** 2 / 4, 4)
                # محاسبه طول بند W  با قطر جدید
                w = round(times_w_t * td, 4)  # [m]
                # محاسبه سطح مقطع ناودان
                ad = round(WToAreaUsedByOneDownSpout / 100 * at, 4)  # [m^2]
                # print(Ad)
                # مساحت سطح فعال
                aa = round((at - 2 * ad) - (0.2 * (at - 2 * ad)), 4)
                # print('Ad', Ad)
                return [at, ad, aa, w]

            def _calc_atmospheric_():
                vf = _calc_vf_()
                # سطح مقطع کل برج منهای یک ناودان
                at, ad = _calc_areas_(TowerDiameter)[0], _calc_areas_(TowerDiameter)[1]
                an = at - ad
                vn = Volumetric_flow_rate_G / an
                #  print(vn)
                #  print(an)
                vntovf = round(vn / vf, 4)
                td = TowerDiameter
                aa = _calc_areas_(td)[2]
                w = _calc_areas_(td)[3]
                context['vntovf'] = vntovf
                if vntovf > 0.8:
                    context['vntovf_warning'] = 'Warning: '
                td = round(td, 4)
                if (Volumetric_flow_rate_L / td) > 0.015:
                    context['qtoTd_War'] = 'Warning: Liquid FlowRate/Tower Diameter > 0.015'
                    context['qtoTd'] = round(Volumetric_flow_rate_L / td, 4)
                return [td, ad, aa, w, an, vntovf]

            WToAreaUsedByOneDownSpout = _w_to_area_used_by_one_downspout_()

            def _calc_under_pressure_():
                t_d = TowerDiameter
                if Volumetric_flow_rate_L / (t_d * times_w_t) > 0.032:
                    context['qtowWar'] = 'Warning: Liquid FlowRate/Weir length> 0.032'
                    context['qtow'] = round(Volumetric_flow_rate_L / (t_d * times_w_t), 4)
                t_d = _round_diameter(t_d)
                at, ad, aa, w = _calc_areas_(t_d)
                an = round(at - ad, 4)
                vn = Volumetric_flow_rate_G / an
                vf = _calc_vf_()
                vntovf_under_pressure = round(vn / vf, 4)
                context['vntovf_under_pressure'] = vntovf_under_pressure
                if vntovf_under_pressure > 0.8:
                    context['vntovf_under_pressure_warning'] = 'Warning: V/Vf > 0.8 in under Pressure Tower ! '

                return [t_d, ad, aa, w, an, vntovf_under_pressure]

            # {{ محاسبات مربوط به برج اتمسفریک , خلا }}
            if Pressure == 1:
                Td = _calc_atmospheric_()[0]
                Ad = _calc_atmospheric_()[1]
                Aa = _calc_atmospheric_()[2]
                print('Aa=', Aa)
                W = _calc_atmospheric_()[3]
                An = _calc_atmospheric_()[4]
                VntoVf = _calc_atmospheric_()[5]

            # {{ محاسبات مربوط به برج تحت فشار }}
            if Pressure > 1:
                Td = _calc_under_pressure_()[0]
                Ad = _calc_under_pressure_()[1]
                Aa = _calc_under_pressure_()[2]
                W = _calc_under_pressure_()[3]
                An = _calc_under_pressure_()[4]
                VntoVf = _calc_under_pressure_()[5]

                # print('An= ', An)
                # print('Td_under_pressure= ', Td_under_pressure)
            context['W'] = W
            context['Td'] = Td

            # {{ مسئله هیدرودینامیک }}

            def _h1_():
                # hh1 همون h1 هست
                hh1 = round((1 / 1.839 * Volumetric_flow_rate_L / W) ** (2 / 3), 4)  # [m]
                # print(hh1)
                if times_w_t < 0.7:
                    # solve w as x
                    eq_solve_w = Eq((Td / W) ** 2 - ((((Td / W) ** 2) - 1) ** 0.5 + (2 * hh1 / Td * (Td / W))) ** 2,
                                    x ** 2)
                    y = solve(eq_solve_w)  # [m^2]
                    hh1 = round((hh1 * (1 / y[1]) ** (2 / 3)), 4)  # [m]
                return hh1

            # ارتفاع مایع روی بند خروجی از سینی
            h1 = _h1_()

            # ارتفاع بند: weir height
            hw = float(form.cleaned_data['hw'])
            context['hw'] = hw

            # print(hw)
            # افت فشار روی سینی ها

            def _calc_h_delta_p_():
                # {{  افت فشار سینی  }}

                # {{  calc hD      افت فشار مایع روی سینی: hD     }}
                # calc Co
                co = round(1.09 / division_L_to_do ** 0.25, 4)  # [mm]
                # print('Co= ', Co)
                # calc Ao
                ao = round(division_AoToAa * Aa, 4)  # [m^2]
                # print(Ao)
                # calc Vo  سرعت گاز در هر سوراخ
                vo = round(Volumetric_flow_rate_G / ao, 4)  # [m/s]
                # print(Vo)
                # calc Re
                re =  (Gas_density * vo * Do * 0.001) / viscosity


                # calc f
                # solve f as x that x = 1 / sqrt(f)
                eq_f = Eq((3.6 * math.log(re / 7, 10)) ** 2, 1 / x)
                f = solve(eq_f)
                f = round(f[0], 3)
                if re>10000:
                    context ['re'] = re
                    context ['re_alert'] = 'Re>10000 So Fill the Fanning friction factor in Moody diagram '
                if f_2 is not None:
                    f = f_2 /4

                # print(f)
                # calc hD
                #  افت فشار مایع روی سینی: hD
                eq_hd = Eq(co * ((0.4 * (1.25 - (ao / An))) + (4 * f * division_L_to_do) + (1 - ao / An) ** 2),
                           2 * x * g *
                           liquid_density / (vo ** 2 * Gas_density))
                solve_hd = solve(eq_hd)
                hd = round(solve_hd[0], 4)  # [متر مایع روی سینی]
                #  print('hD= ', hd)

                # {{  calc hL   # افت اصطکاکی جریان گاز به خاطر مایع روی سینی  }}
                # calc Z
                z = (W + Td) / 2  # [m]
                # print(z)
                # calc Va
                va = round(Volumetric_flow_rate_G / Aa, 4)  # [m/s]
                print('va = ',va)
                # calc hL as x
                eq_hl = Eq((6.1 * 10 ** (-3)) + (0.725 * (hw * 10 ** -3)) - (
                        0.238 * (hw * 10 ** -3) * va * (Gas_density ** 0.5)) + (
                                   1.225 * Volumetric_flow_rate_L / z), x)
                solve_hl = solve(eq_hl)
                hl = round(solve_hl[0], 4)  # [m]
                print('hl= ',hl)
                # {{ hR افت فشار اضافی ناشی از کشش سطحی }}
                # calc hR
                hr = round(6 * surface_tension * gc / (liquid_density * Do * 10 ** -3 * g), 4)  # [m]

                # calc hG  افت فشار گاز در یک سینی
                hg = round(hd + hl + hr, 4)  # [m]
                # print(hG)
                # محاسبه افت فشار روی هر سینی
                delta_p = liquid_density * g * hg  # [pa]
                # print(delta_p)
                # 6.1 (5)   چک کردن افت فشار روی هر سینی
                return [delta_p, hg, vo]

            # برای نشان دادن افت فشار به مخاطب

            # محاسبه افت فشار روی هر سینی
            if Pressure == 1 and _calc_h_delta_p_()[0] > 800:
                context[
                    'calc_h_delta_p'] = 'Warning: The pressure drop on each tray in the tray towers is up to 800 Pascals! It is better to increase the Tower Diameter.'
            if Pressure > 1 and _calc_h_delta_p_()[0] > 1000:
                context[
                    'calc_h_delta_p'] = 'Warning: The pressure drop in the tower is under a pressure of 1000 Pascals! it is better to increase the Tower Diameter.'
            delta_p = round(_calc_h_delta_p_()[0], 4)
            context['delta_p'] = delta_p
            # hG
            hG = _calc_h_delta_p_()[1]  # [m]
            Vo = _calc_h_delta_p_()[2]
            # فاصله تیغه ناودان ورودی از کف سینی
            h2 = hw / 2  # [mm]
            # print(h2)
            # مساحت سطح مایع ورودی به سینی
            A_apron = round(W * h2 * 10 ** -3, 4)  # [m^2]
            # print(A_apron)
            A_da = min(Ad, A_apron)
            # print(A_da)
            # calc h2   (3/(2 * g)) * (Volumetric_liq/Ada)^2
            h2 = round((3 / (2 * g)) * (Volumetric_flow_rate_L / A_da) ** 2, 4)  # [m]
            # print('h2 = ', h2)

            # calc h3
            h3 = round(hG + h2, 4)  # [m]

            # def _check_tray_spacing_():
            liquidDepth_DownComer = round(h3 + (hw * 10 ** -3) + h1, 4)
            if liquidDepth_DownComer > tray_spacing / 2:
                context[
                    'check_tray_spacing'] = 'Warning: tray spacing is small or (liquid depth in Down Comer is up). Arise it!'
                context['liquidDepth_DownComer'] = liquidDepth_DownComer
                # show the range that he can select tray spacing
            else:
                context['liquidDepth_DownComer'] = liquidDepth_DownComer

            # حد پایین سرعت گاز قابل قبول برای weeping
            # calc Vow as x
            Eq_Vow = Eq(
                0.0229 * ((viscosity ** 2 * liquid_density) / (
                        surface_tension * gc * Gas_density * Do * 0.001 * Gas_density))
                ** 0.379
                * division_L_to_do ** 0.293 *
                ((2 * Aa * Do * 0.001) / (math.sqrt(3) * (P_prim * 0.001) ** 3))
                ** (2.8 / (1.06 / Do / 0.001) ** 0.724), (x * viscosity) / (surface_tension * gc))

            # check Vo
            solve_Eq_Vow = solve(Eq_Vow)
            Vow = round(solve_Eq_Vow[0], 4)
            #  print(Vow)
            if Vo < Vow:
                context[
                    'VoLessVow'] = 'Warning: Weeping accrues It is better to increase the Gas Flowrate or decrease Tower diameter'
            # محاسبه ماندگی
            # v/vf = 0.3 ,0.35,0.4, 0.45, 0.5, 0.6, 0.7, 0.8,0.9,0.95
            Horizontal_parameter = round(
                ((Volumetric_flow_rate_L * liquid_density) / (Volumetric_flow_rate_G * Gas_density)) * (
                        Gas_density / liquid_density) ** 0.5, 5)
            print(Horizontal_parameter)
            print(VntoVf)
            Horizontal_parameter = np.log(Horizontal_parameter)
            if True:
                def Entrainment():
                    from sympy.abc import x
                    VntoVf_list = [[0.3, Eq(-0.3707 * Horizontal_parameter - 7.2003, x)],
                                   [0.35, Eq(-0.5005 * Horizontal_parameter - 7.0611, x)],
                                   [0.4, Eq(-0.6286 * Horizontal_parameter - 7.0323, x)],
                                   [0.45, Eq(-0.7449 * Horizontal_parameter - 6.9309, x)],
                                   [0.5, Eq(-0.8953 * Horizontal_parameter - 7.0127, x)],
                                   [0.6, Eq(-0.9957 * Horizontal_parameter - 6.9485, x)],
                                   [0.7, Eq(-1.0439 * Horizontal_parameter - 6.5051, x)],
                                   [0.8, Eq(-1.0817 * Horizontal_parameter - 6.2877, x)],
                                   [0.9, Eq(-1.0578 * Horizontal_parameter - 5.8211, x)],
                                   [0.95, Eq(-1.0182 * Horizontal_parameter - 5.0749, x)]]
                    # for i in range(10):
                    E11 = 0
                    if VntoVf > 0.95:
                        context['E'] = 'Entrainment > 1'
                        E11 = 1
                        return E11
                    if VntoVf < 0.3:
                        context['E'] = 'Entrainment < 0.001'
                        E11 = 0.001
                        return E11
                    for i in range(10):
                        if VntoVf_list[i][0] == VntoVf:
                            Eqq = VntoVf_list[i][1]
                            E11 = solve(Eqq)
                            E11 = round(math.exp(E11[0]), 4)
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
                                    E11 = round(math.exp(E11), 4)
                                    return E11
            if VntoVf > 0.95:
                E = Entrainment()
                context['E'] = E
                context['warn'] = 'or more'
            elif VntoVf < 0.3:
                E = Entrainment()
                context['E'] = E
                context['warn'] = 'or less'
            else:
                E = Entrainment()
                context['E'] = E
            if E > 0.075:
                context['Entrainment'] = 'Entrainment is more than 0.075! '
                # print(E)
            # و بالاخره نمایش نتایج
            context['Do'] = Do

            return render(request, 'sieveTray/sieveTray.html', context)
    else:
        form = give_data_form()
    # return render(request, 'sieveTray.html', {'form': form})
    return render(request, 'sieveTray/sieveTray.html', {'form': form})
