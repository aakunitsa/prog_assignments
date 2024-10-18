import pytest, cirq
import numpy as np
from circuits import UnitaryEvolution2Site, analytic_Uh

def test_unitary_evolution_two_site():
    
    # Generate random angles
    random_angles = np.random.randn(3)
    
    # Create a reference and a unitary representing the gate
    ref_matrix = analytic_Uh(random_angles)
    gate_matrix = cirq.unitary(UnitaryEvolution2Site(random_angles))
    
    # Check if they are equivalent
    assert np.allclose(ref_matrix, gate_matrix)