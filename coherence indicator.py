import sys
import os
import numpy as np
import itertools
import pickle
directory_QREM = '/home/fbm/PycharmProjects/QREM_SECRET_DEVELOPMENT/'
data_directory='/home/fbm/Nextcloud/Theory of Quantum Computation/QREM_Data/'

sys.path.append(os.path.dirname(directory_QREM))
from functions_qrem import ancillary_functions as anf


def TVD(p,q):
    res =0.
    for p1,q1 in zip(p,q):
        res+=np.abs(p1-q1)
    return(res)
#results_file = '/home/fbm/0_Research/Projects/QREM_SECRET/Tutorials/data_storage/ibm/QDT_marginals3_no_0_IBM260422.pkl'




#setting_dictionary={}
#normalisation_dictionary={}
#for i in range(2,6):
#    for j in range(2,6):
#        setting_dictionary[str(i)+str(j)]=np.array([0.,0.,0.,0.])
#      normalisation_dictionary[str(i)+str(j)]=0





#subsets= anf.get_k_local_subsets(109,2)
#marginals_dictionary = results_data_dictionary['marginals_dictionary']
#measurement_settings=marginals_dictionary.keys()







#coherent_experiment={}
#for subset in subsets:
#   setting_dictionary = setting_dictionary.fromkeys(setting_dictionary,[0.,0.,0.,0.])
#   normalisation_dictionary = normalisation_dictionary.fromkeys(normalisation_dictionary,0)
#   for setting in measurement_settings:
#       s1 = setting[subset[0]]
#       s2 = setting[subset[1]]
#       if s1 != '0' and s1 != '1' and s2 != '0' and s2 != '1':
#           setting_dictionary[s1 + s2] += marginals_dictionary[setting][subset]
#           normalisation_dictionary[s1 + s2] += 1

 #  coherent_experiment[subset] = [setting_dictionary,normalisation_dictionary]
 #  print(subset)


#   anf.save_results_pickle(dictionary_to_save=coherent_experiment,
#                           directory=directory_to_save,
#                           custom_name=file_name)

file_name= "cohernce_indicators_IBM260422.pkl"


settings_list=[]
for i in range(2,6):
    for j in range(2,6):
        settings_list.append(str(i)+str(j))
tvd_dic ={}
with open(data_directory + file_name, 'rb') as filein:
    results_data_dictionary = pickle.load(filein)
for keys, elements in results_data_dictionary.items():
    tvd_value=[]
    tvd_settings=[]

    for i in range(len(settings_list)):
        for j in range(i+1,len(settings_list)):
            tvd_value.append(TVD(elements[0][settings_list[i]]/elements[1][settings_list[i]],elements[0][settings_list[j]]/elements[1][settings_list[j]]))
            tvd_settings.append((settings_list[i],settings_list[j]))
    tvd_dic[keys]=[tvd_value,tvd_settings]

max_list =[]
max_setting=[]
for results in tvd_dic.values():
    max_value=max(results[0])
    max_index=results[0].index(max_value)
    max_list.append(max_value)
    max_setting.append(results[1][max_index])

max_el =max(max_list)
max_id=max_list.index(max_el)
print(max(max_list))
print(max_setting[max_id])

file_to_save= "cohernce_tvd_IBM260422.pkl"
anf.save_results_pickle(dictionary_to_save=tvd_dic,
                           directory=data_directory,
                           custom_name=file_to_save)