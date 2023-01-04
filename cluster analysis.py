import sys
import os
import pickle
import numpy as np
import matplotlib.pyplot as plt


operating_system = 'WIN'

if operating_system=='WIN':
    directory_QREM = os.environ["QREM"] +'\\'
    data_directory = 'C:\\CFT Chmura\\Theory of Quantum Computation\\QREM_Data\\ibm\\'
elif operating_system=='LIN':
    directory_QREM = '/home/fbm/PycharmProjects/QREM_SECRET_DEVELOPMENT/'
    data_directory = '/home/fbm/Nextcloud/Theory of Quantum Computation/QREM_Data/'
sys.path.append(os.path.dirname(directory_QREM))
from functions_qrem import ancillary_functions as anf
#results_file ='QDOT_counts_no_0.pkl'
correlations_file ='QDOT_correlations_PLS_IBM_WAS_181122.pkl'
marginals_file ='QDOT_marginals_IBM_WAS_181122.pkl'
povms_file = 'QDOT_POVMs_PLS_IBM_WAS_181122.pkl'
clusters_file = 'QDOT_clusters_IBM_WAS_181122'

with open(clusters_file, 'rb') as filein:
    results_dictionary = pickle.load(filein)

clusters_dictionary=results_dictionary['']