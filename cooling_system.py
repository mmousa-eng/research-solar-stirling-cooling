import math
from scipy.optimize import fsolve
from vortex_correlation import predicted_DTc
from constants import *

def calculate_T_L_out(Q_dot_L_Load, T_L_in):
    """Return outlet temperature of water from the load side."""
    return T_L_in - (Q_dot_L_Load / (m_dot_w * c_p_w))

def calculate_heat_transfers(T_I, T_L_out, T_L_in):
    """Compute the load side transfer and supplemental heat rates."""
    Q_12 = m * R_g * T_I * math.log(v_1 / v_2)
    Q_1_1 = m * c_v * (T_I - T_L_out) * (1 - epsilon_r)
    Q_L = Q_1_1 + Q_12
    Q_dot_L_Supplement = F * Q_L

    fraction = (T_I - T_L_in) / max((T_I - T_L_out), 1e-6)
    Q_dot_L_Transfer = K_L * ((T_I - T_L_in) - (T_I - T_L_out)) / math.log(fraction)

    return Q_dot_L_Transfer, Q_dot_L_Supplement

def calculate_Q_dot_H_Supplement(I, T_H, V_wind, T_amb, T_sky):
    """Heat input from solar and convection/radiation losses."""
    h_c = 5.7 + 3.8 * V_wind
    return (
        I * A_R * C * eta_optical
        - h_c * A_R * (T_H - T_amb)
        - epsilon * sigma * A_R * (T_H**4 - T_sky**4)
    )

def calculate_all_heat_transfers(T_I, T_h):
    """Calculate heat transfer and load on the hot side."""
    Q_3_3_prime = m * c_v * (T_h - T_I) * (1 - epsilon_r)
    Q_34 = m * R_g * T_h * math.log(v_4 / v_3)
    Q_H = Q_3_3_prime + Q_34
    Q_dot_H_Load = F * Q_H
    Q_dot_H_Transfer = K_H * (T_h - T_I)
    return {'Q_dot_H_Load': Q_dot_H_Load, 'Q_dot_H_Transfer': Q_dot_H_Transfer}

def find_T_I(T_L_out, T_L_in):
    """Numerically solve for intermediate temperature T_I."""
    T_I_low = T_L_out + 1
    T_I_high = 900
    tolerance = 0.1

    for _ in range(100):
        T_I = (T_I_low + T_I_high) / 2
        Q_dot_L_Transfer, Q_dot_L_Supplement = calculate_heat_transfers(T_I, T_L_out, T_L_in)
        difference = Q_dot_L_Transfer - Q_dot_L_Supplement
        if abs(difference) < tolerance:
            break
        if difference < 0:
            T_I_low = T_I
        else:
            T_I_high = T_I
    return T_I

def find_T_h(T_I, I, V_wind, T_amb, T_sky):
    """Numerically solve for hot side temperature T_h."""
    def balance(T_h):
        return calculate_Q_dot_H_Supplement(I, T_h, V_wind, T_amb, T_sky) - calculate_all_heat_transfers(T_I, T_h)['Q_dot_H_Load']

    return fsolve(balance, T_I + 1)[0]

def calculate_power(T_h, T_l):
    """Calculate output power (kW)."""
    return F * m * R_g * (T_h - T_l) * math.log(v_4 / v_3) / 1000

def run_simulation(I, V_wind, T_amb):
    """Full simulation of the solar-Stirling-vortex system."""
    T_L_in = T_amb
    T_sky = 0.0552 * T_amb ** 1.5
    T_L_out = T_L_in + 10

    T_I = find_T_I(T_L_out, T_L_in)
    Q_dot_L_Load = -m_dot_w * c_p_w * (T_L_out - T_L_in)
    T_L_out = calculate_T_L_out(Q_dot_L_Load, T_L_in)

    T_h = find_T_h(T_I, I, V_wind, T_amb, T_sky)
    T_l = T_I

    P = calculate_power(T_h, T_l)
    Q_dot_H_Supplement = calculate_Q_dot_H_Supplement(I, T_h, V_wind, T_amb, T_sky)

    return P, Q_dot_H_Supplement

    # Integrating compressor & vortex tube with the solar SE system
def simulate_cooling_system(I=700, T1=298, Cp=1.004, P1=1, P2=3, k=1.4, R=0.287, T_amb=293.15):
    # Convert pressures to kPa
    P1_kPa = P1 * 100
    P2_kPa = P2 * 100

    # Compressor work and densities
    T2 = T1 * (P2_kPa / P1_kPa) ** ((k - 1) / k)
    Wc = Cp * (T2 - T1)
    d1 = P1_kPa / (R * T1)
    d2 = P2_kPa / (R * T2)

    # Call solar system simulation
    P_solar = run_simulation(I, V_wind=0, T_amb=T_amb)  # Or use actual values

    # Vortex tube DTc predictions for different mue and Pe values
    Pe_V_values = [4, 5, 6, 7]
    mue_V_values = [0.35, 0.45, 0.55, 0.65]

    vortex_results = []
    for mue in mue_V_values:
        for Pe in Pe_V_values:
            DTc = predicted_DTc(mue, Pe)
            Tc = T_amb - DTc
            vortex_results.append({'mue': mue, 'Pe': Pe, 'DTc': DTc, 'Tc': Tc})

    return {
        'Compressor Work (W)': Wc,
        'Inlet Temp (T1)': T1,
        'Outlet Temp (T2)': T2,
        'Solar Power (kW)': P_solar,
        'Vortex Cooling Results': vortex_results
    }
