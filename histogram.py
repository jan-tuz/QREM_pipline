import sys
import os
import numpy as np
import matplotlib.pyplot as plt

directory_QREM = '/home/fbm/PycharmProjects/QREM_SECRET_DEVELOPMENT/'
results_file ='/home/fbm/0_Research/Projects/QREM_SECRET/Tutorials/data_storage/experimental_results/ibm_washington/QDOT/2022_04_26/number_of_qubits_109/shots_10000/QDOT_counts_no_0.pkl'
errors_file ='/home/fbm/0_Research/Projects/QREM_SECRET/Tutorials/data_storage/ibm/QDT_errors_data_POVMs-PLS_no_0.pkl'
marginals_file ='/home/fbm/0_Research/Projects/QREM_SECRET/Tutorials/data_storage/ibm/QDT_marginals3_no_0_IBM260422.pkl'
directory_to_save='/home/fbm/0_Research/Projects/QREM_SECRET/Tutorials/data_storage/ibm/'
sys.path.append(os.path.dirname(directory_QREM))
import pickle
def histogram_data(results_dictionary, distance_type,correlation_type):
    return results_dictionary[distance_type][correlation_type].flatten('F')

with open(errors_file, 'rb') as filein:
    results_data_dictionary = pickle.load(filein)

results_dictionary = results_data_dictionary['correlations_data']
wc_classical=histogram_data(results_dictionary,'worst_case','classical')
wc_quantum=histogram_data(results_dictionary,'worst_case','quantum')
ac_classical= histogram_data(results_dictionary,'average_case','classical')
ac_quantum=histogram_data(results_dictionary,'average_case','quantum')
print('start')
plt.hist(ac_quantum,range=(0.01,0.4))
plt.hist(ac_classical,range=(0.01,0.4))
plt.title("Classical correlation coefficients averadge case distance")

plt.show()
print('finish')