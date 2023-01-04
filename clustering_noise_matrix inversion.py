import sys
import os
import numpy as np
import pickle

operating_system = 'WIN'

if operating_system == 'WIN':
    directory_QREM = os.environ["QREM"] + '\\'
    data_directory = 'C:\\CFT Chmura\\Theory of Quantum Computation\\QREM_Data\\ibm\\'
elif operating_system == 'LIN':
    directory_QREM = '/home/fbm/PycharmProjects/QREM_SECRET_DEVELOPMENT/'
    data_directory = '/home/fbm/Nextcloud/Theory of Quantum Computation/QREM_Data/'
sys.path.append(os.path.dirname(directory_QREM))

from noise_characterization.tomography_design.overlapping.QDTMarginalsAnalyzer import QDTMarginalsAnalyzer
from functions_qrem import ancillary_functions as anf

from noise_characterization.tomography_design.overlapping.QDTMarginalsAnalyzer import \
    QDTMarginalsAnalyzer

from noise_model_generation.CN.NoiseModelGenerator import NoiseModelGenerator

from functions_qrem import functions_data_analysis as fda

# Specify directory where results are saved
""" 
Uncomment and specify to read data

number_of_qubits = 

directory_results = ""

file_name_results  = ""


#read saved results
with open(directory_results + file_name_results+'.pkl', 'rb') as filein:
    results_data_dictionary = pickle.load(filein)

results_dictionary = results_data_dictionary['results_dictionary']
metadata = results_data_dictionary['metadata']




file_name_marginals  = ""
#read saved results
with open(directory_results + file_name_marginals+'.pkl', 'rb') as filein:
    marginals_dictionary_data = pickle.load(filein)

marginals_dictionary = marginals_dictionary_data['marginals_dictionary']


file_name_POVMs  = ""
with open(directory_results + file_name_POVMs+'.pkl', 'rb') as filein:
    POVMs_dictionary_data = pickle.load(filein)

if "noise_matrices_dictionary" in POVMs_dictionary_data:
    noise_matrices_dictionary = POVMs_dictionary_data['noise_matrices_dictionary']
else:
    POVMs_dictionary = POVMs_dictionary_data['POVMs_dictionary']
    noise_matrices_dictionary = fda.get_noise_matrices_from_POVMs_dictionary(POVMs_dictionary)


file_name_errors  = ""


#read saved results
with open(directory_results + file_name_errors+'.pkl', 'rb') as filein:
    errors_data_dictionary = pickle.load(filein)

errors_data = errors_data_dictionary['errors_data']
coherence_data = errors_data_dictionary['coherence_data']
correlations_data = errors_data_dictionary['correlations_data']

metadata = errors_data_dictionary['metadata']

"""

noise_model_analyzer = NoiseModelGenerator(results_dictionary=results_dictionary,
                                           marginals_dictionary=marginals_dictionary,
                                           noise_matrices_dictionary=noise_matrices_dictionary,
                                           correlations_data=correlations_data
                                           )

marginals_analyzer = QDTMarginalsAnalyzer(results_dictionary=results_dictionary, experiment_name='QDOT')

sizes_clusters = [2, 3, 4, 5]

distance_type = 'worst_case'
correlations_type = 'classical'
correlations_table = correlations_data[distance_type][correlations_type]

alpha_hyperparameters = np.linspace(0.0, 3.0, 16)
alpha_hyperparameters = [np.round(alpha, 3) for alpha in alpha_hyperparameters]

all_clusters_sets_dictionary = {}

for max_cluster_size in sizes_clusters:
    anf.cool_print("\nCurrent max cluster size:", max_cluster_size, 'red')

    for alpha_multiplier in alpha_hyperparameters:
        clustering_function_arguments = {'alpha_multiplier': alpha_multiplier}

        clusters_tuples_now, score = noise_model_analyzer.compute_clusters(correlations_table=correlations_table,
                                                                           maximal_size=max_cluster_size,
                                                                           method_kwargs=clustering_function_arguments)
        if clusters_tuples_now in all_clusters_sets_dictionary.keys():
            all_clusters_sets_dictionary[clusters_tuples_now].append(
                (max_cluster_size, clustering_function_arguments['alpha_multiplier'], score))
        else:
            all_clusters_sets_dictionary[clusters_tuples_now] = [
                (max_cluster_size, clustering_function_arguments['alpha_multiplier'], score)]

all_clusters_sets_list = list(all_clusters_sets_dictionary.keys())

# print(results_dictionary)
cluster_subsets = []

for cluster_list in all_clusters_sets_list:
    for cluster in cluster_list:
        if cluster not in cluster_subsets:
            cluster_subsets.append(cluster)

# Calculate chosen marginals
marginals_analyzer.compute_all_marginals(cluster_subsets,
                                         show_progress_bar=True,
                                         multiprocessing=False)

marginals_dictionary_clusters = marginals_analyzer.marginals_dictionary

marginals_analyzer.compute_subsets_POVMs_averaged(subsets_list=cluster_subsets,
                                                  show_progress_bar=True,
                                                  estimation_method='PLS')

marginals_analyzer.compute_noise_matrices_from_POVMs(subsets_list=cluster_subsets,
                                                     show_progress_bar=True)

noise_matrices_dictionary = marginals_analyzer.noise_matrices_dictionary

dictionary_to_save = {'noise_matrices_dictionary': noise_matrices_dictionary,
                      'all_clusters_sets_dictionary': all_clusters_sets_dictionary
                      }

"""
Uncomment to save data 


directory_results_noise_models = ""
file_name_noise_models  = ""

anf.save_results_pickle(dictionary_to_save=dictionary_to_save,
                                directory=directory_results_noise_models,
                                custom_name=file_name_noise_models)


"""
pairs_of_qubits = [(i, j) for i in range(number_of_qubits) for j in range(i + 1, number_of_qubits)]

correction_matrices, correction_indices = fda.get_multiple_mitigation_strategies_clusters_for_pairs_of_qubits(
    pairs_of_qubits=pairs_of_qubits,
    clusters_sets=all_clusters_sets_dictionary,
    dictionary_results=results_dictionary,
    noise_matrices_dictionary=noise_matrices_dictionary,
    show_progress_bar=True)

dictionary_to_save = {'metadata': metadata,
                      'correction_matrices': correction_matrices,
                      'correction_indices': correction_indices,
                      'all_clusters_sets_dictionary': all_clusters_sets_dictionary
                      }

"""
Uncomment to save data 
file_name_mitigation  = ""

anf.save_results_pickle(dictionary_to_save=dictionary_to_save,
                                directory= directory_results,
                                custom_name=file_name_mitigation)

"""