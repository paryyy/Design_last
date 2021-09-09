from django.shortcuts import render
from .forms import give_data_form
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
        if data['method'] == 'trybal' and data['types_tower'] == 'sieve tray':
            return redirect('/Home/sieveTray/')
        elif data['method'] == 'trybal' and data['types_tower'] == 'packed tray':
            # return render(request, 'packedTray.html',{data['method']:'trybal', data['types_tower']: 'packed tray' })
            return redirect('/Home/packedtray/')
    return render(request, 'Home.html')


def packedTray_view(request):
    return render(request, 'packedTray/packedTray.html')


# Create your views here.
# create sieve tray page
def sieveTray_view(request, ):
    if request.method == "POST":
        form = give_data_form(request.POST)
        if form.is_valid():
            FlowRateVapor =float( form.cleaned_data['FlowRateVapor'])
            FlowRateLiquid = float(form.cleaned_data['FlowRateLiquid'])
            Temperature = float(form.cleaned_data['Temperature'])
            Pressure = float(form.cleaned_data['Pressure'])
            Mfv = float(form.cleaned_data['Mfv'])
            Mfl = float(form.cleaned_data['Mfl'])
            viscosity = float(form.cleaned_data['viscosity'])
            MolWt_1 = float(form.cleaned_data['MolWt_1'])
            MolWt_2 = float(form.cleaned_data['MolWt_2'])
            liquid_density =float( form.cleaned_data['liquid_density'])
            surface_tension = float(form.cleaned_data['surface_tension'])
            TowerDiameter = float(form.cleaned_data['TowerDiameter'])
            tray_spacing = float(form.cleaned_data['tray_spacing'])
            times_w_t = float(form.cleaned_data['times_w_t'])
            Euser = float(form.cleaned_data['Euser'])
            R = 8.314
            g = 9.807  # [m^2/s]
            gc = 1
            MolAvg_liquid = 100 / ((Mfl / MolWt_1) + ((100 - Mfl) / MolWt_2))
            MolAvg_gas = Mfv / 100 * MolWt_1 + (100 - Mfv) / 100 * MolWt_2
            Volumetric_flow_rate_L = round(FlowRateLiquid * MolAvg_liquid / liquid_density, 3)
            Gas_density = round(Pressure * MolAvg_gas / (R * (Temperature + 273)) * 100, 3)  # kg/m^3
            Volumetric_flow_rate_G = round(FlowRateVapor * MolAvg_gas / Gas_density, 3)  # m^3/s
            context = {'resultt': FlowRateVapor, 'form': form}
            context['tray_spacing'] = tray_spacing
            # check material and Do
            material_design = form.cleaned_data['material_design']
            if material_design == 'Stainless steel':
                material_design_id = 1
            elif material_design == 'Carbon steel':
                material_design_id = 2
            Do = float(form.cleaned_data['Do'])
            if material_design_id == 1 and Do<4.5:
                context['material_design'] = 'Hole Diameter should be 4.5 [mm] or more'
            elif material_design_id == 2 and Do<9:
                context['material_design'] = 'Hole Diameter  should be 9 [mm] or more'
            # به دست آوردن نسبت ضخامت به قطر
            def _ticknessToHoleDiameter_():
                Do_Stainless_Carbon_list = [[3, 0.65, np.NaN], [4.5, 0.43, np.NAN], [6.0, 0.32, np.NAN],
                                            [9.0, 0.22, 0.5],
                                            [12.0, 0.16, 0.38], [15.0, 0.17, 0.3], [18.0, 0.11, 0.25]]
                df_Do_Stainless_Carbon_list = pd.DataFrame(Do_Stainless_Carbon_list,columns='Hole_Diameter 1 2'.split())
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
            Times_dis_hol = float(form.cleaned_data['Times_dis_hol'])
            Times_vn_vf = float(form.cleaned_data['Times_vn_vf'])
            P_prim = math.ceil(Times_dis_hol * Do)
            L =  math.ceil(Do * ticknessToHoleDiameter)  # [mm]
            division_L_to_do = ticknessToHoleDiameter
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

            def _calc_vf_():
                #  {{ Calculation CF }}
                # ابتدا L'/G'(density_g/density_l)^0.5 که نامش را division_for_CF میگذاریم، را  محاسبه میکنیم
                division_for_cf = ((Volumetric_flow_rate_L * liquid_density) / (
                            Volumetric_flow_rate_G * Gas_density)) * (
                                          Gas_density / liquid_density) ** 0.5
                if 0.01 <= division_for_cf <= 0.1:
                    division_for_cf = 0.1
                # Calculation alfa and beta for CF
                alfa = 0.0744 * tray_spacing + 0.01173
                beta = 0.0304 * tray_spacing + 0.015
                if division_AoToAa <= 0.1:  # question for >=
                    alfa = alfa * ((5 * division_AoToAa) + 0.5)
                    beta = beta * ((5 * division_AoToAa) + 0.5)
                #  Calc CF
                cf = (alfa * (math.log((1 / division_for_cf), 10)) + beta) * (surface_tension / 0.020) ** 0.2
                # print('CF= ', CF)
                # {{ Calc VF }}
                vf = cf * ((liquid_density - Gas_density) / Gas_density) ** 0.5
                return vf

            # ایجاد تابع برای شعاع محیط اتمسفریک
            # محاسبهAo/Aa برای محاسبه CF برای محیط اتمسفریک
            def _atmospheric_diam_tower_():
                vf = _calc_vf_()
                # {{ Calc VL }}
                # Give from user
                vn = Times_vn_vf * vf  # [m/s]    question:نمایش داده شده VL  گفت این سرعت گازه اما با
                # سطح مقطع کل برج منهای یک ناودان
                an = Volumetric_flow_rate_G / vn  # [m^2]
                # print('An= ', An)

                #  Give from user Weir length relative to diameter 0.6 0.65 0.7 0.75 0.8
                # is common for first Choice 0.7(Tower Diameter)
                # time_w_t = 0.7  # float(input('How many times your Weir length than the diameter ? (it is better to be 0.7 times'))
                #  table   6.1 (4)
                #  نسبت طول بند به قطر برج  و ارتباطش با درصد سطح اشغال شده توسط ناودان اینجا به دادن جواب نسبت بسنده کردم
                division_ad_to_at_in_w_to_t_dic = {0.6: 5.257, 0.65: 6.899, 0.7: 8.808, 0.75: 11.255, 0.8: 14.145}
                w_to_area_used_by_one_downspout = division_ad_to_at_in_w_to_t_dic[times_w_t]
                # print('WToAreaUsedByOneDownSpout= ', WToAreaUsedByOneDownSpout)

                # solve At as x
                # At = An + (division_ad_to_at_in_w_to_t_dic[times_w_t]/100) * At
                eq_solve_at = Eq(an + (division_ad_to_at_in_w_to_t_dic[times_w_t] / 100) * x, x)
                at = solve(eq_solve_at)  # [m^2]
                # print('At= ', At)

                # value of Tower Diameter(Td) as x
                eq_solve_td = Eq((math.pi * x ** 2) / 4, at[0])
                td = solve(eq_solve_td)
                td = td[1]
                # برای رند کردن به عدد منطقی مانند 1.25 . 1.30 و.. ضرایبی از پنج
                # اول اعشارشو کندم به ضریبی از 5 تبدیل کردم و بعد دوباره اعشارو به عدد اضافه کردم
                td = _round_diameter(td)
                return [td, times_w_t, w_to_area_used_by_one_downspout, an]

            # چک کردن q/T  در برج اتمسفریک
            def _check_diameter_(td_atm):
                while Volumetric_flow_rate_L / td_atm > 0.015:
                    td_atm += 0.05
                return td_atm


            WToAreaUsedByOneDownSpout = _atmospheric_diam_tower_()[2]

            # محاسبه مساحت ها با شعاع جدید
            def _calc_areas_(td):
                at = round(math.pi * td ** 2 / 4, 3)
                # محاسبه طول بند W  با قطر جدید
                w = round(times_w_t * td, 3)  # [m]
                # محاسبه سطح مقطع ناودان
                ad = round(WToAreaUsedByOneDownSpout / 100 * at, 3)  # [m^2]
                # print(Ad)
                # مساحت سطح فعال
                aa = round(at - 2 * ad - 0.2 * (at - 2 * ad), 2)
                # print('Ad', Ad)
                return [at, ad, aa, w]

            def _calcs_atmospheric_():
                # شعاع برج اتمسفریک
                td_atmospheric, an = _atmospheric_diam_tower_()[0], round(_atmospheric_diam_tower_()[3], 4)
                # محاسبه مجدد مساحت ها با شعاع جدید
                at, ad, aa, w = _calc_areas_(td_atmospheric)
                # چک کردن شرط q/T<0.015
                td_atmospheric = _check_diameter_(td_atmospheric)
                return [td_atmospheric, at, ad, aa, w, an]

            def _calc_under_pressure_():
                t_d = Volumetric_flow_rate_L / times_w_t * 0.032
                t_d = _round_diameter(t_d)
                while t_d <= Volumetric_flow_rate_L / times_w_t * 0.032:
                    t_d += 0.05
                at, ad, aa, w = _calc_areas_(t_d)
                an = round(at - ad, 4)
                vn = Volumetric_flow_rate_G / an
                vf = _calc_vf_()
                while vn >= Times_vn_vf * vf:
                    t_d += 0.25
                    at, ad, aa, w = _calc_areas_(t_d)
                    an = at - ad
                    vn = Volumetric_flow_rate_G / an
                return [t_d, at, ad, aa, w, an]

            # {{ محاسبات مربوط به برج اتمسفریک , خلا }}
            if Pressure == 1:
                Td = _calcs_atmospheric_()[0]
                Td_check = Td
                Ad = _calcs_atmospheric_()[2]
                Aa = _calcs_atmospheric_()[3]
                W = _calcs_atmospheric_()[4]
                An = _calcs_atmospheric_()[5]
                # print('An= ', An)
                # print('Aa= ', Aa)
                # print(Td_atmospheric)
            # {{ محاسبات مربوط به برج تحت فشار }}
            if Pressure > 1:
                Td = _calc_under_pressure_()[0]
                Ad = _calc_under_pressure_()[2]
                Aa = _calc_under_pressure_()[3]
                W = _calc_under_pressure_()[4]
                An = _calc_under_pressure_()[5]
                # print('An= ', An)
                # print('Td_under_pressure= ', Td_under_pressure)
            context['W'] = W
            context['Td'] = Td
                # {{ مسئله هیدرودینامیک }}

            def _h1_():
                # hh1 همون h1 هست
                hh1 = round((1 / 1.839 * Volumetric_flow_rate_L / W) ** (2 / 3), 3)  # [m]
                # print(hh1)
                if times_w_t < 0.7:
                    # solve w as x
                    eq_solve_w = Eq((Td / W) ** 2 - ((((Td / W) ** 2) - 1) ** 0.5 + (2 * hh1 / Td * (Td / W))) ** 2,
                                    x ** 2)
                    y = solve(eq_solve_w)  # [m^2]
                    hh1 = round((hh1 * (1 / y[1]) ** (2 / 3)), 3)  # [m]
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
                co = round(1.09 / division_L_to_do ** 0.25, 3)  # [mm]
                # print('Co= ', Co)
                # calc Ao
                ao = round(division_AoToAa * Aa, 2)  # [m^2]
                # print(Ao)
                # calc Vo  سرعت گاز در هر سوراخ
                vo = round(Volumetric_flow_rate_G / ao, 1)  # [m/s]
                # print(Vo)
                # calc Re
                re = (Gas_density * vo * Do * 0.001) / viscosity
                # print(Re)
                # calc f
                # solve f as x that x = 1 / sqrt(f)
                eq_f = Eq((3.6 * math.log(re / 7, 10)) ** 2, 1 / x)
                f = solve(eq_f)
                f = round(f[0], 3)
                # print(f)
                # calc hD
                #  افت فشار مایع روی سینی: hD
                eq_hd = Eq(co * ((0.4 * (1.25 - (ao / An))) + (4 * f * division_L_to_do) + (1 - ao / An) ** 2),
                           2 * x * g *
                           liquid_density / (vo ** 2 * Gas_density))
                solve_hd = solve(eq_hd)
                hd = round(solve_hd[0], 4)  # [متر مایع روی سینی]
                # print('hD= ', hD)

                # {{  calc hL   # افت اصطکاکی جریان گاز به خاطر مایع روی سینی  }}
                # calc Z
                z = (W + Td) / 2  # [m]
                # print(z)
                # calc Va
                va = round(Volumetric_flow_rate_G / Aa, 3)  # [m/s]
                # print(Va)
                # calc hL as x
                eq_hl = Eq((6.1 * 10 ** (-3)) + (0.725 * hw * 10 ** -3) - (
                            0.238 * hw * 10 ** -3 * va * (Gas_density ** 0.5)) + (
                                   1.225 * Volumetric_flow_rate_L / z), x)
                solve_hl = solve(eq_hl)
                hl = round(solve_hl[0], 2)  # [m]
                # print(hL)

                # {{ hR افت فشار اضافی ناشی از کشش سطحی }}
                # calc hR
                hr = round(6 * surface_tension * gc / (liquid_density * Do * 10 ** -3 * g), 4)  # [m]

                # calc hG  افت فشار گاز در یک سینی
                hg = round(hd + hl + hr, 3)  # [m]
                # print(hG)
                # محاسبه افت فشار روی هر سینی
                delta_p = liquid_density * g * hg  # [pa]
                # print(delta_p)
                # 6.1 (5)   چک کردن افت فشار روی هر سینی
                return [delta_p, hg, vo]
            # برای نشان دادن افت فشار به مخاطب

            # محاسبه افت فشار روی هر سینی
            if 1 <= Pressure <= 3 and _calc_h_delta_p_()[0] > 800:
                context['calc_h_delta_p'] = 'Warning: The pressure drop on each tray in the tray towers is up to 800 Pascals! It is better to increase the diameter.'
            if Pressure > 3 and _calc_h_delta_p_()[0] > 1000:
                context['calc_h_delta_p'] ='Warinig: The pressure drop in the tower is under a pressure of 1000 Pascals! it is better to increase the diameter.'
            delta_p = round(_calc_h_delta_p_()[0],3)
            context['delta_p'] = delta_p
            # hG
            hG = _calc_h_delta_p_()[1]  # [m]
            Vo = _calc_h_delta_p_()[2]
            # فاصله تیغه ناودان ورودی از کف سینی
            h2 = hw / 2  # [mm]
            # print(h2)
            # مساحت سطح مایع ورودی به سینی
            A_apron = round(W * h2 * 10 ** -3, 3)  # [m^2]
            # print(A_apron)
            A_da = min(Ad, A_apron)
            # print(A_da)
            # calc h2   (3/(2 * g)) * (Volumetric_liq/Ada)^2
            h2 = round((3 / (2 * g)) * (Volumetric_flow_rate_L / A_da) ** 2, 3)  # [m]
            # print('h2 = ', h2)

            # calc h3
            h3 = round(hG + h2, 3)  # [m]


            # def _check_tray_spacing_():
            liquidDepth_DownComer =round( h3 + (hw * 10**-3) + h1, 4)
            if liquidDepth_DownComer > tray_spacing / 2:
                context['check_tray_spacing'] = 'Warning: tray spacing is small or (liquid depth in Down Comer is up). arise it!'
                context['liquidDepth_DownComer'] =liquidDepth_DownComer
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
            Vow = round(solve_Eq_Vow[0], 3)
            #  print(Vow)
            if Vo < Vow:
                context['VoLessVow'] = 'Warning: your velocity through an orifice is lower than minimum gas velocity through ' \
                                       'perforations below which excessive weeping occurs, select another value for ' \
                                       'Gas Flowrate! '
            # محاسبه ماندگی
            Horizontal_parameter = round((FlowRateLiquid / FlowRateVapor) * (Gas_density / liquid_density) ** 0.5, 3)
            context['Euser'] = Euser
            context['Horizontal_parameter'] = Horizontal_parameter
            context['Times_vn_vf'] = Times_vn_vf
            if Euser > 0.075:
                context['Entrainment'] = 'Warning: Entrainment is remarkable!'

            # و بالاخره نمایش نتایج
            context['Do'] = Do


            return render(request, 'sieveTray/sieveTray.html', context)
    else:
        form = give_data_form()
    # return render(request, 'sieveTray.html', {'form': form})
    return render(request, 'sieveTray/sieveTray.html', {'form': form})

