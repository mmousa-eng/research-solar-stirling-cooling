# 🔍 Research: Solar-Powered Stirling-Vortex Cooling: A Novel Hybrid System for Sustainable Refrigeration
This repository contains the simulation and analysis of a novel solar-powered Stirling engine integrated with a compressor and vortex tube system to provide sustainable cooling and power.

Technologies: Python • NumPy • Matplotlib • Thermodynamic Modeling • Solar Stirling Engine 

## 📈 Objective
Simulation and performance analysis of solar-powered Stirling-vortex cooling hybrid system


research-solar-stirling-cooling/
│
├── main.py
│   # The main entry point. Runs the simulation, saves results, and generates all performance plots.
│
├── constants.py
│   # Contains all physical and simulation constants used throughout the project (temperatures, pressures, Cp, etc.).
│
├── vortex_correlation.py
│   # Contains the function(s) to calculate vortex tube performance/correlation.
│
├── performance_plots.py
│   # Contains all plotting functions for visualizing simulation results (I vs P, I vs CC, I vs η_tot, etc.).
│
├── solar_stirling_system.py
│   # (Assumed from your import) Contains the SolarStirlingSystem class, which models and runs the main system simulation.
│
├── results/
│   # Directory where all output files and generated plots are saved.
│   # - simulation_results.txt: Text file with main simulation results.
│   # - *.png: All generated plots.
│
├── __pycache__/
│   # Python cache directory for compiled .pyc files (auto-generated).
│
├── README.md
│   # Project overview, instructions, and documentation.
