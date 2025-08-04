from math import ceil

def calc_pf(power_kw, emission_co2):
    pf = (emission_co2 / 45) + (power_kw / 40) ** 1.6
    return ceil(pf)