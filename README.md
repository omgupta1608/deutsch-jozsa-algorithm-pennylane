# Deutsch-Jozsa Algorithm
The Deutsch-Jozsa algorithm is one of the first quantum algorithms that demonstrates a clear quantum advantage over classical algorithms. It determines whether a function f: {0,1}^n → {0,1} is constant (returns the same value for all inputs) or balanced (returns 0 for half the inputs and 1 for the other half) using only a single query to the function, compared to 2^(n-1) + 1 queries required classically.

The implementation demonstrates:
- Oracle function construction for constant and balanced functions
- Quantum parallelism and interference
- Single-shot quantum advantage
- Performance comparison with classical approach

## Theory

### Problem Statement

Given a function f: {0,1}^n → {0,1} that is promised to be either:
- **Constant**: f(x) = c for all x ∈ {0,1}^n, where c ∈ {0,1}
- **Balanced**: f(x) = 0 for exactly half of all possible inputs x, and f(x) = 1 for the other half

Determine which type the function is.

### Classical Complexity

In the worst case, a classical algorithm requires 2^(n-1) + 1 function evaluations to determine whether f is constant or balanced. This is because we need to check more than half of all possible inputs to guarantee we've seen both output values if the function is balanced.

### Quantum Algorithm

The Deutsch-Jozsa algorithm solves this problem using only a single query to the function, demonstrating exponential speedup.

### Algorithm Steps

1. **Initialization**: Prepare n+1 qubits, where n qubits are initialized to |0⟩ and one ancilla qubit is initialized to |1⟩.

2. **Superposition**: Apply Hadamard gates to all qubits, creating a uniform superposition:
   |ψ₁⟩ = (1/√2^n) Σ_x |x⟩ ⊗ (|0⟩ - |1⟩)/√2

3. **Oracle Application**: Apply the function f as a quantum oracle U_f:
   U_f|x⟩|y⟩ = |x⟩|y ⊕ f(x)⟩
   
   This transforms the state to:
   |ψ₂⟩ = (1/√2^n) Σ_x (-1)^f(x) |x⟩ ⊗ (|0⟩ - |1⟩)/√2

4. **Hadamard Transform**: Apply Hadamard gates to the first n qubits.

5. **Measurement**: Measure the first n qubits. If all qubits are |0⟩, the function is constant; otherwise, it is balanced.

### Mathematical Analysis

After the Hadamard transform on the first n qubits, the amplitude of the |0⟩^n state is:
   α₀ = (1/2^n) Σ_x (-1)^f(x)

- If f is constant: α₀ = ±1, so |α₀|² = 1
- If f is balanced: α₀ = 0, so |α₀|² = 0

This demonstrates quantum interference: amplitudes cancel out for balanced functions, while they constructively interfere for constant functions.

### Quantum Advantage

The quantum algorithm requires only 1 query versus 2^(n-1) + 1 queries classically, providing an exponential speedup. This is one of the earliest demonstrations of quantum computational advantage.

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation Steps

1. Clone or navigate to this repository:
```bash
cd deutsch-jozsa-algorithm-pennylane
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Running Instructions

1. Ensure you have activated your virtual environment (if using one).

2. Run the main script:
```bash
python src/main.py
```

3. The script will:
   - Test the algorithm with various constant and balanced functions
   - Display the quantum circuit
   - Show measurement results
   - Compare performance with classical approach
   - Visualize the results

### Expected Output

The program will output:
- Quantum circuit diagrams for different oracle types
- Measurement results showing the algorithm correctly identifies constant vs balanced functions
- Comparison showing the quantum algorithm requires only 1 query vs multiple classical queries
- Visualization of measurement probabilities

## Results and Interpretation

The Deutsch-Jozsa algorithm should correctly identify constant functions (all measurements yield |0⟩^n) and balanced functions (measurements yield non-zero states) with high probability. The quantum approach demonstrates clear advantage by solving the problem in a single query, whereas classical algorithms require exponentially more queries in the worst case.

## References

1. Deutsch, D., & Jozsa, R. (1992). Rapid solution of problems by quantum computation. Proceedings of the Royal Society of London. Series A: Mathematical and Physical Sciences, 439(1907), 553-558.

2. Nielsen, M. A., & Chuang, I. L. (2010). Quantum Computation and Quantum Information: 10th Anniversary Edition. Cambridge University Press.

3. PennyLane Documentation: https://docs.pennylane.ai/

