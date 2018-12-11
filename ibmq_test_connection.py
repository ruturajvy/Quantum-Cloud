import qiskit
from qiskit import IBMQ
import Qconfig

# Enable the API token
IBMQ.enable_account(Qconfig.APItoken)

# Print the backends available
print(IBMQ.backends())