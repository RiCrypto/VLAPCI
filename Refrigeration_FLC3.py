#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 29 19:05:47 2019


==================================
The Refrigeration Problem
==================================

 Note: This method computes everything by hand, step by step. For most people,
 the new API for fuzzy systems will be preferable. The same problem is solved
 with the new API `in this example <./plot_refrigeration_problem_newapi.html>`_.

The 'refrigeration problem' is commonly used to illustrate the power of fuzzy logic
principles to generate complex behavior from a compact, intuitive set of
expert rules.

Input variables
---------------

PID - 

Output variable
---------------

The output variable is simply the tip amount, in percentage points:

* ``tip`` : Percent of bill to add as tip


For the purposes of discussion, let's say we need 'high', 'medium', and 'low'
membership functions for both input variables and our output variable. These
are defined in scikit-fuzzy as follows

"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

#'poor' == 'NL'
#'average' == 'ZR'
#'good' == 'PL'

ErroTev = ctrl.Antecedent(np.arange(0 , 11 , 1),'ErroTev')
DeltaErroTev = ctrl.Antecedent(np.arange(0 , 11 , 1), 'DeltaErroTev')
Compressor  = ctrl.Consequent(np.arange(0, 100 , 1), 'Compressor')

ErroTev.automf(3)
DeltaErroTev.automf(3)


ErroTev['NL'] = fuzz.trimf(ErroTev.universe, [0 , 1 , 2])
#ErroTev['NM'] = fuzz.trimf(ErroTev.universe, [-1.5 , -1 , -0.7])
#ErroTev['NS'] = fuzz.trimf(ErroTev.universe, [-1 , -0.7 , 0])
ErroTev['ZR'] = fuzz.trimf(ErroTev.universe, [1 , 2 , 3])
#ErroTev['PS'] = fuzz.trimf(ErroTev.universe, [0 , 0.7 , 1.5])
#ErroTev['PM'] = fuzz.trimf(ErroTev.universe, [0.7 , 1 , 2])
ErroTev['PL'] = fuzz.trimf(ErroTev.universe, [2 , 3 , 4])

DeltaErroTev['NL'] = fuzz.trimf(DeltaErroTev.universe, [0 , 0.2 , 0.4])
#DeltaErroTev['NM'] = fuzz.trimf(DeltaErroTev.universe, [-0.5 , -1 , 0.7])
#DeltaErroTev['NS'] = fuzz.trimf(DeltaErroTev.universe, [-1 , 0.75 , 0])
DeltaErroTev['ZR'] = fuzz.trimf(DeltaErroTev.universe, [0.2 , 0.4 , 0.6])
#DeltaErroTev['PS'] = fuzz.trimf(DeltaErroTev.universe, [0 , 0.5 , 0.7])
#DeltaErroTev['PM'] = fuzz.trimf(DeltaErroTev.universe, [0.2 , 0.7 , 1])
DeltaErroTev['PL'] = fuzz.trimf(DeltaErroTev.universe, [0.4 , 0.6 , 1])

Compressor['low'] = fuzz.trimf(Compressor.universe, [63 , 64 , 65])
#Compressor['NM'] = fuzz.trimf(Compressor.universe, [63.2 , 65.5 , 63.7])
#Compressor['NS'] = fuzz.trimf(Compressor.universe, [63.5 , 63.7 , 64])
Compressor['medium'] = fuzz.trimf(Compressor.universe, [64 , 65 , 66])
#Compressor['PS'] = fuzz.trimf(Compressor.universe, [64 , 68.5 , 73])
#Compressor['PM'] = fuzz.trimf(Compressor.universe, [68.5 , 77.25 , 88])
Compressor['high'] = fuzz.trimf(Compressor.universe, [65 , 75 , 93])

ErroTev['ZR'].view()

DeltaErroTev.view()

Compressor.view()


rule1 = ctrl.Rule(ErroTev['NL'] | DeltaErroTev['NL'],Compressor['low'])

#rule2 = ctrl.Rule(ErroTev['NM'] | DeltaErroTev['NM'],Compressor['NL'])

#rule3 = ctrl.Rule(ErroTev['NS'] | DeltaErroTev['NS'],Compressor['NL'])

rule2 = ctrl.Rule(ErroTev['ZR'] | DeltaErroTev['ZR'],Compressor['medium'])

#rule5 = ctrl.Rule(ErroTev['PS'] | DeltaErroTev['PS'],Compressor['PS'])

#rule6 = ctrl.Rule(ErroTev['PM'] | DeltaErroTev['PM'],Compressor['PM'])

rule3 = ctrl.Rule(ErroTev['PL'] | DeltaErroTev['PL'],Compressor['high'])

#rule8 = ctrl.Rule(ErroTev['NL'] | DeltaErroTev['NL'],Compressor['NL'])

rule1.view()

Compressor_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])

Compressorout = ctrl.ControlSystemSimulation(Compressor_ctrl)

Compressor_ctrl.input['ErroTev'] = 1
Compressor_ctrl.input['DeltaErroTev'] = 1.5

Compressorout.compute()

"""
Once computed, we can view the result as well as visualize it.
"""
print (Compressorout.output['Compressor'])
Compressor.view(sim=Compressorout)