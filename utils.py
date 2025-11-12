"""
Utility functions for quantum random number generator.
Includes file I/O, format conversion, and randomness quality tests.
"""

import json
import random
from datetime import datetime
from scipy import stats as scipy_stats
import numpy as np


class FileManager:
    """Handles saving and loading random number data."""
    
    @staticmethod
    def save_measurements(measurements, filename):
        """
        Save measurements to a JSON file.
        
        Args:
            measurements (list): List of measurement results
            filename (str): Output filename
        """
        data = {
            'timestamp': datetime.now().isoformat(),
            'measurements': measurements,
            'count': len(measurements)
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Measurements saved to {filename}")
    
    @staticmethod
    def load_measurements(filename):
        """
        Load measurements from a JSON file.
        
        Args:
            filename (str): Input filename
        
        Returns:
            list: List of measurement results
        """
        with open(filename, 'r') as f:
            data = json.load(f)
        
        return data['measurements']
    
    @staticmethod
    def save_as_binary_file(measurements, filename):
        """
        Save measurements as binary file (one bit per byte for readability).
        
        Args:
            measurements (list): List of measurement results
            filename (str): Output filename
        """
        binary_str = ''.join(map(str, measurements))
        
        with open(filename, 'w') as f:
            f.write(binary_str)
        
        print(f"Binary data saved to {filename}")
    
    @staticmethod
    def save_as_hex_file(measurements, filename):
        """
        Save measurements as hexadecimal file.
        
        Args:
            measurements (list): List of measurement results
            filename (str): Output filename
        """
        binary_str = ''.join(map(str, measurements))
        # Pad to multiple of 4 for hex conversion
        binary_str = binary_str.ljust((len(binary_str) + 3) // 4 * 4, '0')
        
        hex_str = hex(int(binary_str, 2))[2:]
        
        with open(filename, 'w') as f:
            f.write(hex_str)
        
        print(f"Hexadecimal data saved to {filename}")


class RandomnessTests:
    """Statistical tests for randomness quality."""
    
    @staticmethod
    def chi_square_test(measurements, expected_prob=0.5):
        """
        Perform chi-square test for randomness.
        
        Args:
            measurements (list): List of measurement results
            expected_prob (float): Expected probability for each outcome
        
        Returns:
            dict: Test results including chi-square statistic and p-value
        """
        count_0 = measurements.count(0)
        count_1 = measurements.count(1)
        total = len(measurements)
        
        expected_count = total * expected_prob
        
        chi_square = ((count_0 - expected_count) ** 2 / expected_count + 
                      (count_1 - expected_count) ** 2 / expected_count)
        
        # p-value from chi-square distribution with 1 degree of freedom
        p_value = 1 - scipy_stats.chi2.cdf(chi_square, df=1)
        
        return {
            'chi_square_statistic': chi_square,
            'p_value': p_value,
            'passes_test': p_value > 0.05,  # Typically use 0.05 significance level
            'interpretation': 'Random' if p_value > 0.05 else 'Not random'
        }
    
    @staticmethod
    def runs_test(measurements):
        """
        Perform runs test for randomness (tests for clustering).
        
        Args:
            measurements (list): List of measurement results
        
        Returns:
            dict: Test results including runs count and p-value
        """
        # Count runs (consecutive identical values)
        runs = 1
        for i in range(1, len(measurements)):
            if measurements[i] != measurements[i-1]:
                runs += 1
        
        n0 = measurements.count(0)
        n1 = measurements.count(1)
        n = len(measurements)
        
        # Expected number of runs
        expected_runs = (2 * n0 * n1) / n + 1
        
        # Variance of runs
        variance = (2 * n0 * n1 * (2 * n0 * n1 - n)) / (n ** 2 * (n - 1))
        
        # Z-score
        z_score = (runs - expected_runs) / np.sqrt(variance)
        
        # p-value from normal distribution
        p_value = 2 * (1 - scipy_stats.norm.cdf(abs(z_score)))
        
        return {
            'runs_count': runs,
            'expected_runs': expected_runs,
            'z_score': z_score,
            'p_value': p_value,
            'passes_test': p_value > 0.05,
            'interpretation': 'Random' if p_value > 0.05 else 'Clustered'
        }
    
    @staticmethod
    def entropy_test(measurements):
        """
        Calculate Shannon entropy and compare to theoretical maximum.
        
        Args:
            measurements (list): List of measurement results
        
        Returns:
            dict: Entropy metrics
        """
        total = len(measurements)
        count_0 = measurements.count(0)
        count_1 = measurements.count(1)
        
        prob_0 = count_0 / total
        prob_1 = count_1 / total
        
        # Shannon entropy
        entropy = 0
        if prob_0 > 0:
            entropy -= prob_0 * np.log2(prob_0)
        if prob_1 > 0:
            entropy -= prob_1 * np.log2(prob_1)
        
        max_entropy = 1.0
        entropy_ratio = entropy / max_entropy
        
        return {
            'shannon_entropy': entropy,
            'max_entropy': max_entropy,
            'entropy_ratio': entropy_ratio,
            'quality': 'Excellent' if entropy_ratio > 0.95 else 'Good' if entropy_ratio > 0.85 else 'Poor'
        }
    
    @staticmethod
    def compare_with_classical_random(num_samples=1024):
        """
        Generate classical random numbers and compare statistics.
        
        Args:
            num_samples (int): Number of samples to generate
        
        Returns:
            dict: Comparison statistics
        """
        classical_bits = [random.randint(0, 1) for _ in range(num_samples)]
        
        count_0 = classical_bits.count(0)
        count_1 = classical_bits.count(1)
        
        return {
            'count_0': count_0,
            'count_1': count_1,
            'probability_0': count_0 / num_samples,
            'probability_1': count_1 / num_samples
        }


class FormatConverter:
    """Convert between different number formats."""
    
    @staticmethod
    def binary_to_decimal(binary_str):
        """Convert binary string to decimal."""
        return int(binary_str, 2)
    
    @staticmethod
    def binary_to_hex(binary_str):
        """Convert binary string to hexadecimal."""
        decimal = int(binary_str, 2)
        return hex(decimal)
    
    @staticmethod
    def binary_to_float(binary_str):
        """Convert binary string to float [0, 1)."""
        binary_str = binary_str.ljust(32, '0')[:32]
        decimal = int(binary_str, 2)
        return decimal / (2 ** 32)
    
    @staticmethod
    def decimal_to_binary(decimal):
        """Convert decimal to binary string."""
        return bin(decimal)[2:]
    
    @staticmethod
    def hex_to_binary(hex_str):
        """Convert hexadecimal to binary string."""
        return bin(int(hex_str, 16))[2:]


# Example usage
if __name__ == "__main__":
    from quantum_core import QuantumRandomNumberGenerator
    
    # Generate random bits
    qrng = QuantumRandomNumberGenerator(seed=42)
    measurements = qrng.generate_random_bits(num_measurements=1024)
    
    # Save measurements
    FileManager.save_measurements(measurements, "quantum_measurements.json")
    FileManager.save_as_binary_file(measurements, "quantum_random.bin")
    FileManager.save_as_hex_file(measurements, "quantum_random.hex")
    
    # Run randomness tests
    print("\n=== Randomness Quality Tests ===")
    chi_square = RandomnessTests.chi_square_test(measurements)
    print(f"Chi-Square Test: {chi_square}")
    
    runs = RandomnessTests.runs_test(measurements)
    print(f"Runs Test: {runs}")
    
    entropy = RandomnessTests.entropy_test(measurements)
    print(f"Entropy Test: {entropy}")
    
    # Compare with classical random
    classical = RandomnessTests.compare_with_classical_random(1024)
    print(f"Classical Random Comparison: {classical}")
