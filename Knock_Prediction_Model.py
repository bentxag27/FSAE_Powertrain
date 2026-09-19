'''
___________________________________________________________
|                                                         |
|                Knock Prediction Model                   |
|_________________________________________________________|

'''

from xml.parsers.expat import model

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


Combustion_Elements = {
    'C2H5OH': { 
        'density': 0.78945, #g/cm^3
        'molar_mass': 46.0684400, #g/mol
        'nasa_1': {
            'min_temp': 159.000, #K
            'max_temp': 390.0007, #K
            'a1': 4.501115940E+05,
            'a2': -1.020828990E+04,
            'a3': 1.014266780E+02,
            'a4': -3.874672610E-01,
            'a5': 7.121392610E-04,
            'a6': -1.857071450E-07,
            'a7': -2.037622570E-10,
        },
                'nasa_1': {
            'min_temp': 159.000, #K
            'max_temp': 390.0007, #K
            'a1': 4.501115940E+05,
            'a2': -1.020828990E+04,
            'a3': 1.014266780E+02,
            'a4': -3.874672610E-01,
            'a5': 7.121392610E-04,
            'a6': -1.857071450E-07,
            'a7': -2.037622570E-10,
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
        'bore': 80, #mm
        'stroke': 105, #mm
        'crank_radius': 40, #mm
        'con_rod': 160, #mm ***subject to change based on actual con rod length***
        'compression_ratio': 12.7, #unitless
        'displacement': 692.7, #cc
    },
    'combustion_charicteristics': {
        'CADivc': 55, #deg ABDC
        'redline_rpm': 9000, #rpm
        'volumetric_efficiency': 0.95, #unitless
    }
}

fuel_properties = {
    'stoich_afr': 9.8, #unitless
    'lhv': 29.2 #MJ/kg
}

#Preliminary Functions 

def crank_slider(crank_radius, con_rod, CAD, SHR, Tatm, Patm, CADivc, Disp, CR, Bore):

    '''
    Inputs:
     - crank_radius: crank radius (mm)
     - con_rod: connecting rod length (mm)
     - CAD: crank angle degree (deg)
     - SHR: specific heat ratio (unitless)
     - Tatm: atmospheric temperature (K)
     - Patm: atmospheric pressure (kPa)
     - CADivc: crank angle degree at intake valve closing (deg)
     - Disp: displacement (cc)
     - CR: compression ratio (unitless)

     Outputs:
     - Pcad: pressure at current crank angle degree
     - Tcad: temperatire at current crank angle degree
    '''
    theta = np.deg2rad(CAD)
    piston_position = crank_radius + con_rod - (np.sqrt((con_rod**2)-((crank_radius**2)*(np.sin(theta))**2)) + crank_radius*np.cos(theta)) 
    vol = (Disp/CR-1) + ((np.pi/4) * (Bore**2) * piston_position)/1000
    Tivc = Tatm + 15
    Pivc = 
    Pcad = Patm*(vol/(Disp/CR))
    Tcad = Tivc*(Pcad/Patm)**((SHR-1)/SHR)
    return Pcad, Tcad

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

def wiebe(CAD, Spark, combustion_duration, m):

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
    

    xb = 1 - np.e**(-a*((CAD-Spark)/(combustion_duration))**(m+1))

    return xb

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
  
def shr_unburned(Tcad, lmnbda, Combustion_Elements = Combustion_Elements, engine_parameters = engine_parameters):

    '''
    Inputs:
    - Tcad: Temperature at current crank angle degree
    - Combustion_Elements: dictionary of combustion elements
    - engine_parameters: dictionary of engine parameters
    - lmnbda: A measure of the air fuel ratio of the current mixture

    Outputs:
    - SHR: specific heat ratio (unitless)
    '''

    #constants
    R_u = 8.314472 #J/(mol*K)

    #Atmospheric Air Composition
    V_air = engine_parameters['geometry']['displacement'] * engine_parameters['combustion_charicteristics']['volumetric_efficiency'] #cc
    m_air = V_air * .001225 #g
    m_fuel = m_air / (lmnbda*fuel_properties['stoich_afr']) #cc
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
    
    shr_unburned = Cp_unburned/(Cp_unburned-R_u)

    return shr_unburned

def shr_burned(Tcad, lmnbda, Combustion_Elements = Combustion_Elements, engine_parameters = engine_parameters):

    V_air = engine_parameters['geometry']['displacement'] * engine_parameters['combustion_charicteristics']['volumetric_efficiency'] #cc
    V_fuel = V_air / (lmnbda*fuel_properties['stoich_afr']) #cc
    V_C2H5OH = V_fuel * 0.85 #cc
    V_C8H18 = V_fuel * 0.15 #cc
    m_air = V_air * .001225 #g

    R_u = 8.314472 #J/(mol*K)

    #Precombustion mols

    #Ethanol
    m_C2H5OH = V_C2H5OH * Combustion_Elements['C2H5OH']['density'] #g
    mol_C2H5OH = m_C2H5OH / Combustion_Elements['C2H5OH']['molar_mass'] #mol
    Cp_C2H5OH = nasa_polynomial(Tcad, 'C2H5OH', Combustion_Elements) #J/(mol*K)

    #Octane
    m_C8H18 = V_C8H18 * Combustion_Elements['C8H18']['density'] #g
    mol_C8H18 = m_C8H18 / Combustion_Elements['C8H18']['molar_mass'] #mol
    Cp_C8H18 = nasa_polynomial(Tcad, 'C8H18', Combustion_Elements) #J/(mol*K)

    #Nitrogen
    m_N2 = V_air * .7808 * Combustion_Elements['N2']['density'] #g
    mol_N2 = m_N2 / Combustion_Elements['N2']['molar_mass'] #mol
    Cp_N2 = nasa_polynomial(Tcad, 'N2', Combustion_Elements) #J/(mol*K)

    #Oxygen
    m_O2 = V_air * .2095 * Combustion_Elements['O2']['density'] #g
    mol_O2 = m_O2 / Combustion_Elements['O2']['molar_mass'] #mol
    Cp_O2 = nasa_polynomial(Tcad, 'O2', Combustion_Elements) #J/(mol*K)

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
    mol_C2H5OH = mol_C2H5OH - num_rxn * 1 
    mol_C8H18 = mol_C8H18 - num_rxn * 2
    mol_H2O = num_rxn * 21
    mol_CO2 = mol_CO2 + num_rxn * 18
    mol_O2 = mol_O2 - num_rxn * 28

    #Water
    Cp_H2O = nasa_polynomial(Tcad, 'H2O', Combustion_Elements)

    mol_total = mol_C2H5OH + mol_C8H18 + mol_H2O + mol_CO2 + mol_N2 + mol_Ar + mol_O2

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
        (Cp_H2O*mol_H2O)
        )/ mol_total
    
    shr_burned = Cp_burned/(Cp_burned-R_u)


    return shr_burned

    



    



def livengood_wu(rpm, Pcad_run, Tcad_run, CADivc, CADeoc):

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
   return 0 #Comeback to this function later, need to figure out how to implement it properly




#unburnt gas test 
T = np.arange(200, 900)
y = []
for i in range(len(T)):
    y.append(shr_unburned(T[i],.95))

plt.plot(T,y)
plt.show()

            







