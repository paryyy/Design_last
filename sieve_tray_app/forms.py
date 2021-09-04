from django import forms


class give_data_form(forms.Form):
    FlowRateVapor = forms.DecimalField(label="Vapor Flow Rate(Kmol/s)")
    FlowRateLiquid = forms.DecimalField(label="Liquid Flow Rate (Kmol/s)")
    Temperature = forms.DecimalField(label="Temperature (C)")
    Pressure = forms.DecimalField(label="Pressure (atm)")
    Mfv = forms.DecimalField(label="mole fraction in vapor")
    Mfl = forms.DecimalField(label="mass fraction in liquid")
    viscosity = forms.DecimalField(label="viscosity of gas")
    MolWt_1 = forms.DecimalField(label="Molecular weight first substance")
    MolWt_2 = forms.DecimalField(label="Molecular weight second substance")
    liquid_density = forms.DecimalField(label="liquid density")
    surface_tension = forms.DecimalField(label="Surface tension")
    TowerDiameter = forms.DecimalField(label="TowerDiameter [m] (1 [m] is good for first Choice)")
    tray_spacing = forms.DecimalField(label="tray spacing [m] (0.5 [m] is good for first Choice)")
    times_w_t = forms.DecimalField(label="How many times your Weir length than the diameter")
    Do = forms.DecimalField(label="Hole Diameter [mm] (4.5 [mm] is good for first Choice or 9[mm] for stainless steel)")
    OPTIONS = (
        ("a", "Stainless steel"),
        ("b", "Carbon steel"),
    )
    material_design = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                choices=OPTIONS)



