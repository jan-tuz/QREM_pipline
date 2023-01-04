import sys
import os
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
#coherence_indicator_file="coherence_indicator_IBM260422.pkl"
file=correlations_file



sys.path.append(os.path.dirname(directory_QREM))
import pickle

def data_array(results_dictionary, distance_type,correlation_type):
    return results_dictionary[distance_type][correlation_type]

def histogram_data(results_dictionary, distance_type,correlation_type):
    return results_dictionary[distance_type][correlation_type].flatten('F')

with open(data_directory+file, 'rb') as filein:
    results_data_dictionary = pickle.load(filein)

results_dictionary = results_data_dictionary['correlations_data']
wc_classical=data_array(results_dictionary,'worst_case','classical')
print('WC classical correlations max:', np.max(wc_classical))
print(np.unravel_index(np.argmax(wc_classical, axis=None), wc_classical.shape))
wc_quantum=histogram_data(results_dictionary,'worst_case','quantum')
print('WC quantum correlations max:', np.max(wc_quantum))

ac_classical=data_array(results_dictionary,'average_case','classical')
print('AC classical correlations max:', np.max(ac_classical))
print(np.unravel_index(np.argmax(ac_classical, axis=None), ac_classical.shape))
ac_quantum=histogram_data(results_dictionary,'average_case','quantum')
print('AC quantum correlations max:', np.max(ac_quantum))


for i in range(109):
    for j in range(109):
        if wc_classical[i,j]<ac_classical[i,j]:
            print(i,j)

with open(data_directory+povms_file, 'rb') as filein:
    povms_full_dictionary = pickle.load(filein)

povms_dictionary = povms_full_dictionary['POVMs_dictionary']

povm=povms_dictionary[(93,98)]

povm_sum=povm[0]*0.0
for effect in povm:
    anf.print_array_nicely(effect, 5)
    povm_sum+=effect
print('sum')
anf.print_array_nicely(povm_sum, 5)

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

#coherence_indicator_list = []
#for tvd_list in results_data_dictionary.values():
#    for element in tvd_list[0]:
#        coherence_indicator_list.append(element)
#plt.hist(coherence_indicator_list,range=(0.04,0.06),bins=40)
#plt.title("POVM coherence indicator")
#plt.show()