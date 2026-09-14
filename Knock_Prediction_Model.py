'''
___________________________________________________________
|                                                         |
|                Knock Prediction Model                   |
|_________________________________________________________|

'''

import numpy as np
import matplotlib.pyplt as plt
import pandas as pd

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

    piston_position = crank_radius + con_rod - (((con_rod**2)-((crank_radius**2)*(np.sin(np.pi()/180))**2))**(1/2) + crank_radius*np.cos(np.pi()/180)) 
    vol = (Disp/CR) + ((np.pi()/4) * (Bore**2) * piston_position)/1000
    Tivc = Tatm + 15
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

    IDT = c1 * (ON/100)**c2 * Pcad**(-c3) * e**(c4/Tcad)

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

Combustion_Elements = {
    ethanol: { 
        density: 0.78945, #g/cm^3
        molar_mass: 46.0684400, #g/mol
        nasa_1: {
            min_temp: 159.000, #K
            max_temp: 390.0007, #K
            a1: 4.501115940E+05,
            a2: -1.020828990E+04,
            a3: 1.014266780E+02,
            a4: -3.874672610E-01,
            a5: 7.121392610E-04,
            a6: -1.857071450E-07,
            a7: -2.037622570E-10,
        },
    },
    octane: {
        density: 0.703, #g/cm^3}
        molar_mass: 114.22852, #g/mol
        nasa_1: {
            min_temp: 200.000, #K
            max_temp: 1000.000, #K
            a1: -6.986647150E+05,
            a2: 1.338501096E+04,
            a3: -8.415165920E+01,
            a4: 3.271936660E-01,
            a5: -3.777209590E-04,
            a6: 2.339836988E-07,
            a7: -6.010892650E-11,
        },
        nasa_2: {
            min_temp: 1000.000, #K
            max_temp: 6000.000, #K
            a1: 6.36540695E+06,
            a2: -3.105364657E+04,
            a3: 6.969162340E+01,
            a4: 1.048059637E-02,
            a5: -4.129621950E-06,
            a6: 5.543226320E-10,
            a7: -2.6514366499E-14
        }
    },
    N2: {
        density: 0.0012506, #g/cm^3
        molar_mass: 28.0134, #g/mol
        nasa_1: {
            min_temp: 200.000, #K
            max_temp: 1000.000, #K
            a1: 2.210371497E+04,
            a2: -3.818461820E+02,
            a3: 6.082738360E+00,
            a4: -8.530914410E-03,
            a5: 1.384646189E-05,
            a6: -9.625793620E-09,
            a7: 2.519705809E-12
        },
        nasa_2: {
            min_temp: 1000.000, #K
            max_temp: 6000.000, #K
            a1: 5.877124060E+05,
            a2: -2.239249073E+03,
            a3: 6.066949220E+00,
            a4: -6.139685500E-04,
            a5: 1.491806679E-07,
            a6: -1.923105485E-11,
            a7: 1.061954386E-15
        }
    },
    O2: {
        density: 0.001429, #g/cm^3
        molar_mass: 31.9988, #g/mol
        nasa_1: {
            min_temp: 200.000, #K
            max_temp: 1000.000, #K
            a1: -3.425563420E+04,      
            a2: 4.847000970E+02,
            a3: 1.119010961E+00,
            a4: 4.293889240E-03,
            a5: -6.836300520E-07,
            a6: -2.023372700E-09,
            a7: 1.039040018E-12,
        },
        nasa_2: {
            min_temp: 1000.000, #K
            max_temp: 6000.000, #K
            a1: -1.037939022E+06,     
            a2: 2.344830282E+03,
            a3: 1.819732036E+00,
            a4: 1.267847582E-03,
            a5: -2.188067988E-07,
            a6: 2.053719572E-11,
            a7: -8.193467050E-16
        }
    },
    Ar: {
        density: 0.001784, #g/cm^3
        molar_mass: 39.948, #g/mol
        nasa_1: {
            min_temp: 200.000, #K
            max_temp: 1000.000, #K
            a1: 0.00000000E+00,  
            a2: 0.00000000E+00,
            a3: 0.02500000E+02,
            a4: 0.00000000E+00,
            a5: 0.00000000E+00,
            a6: 0.00000000E+00,
            a7: 0.00000000E+00
        },
        nasa_2: {
            min_temp: 1000.000, #K
            max_temp: 6000.000, #K
            a1: 2.010538475E+01,     
            a2: -5.992661070E-02,
            a3: 2.500069401E+00,
            a4: -3.992141160E-08,
            a5: 1.205272140E-11,
            a6: -1.819015576E-15,
            a7: 1.078576636E-19
        }
    },
    CO2: {
        density: 0.001977, #g/cm^3
        molar_mass: 44.0095, #g/mol
        nasa_1: {
            min_temp: 200.000, #K
            max_temp: 1000.000, #K
            a1: 4.943650540E+04,      
            a2: -6.264116010E+02,
            a3: 5.301725240E+00,
            a4: 2.503813816E-03,
            a5: -2.127308728E-07,
            a6: -7.689988780E-10,
            a7: 2.849677801E-13
        },
        nasa_2: {
            min_temp: 1000.000, #K
            max_temp: 6000.000, #K
            a1: 1.176962419E+05,     
            a2: -1.788791477E+03,
            a3: 8.291523190E+00,
            a4: -9.223156780E-05,
            a5: 4.863676880E-09,
            a6: -1.891053312E-12,
            a7: 6.330036590E-16
        }
    },
    H2O: {
        density: 1.000, #g/cm^3
        molar_mass: 18.01528, #g/mol
        nasa_1: {
            min_temp: 200.000, #K
            max_temp: 1000.000, #K
            a1: -3.947960830E+04,     
            a2: 5.755731020E+02,
            a3: 9.317826530E-01,
            a4: 7.222712860E-03,
            a5: -7.342557370E-06,
            a6: 4.955043490E-09,
            a7: -1.336933246E-12
        },
        nasa_2: {
            min_temp: 1000.000, #K
            max_temp: 6000.000, #K
            a1: 1.034972096E+06,     
            a2: -2.412698562E+03,
            a3: 4.646110780E+00,
            a4: 2.291998307E-03,
            a5: -6.836830480E-07,
            a6: 9.426468930E-11,
            a7: -4.822380530E-15
        }
    }
}




            







