import os
import matplotlib.pyplot as plt
from cooling_system import run_simulation
from constants import T_amb, A_R, C, eta_optical
from constants import Cp, T1, P1, P2, k, R, Ti_V, Pe_V, mue_V, MIN_V_DOT

def plot_I_vs_P_by_wind(T_amb=293.15):
    plt.close('all')  # Clear previous figures to avoid repeated lines
    """Plot solar irradiance (I) vs. power output (P) for different wind speeds."""
    I_values = range(500, 1001, 50)
    V_wind_values = [0, 4, 8, 12]
    colors = ['black', 'red', 'blue', 'green']
    markers = ['o', '^', 's', 'v']

    plt.figure(figsize=(8, 6))
    for V_wind, color, marker in zip(V_wind_values, colors, markers):
        # Only take the first value (P) from run_simulation's output
        P_values = [run_simulation(I, V_wind, T_amb)[0] for I in I_values]
        plt.plot(I_values, P_values, color=color, linestyle='-', marker=marker, markersize=6,
                 fillstyle='full', linewidth=2, label=f'$V_{{wind}} = {V_wind}$ m/s')

    plt.legend(loc='lower right', fontsize=14)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlim(450, 1050)
    plt.ylim(8, 26)
    plt.xlabel("Solar Irradiance (W/m²)", fontsize=16)
    plt.ylabel("Power Output (kW)", fontsize=16)
    plt.title("Effect of Wind Speed on Power Output", fontsize=16)
    # plt.grid(True)
    plt.tight_layout()
    plt.savefig("results/I_vs_P_by_wind.png", dpi=300)
    plt.show()

def plot_I_vs_P_by_Tamb(V_wind=0):
    plt.close('all')  # Clear previous figures to avoid repeated lines
    """Plot solar irradiance (I) vs. power output (P) for different ambient temperatures."""
    I_values = range(500, 1001, 50)
    T_amb_values = [280, 290, 300, 310]
    colors = ['black', 'red', 'blue', 'green']
    markers = ['o', '^', 's', 'v']

    plt.figure(figsize=(8, 6))
    for T_amb, color, marker in zip(T_amb_values, colors, markers):
        # Only take the first value (P) from run_simulation's output
        P_values = [run_simulation(I, V_wind, T_amb)[0] for I in I_values]
        plt.plot(I_values, P_values, color=color, linestyle='-', marker=marker, markersize=6,
                 fillstyle='full', linewidth=2, label=f'$T_{{amb}} = {T_amb}$ K')

    plt.legend(loc='lower right', fontsize=14)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlim(450, 1050)
    plt.ylim(8, 26)
    plt.xlabel("Solar Irradiance (W/m²)", fontsize=16)
    plt.ylabel("Power Output (kW)", fontsize=16)
    plt.title("Effect of Ambient Temperature on Power Output", fontsize=16)
    # plt.grid(True)
    plt.tight_layout()
    plt.savefig("results/I_vs_P_by_Tamb.png", dpi=300)
    plt.show()

def plot_Pe_vs_DTc():
    Ti_V = T_amb
    Pe_V_values = [4, 5, 6, 7]
    mue_V_values = [0.35, 0.45, 0.55, 0.65]
    colors = ['black', 'red', 'blue', 'green']
    markers = ['o', '^', 's', 'v']  # Circle, Up Triangle, Square, Down Triangle

    plt.figure(figsize=(8, 6))
    for mue_V, color, marker in zip(mue_V_values, colors, markers):
        DTc_values = []
        for Pe_V in Pe_V_values:
            Tc_V = Ti_V * (1 - 0.020461 * (mue_V ** -0.593505) * (Pe_V ** 0.199128) *
                           (4 ** -0.128615) * (0.155 ** -0.011456) * (10 ** 0.027844))
            DTc = Ti_V - Tc_V
            DTc_values.append(DTc)
        plt.plot(Pe_V_values, DTc_values, color=color, linestyle='-', marker=marker,
                 markersize=6, fillstyle='full', linewidth=2, label=f'$\\mu = {mue_V}$')

    plt.legend(loc='lower right', fontsize=20)
    plt.xticks(Pe_V_values, [str(int(x)) for x in Pe_V_values], fontsize=20)
    plt.yticks(fontsize=20)
    plt.xlim(3, 8)
    plt.yticks(range(8, 17, 2))
    plt.xlabel("Pe")
    plt.ylabel("DTc (K)")
    plt.title("Pe vs DTc for different μ values")
    # plt.grid(True)
    plt.tight_layout()
    plt.savefig("results/Pe_vs_DTc.png", dpi=300)
    plt.show()

def plot_I_vs_CC_by_Pe():

    I_values = range(500, 1001, 50)
    Pe_V_values = [4, 5, 6, 7]  # Different Pe lines
    mue_V = 0.37  # Fixed mue
    MIN_V_DOT = 0.00466
    Cp = 1.004
    T1 = 298
    P1 = 1 * 100
    P2 = 3 * 100
    k = 1.4
    R = 0.287
    d1 = P1 / (R * T1)
    d2 = P2 / (R * (T1 * (P2 / P1) ** ((k - 1) / k)))
    Wc = Cp * (T1 * (P2 / P1) ** ((k - 1) / k) - T1)
    Ti_V = 293.15
    V_wind = 0
    T_amb = 293.15

    # Colors reversed: green for Pe=4, blue for Pe=5, red for Pe=6, black for Pe=7
    colors = ['green', 'blue', 'red', 'black']
    markers = ['o', '^', 's', 'v']

    plt.figure(figsize=(8, 6))

    for Pe_V, color, marker in zip(Pe_V_values, colors, markers):
        CC_values = []
        for I in I_values:
            P, Q_dot_H_Supplement = run_simulation(I, V_wind, T_amb)
            m_dot = P / Wc
            Tc_V = Ti_V * (1 - 0.020461 * (mue_V ** -0.593505) * (Pe_V ** 0.199128) * (4 ** -0.128615) * (0.155 ** -0.011456) * (10 ** 0.027844))
            CC = -m_dot * Cp * (Tc_V - Ti_V)
            CC_values.append(CC)

        # Plot this Pe line
        plt.plot(I_values, CC_values, color=color, marker=marker, label=f"$Pe = {Pe_V}$", linewidth=2)

    # Plot settings
    plt.xlabel("Irradiance $I$ (W/m²)", fontsize=18)
    plt.ylabel("Cooling Capacity $CC$ (kW)", fontsize=18)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.ylim(top=3.5)  # Set Y-axis upper limit to 3.5
    plt.legend(loc='lower right', fontsize=16)
    # plt.grid(True)
    plt.tight_layout()

    # Save the plot
    os.makedirs("results", exist_ok=True)
    plt.savefig("results/I_vs_CC_by_Pe.png", dpi=300)
    plt.show()

def plot_I_vs_CC_by_mue():

    # Constants
    Cp = 1.004
    Ti_V = 293.15
    Pe_V = 6.92
    mue_V_values = [0.35, 0.45, 0.55, 0.65]
    colors = ['black', 'red', 'blue', 'green']
    markers = ['o', '^', 's', 'v']
    I_values = range(500, 1001, 100)

    # Compressor constants
    T1 = 298
    P1 = 100
    P2 = 300
    k = 1.4
    R = 0.287
    T2 = T1 * (P2 / P1) ** ((k - 1) / k)
    Wc = Cp * (T2 - T1)

    # Plot setup
    plt.figure(figsize=(8, 6))
    for mue_V, color, marker in zip(mue_V_values, colors, markers):
        CC_values = []
        for I in I_values:
            P, _ = run_simulation(I, V_wind=0, T_amb=293.15)
            m_dot = P / Wc
            Tc_V = Ti_V * (1 - 0.020461 * (mue_V ** -0.593505)
                           * (Pe_V ** 0.199128) * (4 ** -0.128615)
                           * (0.155 ** -0.011456) * (10 ** 0.027844))
            CC = -m_dot * Cp * (Tc_V - Ti_V)
            CC_values.append(CC)

        plt.plot(I_values, CC_values, color=color, linestyle='-', marker=marker,
                 label=f'$\\mu = {mue_V}$', linewidth=2)

    plt.xlabel("Irradiance $I$ (W/m²)", fontsize=18)
    plt.ylabel("Cooling Capacity CC (kW)", fontsize=18)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.legend(loc='lower right', fontsize=16)
    plt.tight_layout()
    plt.savefig("results/I_vs_CC_by_mue.png", dpi=300)
    plt.show()

def plot_I_vs_CC_by_Ta():
    """
    Plot I vs CC for different ambient temperatures (T_amb), with V_wind fixed at 0.
    """
    Cp = 1.004
    Ti_V = 293.15
    Pe_V = 6.92
    mue_V = 0.37
    I_values = range(500, 1001, 100)
    T_amb_values = [280, 290, 300, 310]
    colors = ['black', 'red', 'blue', 'green']
    markers = ['o', '^', 's', 'v']
    V_wind = 0

    # Compressor constants
    T1 = 298
    P1 = 100
    P2 = 300
    k = 1.4
    R = 0.287
    T2 = T1 * (P2 / P1) ** ((k - 1) / k)
    Wc = Cp * (T2 - T1)

    plt.figure(figsize=(10, 7))
    for T_amb, color, marker in zip(T_amb_values, colors, markers):
        CC_values = []
        for I in I_values:
            P, _ = run_simulation(I, V_wind=V_wind, T_amb=T_amb)
            m_dot = P / Wc
            Tc_V = Ti_V * (1 - 0.020461 * (mue_V ** -0.593505)
                           * (Pe_V ** 0.199128) * (4 ** -0.128615)
                           * (0.155 ** -0.011456) * (10 ** 0.027844))
            CC = -m_dot * Cp * (Tc_V - Ti_V)
            CC_values.append(CC)
        plt.plot(I_values, CC_values, color=color, linestyle='-', marker=marker,
                 label=f'$T_{{amb}}={T_amb}$ K', linewidth=2)

    plt.xlabel("Irradiance $I$ (W/m²)", fontsize=18)
    plt.ylabel("Cooling Capacity CC (kW)", fontsize=18)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.ylim(top=3.5)  # Set Y-axis upper limit to 3.5
    plt.legend(loc='lower right', fontsize=14)
    plt.tight_layout()
    plt.savefig("results/I_vs_CC_by_Ta.png", dpi=300)
    plt.show()

def plot_I_vs_CC_by_V():
    """
    Plot I vs CC for different wind speeds (V_wind), with T_amb fixed at 293.15.
    """
    Cp = 1.004
    Ti_V = 293.15
    Pe_V = 6.92
    mue_V = 0.37
    I_values = range(500, 1001, 100)
    V_wind_values = [0, 4, 8, 12]
    colors = ['black', 'red', 'blue', 'green']
    markers = ['o', '^', 's', 'v']
    T_amb = 293.15

    # Compressor constants
    T1 = 298
    P1 = 100
    P2 = 300
    k = 1.4
    R = 0.287
    T2 = T1 * (P2 / P1) ** ((k - 1) / k)
    Wc = Cp * (T2 - T1)

    plt.figure(figsize=(10, 7))
    for V_wind, color, marker in zip(V_wind_values, colors, markers):
        CC_values = []
        for I in I_values:
            P, _ = run_simulation(I, V_wind=V_wind, T_amb=T_amb)
            m_dot = P / Wc
            Tc_V = Ti_V * (1 - 0.020461 * (mue_V ** -0.593505)
                           * (Pe_V ** 0.199128) * (4 ** -0.128615)
                           * (0.155 ** -0.011456) * (10 ** 0.027844))
            CC = -m_dot * Cp * (Tc_V - Ti_V)
            CC_values.append(CC)
        plt.plot(I_values, CC_values, color=color, linestyle='-', marker=marker,
                 label=f'$V_{{wind}}={V_wind}$ m/s', linewidth=2)

    plt.xlabel("Irradiance $I$ (W/m²)", fontsize=18)
    plt.ylabel("Cooling Capacity CC (kW)", fontsize=18)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.ylim(top=3.5)  # Set Y-axis upper limit to 3.5
    plt.legend(loc='lower right', fontsize=14)
    plt.tight_layout()
    plt.savefig("results/I_vs_CC_by_V.png", dpi=300)
    plt.show()

def plot_I_vs_eta_tot_by_Ta():
    """
    Plot I vs Total Efficiency (eta_tot) for different ambient temperatures (T_amb), with V_wind fixed at 0.
    """
    Cp = 1.004
    Ti_V = 293.15
    Pe_V = 6.92
    mue_V = 0.37
    I_values = range(500, 1001, 100)
    T_amb_values = [280, 290, 300, 310]
    colors = ['black', 'red', 'blue', 'green']
    markers = ['o', '^', 's', 'v']
    V_wind = 0
    C = 1250
    A_R = 0.0491

    # Compressor constants
    T1 = 298
    P1 = 100
    P2 = 300
    k = 1.4
    R = 0.287
    T2 = T1 * (P2 / P1) ** ((k - 1) / k)
    Wc = Cp * (T2 - T1)

    plt.figure(figsize=(10, 7))
    for T_amb, color, marker in zip(T_amb_values, colors, markers):
        eta_tot_values = []
        for I in I_values:
            P, _ = run_simulation(I, V_wind=V_wind, T_amb=T_amb)
            eta_tot = 100000 * P / (I * C * A_R)  # Efficiency in % (multiplied by 100)
            eta_tot_values.append(eta_tot)
        plt.plot(I_values, eta_tot_values, color=color, linestyle='-', marker=marker,
                 label=f'$T_{{amb}}={T_amb}$ K', linewidth=2)

    plt.xlabel("Irradiance $I$ (W/m²)", fontsize=18)
    plt.ylabel("Total Efficiency $\eta_{tot}$ (%)", fontsize=18)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.legend(loc='lower right', fontsize=14)
    plt.tight_layout()
    plt.savefig("results/I_vs_eta_tot_by_Ta.png", dpi=300)
    plt.show()

def plot_I_vs_eta_tot_by_V():
    """
    Plot I vs Total Efficiency (eta_tot) for different wind speeds (V_wind), with T_amb fixed at 293.15.
    """
    Cp = 1.004
    Ti_V = 293.15
    Pe_V = 6.92
    mue_V = 0.37
    I_values = range(500, 1001, 100)
    V_wind_values = [0, 4, 8, 12]
    colors = ['black', 'red', 'blue', 'green']
    markers = ['o', '^', 's', 'v']
    T_amb = 293.15
    C = 1250
    A_R = 0.0491

    # Compressor constants
    T1 = 298
    P1 = 100
    P2 = 300
    k = 1.4
    R = 0.287
    T2 = T1 * (P2 / P1) ** ((k - 1) / k)
    Wc = Cp * (T2 - T1)

    plt.figure(figsize=(10, 7))
    for V_wind, color, marker in zip(V_wind_values, colors, markers):
        eta_tot_values = []
        for I in I_values:
            P, _ = run_simulation(I, V_wind=V_wind, T_amb=T_amb)
            eta_tot = 100000 * P / (I * C * A_R)  # Efficiency in % (multiplied by 100)
            eta_tot_values.append(eta_tot)
        plt.plot(I_values, eta_tot_values, color=color, linestyle='-', marker=marker,
                 label=f'$V_{{wind}}={V_wind}$ m/s', linewidth=2)

    plt.xlabel("Irradiance $I$ (W/m²)", fontsize=18)
    plt.ylabel("Total Efficiency $\eta_{tot}$ (%)", fontsize=18)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.legend(loc='lower right', fontsize=14)
    plt.tight_layout()
    plt.savefig("results/I_vs_eta_tot_by_V.png", dpi=300)
    plt.show()
