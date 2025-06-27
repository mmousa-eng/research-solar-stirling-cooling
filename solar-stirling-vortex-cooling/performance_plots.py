import matplotlib.pyplot as plt
import numpy as np

def plot_solar_irradiance_vs_power_output(irradiance, power_output):
    plt.figure(figsize=(10, 6))
    plt.plot(irradiance, power_output, marker='o', linestyle='-', color='b')
    plt.title('Solar Irradiance vs Power Output')
    plt.xlabel('Solar Irradiance (W/m²)')
    plt.ylabel('Power Output (W)')
    plt.grid()
    plt.savefig('results/solar_irradiance_vs_power_output.png')
    plt.close()

def plot_pressure_ratio_vs_cooling_effect(pressure_ratios, cooling_effects):
    plt.figure(figsize=(10, 6))
    plt.plot(pressure_ratios, cooling_effects, marker='s', linestyle='-', color='r')
    plt.title('Pressure Ratio vs Cooling Effect')
    plt.xlabel('Pressure Ratio')
    plt.ylabel('Cooling Effect (W)')
    plt.grid()
    plt.savefig('results/pressure_ratio_vs_cooling_effect.png')
    plt.close()

def main():
    # Example data for plotting
    irradiance = np.array([200, 400, 600, 800, 1000])
    power_output = np.array([0, 50, 100, 150, 200])
    
    pressure_ratios = np.array([1, 1.5, 2, 2.5, 3])
    cooling_effects = np.array([0, 20, 40, 60, 80])
    
    plot_solar_irradiance_vs_power_output(irradiance, power_output)
    plot_pressure_ratio_vs_cooling_effect(pressure_ratios, cooling_effects)

if __name__ == "__main__":
    main()