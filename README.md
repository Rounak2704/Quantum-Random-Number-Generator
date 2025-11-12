# ⚛️ Quantum Random Number Generator using Single Qubit Measurements

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Qiskit](https://img.shields.io/badge/Qiskit-Latest-purple.svg)](https://qiskit.org)
[![Platform](https://img.shields.io/badge/Platform-Quantum%20Simulator-lightblue.svg)]()

A **Quantum Random Number Generator (QRNG)** built using **single-qubit measurements** to generate true randomness based on quantum mechanics.  
This project demonstrates how measuring a qubit in superposition can produce **genuine unpredictable results**, unlike classical pseudo-random generators.

---

## 🚀 Features

- 🧩 **Single-Qubit Quantum Measurements** — Generates randomness through quantum superposition and collapse.  
- ⚛️ **Hadamard Gate Application** — Prepares qubits in a perfect 50–50 superposition.  
- 🔢 **Multiple Output Formats** — Binary, decimal, and hexadecimal random numbers.  
- 📊 **Visualization** — Plot histograms of measurement outcomes and view Bloch sphere representations.  
- 💾 **Data Export** — Save generated random sequences to text or CSV files.  
- 🔍 **Comparison Mode** — Compare quantum randomness with Python’s pseudo-random module.  
- 🧠 **Extensible Design** — Modular code for integration with real IBM Quantum hardware.  

---

## 🏗️ Architecture

- **Language**: Python 3.8+
- **Quantum SDK**: Qiskit
- **Visualization**: Matplotlib, Plotly (optional)
- **Interface (optional)**: Streamlit or Tkinter GUI
- **Storage**: Local file-based storage for random outputs

---

## 📋 Prerequisites

- Python 3.8 or above
- pip (Python package manager)
- Internet connection (for Qiskit installation)
- IBM Quantum account (optional, for real hardware execution)

---

## 🛠️ Installation

### Quick Start

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/quantum-rng.git
   cd quantum-rng
   ```

2. **Create and Activate a Virtual Environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux / macOS
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Web Interface 

**Launch the interactive Streamlit web application :**

```bash
streamlit run scripts/streamlit_app.py
```

- On Windows, if the above doesn't work :
  ```bash
  python -m streamlit run scripts/streamlit_app.py
  ```

- Then open your browser to `http://localhost:8501`

## 🎯 Usage

**Command-Line Interface**

1. Choose number of measurements:
   ```bash
   Enter number of random bits to generate: 100
   ```

2. Select output format (binary/decimal/hex):
   ```bash
   Choose format: binary
   ```

3. View output:
   ```bash
   Generated Quantum Random Bits:
   01011001101011100101
   ```
   
# 📊 Visualization

**The project includes visualization options such as :**

- **Measurement Histogram** — Shows distribution of 0s and 1s

- **Bloch Sphere** — Displays qubit state evolution

- **Comparison Graphs** — Quantum vs Classical randomness

  
# 📁 Project Structure

```bash
quantum_rng/
├── main.py                # Main application entry point
├── quantum_core.py        # Quantum circuit logic (Hadamard, measurement)
├── visualizer.py          # Plotting and visualization functions
├── utils.py               # Helper functions
├── app.py                 # Optional Streamlit/Tkinter GUI
├── requirements.txt       # Dependencies list
├── README.md              # Documentation
└── outputs/
    └── random_numbers.txt # Generated random outputs
```

# ⚙️ Core Components
## 🧠 Quantum Logic

- Uses a Hadamard gate (H) to put the qubit into superposition.

- Measurement collapses qubit into |0⟩ or |1⟩ randomly.

- Each measurement contributes to the final random sequence.

## 🔢 Random Data Generation

- Generates n quantum bits.

- Converts binary results into integer or hexadecimal forms.

- Stores results locally or prints to console.

## 📈 Visualization

- Plots probability distribution of outcomes.

- Optional Bloch sphere to illustrate quantum states.

# 📦 Requirements

```nginx
qiskit
matplotlib
numpy
plotly
streamlit
```

# 🧰 **Future Enhancements**

- 🔗 Integration with IBM Quantum Hardware

- 🧮 Statistical randomness tests (NIST suite)

- ☁️ Cloud-based QRNG API

- 💻 Web dashboard for visualization and history tracking

# 📘 **References**

- Qiskit Documentation

- IBM Quantum Experience

- Quantum Randomness - Nature Physics

# 🙏 **Acknowledgments**

- IBM Quantum and Qiskit Community

- Matplotlib and Streamlit Contributors

- Researchers in Quantum Information Science
