'''
============================================================
============================================================
==                                                        ==
==               Knock Prediction Model                   ==
==                                                        ==
============================================================
============================================================

'''
'''
Model Notes:
 - All timing angles are from 0 deg bieng the piston at top
 dead center before the start of the intake stroke.
 - 


'''


'''
___________________________________________________________
|                                                         |
|                        Imports                          |
|_________________________________________________________|

'''
import sys
import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import PySide6 as Py
from tqdm import tqdm
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

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
    'identifiers':{
        'name': "KTM 690",
        'year': "2019"
    },
    'geometry': {
        'bore': 84.5, #mm
        'stroke': 102, #mm
        'crank_radius': 40, #mm
        'con_rod': 160, #mm ***subject to change based on actual con rod length***
        'compression_ratio': 12.6, #unitless
        'displacement': 690, #cc
    },
    'combustion_characteristics': {
        'CADivc': 53, #deg ABDC
        'redline_rpm': 9000, #rpm
        'volumetric_efficiency': 0.95, #unitless
        'MAP' : 86300, #Pa
        'peak_torque_rpm': 6500 #rpm
    }
}

fuel_properties = {
    'E85':{
        'stoich_afr': 9.8, #unitless
        'lhv': 29.2, #MJ/kg
        'ON' : 99, #Octane
        'ethanol_fraction': 0.85, #FIX: composition now travels with fuel_type instead of being a hardcoded global
        'octane_fraction': 0.15
    },
    '93':{
        'stoich_afr': 14.08, #unitless
        'lhv': 41.6, #MJ/kg
        'ON': 93, #Octane
        'ethanol_fraction': 0.00, #FIX: pump 93 modeled as pure iso-octane surrogate (set to 0.10 if E10 is desired)
        'octane_fraction': 1.00
    }
}


weather_data = {
    'standard_sea_level':{
        'p_atm': 101325, #Pa
        't_atm': 298.15 #K
    },
    'michigan_international_speedway':{
        'p_atm': 97522, #Pa
        't_atm': 294.3 #K
    },
    'rellis':{
        'p_atm': 100375, #Pa
        't_atm': 305.4 #K
    }
}


'''
___________________________________________________________
|                                                         |
|                        Functions                        |
|_________________________________________________________|

''' 

def nasa_polynomial(t_cad, element, Combustion_Elements = Combustion_Elements):

    '''
    Overview:
        this function calculates the specific heat at constant pressure for all 
    of the elements present in the unburnt and burnt air-fuel mixtures. These Cps
    are based on the seventh order polynomials published by NASA in 2002. They cover 
    2 different temperature ranges, 200-1000 K & 1000-6000 K.

    Inputs:                   (unit)      [description]
     - t_cad                   (K)        [temperature at the current crank angle degree]
     - element              (unitless)    [the name of the element being evaluated]
     - R                    (J/mol*K)     [universal gas constant]

     Outputs:
     - Cp                   (J/mol*K)     [the specific heat capacity of the desired element at constant pressure]
    '''

    if t_cad < 1000:
        #Calculate Cp for each element
        Cp = R_UNIVERSAL * (
            Combustion_Elements[element]['nasa_1']['a1']*t_cad**-2 + 
            Combustion_Elements[element]['nasa_1']['a2']*t_cad**-1 + 
            Combustion_Elements[element]['nasa_1']['a3'] + 
            Combustion_Elements[element]['nasa_1']['a4']*t_cad + 
            Combustion_Elements[element]['nasa_1']['a5']*t_cad**2 + 
            Combustion_Elements[element]['nasa_1']['a6']*t_cad**3 + 
            Combustion_Elements[element]['nasa_1']['a7']*t_cad**4
            )
    else:
        #Calculate Cp for each element
        Cp = R_UNIVERSAL * (
            Combustion_Elements[element]['nasa_2']['a1']*t_cad**-2 + 
            Combustion_Elements[element]['nasa_2']['a2']*t_cad**-1 + 
            Combustion_Elements[element]['nasa_2']['a3'] + 
            Combustion_Elements[element]['nasa_2']['a4']*t_cad + 
            Combustion_Elements[element]['nasa_2']['a5']*t_cad**2 + 
            Combustion_Elements[element]['nasa_2']['a6']*t_cad**3 + 
            Combustion_Elements[element]['nasa_2']['a7']*t_cad**4
            )

    return Cp


def fresh_charge_composition(lmnbda, fuel_type, engine_parameters=engine_parameters, fuel_properties=fuel_properties, Combustion_Elements=Combustion_Elements):

    '''
    Overview:
        this function returns a dictionary of mol compositions of the initial air-fuel mixture
    that is drawn into the cylinder. additionally the fuel mass and total volume of air are included
    for other function calculations

    Inputs:                   (unit)      [description]
     - lmnbda               (unitless)    [fuel enrichment lmnbda value]
     - fuel_type            (unitless)    [the name of the current fuel being evaluated]

     Outputs:
     - mol_C2H5OH           (unitless)    [the number of ethanol moles in the original fresh charge]
     - mol_C8H18            (unitless)    [the number of octane moles in the original fresh charge]
     - mol_N2               (unitless)    [the number of nitrogen moles in the original fresh charge]
     - mol_O2               (unitless)    [the number of oxygen moles in the original fresh charge]
     - mol_Ar               (unitless)    [the number of argon moles in the original fresh charge]
     - mol_CO2              (unitless)    [the number of carbon dioxide moles in the original fresh charge]
     - m_fuel_g                 (g)       [the mass of the total fuel in the cylinder]
     - V_air                   (cc)       [the total volume of air in the cylinder]
    '''

    #FIX: pull the ethanol/octane split from the selected fuel instead of a fixed global,
    #so a '93' pump-gas run is no longer silently modeled as an E85 blend.
    ethanol_fraction = fuel_properties[fuel_type]['ethanol_fraction']
    octane_fraction = fuel_properties[fuel_type]['octane_fraction']

    comb = engine_parameters['combustion_characteristics']
    V_air = engine_parameters['geometry']['displacement'] * comb['volumetric_efficiency']  # cc
    m_air = V_air * 0.001225  # g  (air density ~1.225 g/L -> 0.001225 g/cc)
    m_fuel_g = m_air / (lmnbda * fuel_properties[fuel_type]['stoich_afr'])  # g

    V_fuel = m_fuel_g / (ethanol_fraction * Combustion_Elements['C2H5OH']['density'] +
                          octane_fraction * Combustion_Elements['C8H18']['density'])
    V_C2H5OH = V_fuel * ethanol_fraction
    V_C8H18 = V_fuel * octane_fraction

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

    mol_total = mol_C2H5OH + mol_C8H18 + mol_N2 + mol_O2 + mol_Ar + mol_CO2

    return {
        'mol_C2H5OH': mol_C2H5OH, 'mol_C8H18': mol_C8H18,
        'mol_N2': mol_N2, 'mol_O2': mol_O2, 'mol_Ar': mol_Ar, 'mol_CO2': mol_CO2,
        'm_fuel_g': m_fuel_g, 'V_air': V_air, 'mol_total': mol_total
    }


def Cp_unburned(t_cad, lmnbda, fuel_type, Combustion_Elements=Combustion_Elements, engine_parameters=engine_parameters):
    '''
    Overview:
        this computes the specific heat capacity of the unburnt fuel mixture in the cylinder

    Inputs:                   (unit)      [description]
     - t_cad                    (K)       [temperature at the current crank angle degree]
     - lmnbda               (unitless)    [fuel enrichment lmnbda value]
     - fuel_type            (unitless)    [the name of the current fuel being evaluated]

     Outputs:
     - Cp_mix                (J/K*mol)    [the specific heat capacity at constant pressure of the unburnt gas mixture]
    '''

    comp = fresh_charge_composition(lmnbda, fuel_type, engine_parameters, fuel_properties, Combustion_Elements)

    Cp_C2H5OH = nasa_polynomial(t_cad, 'C2H5OH', Combustion_Elements)
    Cp_C8H18 = nasa_polynomial(t_cad, 'C8H18', Combustion_Elements)
    Cp_N2 = nasa_polynomial(t_cad, 'N2', Combustion_Elements)
    Cp_O2 = nasa_polynomial(t_cad, 'O2', Combustion_Elements)
    Cp_Ar = nasa_polynomial(t_cad, 'Ar', Combustion_Elements)
    Cp_CO2 = nasa_polynomial(t_cad, 'CO2', Combustion_Elements)

    mol_total = comp['mol_total']

    Cp_mix = (
        Cp_C2H5OH * comp['mol_C2H5OH'] + Cp_C8H18 * comp['mol_C8H18'] +
        Cp_N2 * comp['mol_N2'] + Cp_O2 * comp['mol_O2'] +
        Cp_Ar * comp['mol_Ar'] + Cp_CO2 * comp['mol_CO2']
    ) / mol_total

    return Cp_mix


def Cp_burned(t_cad, lmnbda, fuel_type, Combustion_Elements=Combustion_Elements, engine_parameters=engine_parameters):

    '''
    Overview:
        this function returns a dictionary of mol compositions of the initial air-fuel mixture
    that is drawn into the cylinder. additionally the fuel mass and total volume of air are included
    for other function calculations

    Inputs:                   (unit)      [description]
     - t_cad                    (K)       [temperature at the current crank angle degree]
     - lmnbda               (unitless)    [fuel enrichment lmnbda value]
     - fuel_type            (unitless)    [the name of the current fuel being evaluated]

     Outputs:
     - Cp_mix                (J/K*mol)    [the specific heat capacity at constant pressure of the burnt gas mixture]
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

    Cp_N2 = nasa_polynomial(t_cad, 'N2', Combustion_Elements)
    Cp_Ar = nasa_polynomial(t_cad, 'Ar', Combustion_Elements)
    Cp_CO2 = nasa_polynomial(t_cad, 'CO2', Combustion_Elements)
    Cp_H2O = nasa_polynomial(t_cad, 'H2O', Combustion_Elements)
    Cp_O2 = nasa_polynomial(t_cad, 'O2', Combustion_Elements) if mol_O2_remaining > 0 else 0.0
    Cp_C2H5OH = nasa_polynomial(t_cad, 'C2H5OH', Combustion_Elements) if mol_C2H5OH_unburned > 0 else 0.0
    Cp_C8H18 = nasa_polynomial(t_cad, 'C8H18', Combustion_Elements) if mol_C8H18_unburned > 0 else 0.0

    mol_total = (mol_N2 + mol_Ar + mol_CO2 + mol_H2O + mol_O2_remaining +
                 mol_C2H5OH_unburned + mol_C8H18_unburned)

    Cp_mix = (
        Cp_N2 * mol_N2 + Cp_Ar * mol_Ar + Cp_CO2 * mol_CO2 + Cp_H2O * mol_H2O +
        Cp_O2 * mol_O2_remaining + Cp_C2H5OH * mol_C2H5OH_unburned + Cp_C8H18 * mol_C8H18_unburned
    ) / mol_total

    return Cp_mix


def wiebe(CAD, CAD_step, Spark, combustion_duration, m):

    '''
    Overview:
        the wiebe function is used to determine the percentage of
    mass in the cylinder that is currrently burnt. the shape of the
    curve is set by the correlation constant (a) and shape factor (m)
    which will be refined more with emperical data.

    Inputs:                   (unit)       [description]
     - CAD                    (deg)        [current crank angle degree]
     - CAD_step               (deg)        [current crank angle degree step size]
     - spark                  (deg)        [crank angle degree BTDC when the spark plug is fired]
     - combustion_duration    (deg)        [duration of the combustion event]
     - m                      (unitless)   [shape factor] 
     
     Outputs:
     - xb_i                   (percentage) [percentage of burnt mass in the cylinder at the current CAD step]
     - xb_i_1                 (percentage) [percentage of burnt mass in the cylinder at a crank angle step degree in the future]

    FIX: the original signature took a CADivc argument that the caller never
    supplied (combustion_analysis called wiebe with only 5 args against a 6-arg
    signature, which raises "missing 1 required positional argument"). It's
    removed here. The burn-fraction clock also now starts at the crank angle
    where combustion actually begins (360 - Spark, i.e. Spark degrees BTDC of
    compression TDC, matching the CAD < 360 - spark switch in the main loop)
    instead of the old (CAD - CADivc - Spark), which measured burn progress
    from an angle that didn't correspond to ignition timing at all.
    '''

    a = 6.9078
    CAD_spark = 360.0 - Spark

    def xb(theta):
        if theta <= CAD_spark:
            return 0.0
        if theta >= CAD_spark + combustion_duration:
            return 1.0

        phi = (theta - CAD_spark) / combustion_duration
        value = 1.0 - np.exp(-a * phi**(m + 1.0))
        return float(np.clip(value, 0.0, 1.0))

    xb_i = xb(CAD)
    xb_i_1 = xb(CAD + CAD_step)

    return xb_i, xb_i_1


def crank_slider(CAD, CAD_step, SHR, Tatm, engine_parameters=engine_parameters):

    '''
    Overview:
        this function is a crank-slider model that determines the cylinder
    temperature and pressure from engine geometry and the temperature and 
    pressure at intake valve closing. Solves for the adiabatic portion of 
    the compression stroke is used for the motored pressure necessary for 
    the Woschni heat transfer model. Additionally it provides the current 
    volume and heat transfer area to the walls.

    Inputs:                   (unit)      [description]
     - Engine Geometries     
         - crank_radius       (mm)
         - connecting_rod     (mm)
         - bore               (mm)
         - displacement       (cc)
         - compression_ratio  (unitless)
         - CAD_ivc            (deg)       [crank angle degree at intake valve closing]
         - MAP                (Pa)        [manifold air pressure]
     - CAD                    (deg)       [current crank angle degree]
     - CAD_step               (deg)       [current crank angle degree step size]
     - SHR                    (unitless)  [the specific heat ratio of the gas mixture in the cylinder]
     - t_atm                  (K)         [atmospheric tremperature]

     Outputs:
     - p_cad                  (Pa)        [pressure at the current crank angle degree]
     - t_cad                  (K)         [temperature at the current crank angle degree]
     - v_cad                  (cc)        [volume at the current crank angle degree]
     - v_cad_1                (cc)        [volume at the next crank angle degree step]
     - Ah                     (m^2)       [heat transfer area to the cylinder walls] #FIX: was documented/returned as mm^2
    '''

    crank_radius = engine_parameters['geometry']['crank_radius']      # mm
    con_rod = engine_parameters['geometry']['con_rod']                # mm
    CAD_ivc = engine_parameters['combustion_characteristics']['CADivc']
    displacement = engine_parameters['geometry']['displacement']      # cc
    compression_ratio = engine_parameters['geometry']['compression_ratio']
    bore = engine_parameters['geometry']['bore']                      # mm
    MAP = engine_parameters['combustion_characteristics']['MAP']      # Pa

    # Correct clearance volume
    clearance_volume = displacement / (compression_ratio)       # cc

    def piston_position(theta_deg):
        theta = np.deg2rad(theta_deg)
        return (
            crank_radius + con_rod
            - (
                np.sqrt(con_rod**2 - (crank_radius * np.sin(theta))**2)
                + crank_radius * np.cos(theta)
            )
        )

    piston_position_ivc = piston_position(CAD_ivc)
    piston_position_i = piston_position(CAD)
    piston_position_i1 = piston_position(CAD + CAD_step)

    v_ivc = clearance_volume + ((np.pi / 4.0) * bore**2 * piston_position_ivc) / 1000.0
    v_cad = clearance_volume + ((np.pi / 4.0) * bore**2 * piston_position_i) / 1000.0
    v_cad_1 = clearance_volume + ((np.pi / 4.0) * bore**2 * piston_position_i1) / 1000.0

    t_ivc = Tatm + 15.0
    p_ivc = MAP

    p_cad = p_ivc * (v_ivc / v_cad)**SHR
    t_cad = t_ivc * (v_ivc / v_cad)**(SHR - 1.0)

    # Area in mm^2, then convert to m^2
    Ah_mm2 = (np.pi * bore**2) / 2.0 + np.pi * bore * piston_position_i
    Ah = Ah_mm2 / 1e6

    return p_cad, t_cad, v_cad, v_cad_1, Ah


def combustion_analysis(CAD, CAD_step, P_i, T_i, Spark, combustion_duration, lmnbda, rpm, T_wall, fuel_type, m, location, engine_parameters = engine_parameters, fuel_properties = fuel_properties, weather_data= weather_data):

    '''
    Overview:
        this function models the pressure and temperature increase in the cylinder throughout
    the combustion process. It is currently based on a single zone wiebe function.

    Inputs:                   (unit)      [description]
     - CAD                     (deg)      [current crank angle degree]
     - CAD_step                (deg)      [current crank angle degree step size]
     - p_cad                   (Pa)       [pressure at the current crank angle degree step]
     - t_cad                    (K)       [temperature at the current crank angle degree]
     - spark                   (deg)      [crank angle degree when the spark plug is fired]
     - combustion_duration     (deg)      [estimated length of combustion]
     - lmnbda               (unitless)    [fuel enrichment lmnbda value]
     - rpm                     (rpm)      [the current rpm that knock is being evaluated at]
     - fuel_type            (unitless)    [the name of the current fuel being evaluated]
     - m                    (unitless)    [shape factor] 
     - location             (unitless)    [specified operating location]


     Outputs:
     - P_i_1                   (Pa)       [the estimated pressure at the next crank angle degree step]
     - T_i_1                    (K)       [the estimated temperature at the next crank angle degree step]
    '''

    #Important Engine Metrics
    crank_radius = engine_parameters['geometry']['crank_radius'] #mm
    con_rod = engine_parameters['geometry']['con_rod'] #mm
    CAD_ivc = engine_parameters['combustion_characteristics']['CADivc'] #deg
    Disp = engine_parameters['geometry']['displacement'] #cc
    CR = engine_parameters['geometry']['compression_ratio'] #unitless
    Bore = engine_parameters['geometry']['bore'] #mm
    stroke = engine_parameters['geometry']['stroke'] #mm
    MAP = engine_parameters['combustion_characteristics']['MAP'] #Pa

    #Baseline Metrics at Intake Valve Closing
    piston_position_ivc = crank_radius + con_rod - (np.sqrt((con_rod**2)-((crank_radius**2) * (np.sin(np.deg2rad(CAD_ivc)))**2)) + crank_radius*np.cos(np.deg2rad(CAD_ivc)))
    clearance_volume = Disp / CR
    vol_ivc = clearance_volume + ((np.pi/4) * (Bore**2) * piston_position_ivc)/1000
    Tivc = weather_data[location]['t_atm'] + 15
    Pivc = MAP #Pa


    #Wiebe Function Components
    #FIX: matches wiebe()'s corrected 5-argument signature (CADivc removed, see wiebe()).
    xb_i, xb_i_1 = wiebe(CAD, CAD_step, Spark, combustion_duration, m)

    #Specific Heat Ratio
    Cp_u = Cp_unburned(T_i, lmnbda, fuel_type)
    Cp_b = Cp_burned(T_i, lmnbda, fuel_type)
    Cp = Cp_b*xb_i + Cp_u*(1-xb_i)
    k = Cp/(Cp - R_UNIVERSAL)

    comp = fresh_charge_composition(lmnbda, fuel_type)
    mol_total = comp['mol_total']
    #note: crank_slider's own p_cad/t_cad outputs (isentropic-compression-only) are not
    #used here - only the geometric v_i, v_i_1, Ah are needed, since P_i/T_i already carry
    #the actual (combustion-informed) state from the previous step.
    _, _, v_i, v_i_1, Ah = crank_slider(CAD, CAD_step, k, weather_data[location]['t_atm'])

    #Heat Gained from combustion
    V_air = Disp * engine_parameters['combustion_characteristics']['volumetric_efficiency'] #cc
    m_air = V_air * .001225 #g
    m_fuel = (m_air / (lmnbda*fuel_properties[fuel_type]['stoich_afr']))/1000 #kg
    Qin = m_fuel*fuel_properties[fuel_type]['lhv']*1000000 #J

    #Heat Transfer to the walls
    mean_piston_speed = 2*(stroke/1000)*rpm / 60
    pressure_motored = Pivc * (vol_ivc/v_i)**k

    #FIX: the Woschni constants 0.00324 and 3.26 are both calibrated with pressure in kPa.
    #P_i, pressure_motored and Pivc were all in Pa. In the "w" term this cancels out
    #because pressure only ever appears as a ratio (Pivc in the denominator, P_i-pressure_motored
    #in the numerator - a 1000x factor introduced in both places cancels), so that term is
    #left as-is. But in hcg, P_i is raised to the 0.8 power directly (no cancelling ratio),
    #so it must be converted to kPa or the heat-transfer coefficient comes out ~250x too high.
    w = 2.28*mean_piston_speed + 0.00324*((v_i * Tivc)/(vol_ivc * Pivc))*(P_i - pressure_motored)
    P_i_kPa = P_i / 1000
    hcg = 3.26*(engine_parameters['geometry']['bore']/1000)**-0.2 * P_i_kPa**0.8 * T_i**-0.55 * w**0.8
    Qloss = (hcg * Ah / (2*np.pi*rpm/60))*(T_i - T_wall)  # Ah now arrives in m^2 from crank_slider

    #FIX: v_i/v_i_1/vol_ivc are volumes in cc (cm^3) from crank_slider, but P_i is in Pa
    #(= J/m^3) and Qin/Qloss are in J. The (k-1)/v_i * (Qin*dxb - Qloss*dtheta) term mixes
    #energy (J) with a volume denominator, so v_i must be in m^3 there or the pressure rise
    #comes out ~1e6x too small. The -(k*P_i/v_i)*(v_i_1-v_i) term is a pure volume RATIO, so
    #cc vs m^3 doesn't matter there - but v_i is converted for both terms for clarity/safety.
    v_i_m3 = v_i / 1e6
    v_i_1_m3 = v_i_1 / 1e6

    P_i_1 = P_i + ((k-1)/v_i_m3)*(Qin*(xb_i_1 - xb_i) - Qloss*np.deg2rad(CAD_step)) - (k*P_i/v_i_m3)*(v_i_1_m3-v_i_m3)
    T_i_1 = (P_i_1 * v_i_1_m3)/(mol_total * R_UNIVERSAL)  # v in m^3 so P*V/(n*R) yields K correctly

    return P_i_1, T_i_1


def douaund_eyzat(ON, p_cad, t_cad):

    '''
    Overview:
        this function represents the douaund-eyzat model for ignition
    delay timing, in milliseconds. Although it is the most widely accepted 
    model to solve for IDT, it is only used as a reference in this 
    thermodynamic model because it doesn't take into account fuel 
    enrichement 

    Inputs:                   (unit)      [description]
     - ON                     (Octane)    [octane number]
     - p_cad                  (Pa)        [pressure at the current crank angle degree]
     - t_cad                  (K)         [temperature at the current crank angle degree]

     Outputs:
     - IDT                    (ms)        [ignition delay timing]

    FIX: the Douaud-Eyzat correlation (c1=17.68, c3=1.7 exponent) is calibrated
    with pressure in BAR, not Pa. Passing raw Pa values (~1e6-1e7) into p_cad**-1.7
    collapses the pressure term to ~0, so the correlation was effectively only a
    function of octane number and temperature. p_cad is converted to bar here.
    '''
    
    #Model Constants
    c1 = 17.69
    c2 = 3.402
    c3 = 1.7
    c4 = 3800

    p_bar = max(p_cad / 1e5, 1e-9)

    IDT = c1 * (ON / 100)**c2 * p_bar**(-c3) * np.exp(c4 / t_cad)

    return IDT


def hoepke(x_egr, p_cad, t_cad):

    '''
    Overview:
        this function represents the hoepke model for ignition
    delay timing, in milliseconds. A major model for IDT when taking
    into account exhasust gas recirculation. Once again, it is only 
    used as a reference in this thermodynamic model because it doesn't
    take into account fuel enrichement 

    Inputs:                   (unit)       [description]
     - x_egr                  (percentage) [amount of exhaust gas recirculation]
     - p_cad                  (Pa)         [pressure at the current crank angle degree]
     - t_cad                  (K)          [temperature at the current crank angle degree]

     Outputs:
     - IDT                    (ms)        [ignition delay timing]
    '''

    #Model Constants
    c1 = 8.799
    c2 = 1.006
    c3 = 1.499
    c4 = 5865

    #FIX: same units issue as douaund_eyzat - this correlation is calibrated
    #with pressure in bar, not Pa.
    p_bar = max(p_cad / 1e5, 1e-9)

    IDT = c1 * (p_bar / t_cad)**- c2 * (1 - x_egr)**- c3 * np.exp(c4 / t_cad)

    return IDT


def chen_zheng(lmnbda, x_egr, p_cad, t_cad):

    '''
    Overview:
        this function represents the chen-zheng model for ignition
    delay timing, in milliseconds. this is the TDI model used for this
    thermodynamic model because it seems like the most comprehensive model

    Inputs:                   (unit)       [description]
     - lmnbda                 (unitless)   [fuel enrichment lmnbda value]
     - x_egr                  (percentage) [amount of exhaust gas recirculation]
     - p_cad                  (Pa)         [pressure at the current crank angle degree]
     - t_cad                  (K)          [temperature at the current crank angle degree]

     Outputs:
     - IDT                    (ms)         [ignition delay timing]
    '''

    #Model Constants
    c1 = 0.000053
    c2 = 2.374
    c3 = 3.013
    c4 = 1.927
    c5 = 3167

    #FIX: same units issue as the other two IDT correlations - pressure must be in bar.
    p_bar = max(p_cad / 1e5, 1e-9)

    IDT = c1 * (p_bar/t_cad)**-c2 * (1 - x_egr)**-c3 * lmnbda**-c4 * np.exp(c5 / t_cad)

    return IDT


def livengood_wu(rpm, IDT, CAD_step):
   
    '''
    Inputs:
    - rpm: current engine rpm
    - Pcad_run: List of the pressures for every crank angle degree
    - Tcad_run: List of the temperatures for every crank angle degree
    - CADivc: crank angle degree at intake valve opening
    - CADeoc: crank angle degree at end of combustion

    Outputs:
    - LWI                    (unitless)  [increment of the Livengood-Wu knock integral for this CAD step]

    FIX: the original line mixed two incompatible conventions. "1/(6*rpm)" (with CAD_step
    in degrees) and "np.deg2rad(CAD_step)/omega" (with omega in rad/s) are each valid ways
    to turn a crank-angle step into a time step, but the code combined the constant "6"
    (the deg/s-per-rpm factor) with omega (already in rad/s), which is neither. It also
    never reconciled units between dt (seconds) and IDT (milliseconds), which alone is a
    1000x error. Below, dt is computed explicitly in milliseconds so it can be divided
    directly by IDT (ms) to get a dimensionless increment.
    '''

    dI = (1/(6*rpm))*(1/IDT)*CAD_step

    return  dI 


'''
___________________________________________________________
|                                                         |
|                     Dialouge Box                        |
|_________________________________________________________|

'''
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Knock Prediction Model")
#         self.setGeometry(700, 300, 750, 500)

# def main():
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())

# if __name__ == "__main__":
#     main()




'''
___________________________________________________________
|                                                         |
|                       Main Code                         |
|_________________________________________________________|

'''

#Universal Model Constants
R_UNIVERSAL = 8.31446261815324 #J/K*mol


#User-Updated Model Constants
# location = input('Testing Location:   ')
# fuel_type = input('Fuel Type:   ')
# lmnbda = float(input('Lambda:   '))

location = 'rellis'
fuel_type = '93'
lmnbda = 1.00

CAD_step = 1 #deg


#Important Variables
pk_T_rpm = engine_parameters['combustion_characteristics']['peak_torque_rpm'] #rpm
R = 8.314462618 #J/(mol*K)
ON = fuel_properties[fuel_type]['ON']
Patm = weather_data[location]['p_atm']
Tatm = weather_data[location]['t_atm']
CAD_step = 1 #deg


#Monte Carlo Simulations
monte_carlo_sims = 200
combustion_duration = np.random.uniform(35,50, monte_carlo_sims)
m = np.random.uniform(1.5,2.5, monte_carlo_sims)
T_wall = np.random.uniform(453.15,523.15, monte_carlo_sims)
rpm = np.random.uniform(pk_T_rpm - 100, pk_T_rpm + 100, monte_carlo_sims)

#Initialize Pressure and Temperature Data
pressure = {}
temperature = {}
livengood_wu_integral = {
    'douaund_eyzat':{},
    'hoepke':{},
    'chen_zheng':{}
}
CADs = {}

for spark in tqdm(range(0,20), desc= 'varying spark timing...'):
    
    #Monte Carlo Seed
    #FIX: random.randint(a, b) is inclusive on both ends, so this could draw index 200
    #into arrays of length 200 (valid indices 0-199) and raise an IndexError. Upper
    #bound corrected to monte_carlo_sims - 1.
    seed = random.randint(0, monte_carlo_sims - 1)
    combustion_duration_i = combustion_duration[seed]
    m_i = m[seed]
    T_wall_i = T_wall[seed]
    rpm_i = rpm[seed]

    #Add a dictionary for each tested spark timing
    #pressure and temperature
    pressure.update({spark:[engine_parameters['combustion_characteristics']['MAP']]})
    temperature.update({spark:[weather_data[location]['t_atm'] + 15]})

    #ignition delay timing
    livengood_wu_integral['douaund_eyzat'].update({spark:[0]})
    livengood_wu_integral['hoepke'].update({spark:[0]})
    livengood_wu_integral['chen_zheng'].update({spark:[0]})
    CADs.update({spark:[]})

    
    for CAD in np.arange((engine_parameters['combustion_characteristics']['CADivc']+ 180), (360 - spark + combustion_duration_i),1):

        #Append to CADs
        CADs[spark].append(CAD)


        if CAD < 360-spark: 
            Cp_u = Cp_unburned(temperature[spark][-1],lmnbda, fuel_type)
            shr = Cp_u / (Cp_u - R)
            p_cad, t_cad, v_cad, v_cad_1, Ah = crank_slider(CAD, CAD_step, shr, weather_data[location]['t_atm'])

        else:
            p_cad, t_cad = combustion_analysis(CAD, 1, pressure[spark][-1], temperature[spark][-1], spark, combustion_duration_i, lmnbda, rpm_i, T_wall_i, fuel_type, m_i, location)
        
        #Pressure and Temperature
        pressure[spark].append(p_cad)
        temperature[spark].append(t_cad)

        #Ignition Delay Timing

        IDT_douaund = douaund_eyzat(ON, p_cad, t_cad)
        IDT_hoepke = hoepke(0.0, p_cad, t_cad)
        IDT_chen = chen_zheng(lmnbda, 0.0, p_cad, t_cad)

        dI_douaund = livengood_wu(rpm_i, IDT_douaund, CAD_step)
        dI_hoepke = livengood_wu(rpm_i, IDT_hoepke, CAD_step)
        dI_chen = livengood_wu(rpm_i, IDT_chen, CAD_step)

        livengood_wu_integral['douaund_eyzat'][spark].append(
            livengood_wu_integral['douaund_eyzat'][spark][-1] + dI_douaund
        )

        livengood_wu_integral['hoepke'][spark].append(
            livengood_wu_integral['hoepke'][spark][-1] + dI_hoepke
        )

        livengood_wu_integral['chen_zheng'][spark].append(
            livengood_wu_integral['chen_zheng'][spark][-1] + dI_chen
        )


#print(pressure[12])
# print(temperature[12])
print(livengood_wu_integral['chen_zheng'][12])

plt.plot(CADs[12], temperature[12][:-1])
plt.axvline(x = 360-12, color= 'red', linestyle= '--')
plt.title("Temperature vs Crank Angle Degree")
plt.xlabel('Crank Angle Degree')
plt.ylabel('Temperature (K)')
plt.show()
    

        







            







