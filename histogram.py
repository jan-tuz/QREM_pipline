import sys
import os
import numpy as np
import matplotlib.pyplot as plt


operating_system = 'WIN'

if operating_system=='WIN':
    directory_QREM = os.environ["QREM"] +'\\'
    data_directory = 'C:\\CFT Chmura\\Theory of Quantum Computation\\QREM_Data\\'
elif operating_system=='LIN':
    directory_QREM = '/home/fbm/PycharmProjects/QREM_SECRET_DEVELOPMENT/'
    data_directory = '/home/fbm/Nextcloud/Theory of Quantum Computation/QREM_Data/'
sys.path.append(os.path.dirname(directory_QREM))

results_file ='QDOT_counts_no_0.pkl'
errors_file ='QDT_errors_data_POVMs-PLS_no_0.pkl'
marginals_file ='QDT_marginals3_no_0_IBM260422.pkl'
coherence_indicator_file="coherence_indicator_IBM260422.pkl"
file=coherence_indicator_file

sys.path.append(os.path.dirname(directory_QREM))
import pickle
def histogram_data(results_dictionary, distance_type,correlation_type):
    return results_dictionary[distance_type][correlation_type].flatten('F')

with open(data_directory+file, 'rb') as filein:
    results_data_dictionary = pickle.load(filein)

#results_dictionary = results_data_dictionary['correlations_data']
#wc_classical=histogram_data(results_dictionary,'worst_case','classical')
#wc_quantum=histogram_data(results_dictionary,'worst_case','quantum')
#ac_classical= histogram_data(results_dictionary,'average_case','classical')
#ac_quantum=histogram_data(results_dictionary,'average_case','quantum')
#print('start')
#plt.hist(ac_quantum,range=(0.01,0.4))
#plt.hist(ac_classical,range=(0.01,0.4))
#plt.title("Classical correlation coefficients averadge case distance")

#plt.show()
#print('finish')

coherence_indicator_list = []
for tvd_list in results_data_dictionary.values():
    for element in tvd_list[0]:
        coherence_indicator_list.append(element)
plt.hist(coherence_indicator_list,range=(0.04,0.06),bins=40)
plt.title("POVM coherence indicator")
plt.show()