
import cirq
import numpy as np 
    
def analytic_Uh(theta: np.array) -> np.array:
    delta = theta[0] + theta[1]
    gamma = theta[0] - theta[1]
    propagator_matrix = np.array(
        [
            [np.exp(1.j * theta[2]) * np.cos(gamma), 0, 0, 1.j * np.exp(1.j * theta[2]) * np.sin(gamma)],
            [0, np.exp(-1.j * theta[2]) * np.cos(delta), 1.j * np.exp(-1.j * theta[2]) * np.sin(delta), 0],
            [0, 1.j * np.exp(-1.j * theta[2]) * np.sin(delta), np.exp(-1.j * theta[2]) * np.cos(delta), 0],
            [1.j * np.exp(1.j * theta[2]) * np.sin(gamma), 0, 0, np.exp(1.j * theta[2]) * np.cos(gamma)]
        ]
    )
    
    return propagator_matrix

    
class UnitaryEvolution2Site(cirq.Gate):
    def __init__(self, theta: np.array):
        super(UnitaryEvolution2Site, self)
        self.theta = theta # array of three real numbers
        
    def _num_qubits_(self) -> int:
        return 2
    
    #def _unitary_(self):
    #    return analytic_Uh(self.theta)
    
    def _decompose_(self, qubits):
        a, b = qubits
        yield cirq.rx(np.pi / 2.).on(a)
        yield cirq.rx(np.pi / 2.).on(b)
        yield cirq.CNOT(a, b)
        yield cirq.rx(-2. * self.theta[0]).on(a)
        yield cirq.rz(-2. * self.theta[1]).on(b)
        yield cirq.CNOT(a, b)
        yield cirq.rx(-np.pi / 2.).on(a)
        yield cirq.rx(-np.pi / 2.).on(b)
        yield cirq.CNOT(a, b)
        yield cirq.rz(-2 * self.theta[2]).on(b)
        yield cirq.CNOT(a, b)
        
        
    def _circuit_diagram_info_(self, args):
        return ["Uh"] * self.num_qubits()