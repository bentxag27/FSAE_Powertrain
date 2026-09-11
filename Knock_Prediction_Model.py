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

        for i in range(len(Pcad_run)):

            IDT_de = douaund_eyzat(ON, Pcad_run[i], Tcad_run[i])
            IDT_h = hoepke(Xegr=0, Pcad_run[i], Tcad_run[i])
            IDT_cz = chen_zheng(lmnbda, Xegr, Pcad_run[i], Tcad_run[i])

             
            I_de += (1/(6*rpm))*(1/TDI)

            #penis 
             

            #FUCK THIS SOFTWARE

            







