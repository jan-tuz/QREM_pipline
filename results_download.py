import os
import sys
from qiskit import IBMQ
directory_QREM = os.environ["QREM"] +'\\'
sys.path.append(os.path.dirname(directory_QREM))
import pickle
from backends_support.qiskit import qiskit_utilities
from functions_qrem import functions_data_analysis as fdt, ancillary_functions as anf
from functions_qrem import functions_standarized_directories as dirs


TOKEN='da57aaf4ec4f5d02d587005829816907c93785cfd5686ed380ecadcc2fbfed3cb774837318516fb7099f3806a33ea3292112273254d3d1879768bddfe265d746'

IBMQ.load_account()
IBMQ.providers()



provider_data ={'IBMQ_HUB': 'ibm-q-psnc', 'IBMQ_GROUP': 'internal' , 'IBMQ_PROJECT': 'default' }

data_directory = 'C:\\CFT Chmura\\Theory of Quantum Computation\\QREM_Data\\ibm\\'
file_name_jobs='circuits_1200'

with open(data_directory + file_name_jobs+'.pkl', 'rb') as filein:
    dictionary_data_jobs = pickle.load(filein)
job_IDs_list = dictionary_data_jobs['job_IDs_list']


jobs_downloaded =qiskit_utilities.download_multiple_jobs(backend_name = 'ibm_washington',
                                                         job_IDs_list=dictionary_data_jobs['job_IDs_list'],
                                                         provider_data={'IBMQ_HUB': 'ibm-q-psnc', 'IBMQ_GROUP': 'internal' , 'IBMQ_PROJECT': 'default' })

unprocessed_results = qiskit_utilities.get_counts_from_jobs(jobs_list=jobs_downloaded)


#We will now convert results of experiments to universal format we use in QREM to process data
processed_results = fdt.convert_counts_overlapping_tomography(counts_dictionary=unprocessed_results,
                                                              experiment_name='QDOT',
                                                              reverse_bitstrings=True)

dictionary_to_save_results = {'results_dictionary': processed_results,
                     'metadata':dictionary_data_jobs['metadata']}

anf.save_results_pickle(dictionary_to_save=dictionary_to_save_results,
                                        directory=data_directory,
                                        custom_name='QDOT_counts_IBM_WAS_181122'
                                        )