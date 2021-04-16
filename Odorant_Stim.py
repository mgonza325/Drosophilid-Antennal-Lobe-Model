#!/usr/bin/env python
# coding: utf-8

# In[10]:


import csv
import nengo
import numpy as np
import scipy.optimize

odour_info = list(csv.reader(open('Relative_activity_odor_stims_forcedzeros.csv')))

def hill_function(c, logEC, A_max, n):           
    EC = 10**(logEC)
    return A_max * (c**n/(c**n+EC**n))

def do_curve_fit_forced_EC(compound, receptor):
    concentrations = []
    responses = []
    
    for line in odour_info:
        if line[0] == compound: 
            index = odour_info[0].index(receptor)
            if line[index] == '':
                continue
            else:
                responses.append(float(line[index]))
                concentrations.append(float(line[1]))
            
    def hill_function_forced_EC(c, A_max, n):
        logEC = 0
        for line in odour_info:
            if line[0] == 'EC50_' + compound:
                index = odour_info[0].index(receptor)
                logEC += float(line[index])
        EC = 10**logEC
        return A_max * (c**n/(c**n+EC**n))
            
    p, _ = scipy.optimize.curve_fit(hill_function_forced_EC, concentrations, responses, maxfev=10000, 
                                    bounds=[(-10, -10), (10, 10)])
    return p

def fit_all_forced_EC(compounds, ORs):
    params = np.zeros((len(compounds), len(ORs), 3))
    for i, compound in enumerate(compounds):
        for j, receptor in enumerate(ORs):
            forced_logEC = 0
            for line in odour_info:
                if line[0] == 'EC50_' + compound:
                    index = odour_info[0].index(receptor)
                    forced_logEC += float(line[index])
            params[i,j,:] = [forced_logEC, *do_curve_fit_forced_EC(compound, receptor)]
    return params

or_list = odour_info[0][2:]
compounds = ['geranyl acetate', 'anisole', '2-heptanone', 'menthol']

params_forced_EC = fit_all_forced_EC(compounds, or_list)

def convert_compounds_to_responses(concentrations):
    responses = np.zeros(len(or_list))
    for i, compound in enumerate(compounds):
        for j, response in enumerate(or_list):
            responses[j] += hill_function(concentrations[i], *params_forced_EC[i,j])
    return responses

