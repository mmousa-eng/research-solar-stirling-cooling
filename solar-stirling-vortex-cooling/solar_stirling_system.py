# solar_stirling_system.py

"""
This module combines the solar collector, Stirling engine, compressor, and vortex tube into a unified simulation algorithm.
It includes methods to calculate power output, compressor load, cooling capacity, and other relevant metrics.
"""

from constants import SOLAR_IRRADIANCE, STIRLING_EFFICIENCY, COMPRESSOR_EFFICIENCY, VORTEX_COOLING_CAPACITY

class SolarCollector:
    def __init__(self, area):
        self.area = area

    def calculate_power_output(self, solar_irradiance):
        return self.area * solar_irradiance * STIRLING_EFFICIENCY

class StirlingEngine:
    def __init__(self, efficiency):
        self.efficiency = efficiency

    def calculate_output(self, input_power):
        return input_power * self.efficiency

class Compressor:
    def __init__(self, efficiency):
        self.efficiency = efficiency

    def calculate_load(self, cooling_capacity):
        return cooling_capacity / self.efficiency

class VortexTube:
    def __init__(self, cooling_capacity):
        self.cooling_capacity = cooling_capacity

    def calculate_cooling_effect(self):
        return self.cooling_capacity * VORTEX_COOLING_CAPACITY

class SolarStirlingSystem:
    def __init__(self, collector_area, engine_efficiency, compressor_efficiency):
        self.collector = SolarCollector(collector_area)
        self.engine = StirlingEngine(engine_efficiency)
        self.compressor = Compressor(compressor_efficiency)
        self.vortex_tube = VortexTube(0)  # Initialize with zero cooling capacity

    def run_simulation(self, solar_irradiance):
        power_output = self.collector.calculate_power_output(solar_irradiance)
        engine_output = self.engine.calculate_output(power_output)
        cooling_capacity = self.vortex_tube.calculate_cooling_effect()
        compressor_load = self.compressor.calculate_load(cooling_capacity)

        return {
            'power_output': power_output,
            'engine_output': engine_output,
            'cooling_capacity': cooling_capacity,
            'compressor_load': compressor_load
        }

    def set_vortex_cooling_capacity(self, capacity):
        self.vortex_tube.cooling_capacity = capacity