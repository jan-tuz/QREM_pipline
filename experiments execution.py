from qiskit import IBMQ
import sys
import os

directory_QREM = os.environ["QREM"] +'\\'
sys.path.append(os.path.dirname(directory_QREM))

import datetime
from functions_qrem import ancillary_functions as anf
from functions_qrem import functions_standarized_directories as dirs
from noise_characterization.base_classes.OverlappingTomographyBase import OverlappingTomographyBase
import numpy as np
from noise_characterization.tomography_design.overlapping.SeparableCircuitsCreator import \
    SeparableCircuitsCreator

from backends_support.qiskit import qiskit_utilities
from functions_qrem import functions_data_analysis as fdt
from noise_characterization.tomography_design.overlapping.DOTMarginalsAnalyzer import DOTMarginalsAnalyzer

from noise_characterization.tomography_design.overlapping.QDTMarginalsAnalyzer import \
    QDTMarginalsAnalyzer

from noise_characterization.data_analysis.InitialNoiseAnalyzer import InitialNoiseAnalyzer
from noise_simulation.CN.noise_addition import  add_noise_results_dictionary
from noise_model_generation.CN.NoiseModelGenerator import NoiseModelGenerator
from functions_qrem import functions_data_analysis as fda


TOKEN='da57aaf4ec4f5d02d587005829816907c93785cfd5686ed380ecadcc2fbfed3cb774837318516fb7099f3806a33ea3292112273254d3d1879768bddfe265d746'

IBMQ.load_account()
print(IBMQ.providers())



provider_data ={'IBMQ_HUB': 'ibm-q-psnc', 'IBMQ_GROUP': 'internal' , 'IBMQ_PROJECT': 'default' }


def get_qubits_below_error_rate(backend_properties, gate_symbol, error_rate,number_of_qubits):
    x_error = []
    for i in range(number_of_qubits):
        x_error.append([i, backend_properties.gate_property(gate_symbol, [i])['gate_error'][0]])
    faulty_gates_number = 0
    qubit_ind = []
    for element in x_error:
        if element[1] >= error_rate:

            print(element)
            faulty_gates_number += 1
        else:
            qubit_ind.append(element[0])
    return qubit_ind



# Specify backend on which you wish to perform experiments
backend_name = 'ibm_washington'

psnc_provider=IBMQ.get_provider(hub='ibm-q-psnc')
backend = psnc_provider.get_backend(backend_name)
backend_properties_data=backend.properties()
qubit_indices=get_qubits_below_error_rate(backend.properties(),'x',10**(-3),127)
# Define number of qubits you wish to create DOT circuits for
number_of_qubits = len(qubit_indices)
SDK_name = 'qiskit'
#Chose expeiment type
experiment_name = 'QDOT'

if experiment_name == 'QDOT':
    number_of_symbols = 6
elif experiment_name == 'DDOT':
    number_of_symbols = 2

# Specify desired number of circuits
maximal_circuits_number = 1200

OT_creator = OverlappingTomographyBase(number_of_qubits=number_of_qubits,
                                    maximal_circuits_number=maximal_circuits_number,
                                    experiment_name='QDOT'
                                    )
circuits_DOT = OT_creator.get_random_circuits_list(number_of_circuits=maximal_circuits_number)



#How many measurements on each circuit.
shots_per_setting = 1*10 ** 4

#Specify name of your experiment
experiment_name = 'QDOT'

#Specify (labels of physical) qubits on which you wish to perform experiments
#qubit_indices = [0,1, 2, 3, 4]
#number_of_qubits = 5


#IMPORTANT:
#if you intend to run experiments on actual hardware,
#this has to be set equal to number of qubits on a device
quantum_register_size = 127
classical_register_size = quantum_register_size

#Create class instance that will be used for defining circuits' representation for chosen SDK
circuits_creator = SeparableCircuitsCreator(SDK_name=SDK_name,
                                            experiment_name=experiment_name,
                                            qubit_indices=qubit_indices,
                                            circuits_labels=circuits_DOT,
                                            quantum_register_size=quantum_register_size,
                                            classical_register_size=classical_register_size
                                            )
circuits_per_job=300
OT_circuits_list = circuits_creator.get_circuits()
number_of_circuits = len(OT_circuits_list)

for i in range(30):
    print(circuits_DOT[i])

number_of_jobs = int(np.ceil(number_of_circuits / circuits_per_job))
batches = []
for batch_index in range(number_of_jobs):
    circuits_now = OT_circuits_list[batch_index * circuits_per_job:(batch_index + 1) * circuits_per_job]
    batches.append(circuits_now)

number_of_batches = len(batches)
anf.cool_print('Experiment name:', experiment_name)
anf.cool_print('Backend:', backend_name, 'red')
anf.cool_print("Number of qubits:", number_of_qubits)
anf.cool_print('Number of circuits:', len(OT_circuits_list))
anf.cool_print('Number of batches:', len(batches))
anf.cool_print('Batches lenghts:', [len(x) for x in batches])
anf.cool_print("Number of shots per circuit:", shots_per_setting)

if anf.query_yes_no("Do you want to run?"):
    pass
else:
    raise KeyboardInterrupt("OK, aborting")

# Run jobs (in batches) usingg predefined wrapper
jobs_list = qiskit_utilities.run_batches(batches=batches,
                                         backend_name=backend_name,
                                         shots=shots_per_setting,provider_data=provider_data)


# Get job IDs
job_IDs_list = [job.job_id() for job in jobs_list]
now = datetime.datetime.now()

#Specify what what to save
metadata_jobs = {'number_of_qubits':number_of_qubits,
           'circuits_amount':number_of_circuits,
           'experiment_name':experiment_name,
           'backend_name':backend_name,
           'shots_per_setting':shots_per_setting,
           'circuits_per_batch':circuits_per_job,
           'number_of_batches':number_of_batches,
            'physical_qubits':qubit_indices,
             'date':f"{now.year}-{now.month}-{now.day}"}

dictionary_to_save_jobs = {'job_IDs_list': job_IDs_list,
                     'metadata':metadata_jobs}

data_directory = 'C:\\CFT Chmura\\Theory of Quantum Computation\\QREM_Data\\ibm'
file_name_jobs='job_id_ibm_washington_test'
anf.save_results_pickle(dictionary_to_save=dictionary_to_save_jobs,
                                        directory=data_directory,
                                        custom_name=file_name_jobs
                                        )

metadata = {'number_of_qubits':number_of_qubits,
           'number_of_symbols':number_of_symbols,
           'circuits_amount':number_of_circuits}

dictionary_to_save = {'circuits_list': circuits_DOT,
                     'metadata':metadata}


file_name_circuits = 'QDOT_circuits_IBM_WAS_281122'
anf.save_results_pickle(dictionary_to_save=dictionary_to_save_jobs,
                                        directory=data_directory,
                                        custom_name=file_name_circuits
                                        )
