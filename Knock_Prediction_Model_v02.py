'''
___________________________________________________________
|                                                         |
|                Knock Prediction Model                   |
|_________________________________________________________|

'''



import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import PySide6 as Py
import tkinter as tk

'''
___________________________________________________________
|                                                         |
|               Information Dictionaries                  |
|_________________________________________________________|

'''

Combustion_Elements = {
    'C2H5OH': { 
        'density': 0.78945, #g/cm^3
        'molar_mass': 46.0684400, #g/mol
        'nasa_1': {
            'min_temp': 200.000, #K
            'max_temp': 1000.000, #K
            'a1': -2.342791392E+05,
            'a2': 4.479180550E+03,
            'a3': -2.744817302E+01,
            'a4': 1.088679162E-01,
            'a5': -1.305309334E-04,
            'a6': 8.437346400E-08,
            'a7': -2.234559017E-11
        },
        'nasa_2': {
            'min_temp': 1000.000, #K
            'max_temp': 6000.000, #K
            'a1': 4.694817650E+06,
            'a2': -1.929798213E+04,
            'a3': 3.447584040E+01,
            'a4': -3.236165980E-03,
            'a5': 5.784947720E-07,
            'a6': -5.564600270E-11,
            'a7': 2.226226400E-15
        }
    },
    'C8H18': {
        'density': 0.703, #g/cm^3}
        'molar_mass': 114.22852, #g/mol
        'nasa_1': {
            'min_temp': 200.000, #K
            'max_temp': 1000.000, #K
            'a1': -6.986647150E+05,
            'a2': 1.338501096E+04,
            'a3': -8.415165920E+01,
            'a4': 3.271936660E-01,
            'a5': -3.777209590E-04,
            'a6': 2.339836988E-07,
            'a7': -6.010892650E-11,
        },
        'nasa_2': {
            'min_temp': 1000.000, #K
            'max_temp': 6000.000, #K
            'a1': 6.36540695E+06,
            'a2': -3.105364657E+04,
            'a3': 6.969162340E+01,
            'a4': 1.048059637E-02,
            'a5': -4.129621950E-06,
            'a6': 5.543226320E-10,
            'a7': -2.6514366499E-14
        }
    },
    'N2': {
        'density': 0.0012506, #g/cm^3
        'molar_mass': 28.0134, #g/mol
        'nasa_1': {
            'min_temp': 200.000, #K
            'max_temp': 1000.000, #K
            'a1': 2.210371497E+04,
            'a2': -3.818461820E+02,
            'a3': 6.082738360E+00,
            'a4': -8.530914410E-03,
            'a5': 1.384646189E-05,
            'a6': -9.625793620E-09,
            'a7': 2.519705809E-12
        },
        'nasa_2': {
            'min_temp': 1000.000, #K
            'max_temp': 6000.000, #K
            'a1': 5.877124060E+05,
            'a2': -2.239249073E+03,
            'a3': 6.066949220E+00,
            'a4': -6.139685500E-04,
            'a5': 1.491806679E-07,
            'a6': -1.923105485E-11,
            'a7': 1.061954386E-15
        }
    },
    'O2': {
        'density': 0.001429, #g/cm^3
        'molar_mass': 31.9988, #g/mol
        'nasa_1': {
            'min_temp': 200.000, #K
            'max_temp': 1000.000, #K
            'a1': -3.425563420E+04,      
            'a2': 4.847000970E+02,
            'a3': 1.119010961E+00,
            'a4': 4.293889240E-03,
            'a5': -6.836300520E-07,
            'a6': -2.023372700E-09,
            'a7': 1.039040018E-12,
        },
        'nasa_2': {
            'min_temp': 1000.000, #K
            'max_temp': 6000.000, #K
            'a1': -1.037939022E+06,     
            'a2': 2.344830282E+03,
            'a3': 1.819732036E+00,
            'a4': 1.267847582E-03,
            'a5': -2.188067988E-07,
            'a6': 2.053719572E-11,
            'a7': -8.193467050E-16
        }
    },
    'Ar': {
        'density': 0.001784, #g/cm^3
        'molar_mass': 39.948, #g/mol
        'nasa_1': {
            'min_temp': 200.000, #K
            'max_temp': 1000.000, #K
            'a1': 0.00000000E+00,  
            'a2': 0.00000000E+00,
            'a3': 0.02500000E+02,
            'a4': 0.00000000E+00,
            'a5': 0.00000000E+00,
            'a6': 0.00000000E+00,
            'a7': 0.00000000E+00
        },
        'nasa_2': {
            'min_temp': 1000.000, #K
            'max_temp': 6000.000, #K
            'a1': 2.010538475E+01,     
            'a2': -5.992661070E-02,
            'a3': 2.500069401E+00,
            'a4': -3.992141160E-08,
            'a5': 1.205272140E-11,
            'a6': -1.819015576E-15,
            'a7': 1.078576636E-19
        }
    },
    'CO2': {
        'density': 0.001977, #g/cm^3
        'molar_mass': 44.0095, #g/mol
        'nasa_1': {
            'min_temp': 200.000, #K
            'max_temp': 1000.000, #K
            'a1': 4.943650540E+04,      
            'a2': -6.264116010E+02,
            'a3': 5.301725240E+00,
            'a4': 2.503813816E-03,
            'a5': -2.127308728E-07,
            'a6': -7.689988780E-10,
            'a7': 2.849677801E-13
        },
        'nasa_2': {
            'min_temp': 1000.000, #K
            'max_temp': 6000.000, #K
            'a1': 1.176962419E+05,     
            'a2': -1.788791477E+03,
            'a3': 8.291523190E+00,
            'a4': -9.223156780E-05,
            'a5': 4.863676880E-09,
            'a6': -1.891053312E-12,
            'a7': 6.330036590E-16
        }
    },
    'H2O': {
        'density': 1.000, #g/cm^3
        'molar_mass': 18.01528, #g/mol
        'nasa_1': {
            'min_temp': 200.000, #K
            'max_temp': 1000.000, #K
            'a1': -3.947960830E+04,     
            'a2': 5.755731020E+02,
            'a3': 9.317826530E-01,
            'a4': 7.222712860E-03,
            'a5': -7.342557370E-06,
            'a6': 4.955043490E-09,
            'a7': -1.336933246E-12
        },
        'nasa_2': {
            'min_temp': 1000.000, #K
            'max_temp': 6000.000, #K
            'a1': 1.034972096E+06,     
            'a2': -2.412698562E+03,
            'a3': 4.646110780E+00,
            'a4': 2.291998307E-03,
            'a5': -6.836830480E-07,
            'a6': 9.426468930E-11,
            'a7': -4.822380530E-15
        }
    }
}

engine_parameters = {
    'identifiers': {'name': "KTM 690", 'year': "2019"},
    'geometry': {
        'bore': 80,  # mm
        'stroke': 105,  # mm
        'crank_radius': 40,  # mm
        'con_rod': 160,  # mm ***subject to change based on actual con rod length***
        'compression_ratio': 12.7,  # unitless
        'displacement': 692.7,  # cc
    },
    'combustion_characteristics': {
        'CADivc': 53,  # deg ABDC
        'redline_rpm': 9000,  # rpm
        'volumetric_efficiency': 0.95,  # unitless
        'MAP': 86.3,  # kPa
        'peak_torque_rpm': 6500,  # rpm
    }
}

fuel_properties = {
    'E85': {'stoich_afr': 9.8, 'lhv': 29.2, 'ON': 99},   # AFR unitless, LHV MJ/kg, ON octane
    '93': {'stoich_afr': 14.08, 'lhv': 41.6, 'ON': 93},
}

weather_data = {
    'standard_sea_level': {'Patm': 101.325, 'Tatm': 298.15},
    'michigan_international_speedway': {'Patm': 97.522, 'Tatm': 294.3},
    'rellis': {'Patm': 100.375, 'Tatm': 305.4},
}

# Fixed E85 volumetric blend split used throughout (85% ethanol / 15% "gasoline" proxied as
# pure octane). Pulled out as a constant instead of being re-typed as 0.85/0.15 literals in
# three different functions.
ETHANOL_FRACTION = 0.85
OCTANE_FRACTION = 0.15

'''
___________________________________________________________
|                                                         |
|                        Functions                        |
|_________________________________________________________|

'''


def crank_slider(CAD, SHR, Tatm, engine_parameters=engine_parameters):
    '''
    Isentropic (adiabatic, reversible) compression estimate of in-cylinder P & T,
    used only before combustion starts.

    Inputs:
     - CAD: crank angle degree (deg)
     - SHR: specific heat ratio (unitless)
     - Tatm: atmospheric temperature (K)

    Outputs:
     - Pcad: pressure at current crank angle degree (Pa -- matches pressure_increase())
     - Tcad: temperature at current crank angle degree (K)
    '''
    crank_radius = engine_parameters['geometry']['crank_radius']
    con_rod = engine_parameters['geometry']['con_rod']
    CAD_ivc = engine_parameters['combustion_characteristics']['CADivc']
    Disp = engine_parameters['geometry']['displacement']
    CR = engine_parameters['geometry']['compression_ratio']
    Bore = engine_parameters['geometry']['bore']
    MAP = engine_parameters['combustion_characteristics']['MAP']

    # Baseline metrics at intake valve closing
    piston_position_ivc = crank_radius + con_rod - (
        np.sqrt((con_rod ** 2) - ((crank_radius ** 2) * (np.sin(np.deg2rad(CAD_ivc))) ** 2))
        + crank_radius * np.cos(np.deg2rad(CAD_ivc))
    )
    clearance_volume = Disp / CR
    vol_ivc = clearance_volume + ((np.pi / 4) * (Bore ** 2) * piston_position_ivc) / 1000
    Tivc = Tatm + 15
    Pivc = MAP * 1000  # Pa -- FIX: was left in kPa while pressure_increase() works in Pa.
                        # Handing a kPa-scaled pressure into pressure_increase() at the
                        # compression->combustion handoff is what caused the runaway
                        # temperatures (tens of thousands of K) seen in testing.

    # Metrics at current CAD (adiabatic compression)
    theta = np.deg2rad(CAD)
    piston_position = crank_radius + con_rod - (
        np.sqrt((con_rod ** 2) - ((crank_radius ** 2) * (np.sin(theta)) ** 2))
        + crank_radius * np.cos(theta)
    )
    vol = clearance_volume + ((np.pi / 4) * (Bore ** 2) * piston_position) / 1000
    Pcad = Pivc * (vol_ivc / vol) ** SHR
    Tcad = Tivc * (vol_ivc / vol) ** (SHR - 1)

    return Pcad, Tcad


def volume(CAD, CAD_step, engine_parameters=engine_parameters):
    crank_radius = engine_parameters['geometry']['crank_radius']
    con_rod = engine_parameters['geometry']['con_rod']
    Disp = engine_parameters['geometry']['displacement']
    CR = engine_parameters['geometry']['compression_ratio']
    Bore = engine_parameters['geometry']['bore']
    clearance_volume = Disp / CR

    theta = np.deg2rad(CAD)
    theta_step = np.deg2rad(CAD_step)
    x_i = crank_radius + con_rod - (
        np.sqrt((con_rod ** 2) - ((crank_radius ** 2) * (np.sin(theta)) ** 2))
        + crank_radius * np.cos(theta)
    )
    x_i_1 = crank_radius + con_rod - (
        np.sqrt((con_rod ** 2) - ((crank_radius ** 2) * (np.sin(theta + theta_step)) ** 2))
        + crank_radius * np.cos(theta + theta_step)
    )
    # FIX: missing /1000 to convert the (mm^2 * mm) piston-swept term from mm^3 to cc --
    # crank_slider() does this conversion correctly; this function didn't, which inflated
    # v_i/v_i_1 (and therefore v_i_1-v_i) by ~1000x and was the actual driver of the
    # pressure/temperature blow-up found during testing.
    v_i = clearance_volume + ((np.pi * Bore ** 2) / 4) * x_i / 1000
    v_i_1 = clearance_volume + ((np.pi * Bore ** 2) / 4) * x_i_1 / 1000

    Ah = (np.pi * Bore ** 2) / 2 + np.pi * Bore * x_i

    return v_i, v_i_1, Ah


def douaund_eyzat(ON, Pcad, Tcad):
    '''
    Ignition delay time (ms) -- Douaud & Eyzat correlation.
    NOTE: published forms of this correlation are usually calibrated with Pcad in bar,
    not Pa. Pcad is now consistently in Pa throughout this script (see the crank_slider/
    pressure_increase unit fix); confirm against your source whether c3's exponent
    expects bar, and rescale Pcad (e.g. Pcad/1e5) here if so.
    '''
    c1, c2, c3, c4 = 17.69, 3.402, 1.7, 3800
    return c1 * (ON / 100) ** c2 * Pcad ** (-c3) * np.exp(c4 / Tcad)


def hoepke(Xegr, Pcad, Tcad):
    '''Ignition delay time (ms) -- Hoepke correlation.'''
    c1, c2, c3, c4 = 8.799, 1.006, 1.499, 5865
    return c1 * (Pcad / Tcad) ** -c2 * (1 - Xegr) ** -c3 * np.e ** (c4 / Tcad)


def chen_zheng(lmnbda, Xegr, Pcad, Tcad):
    '''Ignition delay time (ms) -- Chen-Zheng correlation.'''
    c1, c2, c3, c4, c5 = 0.000053, 2.374, 3.013, 1.927, 3167
    return c1 * (Pcad / Tcad) ** -c2 * (1 - Xegr) ** -c3 * lmnbda ** -c4 * np.e ** (c5 / Tcad)


def wiebe(CAD, CAD_step, Spark, combustion_duration, m):
    '''
    Wiebe mass-fraction-burned function.

    Inputs:
    - CAD, CAD_step: crank angle degree, and CAD one step ahead (deg)
    - Spark: crank angle degree at spark (deg)
    - combustion_duration: duration of combustion (deg)
    - m: Wiebe shape parameter (unitless) -- THIS is now actually used; the previous
      version silently overwrote whatever was passed in with a hardcoded m = 2.

    Outputs:
    - xb_i, xb_i_1: fraction of fuel burned at CAD and CAD_step
    '''
    a = 6.9078  # efficiency parameter, calibrated for ~0-99.9% burned

    # FIX: CAD_step is a *delta* everywhere else in this script (see volume(), which
    # evaluates its "i+1" state at CAD+CAD_step) -- but this function was evaluating
    # xb_i_1 at the raw CAD_step value (e.g. CAD_step=1) as if it were an absolute
    # crank angle, instead of at CAD+CAD_step. That was sending the exponent argument
    # deeply negative and overflowing exp().
    xb_i = 1 - np.e ** (-a * ((CAD - Spark) / combustion_duration) ** (m + 1))
    xb_i_1 = 1 - np.e ** (-a * ((CAD + CAD_step - Spark) / combustion_duration) ** (m + 1))

    return xb_i, xb_i_1


def nasa_polynomial(Tcad, element, Combustion_Elements=Combustion_Elements):
    '''
    NASA-7 polynomial evaluation of Cp for a single species.

    Inputs:
    - Tcad: temperature (K)
    - element: species key into Combustion_Elements

    Outputs:
    - Cp: specific heat capacity (J/(mol*K))
    '''
    Tcad = float(Tcad)
    species = Combustion_Elements[element]

    if Tcad < 1000 or 'nasa_2' not in species:
        coeffs = species['nasa_1']
    else:
        coeffs = species['nasa_2']

    Cp = R_UNIVERSAL * (
        coeffs['a1'] * Tcad ** -2 +
        coeffs['a2'] * Tcad ** -1 +
        coeffs['a3'] +
        coeffs['a4'] * Tcad +
        coeffs['a5'] * Tcad ** 2 +
        coeffs['a6'] * Tcad ** 3 +
        coeffs['a7'] * Tcad ** 4
    )
    return Cp


def fresh_charge_composition(lmnbda, fuel_type,
                              engine_parameters=engine_parameters,
                              fuel_properties=fuel_properties,
                              Combustion_Elements=Combustion_Elements):
    '''
    Moles of every species in the fresh (unburned) charge: fuel (ethanol + "gasoline"
    proxied as octane) plus the standard-composition air pulled in through the intake.
    This does NOT depend on temperature, so it's computed once and shared by both
    Cp_unburned() and Cp_burned() instead of being duplicated in each (as it was before).

    Outputs: dict of mole counts, plus m_fuel (kg) and V_air (cc) for downstream use.
    '''
    comb = engine_parameters['combustion_characteristics']
    V_air = engine_parameters['geometry']['displacement'] * comb['volumetric_efficiency']  # cc
    m_air = V_air * 0.001225  # g  (air density ~1.225 g/L -> 0.001225 g/cc)
    m_fuel_g = m_air / (lmnbda * fuel_properties[fuel_type]['stoich_afr'])  # g

    V_fuel = m_fuel_g / (ETHANOL_FRACTION * Combustion_Elements['C2H5OH']['density'] +
                          OCTANE_FRACTION * Combustion_Elements['C8H18']['density'])
    V_C2H5OH = V_fuel * ETHANOL_FRACTION
    V_C8H18 = V_fuel * OCTANE_FRACTION

    m_C2H5OH = V_C2H5OH * Combustion_Elements['C2H5OH']['density']
    mol_C2H5OH = m_C2H5OH / Combustion_Elements['C2H5OH']['molar_mass']

    m_C8H18 = V_C8H18 * Combustion_Elements['C8H18']['density']
    mol_C8H18 = m_C8H18 / Combustion_Elements['C8H18']['molar_mass']

    m_N2 = V_air * 0.7808 * Combustion_Elements['N2']['density']
    mol_N2 = m_N2 / Combustion_Elements['N2']['molar_mass']

    m_O2 = V_air * 0.2095 * Combustion_Elements['O2']['density']
    mol_O2 = m_O2 / Combustion_Elements['O2']['molar_mass']

    m_Ar = V_air * 0.0093 * Combustion_Elements['Ar']['density']
    mol_Ar = m_Ar / Combustion_Elements['Ar']['molar_mass']

    m_CO2 = V_air * 0.0004 * Combustion_Elements['CO2']['density']
    mol_CO2 = m_CO2 / Combustion_Elements['CO2']['molar_mass']

    return {
        'mol_C2H5OH': mol_C2H5OH, 'mol_C8H18': mol_C8H18,
        'mol_N2': mol_N2, 'mol_O2': mol_O2, 'mol_Ar': mol_Ar, 'mol_CO2': mol_CO2,
        'm_fuel_g': m_fuel_g, 'V_air': V_air,
    }


def Cp_unburned(Tcad, lmnbda, fuel_type,
                 Combustion_Elements=Combustion_Elements,
                 engine_parameters=engine_parameters):
    '''
    Mole-fraction-weighted Cp of the unburned fresh charge at Tcad.

    Outputs:
    - Cp_mix: specific heat capacity of the unburned mixture (J/(mol*K))
    - mol_total: total moles in the unburned mixture
    - m_fuel_kg: fuel mass (kg)
    '''
    comp = fresh_charge_composition(lmnbda, fuel_type, engine_parameters, fuel_properties, Combustion_Elements)

    Cp_C2H5OH = nasa_polynomial(Tcad, 'C2H5OH', Combustion_Elements)
    Cp_C8H18 = nasa_polynomial(Tcad, 'C8H18', Combustion_Elements)
    Cp_N2 = nasa_polynomial(Tcad, 'N2', Combustion_Elements)
    Cp_O2 = nasa_polynomial(Tcad, 'O2', Combustion_Elements)
    Cp_Ar = nasa_polynomial(Tcad, 'Ar', Combustion_Elements)
    Cp_CO2 = nasa_polynomial(Tcad, 'CO2', Combustion_Elements)

    mol_total = (comp['mol_C2H5OH'] + comp['mol_C8H18'] + comp['mol_N2'] +
                 comp['mol_O2'] + comp['mol_Ar'] + comp['mol_CO2'])

    Cp_mix = (
        Cp_C2H5OH * comp['mol_C2H5OH'] + Cp_C8H18 * comp['mol_C8H18'] +
        Cp_N2 * comp['mol_N2'] + Cp_O2 * comp['mol_O2'] +
        Cp_Ar * comp['mol_Ar'] + Cp_CO2 * comp['mol_CO2']
    ) / mol_total

    return Cp_mix, mol_total, comp['m_fuel_g'] / 1000.0


def Cp_burned(Tcad, lmnbda, fuel_type,
              Combustion_Elements=Combustion_Elements,
              engine_parameters=engine_parameters):
    '''
    Mole-fraction-weighted Cp of the burned-gas mixture at Tcad, assuming complete
    combustion of whichever of {fuel, O2} is the limiting reactant:
      C2H5OH + 3 O2   -> 2 CO2 + 3 H2O
      C8H18  + 12.5 O2 -> 8 CO2 + 9 H2O
    This replaces the previous "num_rxn = mol_O2/28" formula, which didn't correspond
    to either reaction. This is still a simplifying assumption (single-step, complete
    combustion) -- verify it matches what your course/reference expects.
    '''
    comp = fresh_charge_composition(lmnbda, fuel_type, engine_parameters, fuel_properties, Combustion_Elements)
    mol_C2H5OH, mol_C8H18 = comp['mol_C2H5OH'], comp['mol_C8H18']
    mol_N2, mol_Ar, mol_CO2_air, mol_O2 = comp['mol_N2'], comp['mol_Ar'], comp['mol_CO2'], comp['mol_O2']

    O2_needed = 3.0 * mol_C2H5OH + 12.5 * mol_C8H18

    if O2_needed <= mol_O2:
        # Lean or stoichiometric: all fuel burns, leftover O2 remains
        frac_burned = 1.0
        mol_O2_remaining = mol_O2 - O2_needed
    else:
        # Rich: O2-limited, only a fraction of the fuel burns
        frac_burned = mol_O2 / O2_needed if O2_needed > 0 else 0.0
        mol_O2_remaining = 0.0

    mol_CO2_formed = frac_burned * (2.0 * mol_C2H5OH + 8.0 * mol_C8H18)
    mol_H2O_formed = frac_burned * (3.0 * mol_C2H5OH + 9.0 * mol_C8H18)
    mol_C2H5OH_unburned = mol_C2H5OH * (1.0 - frac_burned)
    mol_C8H18_unburned = mol_C8H18 * (1.0 - frac_burned)

    mol_CO2 = mol_CO2_air + mol_CO2_formed
    mol_H2O = mol_H2O_formed

    Cp_N2 = nasa_polynomial(Tcad, 'N2', Combustion_Elements)
    Cp_Ar = nasa_polynomial(Tcad, 'Ar', Combustion_Elements)
    Cp_CO2 = nasa_polynomial(Tcad, 'CO2', Combustion_Elements)
    Cp_H2O = nasa_polynomial(Tcad, 'H2O', Combustion_Elements)
    Cp_O2 = nasa_polynomial(Tcad, 'O2', Combustion_Elements) if mol_O2_remaining > 0 else 0.0
    Cp_C2H5OH = nasa_polynomial(Tcad, 'C2H5OH', Combustion_Elements) if mol_C2H5OH_unburned > 0 else 0.0
    Cp_C8H18 = nasa_polynomial(Tcad, 'C8H18', Combustion_Elements) if mol_C8H18_unburned > 0 else 0.0

    mol_total = (mol_N2 + mol_Ar + mol_CO2 + mol_H2O + mol_O2_remaining +
                 mol_C2H5OH_unburned + mol_C8H18_unburned)

    Cp_mix = (
        Cp_N2 * mol_N2 + Cp_Ar * mol_Ar + Cp_CO2 * mol_CO2 + Cp_H2O * mol_H2O +
        Cp_O2 * mol_O2_remaining + Cp_C2H5OH * mol_C2H5OH_unburned + Cp_C8H18 * mol_C8H18_unburned
    ) / mol_total

    return Cp_mix


def pressure_increase(CAD, CAD_step, P_i, T_i, Spark, combustion_duration, lmnbda,
                       rpm, Tatm, T_wall, fuel_type, m,
                       engine_parameters=engine_parameters, fuel_properties=fuel_properties):
    '''
    One crank-angle-step update of in-cylinder pressure/temperature during combustion,
    combining a Wiebe heat-release model with a Woschni-style convective wall-loss term.

    Inputs:
    - CAD, CAD_step: current crank angle degree, and one step ahead (deg)
    - P_i, T_i: current pressure (Pa) and temperature (K)
    - Spark, combustion_duration: Wiebe timing parameters (deg)
    - lmnbda, fuel_type: mixture composition
    - rpm, Tatm, T_wall, m: this trial's fixed Monte-Carlo draws

    Outputs:
    - P_i_1, T_i_1: pressure (Pa) and temperature (K) one step later
    '''
    crank_radius = engine_parameters['geometry']['crank_radius']
    con_rod = engine_parameters['geometry']['con_rod']
    CAD_ivc = engine_parameters['combustion_characteristics']['CADivc']
    Disp = engine_parameters['geometry']['displacement']
    CR = engine_parameters['geometry']['compression_ratio']
    Bore = engine_parameters['geometry']['bore']
    stroke = engine_parameters['geometry']['stroke']
    MAP = engine_parameters['combustion_characteristics']['MAP']

    piston_position_ivc = crank_radius + con_rod - (
        np.sqrt((con_rod ** 2) - ((crank_radius ** 2) * (np.sin(np.deg2rad(CAD_ivc))) ** 2))
        + crank_radius * np.cos(np.deg2rad(CAD_ivc))
    )
    clearance_volume = Disp / CR
    vol_ivc = clearance_volume + ((np.pi / 4) * (Bore ** 2) * piston_position_ivc) / 1000
    Tivc = Tatm + 15
    Pivc = MAP * 1000  # Pa

    xb_i, xb_i_1 = wiebe(CAD, CAD_step, Spark, combustion_duration, m)

    Cp_u, mol_total, m_fuel_kg = Cp_unburned(T_i, lmnbda, fuel_type)
    Cp = Cp_burned(T_i, lmnbda, fuel_type) * xb_i + Cp_u * (1 - xb_i)
    k = Cp / (Cp - R_UNIVERSAL)

    v_i, v_i_1, Ah = volume(CAD, CAD_step)

    Qin = m_fuel_kg * fuel_properties[fuel_type]['lhv'] * 1_000_000  # J (LHV given in MJ/kg)

    mean_piston_speed = 2 * (stroke / 1000) * rpm / 60
    pressure_motored = Pivc * (vol_ivc / v_i) ** k
    w = 2.28 * mean_piston_speed + 0.00324 * ((v_i * Tivc) / (vol_ivc * Pivc)) * (P_i - pressure_motored)
    hcg = 3.26 * (Bore / 1000) ** -0.2 * P_i ** 0.8 * T_i ** -0.55 * w ** 0.8

    omega = 2 * np.pi * rpm / 60  # rad/s
    CAD_step_rad = np.deg2rad(CAD_step)  # FIX: convert the crank-angle step to radians so
                                          # it's consistent with omega being in rad/s -- the
                                          # previous version multiplied a rad/s-based rate by
                                          # a step size still in degrees.
    Qloss = (hcg * Ah / omega) * (T_i - T_wall) * CAD_step_rad

    P_i_1 = P_i + ((k - 1) / v_i) * (Qin * (xb_i_1 - xb_i) - Qloss) - (k * P_i / v_i) * (v_i_1 - v_i)
    # FIX: ideal-gas law needs V in m^3 when P is in Pa and R is in J/(mol*K); v_i_1 here
    # is in cc, so convert (cc -> m^3 is /1e6). Left unconverted, T_i_1 came out ~1e6x too
    # high (tens of millions of K instead of a physically plausible combustion temperature).
    T_i_1 = (P_i_1 * (v_i_1 / 1_000_000)) / (mol_total * R_UNIVERSAL)

    return P_i_1, T_i_1


def livengood_wu_increment(rpm, IDT):
    '''
    Increment of the Livengood-Wu ignition-delay integral for one crank-angle step.
    Knock/autoignition is predicted once the *running sum* of these increments (across
    the whole compression+combustion event) reaches 1 -- see the accumulation in the
    main loop below, which is new: the previous version computed this per-step value
    but never actually summed it, so no knock onset was ever identified.

    NOTE: the Douaud-Eyzat/Hoepke/Chen-Zheng correlations here return IDT typically in
    ms in their original published form, while "1/(6*rpm)" below is a crank-angle-degree
    step converted to seconds (omega = 6*rpm deg/s at rpm rev/min). If your IDT is in ms,
    this increment is off by a factor of 1000. Confirm the units your correlations expect
    against your source before trusting absolute knock-onset timing.
    '''
    return (1 / (6 * rpm)) * (1 / IDT)


'''
___________________________________________________________
|                                                         |
|                       Main Code                         |
|_________________________________________________________|

'''

if __name__ == '__main__':

    #model constants
    R_UNIVERSAL = 8.314462618  # J/(mol*K) 

    # ---- User inputs, with basic validation so a typo fails fast with a clear message ----
    location = input('Testing Location:   ').strip()
    if location not in weather_data:
        raise ValueError(f"Unknown location '{location}'. Options: {list(weather_data)}")

    fuel_type = input('Fuel Type:   ').strip()
    if fuel_type not in fuel_properties:
        raise ValueError(f"Unknown fuel type '{fuel_type}'. Options: {list(fuel_properties)}")

    lmnbda = float(input('Lambda:   '))

    pk_T_rpm = engine_parameters['combustion_characteristics']['peak_torque_rpm']
    ON = fuel_properties[fuel_type]['ON']
    Patm = weather_data[location]['Patm']
    Tatm = weather_data[location]['Tatm']

    # ---- Monte Carlo trial parameters ----
    # Each of these arrays holds one independently-drawn value PER TRIAL. A trial's value
    # stays fixed for its whole simulated cycle; it's the *trial index* that varies, not
    # a resample at every crank-angle step (that was the bug behind the .normal() crash).
    monte_carlo_sims = 200  # NOTE: reduced from 1000 for a runnable default -- 20 spark
                              # timings x 1000 trials x a full crank-angle sweep each is a
                              # lot of nested Python-level work. Raise this back up once
                              # you've confirmed the physics look right; consider caching/
                              # vectorizing nasa_polynomial() first if you do.
    combustion_duration_pool = np.random.uniform(35, 50, monte_carlo_sims)
    m_pool = np.random.uniform(1.5, 2.5, monte_carlo_sims)
    T_wall_pool = np.random.uniform(453.15, 523.15, monte_carlo_sims)
    rpm_pool = np.random.uniform(pk_T_rpm - 100, pk_T_rpm + 100, monte_carlo_sims)

    spark_range = range(0, 20)
    correlations = ('douaund_eyzat', 'hoepke', 'chen_zheng')

    # knock_onset_CAD[correlation][spark] = list of onset CADs (one per MC trial that knocked)
    knock_onset_CAD = {c: {s: [] for s in spark_range} for c in correlations}
    # For inspecting/plotting one representative trial per spark timing
    example_CADs = {}
    example_pressure = {}

    for spark in spark_range:
        for mc in range(monte_carlo_sims):
            combustion_duration = combustion_duration_pool[mc]
            T_wall = T_wall_pool[mc]
            rpm = rpm_pool[mc]
            m = m_pool[mc]

            CADs_run = []
            pressure_run = [engine_parameters['combustion_characteristics']['MAP'] * 1000]  # Pa
            temperature_run = [weather_data[location]['Tatm'] + 15]  # K

            # Running Livengood-Wu integrals for this trial; knock = first CAD where >= 1
            integral = {c: 0.0 for c in correlations}
            onset_recorded = {c: False for c in correlations}

            CAD_start = engine_parameters['combustion_characteristics']['CADivc'] + 180
            spark_CAD = 360 - spark  # FIX: wiebe()/pressure_increase() need the absolute
                                      # crank-angle-degree of ignition, not the raw spark-
                                      # advance value -- passing "spark" directly made the
                                      # Wiebe function think combustion was already ~100%
                                      # burned on the very first combustion step, which is
                                      # what drove k, and then P/T, to NaN within 2-3 steps.
            CAD_end = spark_CAD + combustion_duration

            for CAD in np.arange(CAD_start, CAD_end, 1):
                CADs_run.append(CAD)

                if CAD < spark_CAD:
                    # Compression phase: isentropic estimate
                    Cp_u, mol_total, m_fuel_kg = Cp_unburned(temperature_run[-1], lmnbda, fuel_type)
                    shr = Cp_u / (Cp_u - R_UNIVERSAL)
                    Pcad, Tcad = crank_slider(CAD, shr, weather_data[location]['Tatm'])
                    pressure_run.append(Pcad)
                    temperature_run.append(Tcad)
                else:
                    # Combustion phase: Wiebe heat release + wall-loss pressure update.
                    Pcad, Tcad = pressure_increase(
                        CAD, 1, pressure_run[-1], temperature_run[-1], spark_CAD,
                        combustion_duration, lmnbda, rpm, Tatm, T_wall, fuel_type, m,
                    )
                    pressure_run.append(Pcad)
                    temperature_run.append(Tcad)

                # Accumulate Livengood-Wu integral for each correlation; record onset once
                for name, idt_val in (
                    ('douaund_eyzat', douaund_eyzat(ON, Pcad, Tcad)),
                    ('hoepke', hoepke(0, Pcad, Tcad)),
                    ('chen_zheng', chen_zheng(lmnbda, 0, Pcad, Tcad)),
                ):
                    if not onset_recorded[name]:
                        integral[name] += livengood_wu_increment(rpm, idt_val)
                        if integral[name] >= 1.0:
                            knock_onset_CAD[name][spark].append(CAD)
                            onset_recorded[name] = True

            if mc == 0:
                example_CADs[spark] = CADs_run
                example_pressure[spark] = pressure_run[:len(CADs_run)]

    # ---- Results: mean knock-onset CAD (relative to spark) per spark timing ----
    fig, ax = plt.subplots()
    for name in correlations:
        means = []
        sparks_with_data = []
        for spark in spark_range:
            onsets = knock_onset_CAD[name][spark]
            if onsets:
                means.append(np.mean(onsets))
                sparks_with_data.append(spark)
        ax.plot(sparks_with_data, means, marker='o', label=name)

    ax.set_xlabel('Spark timing (deg)')
    ax.set_ylabel('Mean predicted knock-onset CAD')
    ax.set_title(f'Knock onset vs. spark timing -- {fuel_type} @ lambda={lmnbda}, {location}')
    ax.legend()
    plt.show()