# constants.py
T_amb = 293.15
A_R = 0.0491
C = 1250
eta_optical = 0.8
epsilon = 0.8
sigma = 5.67e-8
K_H = 300
K_L = 500
m = 8e-4
c_v = 3116
R_g = 2077
epsilon_r = 0.8
F = 25
m_dot_w = 0.4
c_p_w = 4180
v_1 = v_4 = 1.3
v_2 = v_3 = 0.6
T_H = 900             # Assumed hot side temperature (K)
T_l_initial = 300     # Initial lower temp for iteration (K)

# Vortex tube constants
Ti_V = T_amb
mue_V = 0.37
Pe_V = 6.92
MIN_V_DOT = 0.00466

# Compressor constants
T1 = T_amb
Cp = 1.004
P1 = 100  # (1 * 100)
P2 = 300  # (3 * 100)
k = 1.4
R = 0.287