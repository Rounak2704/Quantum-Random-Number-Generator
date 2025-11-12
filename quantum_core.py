"""
Core quantum random number generator using Qiskit.
Implements single-qubit measurements with Hadamard gate for true quantum randomness.
"""

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
import numpy as np


class QuantumRandomNumberGenerator:
    """
    Generates random numbers using quantum mechanics principles.
    Uses a single qubit in superposition (Hadamard gate) and measures it.
    """
    
    def __init__(self, seed=None):
        """
        Initialize the QRNG with optional seed for reproducibility.
        
        Args:
            seed (int, optional): Random seed for simulator reproducibility
        """
        self.simulator = AerSimulator(seed_simulator=seed)
        self.measurements = []
        self.counts = {}
    
    def generate_random_bits(self, num_measurements=1024):
        """
        Generate random bits using quantum measurements.
        
        Args:
            num_measurements (int): Number of measurements to perform (default: 1024)
        
        Returns:
            list: List of random bits (0 or 1)
        """
        # Create quantum circuit with 1 qubit and 1 classical bit
        qr = QuantumRegister(1, 'q')
        cr = ClassicalRegister(1, 'c')
        circuit = QuantumCircuit(qr, cr)
        
        # Apply Hadamard gate to create superposition
        circuit.h(qr[0])
        
        # Measure the qubit
        circuit.measure(qr[0], cr[0])
        
        # Execute the circuit multiple times
        job = self.simulator.run(circuit, shots=num_measurements)
        result = job.result()
        self.counts = result.get_counts(circuit)
        
        # Extract measurements as list of bits
        measurements = []
        for bitstring, count in self.counts.items():
            bit = int(bitstring)
            measurements.extend([bit] * count)
        
        self.measurements = measurements
        return measurements
    
    def to_binary_string(self):
        """
        Convert measurements to binary string.
        
        Returns:
            str: Binary representation of measurements
        """
        if not self.measurements:
            raise ValueError("No measurements available. Call generate_random_bits() first.")
        return ''.join(map(str, self.measurements))
    
    def to_decimal(self):
        """
        Convert binary measurements to decimal number.
        
        Returns:
            int: Decimal representation of measurements
        """
        binary_str = self.to_binary_string()
        return int(binary_str, 2)
    
    def to_hex(self):
        """
        Convert measurements to hexadecimal string.
        
        Returns:
            str: Hexadecimal representation of measurements
        """
        decimal = self.to_decimal()
        return hex(decimal)
    
    def to_float(self):
        """
        Convert measurements to float between 0 and 1.
        
        Returns:
            float: Random float in range [0, 1)
        """
        binary_str = self.to_binary_string()
        # Pad to 32 bits for float conversion
        binary_str = binary_str.ljust(32, '0')[:32]
        decimal = int(binary_str, 2)
        return decimal / (2 ** 32)
    
    def get_statistics(self):
        """
        Get statistical information about the measurements.
        
        Returns:
            dict: Statistics including counts, probabilities, and entropy
        """
        if not self.measurements:
            raise ValueError("No measurements available. Call generate_random_bits() first.")
        
        total = len(self.measurements)
        count_0 = self.measurements.count(0)
        count_1 = self.measurements.count(1)
        
        prob_0 = count_0 / total
        prob_1 = count_1 / total
        
        # Calculate Shannon entropy (max is 1.0 for perfect randomness)
        entropy = 0
        if prob_0 > 0:
            entropy -= prob_0 * np.log2(prob_0)
        if prob_1 > 0:
            entropy -= prob_1 * np.log2(prob_1)
        
        return {
            'total_measurements': total,
            'count_0': count_0,
            'count_1': count_1,
            'probability_0': prob_0,
            'probability_1': prob_1,
            'shannon_entropy': entropy,
            'max_entropy': 1.0,
            'entropy_ratio': entropy / 1.0
        }
    
    def reset(self):
        """Reset the generator state."""
        self.measurements = []
        self.counts = {}


# Example usage
if __name__ == "__main__":
    qrng = QuantumRandomNumberGenerator(seed=42)
    
    # Generate 256 random bits
    bits = qrng.generate_random_bits(num_measurements=256)
    
    print("Random Bits (first 50):", ''.join(map(str, bits[:50])))
    print("Binary String (first 50):", qrng.to_binary_string()[:50])
    print("Decimal:", qrng.to_decimal())
    print("Hexadecimal:", qrng.to_hex())
    print("Float [0,1):", qrng.to_float())
    
    # Print statistics
    stats = qrng.get_statistics()
    print("\nStatistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
