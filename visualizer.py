"""
Visualization module for quantum random number generator.
Provides histogram and Bloch sphere visualizations.
"""

import matplotlib.pyplot as plt
import numpy as np
from qiskit.visualization import plot_bloch_multivector
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator


class QuantumVisualizer:
    """Handles visualization of quantum measurements and states."""
    
    @staticmethod
    def plot_measurement_histogram(measurements, title="Quantum Measurement Results", 
                                   save_path=None):
        """
        Plot histogram of measurement results (0s vs 1s).
        
        Args:
            measurements (list): List of measurement results (0 or 1)
            title (str): Title for the plot
            save_path (str, optional): Path to save the figure
        
        Returns:
            matplotlib.figure.Figure: The figure object
        """
        count_0 = measurements.count(0)
        count_1 = measurements.count(1)
        total = len(measurements)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Create bar chart
        bars = ax.bar(['0', '1'], [count_0, count_1], color=['#3498db', '#e74c3c'], 
                      edgecolor='black', linewidth=1.5, alpha=0.8)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}\n({height/total*100:.1f}%)',
                   ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        ax.set_ylabel('Count', fontsize=12, fontweight='bold')
        ax.set_xlabel('Measurement Result', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_ylim(0, max(count_0, count_1) * 1.15)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    @staticmethod
    def plot_bloch_sphere(save_path=None):
        """
        Plot Bloch sphere showing superposition state after Hadamard gate.
        
        Args:
            save_path (str, optional): Path to save the figure
        
        Returns:
            matplotlib.figure.Figure: The figure object
        """
        # Create circuit with Hadamard gate
        qr = QuantumRegister(1, 'q')
        circuit = QuantumCircuit(qr)
        circuit.h(qr[0])
        circuit.save_statevector()
        
        # Get statevector
        simulator = AerSimulator(method='statevector')
        job = simulator.run(circuit)
        result = job.result()
        statevector = result.get_statevector(circuit)
        
        # Plot Bloch sphere
        fig = plot_bloch_multivector(statevector)
        fig.suptitle('Bloch Sphere: Qubit State After Hadamard Gate', 
                     fontsize=14, fontweight='bold', y=0.98)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    @staticmethod
    def plot_statistics(stats, save_path=None):
        """
        Plot statistical analysis of measurements.
        
        Args:
            stats (dict): Statistics dictionary from QRNG
            save_path (str, optional): Path to save the figure
        
        Returns:
            matplotlib.figure.Figure: The figure object
        """
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Probability distribution
        ax1 = axes[0]
        probs = [stats['probability_0'], stats['probability_1']]
        bars = ax1.bar(['P(0)', 'P(1)'], probs, color=['#3498db', '#e74c3c'], 
                       edgecolor='black', linewidth=1.5, alpha=0.8)
        
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.4f}',
                    ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        ax1.axhline(y=0.5, color='green', linestyle='--', linewidth=2, label='Ideal (0.5)')
        ax1.set_ylabel('Probability', fontsize=11, fontweight='bold')
        ax1.set_title('Probability Distribution', fontsize=12, fontweight='bold')
        ax1.set_ylim(0, 0.6)
        ax1.legend()
        ax1.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Entropy analysis
        ax2 = axes[1]
        entropy_ratio = stats['entropy_ratio']
        colors = ['#2ecc71' if entropy_ratio > 0.95 else '#f39c12' if entropy_ratio > 0.85 else '#e74c3c']
        bar = ax2.barh(['Shannon Entropy'], [entropy_ratio], color=colors, 
                       edgecolor='black', linewidth=1.5, alpha=0.8)
        
        ax2.text(entropy_ratio/2, 0, f'{entropy_ratio:.4f}',
                ha='center', va='center', fontsize=12, fontweight='bold', color='white')
        ax2.axvline(x=0.95, color='green', linestyle='--', linewidth=2, label='Excellent (>0.95)')
        ax2.axvline(x=0.85, color='orange', linestyle='--', linewidth=2, label='Good (>0.85)')
        ax2.set_xlim(0, 1.1)
        ax2.set_xlabel('Entropy Ratio (Normalized)', fontsize=11, fontweight='bold')
        ax2.set_title('Randomness Quality', fontsize=12, fontweight='bold')
        ax2.legend(loc='lower right')
        ax2.grid(axis='x', alpha=0.3, linestyle='--')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    @staticmethod
    def plot_bit_sequence(measurements, window_size=100, save_path=None):
        """
        Plot running average of bit values to visualize randomness over time.
        
        Args:
            measurements (list): List of measurement results
            window_size (int): Size of moving window for averaging
            save_path (str, optional): Path to save the figure
        
        Returns:
            matplotlib.figure.Figure: The figure object
        """
        # Calculate running average
        running_avg = []
        for i in range(len(measurements) - window_size + 1):
            window = measurements[i:i+window_size]
            avg = sum(window) / len(window)
            running_avg.append(avg)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        ax.plot(running_avg, linewidth=2, color='#3498db', label=f'Running Average (window={window_size})')
        ax.axhline(y=0.5, color='green', linestyle='--', linewidth=2, label='Ideal (0.5)')
        ax.fill_between(range(len(running_avg)), 0.45, 0.55, alpha=0.2, color='green', 
                        label='±5% tolerance')
        
        ax.set_xlabel('Measurement Index', fontsize=12, fontweight='bold')
        ax.set_ylabel('Average Bit Value', fontsize=12, fontweight='bold')
        ax.set_title('Randomness Quality Over Time', fontsize=14, fontweight='bold')
        ax.set_ylim(0, 1)
        ax.legend(loc='best')
        ax.grid(alpha=0.3, linestyle='--')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig


# Example usage
if __name__ == "__main__":
    from quantum_core import QuantumRandomNumberGenerator
    
    # Generate random bits
    qrng = QuantumRandomNumberGenerator(seed=42)
    measurements = qrng.generate_random_bits(num_measurements=1024)
    stats = qrng.get_statistics()
    
    # Create visualizations
    QuantumVisualizer.plot_measurement_histogram(measurements, 
                                                 save_path="measurement_histogram.png")
    QuantumVisualizer.plot_bloch_sphere(save_path="bloch_sphere.png")
    QuantumVisualizer.plot_statistics(stats, save_path="statistics.png")
    QuantumVisualizer.plot_bit_sequence(measurements, save_path="bit_sequence.png")
    
    print("Visualizations saved successfully!")
