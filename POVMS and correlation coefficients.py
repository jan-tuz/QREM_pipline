import sys
import os
directory_QREM = '/home/fbm/PycharmProjects/QREM_SECRET_DEVELOPMENT/'
results_file ='/home/fbm/0_Research/Projects/QREM_SECRET/Tutorials/data_storage/experimental_results/ibm_washington/QDOT/2022_04_26/number_of_qubits_109/shots_10000/QDOT_counts_no_0.pkl'

marginals_file ='/home/fbm/0_Research/Projects/QREM_SECRET/Tutorials/data_storage/ibm/QDT_marginals3_no_0_IBM260422.pkl'
directory_to_save='/home/fbm/0_Research/Projects/QREM_SECRET/Tutorials/data_storage/ibm/'
sys.path.append(os.path.dirname(directory_QREM))
import pickle
from noise_characterization.data_analysis.InitialNoiseAnalyzer import InitialNoiseAnalyzer

from noise_characterization.tomography_design.overlapping.DOTMarginalsAnalyzer import DOTMarginalsAnalyzer
from noise_characterization.tomography_design.overlapping.QDTMarginalsAnalyzer import QDTMarginalsAnalyzer
from functions_qrem import ancillary_functions as anf

experiment_name='QDT'
collection_index =0
number_of_qubits=109
locality =2

with open(results_file, 'rb') as filein:
    results_data_dictionary = pickle.load(filein)

results_dictionary = results_data_dictionary['results_dictionary']
metadata = results_data_dictionary['metadata']


with open(marginals_file, 'rb') as filein:
  marginals_data_dictionary = pickle.load(filein)

marginals_dictionary = marginals_data_dictionary['marginals_dictionary']
metadata = marginals_data_dictionary['metadata']
marginals_analyzer = QDTMarginalsAnalyzer(results_dictionary,experiment_name=experiment_name,marginals_dictionary=marginals_dictionary)

#Tell analyzer how to interpret labels of circuits. For now we can only use Pauli overcomplete basis.
marginals_analyzer.initialize_labels_interpreter(interpreter='PAULI')
#Choose method for estimating POVMs
estimation_method = 'PLS'


subset_of_qubits=anf.get_k_local_subsets(number_of_qubits,locality)

#calculate reduced POVMs
marginals_analyzer.compute_subsets_POVMs_averaged(subset_of_qubits,
                                                           show_progress_bar=True,
                                                           estimation_method=estimation_method)
POVMs_dictionary = marginals_analyzer._POVM_dictionary

noise_analyzer = InitialNoiseAnalyzer(results_dictionary,
                                      marginals_dictionary=marginals_dictionary,
                                      POVM_dictionary=POVMs_dictionary
                                              )

#Specify what qubits are of interest to you (here default is all of them)
qubit_indices = list(range(number_of_qubits))

#Specify what types of distances you want to calculate
distances_types_correlations = [('worst_case', 'classical'),
                   ('average_case', 'classical')
                  ,('worst_case', 'quantum'),
                  ('average_case', 'quantum')]
#Tell analyzer how to interpret labels of circuits. For now we can only use Pauli overcomplete basis.
noise_analyzer.compute_correlations_data_pairs(qubit_indices=range(number_of_qubits),
                                              distances_types=distances_types_correlations)

correlations_data = noise_analyzer.correlations_data

dictionary_to_save = {'correlations_data':correlations_data,
                      'metadata':metadata
                     }

file_name_errors  = f"{experiment_name}_errors_data_POVMs-{estimation_method}_no_{collection_index}"
anf.save_results_pickle(dictionary_to_save=dictionary_to_save,
                                directory=directory_to_save,
                                custom_name=file_name_errors)