import sys
import os

operating_system = 'WIN'

if operating_system == 'WIN':
    directory_QREM = os.environ["QREM"] + '\\'
    data_directory = 'C:\\CFT Chmura\\Theory of Quantum Computation\\QREM_Data\\ibm\\'
elif operating_system == 'LIN':
    directory_QREM = '/home/fbm/PycharmProjects/QREM_SECRET_DEVELOPMENT/'
    data_directory = '/home/fbm/Nextcloud/Theory of Quantum Computation/QREM_Data/'
sys.path.append(os.path.dirname(directory_QREM))sys.path.append(os.path.dirname(directory_QREM))
import pickle

from functions_qrem import functions_data_analysis as fdt


from functions_qrem import functions_benchmarks as fun_ben

data_directory = '' #insert directory to data 'C:\\CFT Chmura\\Theory of Quantum Computation\\QREM_Data\\'

file_name_results = '' #insert name of a file with full DDOT results 'DDOT_counts_IBM_WAS_281122'

file_name_marginals = ''#insert name of a file with marginals results'DDOT_marginals_IBM_WAS_281122'

file_name_hamiltonians = ''#insert name with hamiltonian data (if generated previously) 'hamiltonians_no_0-299'

with open(data_directory+'hamiltonians\\' + file_name_hamiltonians+'.pkl', 'rb') as filein:
    hamiltonians_data = pickle.load(filein)

#if Hamiltonians were not generated not use the code beloe

"""
number_of_qubits - number of qubits unsed in the experiments
number_of_hamiltonians - equal to number of states prepared in benchmark (DDOT) experiment
clause_density - I need to figure out this paprameter, it relates to the number of clauses but unsusre how
 
 
 hamiltonians_dictionary=fun_ben.create_hamiltonians_for_benchmarks(number_of_qubits= 5,number_of_hamiltonians=,clause_density= 4.0)

"""

directory_results_noise_models = '' #insert path do directory with clusters 'C:\\Users\\Enter\\PycharmProjects\\QREM_SECRET_DEVELOPMENT_LOC\\Tutorials\\clusters\\'
file_name_noise_models  = '' #insert name of a file with clustering results  "noise_matrices"

number_of_qubits='' #set number of qubits

with open(directory_results_noise_models + file_name_noise_models+'.pkl', 'rb') as filein:
    noise_models_dictionary = pickle.load(filein)

noise_matrices_dictionary = noise_models_dictionary['noise_matrices_dictionary']
all_clusters_sets_dictionary = noise_models_dictionary['all_clusters_sets_dictionary']


with open(data_directory+'ibm\\' + file_name_results+'.pkl', 'rb') as filein:
    results_data_dictionary = pickle.load(filein)

results_dictionary = results_data_dictionary['results_dictionary']

with open(data_directory+'ibm\\' + file_name_marginals+'.pkl', 'rb') as filein:
    marginals_dictionary_data = pickle.load(filein)

marginals_dictionary = marginals_dictionary_data['marginals_dictionary']




#this estimates energy of states created with DDOT for created hamiltonians
results_energy_estimation= fun_ben.eigenstate_energy_calculation_and_estimationy(results_dictionary,marginals_dictionary,hamiltonians_dictionary)

#



#create mitigation data

pairs_of_qubits =  [(i, j) for i in range(number_of_qubits) for j in range(i + 1, number_of_qubits)]
correction_matrices, correction_indices = fdt.get_multiple_mitigation_strategies_clusters_for_pairs_of_qubits(
                                                    pairs_of_qubits=pairs_of_qubits,
                                                    clusters_sets=all_clusters_sets_dictionary,
                                                    dictionary_results=results_dictionary,
                                                    noise_matrices_dictionary=noise_matrices_dictionary,
                                                    show_progress_bar = True)
#run benchmars, a super ugly input to be changed later
benchmarks_results=fun_ben.run_benchmarks(number_of_qubits,results_dictionary, marginals_dictionary, results_energy_estimation, hamiltonians_dictionary,all_clusters_sets_dictionary,correction_matrices, correction_indices,noise_matrices_dictionary)


#below analysis of benchmark results starts
all_tested_clusters_sets = list(benchmarks_results[0]['energies']['predicted_energies'].keys())


#the code below rewrites benchmark results into spearate dictionaries for mitigation/prediction
benchmark_results_prediction = {}
for cluster_set in all_tested_clusters_sets:
       benchmark_results_prediction[cluster_set] = {'errors_list': {
       state_index: benchmarks_results[state_index]['errors']['energy_prediction_errors'][cluster_set] for
       state_index in benchmarks_results.keys()}}


all_tested_clusters_sets = list(benchmarks_results[0]['energies']['corrected_energies'].keys())

benchmark_results_mitigation = {}
for cluster_set in all_tested_clusters_sets:
      benchmark_results_mitigation[cluster_set] = {
      'errors_list': {state_index: benchmarks_results[state_index]['errors']['corrected_errors'][cluster_set] for
      state_index in benchmarks_results.keys()}}

#division of hamiltonians into test and traning set

traning_set,test_set= fun_ben.create_traning_and_test_set(number_of_hamiltonians=300, traning_set_cardinality=200)

#here one by choosig benchmark_results_mitigation/benchmark_results_prediction one can analyze mitigation/porediction
traning_data=fun_ben.calculate_results_test_set(benchmark_results_mitigation, traning_set)
test_data=fun_ben.calculate_results_test_set(benchmark_results_mitigation, test_set)

#this creates data for plots
alpha_list, median_list_traning, mean_list_traning = fun_ben.cerate_data_alpha_plot(all_clusters_sets_dictionary,traning_data)
alpha_list, median_list_test, mean_list_test = fun_ben.cerate_data_alpha_plot(all_clusters_sets_dictionary,test_data)

#this creates plots, median_list_test[0][0] is a reference value for uncorrelated noise model, the same holds for other choices (mean_list, and test data)
fun_ben.create_plots(alpha_list,median_list_test, median_list_test[0][0],'Mitigation median (test data) IBM WAS 281122')