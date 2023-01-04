import sys
import os
import numpy as np

import time
import datetime
import copy

operating_system = 'WIN'

if operating_system=='WIN':
    directory_QREM = os.environ["QREM"] +'\\'
    data_directory = 'C:\\CFT Chmura\\Theory of Quantum Computation\\QREM_Data\\rigetti\\'
elif operating_system=='LIN':
    directory_QREM = '/home/fbm/PycharmProjects/QREM_SECRET_DEVELOPMENT/'
    data_directory = '/home/fbm/Nextcloud/Theory of Quantum Computation/QREM_Data/rigetti/'

sys.path.append(os.path.dirname(directory_QREM))

from noise_characterization.data_analysis.InitialNoiseAnalyzer import InitialNoiseAnalyzer
from noise_simulation.CN.noise_addition import  add_noise_results_dictionary
from noise_model_generation.CN.NoiseModelGenerator import NoiseModelGenerator
from functions_qrem import functions_data_analysis as fda
from backends_support.pyquil import pyquil_utilities
from noise_characterization.base_classes.OverlappingTomographyBase import OverlappingTomographyBase
from noise_characterization.tomography_design.overlapping.SeparableCircuitsCreator import \
    SeparableCircuitsCreator

from functions_qrem import ancillary_functions as anf






SDK_name = 'pyquil-for-azure-quantum'

file_name_results  = "QDOT_counts_RIG_M2_291122"

# Specify backend on which you wish to perform experiments
backend_name = 'Aspen-M-2'

# Define number of qubits you wish to create DOT circuits for
number_of_qubits = 72



# Specify desired number of circuits
maximal_circuits_number = 300

OT_creator = OverlappingTomographyBase(number_of_qubits=number_of_qubits,
                                    maximal_circuits_number=maximal_circuits_number,
                                    experiment_name = 'QDOT'
                                    )
circuits_DOT = OT_creator.get_random_circuits_list(number_of_circuits=maximal_circuits_number)

#How many measurements on each circuit.
shots_per_setting = 10**4

#Specify name of your experiment
experiment_name = 'QDOT'

#Specify (labels of physical) qubits on which you wish to perform experiments
# qubit_indices = sorted([1, 2, 3, 4, 5, 6, 7,
#                  10, 11, 12, 13, 14, 15,
#                  16, 17, 21, 22, 23, 24,
#                  25, 26, 27, 31, 33,
#                  34, 35, 36, 37, 40,
#                  41, 42, 43, 44, 45, 46, 47,
#                  100, 101, 103, 105, 107, 110,
#                  111, 112, 113, 115, 117, 120,
#                  121, 122, 123, 124, 126, 127,
#                  130, 131, 132, 133, 134, 135,
#                  137, 140, 141, 143, 145, 146,
#                  147])


qubits_with_to_high_error_rates=[0,5,30,100,106,114,115,123]

qubit_indices=[]

for i in range(5):
    for j in range(8):
        index= i*10+j
        if index not in qubits_with_to_high_error_rates:
            qubit_indices.append(index)

for i in range(5):
    for j in range(8):
        index= 100+ i*10+j
        if index not in qubits_with_to_high_error_rates:
            qubit_indices.append(index)

qubit_indices=sorted(qubit_indices)
#qubit_indices = sorted([1, 2, 3,4, 6, 7, 10, 11, 12, 13,14, 15, 16, 17, 2021, 22, 23, 24, 25, 26, 27, 30, 31, 32, 33, 35, 37, 40, 41, 42, 43, 44, 45, 46, 47, 100, 101, 102, 103, 105, 106, 107, 110, 111, 112, 113, 115, 117, 120, 121, 122, 123, 124, 127, 130, 131, 132, 133, 134, 135, 137, 140, 143, 145, 146, 147])


#qubit_indices = sorted([1, 2])
print(os.environ.keys())
# qubit_indices = [0]
number_of_qubits = len(qubit_indices)

print(number_of_qubits)

#IMPORTANT:
#if you intend to run experiments on actual hardware,
#this has to be set equal to number of qubits on a device
quantum_register_size = 80
classical_register_size = number_of_qubits

#Create class instance that will be used for defining circuits' representation for chosen SDK
circuits_creator = SeparableCircuitsCreator(SDK_name=SDK_name,
                                            experiment_name=experiment_name,
                                            qubit_indices=qubit_indices,
                                            circuits_labels=circuits_DOT,
                                            quantum_register_size=quantum_register_size,
                                            classical_register_size=classical_register_size
                                            )

OT_circuits_list = circuits_creator.get_circuits()
number_of_circuits = len(circuits_DOT)

circuits_per_batch = 150
number_of_batches = int(np.ceil(number_of_circuits / circuits_per_batch))

memory_map_DOT = circuits_creator.get_circuits()


def divide_memory_map_into_batches(number_of_batches,
                                   circuits_per_batch,
                                   memory_map):
    memory_maps_list = []
    for batch_index in range(number_of_batches):

        current_memory_map = {}

        for angles_label, list_of_values in memory_map.items():
            values_now = list_of_values[batch_index * circuits_per_batch:(batch_index + 1) * circuits_per_batch]

            current_memory_map[angles_label] = values_now
        memory_maps_list.append(current_memory_map)

    return memory_maps_list


memory_maps_list = divide_memory_map_into_batches(number_of_batches=number_of_batches,
                                                  circuits_per_batch=circuits_per_batch,
                                                  memory_map=memory_map_DOT)

base_program_DOT = pyquil_utilities.get_generic_base_program_DOT(qubit_indices=qubit_indices)


backend_instance = pyquil_utilities.get_backend_wrapper(backend_name=backend_name,
                                            sdk_name=SDK_name)

native_quil = backend_instance.compiler.quil_to_native_quil(base_program_DOT)






executable = backend_instance.compile(native_quil, to_native_gates=False)


# # print(executable)
# # print(native_quil)

circuits_labels_list = circuits_DOT

#hard_copy_circuits_labels = copy.deepcopy(circuits_labels_list)

anf.cool_print('Experiment name:', experiment_name)
anf.cool_print('Backend:', backend_name, 'red')
anf.cool_print('Active qubits:', qubit_indices, 'red')
#anf.cool_print("Collection index:", collection_index, 'red')
anf.cool_print("Number of qubits:", number_of_qubits)
anf.cool_print('Number of circuits:', len(circuits_labels_list))
anf.cool_print('Number of batches:', len(memory_maps_list))
anf.cool_print('Batches lenghts:', [len(list(x.values())[0]) for x in memory_maps_list])
anf.cool_print("Number of shots per circuit:", shots_per_setting)

if anf.query_yes_no("Do you want to run?"):
    pass
else:
    raise KeyboardInterrupt("OK, aborting")



unprocessed_results = []

canceled_batches_indices = []
uncanceled_batches_indices = []
taken_times_batches = []

t_start = time.time()
for batch_index in range(number_of_batches):
    now = datetime.datetime.now()
    # print(now.year, now.month, now.day, now.hour, now.minute, now.second)
    anf.cool_print("\nCURRENT BATCH:", batch_index)
    anf.cool_print("START AT:", f"{now.hour}:{now.minute}")
    current_batch = memory_maps_list[batch_index]

    # Run jobs  using predefined wrapper

    time_start_batch = time.time()

    try:
        unprocessed_results_now = pyquil_utilities.run_batches_parametric(backend_name=backend_name,
                                                                          sdk_name=SDK_name,
                                                                          number_of_shots=shots_per_setting,
                                                                          qubit_indices=qubit_indices,
                                                                          base_program=base_program_DOT,
                                                                          memory_map=current_batch)

        unprocessed_results += unprocessed_results_now

        anf.cool_print("BATCH:", f"{batch_index} finished!")
        now = datetime.datetime.now()
        anf.cool_print("FINISHED AT:", f"{now.hour}:{now.minute}")
        uncanceled_batches_indices.append(batch_index)

        time_end_batch = time.time()
        time_taken_batch = time_end_batch - time_start_batch

        taken_times_batches.append(time_taken_batch)

        anf.cool_print("It took:", time_taken_batch)

    except(KeyboardInterrupt):
        anf.cool_print("BATCH:", f"{batch_index} canceled!", 'red')
        canceled_batches_indices.append(batch_index)

if len(canceled_batches_indices) > 0:
    circuits_labels_list_changing = []

    for batch_index in uncanceled_batches_indices:
        circuits_labels_list_changing += hard_copy_circuits_labels[
                                         batch_index * circuits_per_batch:(batch_index + 1) * circuits_per_batch]

    circuits_labels_list = circuits_labels_list_changing

#     print(circuits_labels_list[0])
#     print(hard_copy_circuits_labels[0])

from functions_qrem import functions_data_analysis as fdt

#Specify directory where to save results of experiments


#Specfiy name of file with experimental results


processed_results = pyquil_utilities.convert_results_to_counts_dictionaries_DOT(list_of_circuits_labels=circuits_labels_list,
                                               results_list=unprocessed_results)

#Specify what to save
now = datetime.datetime.now()
#Specify what what to save
metadata_jobs = {'number_of_qubits':number_of_qubits,
           'circuits_amount':number_of_circuits,
           'experiment_name':experiment_name,
           'backend_name':backend_name,
           'shots_per_setting':shots_per_setting,
                 'time_taken':time_taken,
                 'date':f"{now.year}-{now.month}-{now.day}",
           'circuits_per_batch':circuits_per_batch,
           'number_of_batches':number_of_batches,
                 'physical_qubits':qubit_indices,
                 'circuits_labels_list':circuits_labels_list,
                 'canceled_batches_indices':canceled_batches_indices,
                 'taken_times_batches':taken_times_batches
                }

dictionary_to_save_results = {'results_dictionary': processed_results,
                     'metadata':metadata_jobs}

#Save results
anf.save_results_pickle(dictionary_to_save=dictionary_to_save_results,
                                        directory=data_directory,
                                        custom_name=file_name_results
                                        )