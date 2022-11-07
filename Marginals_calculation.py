

import sys
import os
directory_QREM = '/home/fbm/PycharmProjects/QREM_SECRET_DEVELOPMENT/'
results_file ='/home/fbm/0_Research/Projects/QREM_SECRET/Tutorials/data_storage/experimental_results/ibm_washington/QDOT/2022_04_26/number_of_qubits_109/shots_10000/QDOT_counts_no_0.pkl'
directory_to_save='/home/fbm/0_Research/Projects/QREM_SECRET/Tutorials/data_storage/ibm/'
sys.path.append(os.path.dirname(directory_QREM))
import pickle

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

subset_of_qubits=[]
for i in range(locality):
    subset_of_qubits += anf.get_k_local_subsets(number_of_qubits,i+1)


marginals_analyzer = QDTMarginalsAnalyzer(results_dictionary,experiment_name=experiment_name)
print('Calculation starts')
marginals_analyzer.compute_all_marginals(subset_of_qubits,show_progress_bar=True,multiprocessing=True)

marginals_dictionary = marginals_analyzer.marginals_dictionary

print('done')

dictionary_to_save = {'metadata':metadata,
                     'marginals_dictionary':marginals_dictionary}


file_name_marginals  = f"{experiment_name}_marginals3_no_{collection_index}_IBM260422"


anf.save_results_pickle(dictionary_to_save=dictionary_to_save,
                                directory=directory_to_save,
                                custom_name=file_name_marginals)
