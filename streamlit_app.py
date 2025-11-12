"""
Streamlit web interface for the Quantum Random Number Generator.
Provides an interactive, user-friendly interface for quantum randomness generation.
"""

import streamlit as st
import sys
import os
from pathlib import Path

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from quantum_core import QuantumRandomNumberGenerator
from visualizer import QuantumVisualizer
from utils import FileManager, RandomnessTests, FormatConverter
import matplotlib.pyplot as plt


# Page configuration
st.set_page_config(
    page_title="Quantum Random Number Generator",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables."""
    if 'qrng' not in st.session_state:
        st.session_state.qrng = None
    if 'measurements' not in st.session_state:
        st.session_state.measurements = None
    if 'stats' not in st.session_state:
        st.session_state.stats = None


def main():
    """Main Streamlit application."""
    init_session_state()
    
    # Header
    st.title("⚛️ Quantum Random Number Generator")
    st.markdown("Generate true random numbers using quantum mechanics and Qiskit")
    
    # Sidebar configuration
    st.sidebar.header("Configuration")
    
    num_measurements = st.sidebar.slider(
        "Number of Measurements",
        min_value=64,
        max_value=10000,
        value=1024,
        step=64,
        help="Number of quantum measurements to perform"
    )
    
    use_seed = st.sidebar.checkbox("Use Random Seed", value=False)
    seed = None
    if use_seed:
        seed = st.sidebar.number_input("Seed Value", value=42, step=1)
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Generate", "Analyze", "Visualize", "Compare", "About"
    ])
    
    # TAB 1: Generate
    with tab1:
        st.header("Generate Quantum Random Numbers")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Generate Random Numbers", key="gen_btn", use_container_width=True):
                with st.spinner("Generating quantum random numbers..."):
                    qrng = QuantumRandomNumberGenerator(seed=seed)
                    measurements = qrng.generate_random_bits(num_measurements=num_measurements)
                    stats = qrng.get_statistics()
                    
                    st.session_state.qrng = qrng
                    st.session_state.measurements = measurements
                    st.session_state.stats = stats
                    
                    st.success("Random numbers generated successfully!")
        
        if st.session_state.measurements is not None:
            st.divider()
            
            # Display results
            st.subheader("Results")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Bits", st.session_state.stats['total_measurements'])
            
            with col2:
                st.metric("Count of 0s", st.session_state.stats['count_0'])
            
            with col3:
                st.metric("Count of 1s", st.session_state.stats['count_1'])
            
            with col4:
                entropy_ratio = st.session_state.stats['entropy_ratio']
                quality = "Excellent" if entropy_ratio > 0.95 else "Good" if entropy_ratio > 0.85 else "Poor"
                st.metric("Entropy Ratio", f"{entropy_ratio:.4f}", delta=quality)
            
            st.divider()
            
            # Display formats
            st.subheader("Output Formats")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Binary (first 100 bits):**")
                binary_str = st.session_state.qrng.to_binary_string()
                st.code(binary_str[:100], language="text")
            
            with col2:
                st.write("**Decimal:**")
                st.code(str(st.session_state.qrng.to_decimal()), language="text")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Hexadecimal:**")
                st.code(st.session_state.qrng.to_hex(), language="text")
            
            with col2:
                st.write("**Float [0,1):**")
                st.code(f"{st.session_state.qrng.to_float():.10f}", language="text")
            
            st.divider()
            
            # Download options
            st.subheader("Download Results")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                json_data = FileManager.save_measurements(
                    st.session_state.measurements, 
                    "temp.json"
                )
                with open("temp.json", "r") as f:
                    st.download_button(
                        label="Download as JSON",
                        data=f.read(),
                        file_name="quantum_measurements.json",
                        mime="application/json"
                    )
            
            with col2:
                binary_str = st.session_state.qrng.to_binary_string()
                st.download_button(
                    label="Download as Binary",
                    data=binary_str,
                    file_name="quantum_random.bin",
                    mime="text/plain"
                )
            
            with col3:
                hex_str = st.session_state.qrng.to_hex()
                st.download_button(
                    label="Download as Hex",
                    data=hex_str,
                    file_name="quantum_random.hex",
                    mime="text/plain"
                )
    
    # TAB 2: Analyze
    with tab2:
        st.header("Randomness Quality Analysis")
        
        if st.button("Run Analysis", key="ana_btn", use_container_width=True):
            if st.session_state.measurements is None:
                st.warning("Please generate random numbers first in the Generate tab.")
            else:
                with st.spinner("Running randomness tests..."):
                    measurements = st.session_state.measurements
                    
                    # Chi-square test
                    chi_square = RandomnessTests.chi_square_test(measurements)
                    
                    # Runs test
                    runs = RandomnessTests.runs_test(measurements)
                    
                    # Entropy test
                    entropy = RandomnessTests.entropy_test(measurements)
                    
                    st.success("Analysis complete!")
                    
                    # Display results
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        status = "PASS" if chi_square['passes_test'] else "FAIL"
                        st.metric(
                            "Chi-Square Test",
                            status,
                            delta=f"p-value: {chi_square['p_value']:.4f}"
                        )
                    
                    with col2:
                        status = "PASS" if runs['passes_test'] else "FAIL"
                        st.metric(
                            "Runs Test",
                            status,
                            delta=f"p-value: {runs['p_value']:.4f}"
                        )
                    
                    with col3:
                        st.metric(
                            "Entropy Quality",
                            entropy['quality'],
                            delta=f"Ratio: {entropy['entropy_ratio']:.4f}"
                        )
                    
                    st.divider()
                    
                    # Detailed results
                    st.subheader("Detailed Test Results")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Chi-Square Test**")
                        st.write(f"- Statistic: {chi_square['chi_square_statistic']:.6f}")
                        st.write(f"- P-Value: {chi_square['p_value']:.6f}")
                        st.write(f"- Interpretation: {chi_square['interpretation']}")
                    
                    with col2:
                        st.write("**Runs Test**")
                        st.write(f"- Runs Count: {runs['runs_count']}")
                        st.write(f"- Expected: {runs['expected_runs']:.2f}")
                        st.write(f"- Z-Score: {runs['z_score']:.6f}")
                    
                    st.write("**Entropy Analysis**")
                    st.write(f"- Shannon Entropy: {entropy['shannon_entropy']:.6f}")
                    st.write(f"- Max Entropy: {entropy['max_entropy']:.6f}")
                    st.write(f"- Entropy Ratio: {entropy['entropy_ratio']:.4f}")
    
    # TAB 3: Visualize
    with tab3:
        st.header("Visualizations")
        
        if st.button("Generate Visualizations", key="vis_btn", use_container_width=True):
            if st.session_state.measurements is None:
                st.warning("Please generate random numbers first in the Generate tab.")
            else:
                with st.spinner("Generating visualizations..."):
                    measurements = st.session_state.measurements
                    stats = st.session_state.stats
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("Measurement Histogram")
                        fig = QuantumVisualizer.plot_measurement_histogram(measurements)
                        st.pyplot(fig)
                        plt.close(fig)
                    
                    with col2:
                        st.subheader("Bloch Sphere")
                        fig = QuantumVisualizer.plot_bloch_sphere()
                        st.pyplot(fig)
                        plt.close(fig)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("Statistics")
                        fig = QuantumVisualizer.plot_statistics(stats)
                        st.pyplot(fig)
                        plt.close(fig)
                    
                    with col2:
                        st.subheader("Bit Sequence Analysis")
                        fig = QuantumVisualizer.plot_bit_sequence(measurements)
                        st.pyplot(fig)
                        plt.close(fig)
    
    # TAB 4: Compare
    with tab4:
        st.header("Quantum vs Classical Randomness")
        
        if st.button("Run Comparison", key="cmp_btn", use_container_width=True):
            with st.spinner("Comparing quantum and classical randomness..."):
                # Generate quantum
                qrng = QuantumRandomNumberGenerator(seed=seed)
                quantum_measurements = qrng.generate_random_bits(num_measurements=num_measurements)
                quantum_stats = qrng.get_statistics()
                
                # Get classical
                classical_stats = RandomnessTests.compare_with_classical_random(num_measurements)
                
                st.success("Comparison complete!")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Quantum Random Numbers")
                    st.metric("Count of 0s", quantum_stats['count_0'])
                    st.metric("Count of 1s", quantum_stats['count_1'])
                    st.metric("Probability of 0", f"{quantum_stats['probability_0']:.4f}")
                    st.metric("Probability of 1", f"{quantum_stats['probability_1']:.4f}")
                    st.metric("Shannon Entropy", f"{quantum_stats['shannon_entropy']:.6f}")
                
                with col2:
                    st.subheader("Classical Random Numbers")
                    st.metric("Count of 0s", classical_stats['count_0'])
                    st.metric("Count of 1s", classical_stats['count_1'])
                    st.metric("Probability of 0", f"{classical_stats['probability_0']:.4f}")
                    st.metric("Probability of 1", f"{classical_stats['probability_1']:.4f}")
                
                st.divider()
                
                st.subheader("Analysis")
                st.write("""
                **Key Differences:**
                - Quantum randomness is based on fundamental quantum mechanics principles
                - Classical randomness uses pseudo-random algorithms
                - Quantum randomness is theoretically more uniform and unpredictable
                - Both should pass statistical randomness tests
                """)
    
    # TAB 5: About
    with tab5:
        st.header("About Quantum Random Number Generator")
        
        st.markdown("""
        ## How It Works
        
        This application generates true random numbers using quantum mechanics principles:
        
        1. **Quantum Superposition**: A single qubit is initialized in the |0⟩ state
        2. **Hadamard Gate**: Applied to create an equal superposition of |0⟩ and |1⟩
        3. **Measurement**: The qubit is measured, collapsing to either 0 or 1 with 50% probability
        4. **Repetition**: This process is repeated to generate multiple random bits
        
        ## Why Quantum Randomness?
        
        - **True Randomness**: Based on quantum mechanics, not pseudo-random algorithms
        - **Unpredictable**: Cannot be predicted even with perfect knowledge of the system
        - **Uniform Distribution**: Theoretically produces perfectly uniform random bits
        - **Cryptographic Quality**: Suitable for security-critical applications
        
        ## Technology Stack
        
        - **Qiskit**: IBM's quantum computing framework
        - **Streamlit**: Interactive web interface
        - **Matplotlib**: Visualization
        - **SciPy**: Statistical analysis
        
        ## Statistical Tests
        
        The application includes several randomness quality tests:
        
        - **Chi-Square Test**: Tests if the distribution matches expected probabilities
        - **Runs Test**: Detects clustering or patterns in the sequence
        - **Shannon Entropy**: Measures the information content and uniformity
        
        ## References
        
        - [Qiskit Documentation](https://qiskit.org/)
        - [Quantum Computing Basics](https://en.wikipedia.org/wiki/Quantum_computing)
        - [Random Number Generation](https://en.wikipedia.org/wiki/Random_number_generation)
        """)


if __name__ == "__main__":
    main()
