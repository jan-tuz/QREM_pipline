from pyquil import get_qc, Program
from pyquil.api import local_forest_runtime
from pyquil.quilbase import Declare
from pyquil.gates import *

p = Program(
    Declare("ro", "BIT", 2),
    H(0),
    CNOT(0, 1),
    MEASURE(0, ("ro", 0)),
    MEASURE(1, ("ro", 1)),
).wrap_in_numshots_loop(10)

with local_forest_runtime():
    qc = get_qc('9q-square-qvm')
    result = qc.run(qc.compile(p)).readout_data.get("ro")
    print(result[0])
    print(result[1])