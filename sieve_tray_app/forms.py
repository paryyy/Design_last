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
    percent_first_sub_gas = forms.DecimalField(label="percent_first_sub_gas")
    Mw_first_sub_gas = forms.DecimalField(label="Mw_first_sub_gas")
    Mw_gas = forms.DecimalField(label="Mw_gas")
    Packing_CHOICES = (
        ('ceramic_Intalox_saddles', '25[mm] ceramic Intalox saddles'),
    )
    type_packing = forms.ChoiceField(choices=Packing_CHOICES, widget=forms.RadioSelect)
    rate_gas_entering = forms.DecimalField(label="rate_gas_entering")
    Temp_gas_entering = forms.DecimalField(label="Temp_gas_entering")
    Pressure_gas_entering = forms.DecimalField(label="Pressure_gas_entering")
    rate_sub_in_liq = forms.DecimalField(label="rate_sub_in_liq")
    density_sub_in_liq = forms.DecimalField(label="density_sub_in_liq")
    viscosity_sub_in_liq = forms.DecimalField(label="viscosity_sub_in_liq")


