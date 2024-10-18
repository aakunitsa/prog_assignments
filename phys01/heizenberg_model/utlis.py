
from openfermion import QubitOperator, get_sparse_operator, count_qubits
import numpy as np
from typing import List, Union, Optional
from scipy.linalg import expm

def create_heizenberg_h(j: Union[np.array, List[float]], n_spins: int) -> QubitOperator:
    '''The function generates 1-D Heizenberg model Hamiltonian  with nearest neighbor 
    interaction in the openfermion.QubitOperator form. 
    '''
    
    hamiltonian = QubitOperator()
    for i in range(0, n_spins - 1):
        for coeff, term in zip(j, ['X', 'Y', 'Z']):
            hamiltonian += coeff * QubitOperator([(i, term), (i + 1, term)]) 
            
    return -1 * hamiltonian

def decompose_into_pairs(op: QubitOperator) -> List[QubitOperator]:
    '''Given a 1-D Heizenberg model Hamiltonian decomposes it into a sum of two-qubit
    Hamiltonians and returns them in the natural oreder, i.e. (0, 1), (1, 2), etc.
    '''
    n_spins = count_qubits(op)
    h_list = []
    for i in range(0, n_spins - 1):
        target_qubits = set([i, i + 1])
        op_ = QubitOperator()
        for term in op.terms:
            qubits_in_term = {q for q, _ in term}
            if target_qubits == qubits_in_term:
                op_ += QubitOperator(term) * op.terms[term]
                
        h_list.append(op_)
        
    return h_list

def create_exact_propagator(op: QubitOperator, dt: float, n_spins: Optional[int] = None) -> np.array:
    '''Creates an exact time evolution operator from a Hermitian
    operator op. Atomic units are assumed.
    ''' 
    
    if not n_spins:
        n_spins = count_qubits(op)
        
    op_sparse = get_sparse_operator(op, n_qubits=n_spins)
    op_dense  = op_sparse.toarray()
    return expm(-1.j * dt * op_dense)



# Different Trotterization methods

def trotterized_propagator1(j: Union[np.array, List[float]], n_spins: int, dt: float) -> np.array:
    '''Implements a first-order Trotter propagator by grouping the terms based on the spin projection
    '''
    
    op_x = create_heizenberg_h([j[0], 0., 0.], n_spins=n_spins)
    op_y = create_heizenberg_h([0., j[1], 0.], n_spins=n_spins)
    op_z = create_heizenberg_h([0., 0., j[2]], n_spins=n_spins)
    
    trotter_factor_x = create_exact_propagator(op_x, dt)
    trotter_factor_y = create_exact_propagator(op_y, dt)
    trotter_factor_z = create_exact_propagator(op_z, dt)
    
    return trotter_factor_x @ trotter_factor_y @ trotter_factor_z
    

def trotterized_propagator2(j: Union[np.array, List[float]], n_spins: int, dt: float) -> np.array:
    '''Implements a first-order Trotter propagator by grouping the terms based on the sites they act on.
    '''
    
    h_full = create_heizenberg_h(j, n_spins)
    pair_h = decompose_into_pairs(h_full)
    propagator = np.eye(2**n_spins)
    
    # Even pairs 
    for h in pair_h[0::2]:
        propagator = propagator @ create_exact_propagator(h, dt, n_spins)
    # Odd pairs
    for h in pair_h[1::2]:
        propagator = propagator @ create_exact_propagator(h, dt, n_spins)
        
    return propagator