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
___________________________________________________________
|                                                         |
|                        Imports                          |
|_________________________________________________________|

'''
import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import PySide6 as Py
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
        'ON' : 99 #Octane
    },
    '93':{
        'stoich_afr': 14.08, #unitless
        'lhv': 41.6, #MJ/kg
        'ON': 93 #Octane
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

def crank_slider(CAD, SHR, Tatm, engine_parameters = engine_parameters):

    '''
    Overview:
        this function is a crank-slider model that determines the cylinder
    temperature and pressure from engine geometry and the temperature and 
    pressure at intake valve closing. Solves for the adiabatic portion of 
    the compression stroke is used for the motored pressure necessary for 
    the Woschni heat transfer model

    Inputs:
     - Engine Geometries
         - crank_radius (mm)
         - connecting_rod (mm)
         - bore (mm)
         - displacement (cc)
         - compression_ratio (unitless)
         - CAD_ivc (deg)
         - MAP (Pa)
     - CAD (deg)
     - SHR (unitless)
     - t_atm (K)

     Outputs:
     - p_cad (Pa)
     - t_cad (K)
    '''

    #Important Engine Metrics
    crank_radius = engine_parameters['geometry']['crank_radius']
    connecting_rod = engine_parameters['geometry']['con_rod']
    CAD_ivc = engine_parameters['combustion_characteristics']['CADivc']
    displacement = engine_parameters['geometry']['displacement']
    compression_ratio = engine_parameters['geometry']['compression_ratio']
    bore = engine_parameters['geometry']['bore']
    MAP = engine_parameters['combustion_characteristics']['MAP']


    #Baseline Metrics at Intake Valve Closing
    piston_position_ivc = crank_radius + connecting_rod - (np.sqrt((connecting_rod**2)-((crank_radius**2) * (np.sin(np.deg2rad(CAD_ivc)))**2)) + crank_radius*np.cos(np.deg2rad(CAD_ivc)))
    clearance_volume = displacement / compression_ratio
    v_ivc = clearance_volume + ((np.pi/4) * (bore**2) * piston_position_ivc)/1000
    t_ivc = Tatm + 15
    p_ivc = MAP #Pa
    

    #Metrics throughout adiabatic compression
    theta = np.deg2rad(CAD)
    piston_position = crank_radius + connecting_rod - (np.sqrt((connecting_rod**2)-((crank_radius**2)*(np.sin(theta))**2)) + crank_radius*np.cos(theta))
    vol = clearance_volume + ((np.pi/4) * (bore**2) * piston_position)/1000
    p_cad = p_ivc*(v_ivc/vol)**SHR
    t_cad = t_ivc*(v_ivc/vol)**(SHR-1)


    return p_cad, t_cad

def volume(CAD, CAD_step, engine_parameters = engine_parameters):

    #Important Engine Metrics
    crank_radius = engine_parameters['geometry']['crank_radius']
    con_rod = engine_parameters['geometry']['con_rod']
    Disp = engine_parameters['geometry']['displacement']
    CR = engine_parameters['geometry']['compression_ratio']
    Bore = engine_parameters['geometry']['bore']
    clearance_volume = Disp/CR

    #Volume Model
    theta = np.deg2rad(CAD)
    theta_step = np.deg2rad(CAD_step)
    x_i = crank_radius + con_rod - (np.sqrt((con_rod**2)-((crank_radius**2)*(np.sin(theta))**2)) + crank_radius*np.cos(theta))
    x_i_1 = crank_radius + con_rod - (np.sqrt((con_rod**2)-((crank_radius**2)*(np.sin(theta+theta_step))**2)) + crank_radius*np.cos(theta+theta_step))
    v_i = clearance_volume + (((np.pi * Bore**2)/4)*x_i)/1000
    v_i_1 = clearance_volume + (((np.pi * Bore**2)/4)*x_i_1)/1000

    #Heat transfer area
    Ah = (np.pi*Bore**2)/2 + np.pi*Bore*x_i

    return v_i, v_i_1, Ah


def douaund_eyzat(ON, Pcad, Tcad):

    '''
    Inputs:
    - ON: Octane Number (unitless)
    - Pcad: Pressure at current crank angle degree
    - Tcad: Temperature at current crank angle degree

    Output:
    - IDT: ignition delay time (ms)
    '''

    #Model Constants
    c1 = 17.69
    c2 = 3.402
    c3 = 1.7
    c4 = 3800

    IDT = c1 * (ON/100)**c2 * Pcad**(-c3) * np.exp(c4/Tcad)

    return IDT

def hoepke(Xegr,Pcad,Tcad):

    '''
    Inputs:
    - Xeger: Portion of exhuast gas recirculated
    - Pcad: Pressure at current crank angle degree
    - Tcad: Temperature at current crank angle degree

    Outputs:
    - IDT: ignition delay time (ms)
    '''

    #Model Constants
    c1 = 8.799
    c2 = 1.006
    c3 = 1.499
    c4 = 5865

    IDT = c1 * (Pcad/Tcad)**-c2 * (1 - Xegr)**-c3 * np.e**(c4/Tcad)

    return IDT

def chen_zheng(lmnbda, Xegr, Pcad, Tcad):

    '''
    Inputs:
    - lmnbda: A measure of the air fuel ratio of the current mixture
    - Xeger: Portion of exhuast gas recirculated
    - Pcad: Pressure at current crank angle degree
    - Tcad: Temperature at current crank angle degree

    Outputs:
    - IDT: ignition delay time (ms)
    '''

    #Model Constants
    c1 = 0.000053
    c2 = 2.374
    c3 = 3.013
    c4 = 1.927
    c5 = 3167

    IDT = c1 * (Pcad/Tcad)**-c2 * (1 - Xegr)**-c3 * lmnbda**-c4 * np.e**(c5/Tcad)

    return IDT

def wiebe(CAD, CAD_step, CADivc, Spark, combustion_duration, m ):

    '''
    Inputs:
    - CAD: crank angle degree (deg)
    - Spark: crank angle degree at spark (deg)
    - combustion_duration: duration of combustion (deg)
    - a: amount burned (unitless)
    - m: shape parameter (unitless)

    Outputs:
    - x: fraction of fuel burned
    '''
    #constants
    a = 6.9078 #0-99.9% burned

    xb_i = 1 - np.e**(-a*(((CAD-CADivc)-Spark)/(combustion_duration))**(m+1))
    xb_i_1 = 1 - np.e**(-a*(((CAD+CAD_step-CADivc)-Spark)/(combustion_duration))**(m+1))

    return xb_i, xb_i_1

def pressure_increase(CAD, CAD_step, P_i, T_i, Spark, combustion_duration, lmnbda, rpm, Tatm, T_wall, fuel_type, m, engine_parameters = engine_parameters, fuel_properties = fuel_properties):

    '''
    Inputs:
    - CAD: current crank angle degree (deg)
    - CAD_step: crank angle step size (deg)
    - P_i: current pressure (Pa)
    - T_i: current temperature (K)
    
    Outputs:
    - P_i_1: pressure increase over CAD_step (Pa)
    '''

    #Important Engine Metrics
    crank_radius = engine_parameters['geometry']['crank_radius'] #mm
    con_rod = engine_parameters['geometry']['con_rod'] #mm
    CAD_ivc = engine_parameters['combustion_characteristics']['CADivc'] #deg
    Disp = engine_parameters['geometry']['displacement'] #cc
    CR = engine_parameters['geometry']['compression_ratio'] #unitless
    Bore = engine_parameters['geometry']['bore'] #mm
    stroke = engine_parameters['geometry']['stroke'] #mm
    MAP = engine_parameters['combustion_characteristics']['MAP'] #kPa

    #Universal Gas Constant
    R_u = 8.314462618 #J/(mol*K)

    #Baseline Metrics at Intake Valve Closing
    piston_position_ivc = crank_radius + con_rod - (np.sqrt((con_rod**2)-((crank_radius**2) * (np.sin(np.deg2rad(CAD_ivc)))**2)) + crank_radius*np.cos(np.deg2rad(CAD_ivc)))
    clearance_volume = Disp / CR
    vol_ivc = clearance_volume + ((np.pi/4) * (Bore**2) * piston_position_ivc)/1000
    Tivc = Tatm + 15
    Pivc = MAP*1000 #Pa


    #Wiebe Function Components 
    xb_i, xb_i_1 = wiebe(CAD, CAD_step, Spark, combustion_duration, m)

    #Specific Heat Ratio
    Cp_u, mol_total, m_fuel = Cp_unburned(T_i, lmnbda, fuel_type)
    Cp = Cp_burned(T_i, lmnbda)*xb_i + Cp_u*(1-xb_i)
    k = Cp/(Cp - R_u)

    #Volume
    v_i, v_i_1, Ah = volume(CAD, CAD_step)

    #Heat Gained from combustion
    V_air = Disp * engine_parameters['combustion_characteristics']['volumetric_efficiency'] #cc
    m_air = V_air * .001225 #g
    m_fuel = (m_air / (lmnbda*fuel_properties[fuel_type]['stoich_afr']))/1000 #kg
    Qin = m_fuel*fuel_properties[fuel_type]['lhv']*1000000 #J

    #Heat Transfer to the walls
    mean_piston_speed = 2*(stroke/1000)*rpm / 60
    pressure_motored = Pivc * (vol_ivc/v_i)**k
    w = 2.28*mean_piston_speed + 0.00324*((v_i * Tivc)/(vol_ivc * Pivc))*(P_i - pressure_motored)
    hcg = 3.26*(engine_parameters['geometry']['bore']/1000)**-0.2 * P_i**0.8 * T_i**-0.55 * w**0.8
    Qloss = (hcg * Ah / (2*np.pi*rpm/60))*(T_i - T_wall)

    P_i_1 = P_i + ((k-1)/v_i)*(Qin*(xb_i_1 - xb_i) - Qloss*np.deg2rad(CAD_step)) - (k*P_i/v_i)*(v_i_1-v_i)
    T_i_1 = (P_i_1 * v_i_1)/(mol_total * R_u)

    return P_i_1, T_i_1

def nasa_polynomial(Tcad, element, Combustion_Elements = Combustion_Elements):

    '''
    Inputs:
    - Tcad: Temperature at current crank angle degree
    - Combustion_Elements: dictionary of combustion elements
    - desired element: string of desired element to calculate Cp for (N2, O2, CO2, H2O, )

    Outputs:
    - Cp: specific heat capacity (J/(mol*K))
    '''

    Tcad = float(Tcad)

    #constants
    R = 8.314462618 #J/(mol*K)

    if Tcad < 1000:
        #Calculate Cp for each element
        Cp = R * (
            Combustion_Elements[element]['nasa_1']['a1']*Tcad**-2 + 
            Combustion_Elements[element]['nasa_1']['a2']*Tcad**-1 + 
            Combustion_Elements[element]['nasa_1']['a3'] + 
            Combustion_Elements[element]['nasa_1']['a4']*Tcad + 
            Combustion_Elements[element]['nasa_1']['a5']*Tcad**2 + 
            Combustion_Elements[element]['nasa_1']['a6']*Tcad**3 + 
            Combustion_Elements[element]['nasa_1']['a7']*Tcad**4
            )
    else:
        #Calculate Cp for each element
        Cp = R * (
            Combustion_Elements[element]['nasa_2']['a1']*Tcad**-2 + 
            Combustion_Elements[element]['nasa_2']['a2']*Tcad**-1 + 
            Combustion_Elements[element]['nasa_2']['a3'] + 
            Combustion_Elements[element]['nasa_2']['a4']*Tcad + 
            Combustion_Elements[element]['nasa_2']['a5']*Tcad**2 + 
            Combustion_Elements[element]['nasa_2']['a6']*Tcad**3 + 
            Combustion_Elements[element]['nasa_2']['a7']*Tcad**4
            )

    return Cp
  
def Cp_unburned(Tcad, lmnbda, fuel_type, Combustion_Elements = Combustion_Elements, engine_parameters = engine_parameters):

    '''
    Inputs:
    - Tcad: Temperature at current crank angle degree
    - Combustion_Elements: dictionary of combustion elements
    - engine_parameters: dictionary of engine parameters
    - lmnbda: A measure of the air fuel ratio of the current mixture

    Outputs:
    - SHR: specific heat ratio (unitless)
    '''


    #Atmospheric Air Composition
    V_air = engine_parameters['geometry']['displacement'] * engine_parameters['combustion_characteristics']['volumetric_efficiency'] #cc
    m_air = V_air * .001225 #g
    m_fuel = m_air / (lmnbda*fuel_properties[fuel_type]['stoich_afr']) #g
    V_fuel = m_fuel / (0.85*Combustion_Elements['C2H5OH']['density'] + 0.15*Combustion_Elements['C8H18']['density'])
    V_C2H5OH = V_fuel * 0.85 #cc
    V_C8H18 = V_fuel * 0.15 #cc
    

    #elemental composition of fuel

    #ethanol
    m_C2H5OH = V_C2H5OH * Combustion_Elements['C2H5OH']['density'] #g
    mol_C2H5OH = m_C2H5OH / Combustion_Elements['C2H5OH']['molar_mass'] #mol
    Cp_C2H5OH = nasa_polynomial(Tcad, 'C2H5OH', Combustion_Elements) #J/(mol*K)

    #Octane
    m_C8H18 = V_C8H18 * Combustion_Elements['C8H18']['density'] #g
    mol_C8H18 = m_C8H18 / Combustion_Elements['C8H18']['molar_mass']
    Cp_C8H18 = nasa_polynomial(Tcad, 'C8H18', Combustion_Elements) #J/(mol*K)

    #elemental composition of air

    #Nitrogen
    m_N2 = V_air * .7808 * Combustion_Elements['N2']['density'] #g
    mol_N2 = m_N2 / Combustion_Elements['N2']['molar_mass'] #mol
    Cp_N2 = nasa_polynomial(Tcad, 'N2', Combustion_Elements) #J/(mol*K)

    #Oxygen
    m_O2 = V_air * .2095 * Combustion_Elements['O2']['density'] #g
    mol_O2 = m_O2 / Combustion_Elements['O2']['molar_mass'] # mol
    Cp_O2 = nasa_polynomial(Tcad, 'O2', Combustion_Elements) #J/(mol*K)

    #Argon
    m_Ar = V_air * .0093 * Combustion_Elements['Ar']['density'] #g
    mol_Ar = m_Ar / Combustion_Elements['Ar']['molar_mass'] # mol
    Cp_Ar = nasa_polynomial(Tcad, 'Ar', Combustion_Elements) #J/(mol*K)

    #Carbon Dioxide
    m_CO2 = V_air * .0004 * Combustion_Elements['CO2']['density'] #g
    mol_CO2 = m_CO2 / Combustion_Elements['CO2']['molar_mass']
    Cp_CO2 = nasa_polynomial(Tcad, 'CO2', Combustion_Elements) #J/(mol*K)

    #totals across unburnt gas mixture
    mol_total = mol_C2H5OH + mol_C8H18 + mol_N2 + mol_O2 + mol_Ar + mol_CO2
    
    Cp_unburned  = (
        (Cp_C2H5OH*mol_C2H5OH) + 
        (Cp_C8H18*mol_C8H18) + 
        (Cp_N2*mol_N2) + 
        (Cp_O2*mol_O2) + 
        (Cp_Ar*mol_Ar) + 
        (Cp_CO2*mol_CO2)
        )/ (mol_total)

    return Cp_unburned, mol_total, m_fuel 

def Cp_burned(Tcad, lmnbda, Combustion_Elements = Combustion_Elements, engine_parameters = engine_parameters):

    #Atmospheric Air Composition
    V_air = engine_parameters['geometry']['displacement'] * engine_parameters['combustion_characteristics']['volumetric_efficiency'] #cc
    m_air = V_air * .001225 #g
    m_fuel = m_air / (lmnbda*fuel_properties[fuel_type]['stoich_afr']) #g
    V_fuel = m_fuel / (0.85*Combustion_Elements['C2H5OH']['density'] + 0.15*Combustion_Elements['C8H18']['density'])
    V_C2H5OH = V_fuel * 0.85 #cc
    V_C8H18 = V_fuel * 0.15 #cc

    #Precombustion mols

    #ethanol
    m_C2H5OH = V_C2H5OH * Combustion_Elements['C2H5OH']['density'] #g
    mol_C2H5OH = m_C2H5OH / Combustion_Elements['C2H5OH']['molar_mass'] #mol
    Cp_C2H5OH = nasa_polynomial(Tcad, 'C2H5OH', Combustion_Elements) #J/(mol*K)

    #Octane
    m_C8H18 = V_C8H18 * Combustion_Elements['C8H18']['density'] #g
    mol_C8H18 = m_C8H18 / Combustion_Elements['C8H18']['molar_mass']
    Cp_C8H18 = nasa_polynomial(Tcad, 'C8H18', Combustion_Elements) #J/(mol*K)

    #Nitrogen
    m_N2 = V_air * .7808 * Combustion_Elements['N2']['density'] #g
    mol_N2 = m_N2 / Combustion_Elements['N2']['molar_mass'] #mol
    Cp_N2 = nasa_polynomial(Tcad, 'N2', Combustion_Elements) #J/(mol*K)

    #Oxygen
    m_O2 = V_air * .2095 * Combustion_Elements['O2']['density'] #g
    mol_O2 = m_O2 / Combustion_Elements['O2']['molar_mass'] #mol

    #Argon
    m_Ar = V_air * .0093 * Combustion_Elements['Ar']['density'] #g
    mol_Ar = m_Ar / Combustion_Elements['Ar']['molar_mass'] #mol
    Cp_Ar = nasa_polynomial(Tcad, 'Ar', Combustion_Elements) #J/(mol*K)

    #Carbon Dioxide
    m_CO2 = V_air * .0004 * Combustion_Elements['CO2']['density'] #g
    mol_CO2 = m_CO2 / Combustion_Elements['CO2']['molar_mass'] #mol
    Cp_CO2 = nasa_polynomial(Tcad, 'CO2', Combustion_Elements) #J/(mol*K)

    #Reaction Amounts
    num_rxn = mol_O2/28
    mol_C2H5OH_b = mol_C2H5OH - num_rxn * 1 
    mol_C8H18_b = mol_C8H18 - num_rxn * 2
    mol_H2O = num_rxn * 21
    mol_CO2 = mol_CO2 + num_rxn * 18

    #Water
    Cp_H2O = nasa_polynomial(Tcad, 'H2O', Combustion_Elements)

    mol_total = mol_H2O + mol_CO2 + mol_N2 + mol_Ar + (mol_C2H5OH - mol_C2H5OH_b) + (mol_C8H18 - mol_C8H18_b) 

    #Post Combustion
    m_C2H5OH = mol_C2H5OH * Combustion_Elements['C2H5OH']['molar_mass']
    m_C8H18 = mol_C8H18 * Combustion_Elements['C8H18']['molar_mass']
    m_H20  = mol_H2O * Combustion_Elements['H2O']['molar_mass']
    m_CO2 = mol_CO2 * Combustion_Elements['CO2']['molar_mass']
    m_O2 = mol_O2 * Combustion_Elements['O2']['molar_mass']

    #totals across unburnt gas mixture

    Cp_burned  = (
        (Cp_N2*mol_N2) +  
        (Cp_Ar*mol_Ar) + 
        (Cp_CO2*mol_CO2) + 
        (Cp_H2O*mol_H2O) +
        (Cp_C2H5OH*mol_C2H5OH) +
        (Cp_C8H18*mol_C8H18)
        )/ mol_total

    return Cp_burned

def livengood_wu(rpm, IDT, CAD_step):

   '''
    Inputs:
    - rpm: current engine rpm
    - Pcad_run: List of the pressures for every crank angle degree
    - Tcad_run: List of the temperatures for every crank angle degree
    - CADivc: crank angle degree at intake valve opening
    - CADeoc: crank angle degree at end of combustion

    Outputs:
    - 
    '''

   LWI = (1 / (6 * rpm)) * (1/IDT) * CAD_step
   
   return  LWI 

'''
___________________________________________________________
|                                                         |
|                     Dialouge Box                        |
|_________________________________________________________|

'''
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Knock Prediction Model")
        self.setGeometry(700, 300, 750, 500)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()




'''
___________________________________________________________
|                                                         |
|                       Main Code                         |
|_________________________________________________________|

'''
#User imports for specific model
location = input('Testing Location:   ')
fuel_type = input('Fuel Type:   ')
lmnbda = float(input('Lambda:   '))


#Important Variables
pk_T_rpm = engine_parameters['combustion_characteristics']['peak_torque_rpm'] #rpm
R = 8.314462618 #J/(mol*K)
ON = fuel_properties[fuel_type]['ON']
Patm = weather_data[location]['Patm']
Tatm = weather_data[location]['Tatm']
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

for spark in range(0,20):
    

    #Add a dictionary for each tested spark timing
    #pressure and temperature
    pressure.update({spark:[engine_parameters['combustion_characteristics']['MAP']]})
    temperature.update({spark:[weather_data[location]['Tatm'] + 15]})

    #ignition delay timing
    livengood_wu_integral['douaund_eyzat'].update({spark:[0]})
    livengood_wu_integral['hoepke'].update({spark:[0]})
    livengood_wu_integral['chen_zheng'].update({spark:[0]})
    CADs.update({spark:[]})

    
    for CAD in np.arange((engine_parameters['combustion_characteristics']['CADivc']+ 180), (360 - spark + combustion_duration.normal()),1):

        #Append to CADs
        CADs[spark].append(CAD)


        if CAD < 360-spark: 
            Cp_u, mol_total, m_fuel = Cp_unburned(temperature[spark][-1],lmnbda, fuel_type)
            shr = Cp_u / (Cp_u - R)
            Pcad, Tcad = crank_slider(CAD, shr, weather_data[location]['Tatm'])

        else:
            Pcad, Tcad = pressure_increase(CAD, 1, pressure[spark][-1], temperature[spark][-1], spark, combustion_duration, lmnbda, rpm.normal(), Tatm, T_wall.normal(), fuel_type, m.normal())
        
        #Pressure and Temperature
        pressure[spark].append(Pcad)
        temperature[spark].append(Tcad)

        #Ignition Delay Timing
        livengood_wu_integral['douaund_eyzat'][spark].append(livengood_wu(rpm, douaund_eyzat(ON, Pcad, Tcad)))
        livengood_wu_integral['hoepke'][spark].append(livengood_wu(rpm, hoepke(0, Pcad, Tcad)))
        livengood_wu_integral['chen_zheng'][spark].append(livengood_wu(rpm, chen_zheng(lmnbda,0,Pcad,Tcad)))


plt.plot(CADs[12], livengood_wu_integral['chen_zheng'])
plt.show()
    

        







            







