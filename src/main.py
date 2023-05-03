"""
Deutsch-Jozsa Algorithm Implementation

This script demonstrates the Deutsch-Jozsa algorithm using PennyLane.
It determines whether a function is constant or balanced using only
a single quantum query, demonstrating exponential speedup over classical algorithms.
"""

import pennylane as qml
import numpy as np
import matplotlib.pyplot as plt
from typing import Callable, List


def constant_oracle_0(n_qubits: int):
    # Constant function: f(x) = 0 for all x
    # No operations needed - identity
    pass


def constant_oracle_1(n_qubits: int):
    # Constant function: f(x) = 1 for all x
    # Apply X gate to ancilla qubit (flips |0⟩ to |1⟩)
    qml.PauliX(n_qubits)


def balanced_oracle_parity(n_qubits: int):
    # Balanced function: XOR of all input bits
    # Apply CNOT gates from each input qubit to ancilla
    for i in range(n_qubits):
        qml.CNOT(wires=[i, n_qubits])


def balanced_oracle_first_half(n_qubits: int):
    # Balanced function: return 1 if most significant bit is 0
    # Apply CNOT from MSB to ancilla
    qml.CNOT(wires=[0, n_qubits])


def deutsch_jozsa_circuit(n_qubits: int, oracle: Callable):
    dev = qml.device('default.qubit', wires=n_qubits + 1)
    
    @qml.qnode(dev)
    def circuit():
        # Step 1: Initialize ancilla qubit to |1⟩
        qml.PauliX(n_qubits)
        
        # Step 2: Apply Hadamard gates to all qubits
        for i in range(n_qubits + 1):
            qml.Hadamard(wires=i)
        
        # Step 3: Apply oracle
        oracle(n_qubits)
        
        # Step 4: Apply Hadamard gates to input qubits
        for i in range(n_qubits):
            qml.Hadamard(wires=i)
        
        # Step 5: Measure input qubits
        return [qml.sample(qml.PauliZ(i)) for i in range(n_qubits)]
    
    return circuit


def deutsch_jozsa_probability(n_qubits: int, oracle: Callable, shots: int = 1000):
    dev = qml.device('default.qubit', wires=n_qubits + 1, shots=shots)
    
    @qml.qnode(dev)
    def circuit():
        # Initialize ancilla
        qml.PauliX(n_qubits)
        
        # Hadamard on all qubits
        for i in range(n_qubits + 1):
            qml.Hadamard(wires=i)
        
        # Oracle
        oracle(n_qubits)
        
        # Hadamard on input qubits
        for i in range(n_qubits):
            qml.Hadamard(wires=i)
        
        # Measure input qubits
        return [qml.sample(qml.PauliZ(i)) for i in range(n_qubits)]
    
    # Execute circuit
    results = circuit()
    
    # Process results: convert to bitstrings
    # PauliZ measurement returns +1 for |0⟩ and -1 for |1⟩
    # Convert to 0 and 1
    bitstrings = []
    for i in range(shots):
        bitstring = ''.join(['0' if r[i] == 1 else '1' for r in results])
        bitstrings.append(bitstring)
    
    # Count occurrences
    counts = {}
    for bitstring in bitstrings:
        counts[bitstring] = counts.get(bitstring, 0) + 1
    
    # Convert to probabilities
    probabilities = {k: v / shots for k, v in counts.items()}
    
    return probabilities


def classical_algorithm(function_type: str, n_qubits: int):
    total_inputs = 2 ** n_qubits
    
    if function_type == 'constant':
        # For constant function, need to check 2 inputs to be sure
        return 2
    else:
        # For balanced function, worst case need 2^(n-1) + 1 queries
        return 2 ** (n_qubits - 1) + 1


def test_deutsch_jozsa():
    n_qubits = 3
    shots = 1000
    
    print("=" * 70)
    print("Deutsch-Jozsa Algorithm Demonstration")
    print("=" * 70)
    print(f"Number of input qubits: {n_qubits}")
    print(f"Measurement shots: {shots}")
    print()
    
    test_cases = [
        ("Constant (f(x) = 0)", constant_oracle_0, "constant"),
        ("Constant (f(x) = 1)", constant_oracle_1, "constant"),
        ("Balanced (Parity)", balanced_oracle_parity, "balanced"),
        ("Balanced (First Half)", balanced_oracle_first_half, "balanced"),
    ]
    
    results = []
    
    for name, oracle, function_type in test_cases:
        print("-" * 70)
        print(f"Testing: {name}")
        print("-" * 70)
        
        # Run quantum algorithm
        probabilities = deutsch_jozsa_probability(n_qubits, oracle, shots)
        
        # Check if all-zero state has high probability (constant) or low (balanced)
        zero_state = '0' * n_qubits
        zero_prob = probabilities.get(zero_state, 0.0)
        
        # Determine result
        if zero_prob > 0.9:
            result = "CONSTANT"
            correct = function_type == "constant"
        else:
            result = "BALANCED"
            correct = function_type == "balanced"
        
        print(f"Quantum algorithm result: {result}")
        print(f"Expected: {function_type.upper()}")
        print(f"Correct: {'✓' if correct else '✗'}")
        print()
        
        print("Measurement probabilities (top 5):")
        sorted_probs = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)
        for bitstring, prob in sorted_probs[:5]:
            print(f"  |{bitstring}⟩: {prob:.4f}")
        print()
        
        # Classical comparison
        classical_queries = classical_algorithm(function_type, n_qubits)
        print(f"Classical queries needed: {classical_queries}")
        print(f"Quantum queries needed: 1")
        print(f"Speedup: {classical_queries}x")
        print()
        
        results.append({
            'name': name,
            'type': function_type,
            'result': result,
            'correct': correct,
            'probabilities': probabilities,
            'classical_queries': classical_queries
        })
    
    return results


def visualize_results(results: List[dict], n_qubits: int):
    import os
    os.makedirs('data', exist_ok=True)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()
    
    for idx, result in enumerate(results):
        ax = axes[idx]
        probs = result['probabilities']
        
        # Sort by bitstring value
        sorted_items = sorted(probs.items(), key=lambda x: int(x[0], 2))
        bitstrings = [item[0] for item in sorted_items]
        probabilities = [item[1] for item in sorted_items]
        
        ax.bar(range(len(bitstrings)), probabilities, alpha=0.7)
        ax.set_xlabel('Bitstring')
        ax.set_ylabel('Probability')
        ax.set_title(f"{result['name']}\nResult: {result['result']}")
        ax.set_xticks(range(len(bitstrings)))
        ax.set_xticklabels(bitstrings, rotation=45, ha='right')
        ax.grid(True, alpha=0.3)
        
        # Highlight the all-zero state
        zero_idx = bitstrings.index('0' * n_qubits)
        ax.bar(zero_idx, probabilities[zero_idx], color='red', alpha=0.8, label='|0⟩^n')
        ax.legend()
    
    plt.tight_layout()
    plt.savefig('data/deutsch_jozsa_results.png', dpi=150, bbox_inches='tight')
    print("Saved visualization: data/deutsch_jozsa_results.png")


def print_circuit_diagram(n_qubits: int, oracle_name: str):
    print(f"\nCircuit structure for {oracle_name}:")
    print("-" * 50)
    print("Input qubits:")
    for i in range(n_qubits):
        print(f"  q[{i}]: |0⟩ --H--[Oracle]--H--[Measure]")
    print(f"Ancilla qubit:")
    print(f"  q[{n_qubits}]: |1⟩ --H--[Oracle]--[Measure]")
    print("-" * 50)


def main():
    # Test the algorithm
    results = test_deutsch_jozsa()
    
    # Visualize results
    print("=" * 70)
    print("Generating Visualizations")
    print("=" * 70)
    print()
    visualize_results(results, n_qubits=3)
    
    # Print circuit diagrams
    print("=" * 70)
    print("Circuit Diagrams")
    print("=" * 70)
    print_circuit_diagram(3, "Deutsch-Jozsa")
    
    print()
    print("=" * 70)
    print("Demonstration Complete!")
    print("=" * 70)
    print()
    print("Summary:")
    print(f"  Total test cases: {len(results)}")
    correct_count = sum(1 for r in results if r['correct'])
    print(f"  Correctly identified: {correct_count}/{len(results)}")
    print()
    print("The quantum algorithm successfully identifies constant vs balanced")
    print("functions using only 1 query, demonstrating exponential speedup.")


if __name__ == "__main__":
    main()

