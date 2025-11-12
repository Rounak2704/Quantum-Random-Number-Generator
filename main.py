"""
Command-line interface for the Quantum Random Number Generator.
Provides easy access to quantum randomness generation and analysis.
"""

import argparse
import sys
from quantum_core import QuantumRandomNumberGenerator
from visualizer import QuantumVisualizer
from utils import FileManager, RandomnessTests, FormatConverter


def print_header():
    """Print application header."""
    print("\n" + "="*60)
    print("  QUANTUM RANDOM NUMBER GENERATOR (QRNG)")
    print("  Using Qiskit and Single-Qubit Measurements")
    print("="*60 + "\n")


def generate_command(args):
    """Handle the generate command."""
    print(f"Generating {args.count} quantum random bits...")
    
    # Initialize QRNG
    qrng = QuantumRandomNumberGenerator(seed=args.seed)
    
    # Generate measurements
    measurements = qrng.generate_random_bits(num_measurements=args.count)
    
    # Get statistics
    stats = qrng.get_statistics()
    
    # Display results
    print("\n" + "-"*60)
    print("GENERATION RESULTS")
    print("-"*60)
    
    print(f"\nBinary (first 100 bits): {qrng.to_binary_string()[:100]}")
    print(f"Decimal: {qrng.to_decimal()}")
    print(f"Hexadecimal: {qrng.to_hex()}")
    print(f"Float [0,1): {qrng.to_float():.10f}")
    
    print("\n" + "-"*60)
    print("STATISTICS")
    print("-"*60)
    print(f"Total Measurements: {stats['total_measurements']}")
    print(f"Count of 0s: {stats['count_0']} ({stats['probability_0']*100:.2f}%)")
    print(f"Count of 1s: {stats['count_1']} ({stats['probability_1']*100:.2f}%)")
    print(f"Shannon Entropy: {stats['shannon_entropy']:.6f} / {stats['max_entropy']:.6f}")
    print(f"Entropy Ratio: {stats['entropy_ratio']:.4f} (Quality: {'Excellent' if stats['entropy_ratio'] > 0.95 else 'Good' if stats['entropy_ratio'] > 0.85 else 'Poor'})")
    
    # Save if requested
    if args.save:
        FileManager.save_measurements(measurements, args.save)
        print(f"\nMeasurements saved to {args.save}")
    
    if args.binary:
        FileManager.save_as_binary_file(measurements, args.binary)
    
    if args.hex:
        FileManager.save_as_hex_file(measurements, args.hex)
    
    return measurements, stats


def analyze_command(args):
    """Handle the analyze command."""
    print(f"Analyzing randomness quality of {args.count} measurements...")
    
    # Generate measurements
    qrng = QuantumRandomNumberGenerator(seed=args.seed)
    measurements = qrng.generate_random_bits(num_measurements=args.count)
    
    print("\n" + "-"*60)
    print("RANDOMNESS QUALITY TESTS")
    print("-"*60)
    
    # Chi-square test
    chi_square = RandomnessTests.chi_square_test(measurements)
    print(f"\nChi-Square Test:")
    print(f"  Chi-Square Statistic: {chi_square['chi_square_statistic']:.6f}")
    print(f"  P-Value: {chi_square['p_value']:.6f}")
    print(f"  Result: {'PASS' if chi_square['passes_test'] else 'FAIL'} ({chi_square['interpretation']})")
    
    # Runs test
    runs = RandomnessTests.runs_test(measurements)
    print(f"\nRuns Test:")
    print(f"  Runs Count: {runs['runs_count']}")
    print(f"  Expected Runs: {runs['expected_runs']:.2f}")
    print(f"  Z-Score: {runs['z_score']:.6f}")
    print(f"  P-Value: {runs['p_value']:.6f}")
    print(f"  Result: {'PASS' if runs['passes_test'] else 'FAIL'} ({runs['interpretation']})")
    
    # Entropy test
    entropy = RandomnessTests.entropy_test(measurements)
    print(f"\nEntropy Test:")
    print(f"  Shannon Entropy: {entropy['shannon_entropy']:.6f}")
    print(f"  Max Entropy: {entropy['max_entropy']:.6f}")
    print(f"  Entropy Ratio: {entropy['entropy_ratio']:.4f}")
    print(f"  Quality: {entropy['quality']}")
    
    # Overall assessment
    all_pass = chi_square['passes_test'] and runs['passes_test']
    print("\n" + "-"*60)
    print(f"OVERALL ASSESSMENT: {'EXCELLENT' if all_pass and entropy['entropy_ratio'] > 0.95 else 'GOOD' if all_pass else 'NEEDS IMPROVEMENT'}")
    print("-"*60)


def visualize_command(args):
    """Handle the visualize command."""
    print(f"Generating visualizations for {args.count} measurements...")
    
    # Generate measurements
    qrng = QuantumRandomNumberGenerator(seed=args.seed)
    measurements = qrng.generate_random_bits(num_measurements=args.count)
    stats = qrng.get_statistics()
    
    # Create visualizations
    print("Creating measurement histogram...")
    QuantumVisualizer.plot_measurement_histogram(measurements, 
                                                 save_path=args.output + "_histogram.png")
    
    print("Creating Bloch sphere visualization...")
    QuantumVisualizer.plot_bloch_sphere(save_path=args.output + "_bloch.png")
    
    print("Creating statistics plot...")
    QuantumVisualizer.plot_statistics(stats, save_path=args.output + "_stats.png")
    
    print("Creating bit sequence analysis...")
    QuantumVisualizer.plot_bit_sequence(measurements, save_path=args.output + "_sequence.png")
    
    print(f"\nVisualizations saved with prefix: {args.output}")


def compare_command(args):
    """Handle the compare command."""
    print(f"Comparing quantum vs classical randomness ({args.count} samples each)...")
    
    # Generate quantum random numbers
    qrng = QuantumRandomNumberGenerator(seed=args.seed)
    quantum_measurements = qrng.generate_random_bits(num_measurements=args.count)
    quantum_stats = qrng.get_statistics()
    
    # Get classical random statistics
    classical_stats = RandomnessTests.compare_with_classical_random(args.count)
    
    print("\n" + "-"*60)
    print("QUANTUM vs CLASSICAL RANDOMNESS")
    print("-"*60)
    
    print(f"\nQuantum Random Numbers ({args.count} samples):")
    print(f"  Count of 0s: {quantum_stats['count_0']} ({quantum_stats['probability_0']*100:.2f}%)")
    print(f"  Count of 1s: {quantum_stats['count_1']} ({quantum_stats['probability_1']*100:.2f}%)")
    print(f"  Shannon Entropy: {quantum_stats['shannon_entropy']:.6f}")
    print(f"  Entropy Ratio: {quantum_stats['entropy_ratio']:.4f}")
    
    print(f"\nClassical Random Numbers ({args.count} samples):")
    print(f"  Count of 0s: {classical_stats['count_0']} ({classical_stats['probability_0']*100:.2f}%)")
    print(f"  Count of 1s: {classical_stats['count_1']} ({classical_stats['probability_1']*100:.2f}%)")
    
    print("\n" + "-"*60)
    print("ANALYSIS")
    print("-"*60)
    print(f"Quantum entropy ratio is {quantum_stats['entropy_ratio']/classical_stats['probability_0']:.2f}x more uniform")


def main():
    """Main entry point."""
    print_header()
    
    parser = argparse.ArgumentParser(
        description="Quantum Random Number Generator using Qiskit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py generate --count 1024
  python main.py generate --count 256 --save results.json --binary random.bin
  python main.py analyze --count 2048
  python main.py visualize --count 1024 --output qrng
  python main.py compare --count 512
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Generate command
    gen_parser = subparsers.add_parser('generate', help='Generate quantum random numbers')
    gen_parser.add_argument('--count', type=int, default=1024, 
                           help='Number of measurements (default: 1024)')
    gen_parser.add_argument('--seed', type=int, default=None,
                           help='Random seed for reproducibility')
    gen_parser.add_argument('--save', type=str, help='Save measurements to JSON file')
    gen_parser.add_argument('--binary', type=str, help='Save as binary file')
    gen_parser.add_argument('--hex', type=str, help='Save as hexadecimal file')
    gen_parser.set_defaults(func=generate_command)
    
    # Analyze command
    ana_parser = subparsers.add_parser('analyze', help='Analyze randomness quality')
    ana_parser.add_argument('--count', type=int, default=2048,
                           help='Number of measurements (default: 2048)')
    ana_parser.add_argument('--seed', type=int, default=None,
                           help='Random seed for reproducibility')
    ana_parser.set_defaults(func=analyze_command)
    
    # Visualize command
    vis_parser = subparsers.add_parser('visualize', help='Generate visualizations')
    vis_parser.add_argument('--count', type=int, default=1024,
                           help='Number of measurements (default: 1024)')
    vis_parser.add_argument('--seed', type=int, default=None,
                           help='Random seed for reproducibility')
    vis_parser.add_argument('--output', type=str, default='qrng',
                           help='Output file prefix (default: qrng)')
    vis_parser.set_defaults(func=visualize_command)
    
    # Compare command
    cmp_parser = subparsers.add_parser('compare', help='Compare quantum vs classical randomness')
    cmp_parser.add_argument('--count', type=int, default=1024,
                           help='Number of samples for each (default: 1024)')
    cmp_parser.add_argument('--seed', type=int, default=None,
                           help='Random seed for reproducibility')
    cmp_parser.set_defaults(func=compare_command)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == "__main__":
    main()
