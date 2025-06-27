import os
import constants
from vortex_correlation import calculate_vortex_correlation
from solar_stirling_system import SolarStirlingSystem
from performance_plots import plot_performance

def main():
    # Create results directory if it doesn't exist
    if not os.path.exists('results'):
        os.makedirs('results')

    # Initialize the solar Stirling system
    system = SolarStirlingSystem()

    # Run the simulation
    power_output, compressor_load, cooling_capacity = system.run_simulation()

    # Calculate vortex correlation
    vortex_correlation = calculate_vortex_correlation()

    # Save results to a file
    with open('results/simulation_results.txt', 'w') as f:
        f.write(f'Power Output: {power_output}\n')
        f.write(f'Compressor Load: {compressor_load}\n')
        f.write(f'Cooling Capacity: {cooling_capacity}\n')
        f.write(f'Vortex Correlation: {vortex_correlation}\n')

    # Generate performance plots
    plot_performance()

if __name__ == '__main__':
    main()