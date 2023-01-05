import sys
import os
import numpy as np
import pickle


operating_system = 'LIN'

if operating_system=='WIN':
    directory_QREM = os.environ["QREM"] +'\\'
    data_directory = 'C:\\CFT Chmura\\Theory of Quantum Computation\\QREM_Data'
elif operating_system=='LIN':
    directory_QREM = '/home/fbm/PycharmProjects/QREM_SECRET_DEVELOPMENT/'
    data_directory = '/home/fbm/Nextcloud/Theory of Quantum Computation/QREM_Data/ibm/'
sys.path.append(os.path.dirname(directory_QREM))

number_of_qubits=109
locality=2


def estimation_precision(number_of_outcomes,number_of_samples):
    return np.sqrt((np.log(2**number_of_outcomes-2) +np.log(2/3))/(2*number_of_samples))

from functions_qrem import ancillary_functions as anf

def TVD(p,q):
    res =0.
    for p1,q1 in zip(p,q):
        res+=0.5*np.abs(p1-q1)
    return(res)

def Overlap(s1,s2):
    if s1==s2:
        return 1
    elif (s1=='2' and s2=='3') or (s2=='2' and s1=='3') or (s1=='4' and s2 =='5') or (s2=='4' and s1 =='5'):
        return 0
    else:
        return 0.5
def compute_indicator_normalization(dim,setting1,setting2,overlap_dic):
    return dim*np.sqrt((2*(1- overlap_dic[setting1[1]+setting2[1]]*overlap_dic[setting1[0]+setting2[0]])))


settings_list = ['2','3','4','5']
overlap_dictionary={}
for i in settings_list:
    for j in settings_list:
        overlap_dictionary[i+j] = Overlap(i,j)



results_file = 'QDOT_marginals_IBM_WAS_281122.pkl'

setting_dictionary={}
normalisation_dictionary={}
for i in range(2,6):
    for j in range(2,6):
        setting_dictionary[str(i)+str(j)]=np.array([0.,0.,0.,0.])
        normalisation_dictionary[str(i)+str(j)]=0




subsets= anf.get_k_local_subsets(number_of_qubits,locality)

with open(data_directory+results_file, 'rb') as filein:
    results_data_dictionary = pickle.load(filein)

marginals_dictionary = results_data_dictionary['marginals_dictionary']
measurement_settings=marginals_dictionary.keys()







coherent_experiment={}
for subset in subsets:
   setting_dictionary = setting_dictionary.fromkeys(setting_dictionary,[0.,0.,0.,0.])
   normalisation_dictionary = normalisation_dictionary.fromkeys(normalisation_dictionary,0)
   for setting in measurement_settings:
       s1 = setting[subset[0]]
       s2 = setting[subset[1]]
       if s1 != '0' and s1 != '1' and s2 != '0' and s2 != '1':
           setting_dictionary[s1 + s2] += marginals_dictionary[setting][subset]
           normalisation_dictionary[s1 + s2] += 1

   coherent_experiment[subset] = [setting_dictionary,normalisation_dictionary]



settings_list=[]
for i in range(2,6):
    for j in range(2,6):
        settings_list.append(str(i)+str(j))
tvd_dic ={}

for keys, elements in coherent_experiment.items():
    tvd_value=[]
    tvd_settings=[]

    for i in range(len(settings_list)):
        for j in range(i+1,len(settings_list)):
            s1=settings_list[i]
            s2=settings_list[j]

            #A proper probability vector is obtained here by normalization, we check wheter a particualr combination of Pauli preparations appeared in the experimental data
            if elements[1][s1]!=0 and elements[1][s2]!=0:
                indicator = TVD(elements[0][s1] / elements[1][s1], elements[0][s2] / elements[1][s2])
                indicator = indicator / (compute_indicator_normalization(2, s1, s2, overlap_dictionary))
                tvd_value.append(indicator)
                tvd_settings.append((settings_list[i],elements[1][s1],estimation_precision(4,10**4*elements[1][s1]),settings_list[j],elements[1][s2],estimation_precision(4,10**4*elements[1][s2])))


    tvd_dic[keys]=[tvd_value,tvd_settings]

max_list =[]
max_setting=[]
sub=[]
for key, results in tvd_dic.items():
    max_value=max(results[0])
    max_index=results[0].index(max_value)
    max_list.append(max_value)
    max_setting.append(results[1][max_index])
    sub.append(key)

max_el =max(max_list)
max_id=max_list.index(max_el)
print(max(max_list))
print(max_setting[max_id])
print(sub[max_id])

file_to_save= "coherence_indicator_IBM_WAS_281122.pkl"
anf.save_results_pickle(dictionary_to_save=tvd_dic,
                           directory=data_directory,
                           custom_name=file_to_save)