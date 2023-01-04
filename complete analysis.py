import sys
import os
import numpy as np
import pickle




operating_system = 'WIN'


if operating_system=='WIN':
    directory_QREM = os.environ["QREM"] +'\\'
    data_directory = 'C:\\CFT Chmura\\Theory of Quantum Computation\\QREM_Data\\ibm\\'
elif operating_system=='LIN':
    directory_QREM = '/home/fbm/PycharmProjects/QREM_SECRET_DEVELOPMENT/'
    data_directory = '/home/fbm/Nextcloud/Theory of Quantum Computation/QREM_Data/'
sys.path.append(os.path.dirname(directory_QREM))

from noise_characterization.tomography_design.overlapping.QDTMarginalsAnalyzer import QDTMarginalsAnalyzer
from functions_qrem import ancillary_functions as anf
from noise_characterization.data_analysis.InitialNoiseAnalyzer import InitialNoiseAnalyzer




results_file ='QDOT_counts_IBM_WAS_181122'


with open(data_directory+'circuits_1200_.pkl', 'rb') as filein:
    circuits = pickle.load(filein)

with open(data_directory+results_file+'.pkl', 'rb') as filein:
    results_data_dictionary = pickle.load(filein)

results_dictionary = results_data_dictionary['results_dictionary']
metadata = results_data_dictionary['metadata']

locality=2
subset_of_qubits = []
for i in range(locality):
    subset_of_qubits += anf.get_k_local_subsets(len(metadata['physical_qubits']), i + 1)

marginals_analyzer = QDTMarginalsAnalyzer(results_dictionary,experiment_name='QDT''')
print('Calculation starts')
marginals_analyzer.compute_all_marginals(subset_of_qubits,show_progress_bar=True,multiprocessing=True)

marginals_dictionary = marginals_analyzer.marginals_dictionary

print('done')

dictionary_to_save = {'metadata':metadata,
                     'marginals_dictionary':marginals_dictionary}


file_name_marginals = 'QDOT_marginals_IBM_WAS_181122'


anf.save_results_pickle(dictionary_to_save=dictionary_to_save,
                                directory=data_directory,
                                custom_name=file_name_marginals)

marginals_analyzer = QDTMarginalsAnalyzer(results_dictionary,experiment_name='QDT',marginals_dictionary=marginals_dictionary)

#calculate reduced POVMs
marginals_analyzer.compute_subsets_POVMs_averaged(subset_of_qubits,
                                                           show_progress_bar=True,
                                                           estimation_method='PLS')
POVMs_dictionary = marginals_analyzer._POVM_dictionary

dictionary_to_save = {'metadata':metadata,
                     'POVMs_dictionary':POVMs_dictionary}


file_name_POVMs  = 'QDOT_POVMs_PLS_IBM_WAS_181122'

noise_analyzer = InitialNoiseAnalyzer(results_dictionary,
                                      marginals_dictionary=marginals_dictionary,
                                      POVM_dictionary=POVMs_dictionary
                                              )

anf.save_results_pickle(dictionary_to_save=dictionary_to_save,
                                directory=data_directory,
                                custom_name=file_name_POVMs)

#Specify what qubits are of interest to you (here default is all of them)
qubit_indices = list(range(len(metadata['physical_qubits'])))

#Specify what types of distances you want to calculate
distances_types_correlations = [('worst_case', 'classical'),
                   ('average_case', 'classical')
                  ,('worst_case', 'quantum'),
                  ('average_case', 'quantum')]
#Tell analyzer how to interpret labels of circuits. For now we can only use Pauli overcomplete basis.
noise_analyzer.compute_correlations_data_pairs(qubit_indices=range(len(metadata['physical_qubits'])),
                                              distances_types=distances_types_correlations)

correlations_data = noise_analyzer.correlations_data

dictionary_to_save = {'correlations_data':correlations_data,
                      'metadata':metadata
                     }

file_name_errors  = 'QDOT_correlations_PLS_IBM_WAS_181122'
anf.save_results_pickle(dictionary_to_save=dictionary_to_save,
                                directory=data_directory,
                                custom_name=file_name_errors)
