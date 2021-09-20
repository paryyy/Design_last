from django import forms


class give_data_form(forms.Form):
    FlowRateVapor = forms.DecimalField(label="Vapor Flow Rate(Kmol/s)")
    FlowRateLiquid = forms.DecimalField(label="Liquid Flow Rate (Kmol/s)")
    Pressure = forms.DecimalField(label="Pressure (atm)")
    viscosity = forms.DecimalField(label="viscosity of gas")
    liquid_density = forms.DecimalField(label="liquid density")
    Gas_density = forms.DecimalField(label="Gas_density")
    surface_tension = forms.DecimalField(label="Surface tension")
    TowerDiameter = forms.DecimalField(label="TowerDiameter [m] (1 [m] is good for first Choice)")
    tray_spacing = forms.DecimalField(label="tray spacing [m] (0.5 [m] is good for first Choice)")
    times_w_t = forms.DecimalField(label="How many times your Weir length than the diameter")
    MATERIAL_CHOICES = (
        ('Stainless steel', 'Stainless steel'),
        ('Carbon steel', 'Carbon steel')
    )
    material_design = forms.ChoiceField(choices=MATERIAL_CHOICES, widget=forms.RadioSelect)
    Do = forms.DecimalField(label="Hole Diameter [mm] (4.5 [mm] is good for first Choice or 9[mm] for stainless "
                                  "steel)")
    Times_dis_hol = forms.DecimalField(label="Times_dis_hol")
    #  Times_vn_vf = forms.DecimalField(label="Times_vn_vf")
    hw = forms.DecimalField(label="hw")




class give_data_packed_form(forms.Form):
    Tower_Diam = forms.DecimalField(label="Tower_Diam")
    Gas_Flowrate = forms.DecimalField(label="Gas_Flowrate")  # [Kg/s]
    Gas_density = forms.DecimalField(label="Gas_density")  # [Kg/m^3]
    Liq_Flowrate = forms.DecimalField(label="Liq_Flowrate")  # [Kg/s]
    Liq_density = forms.DecimalField(label="Liq_density")
    viscosity_sub_in_liq = forms.DecimalField(label="viscosity_sub_in_liq")
    Cf = forms.DecimalField(label="Cf")


