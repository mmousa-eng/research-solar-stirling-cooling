import numpy as np
from scipy.optimize import curve_fit

# Data
DTc_V = np.array([14, 13, 12, 10, 13, 13, 13, 14, 14, 14, 14, 11, 12, 12, 12, 13, 13, 13,
                  9, 10, 10, 11, 11, 11, 12, 8, 9, 10, 10, 10, 11, 11, 15, 13])
mue_V = np.array([0.37, 0.43, 0.54, 0.66, 0.42, 0.42, 0.42, 0.42, 0.42, 0.42, 0.42, 0.51,
                 0.51, 0.51, 0.51, 0.51, 0.51, 0.51, 0.61, 0.61, 0.61, 0.61, 0.61, 0.61,
                 0.61, 0.68, 0.68, 0.68, 0.68, 0.68, 0.68, 0.68, 0.32, 0.44])
Pe_V = np.array([6.92, 6.92, 6.92, 6.92, 4, 5, 6, 7, 8, 9, 10, 4, 5, 6, 7, 8, 9, 10,
                4, 5, 6, 7, 8, 9, 10, 4, 5, 6, 7, 8, 9, 10, 6.92, 6.92])
Ti_V = 293.15  # Ambient temperature in K

def correlation(x, c0, c1, c4, c2, c3, c5):
    mue_V, Pe_V = x
    return c0 * (mue_V ** c1) * (Pe_V ** c4) * (4 ** c2) * (0.155 ** c3) * (10 ** c5)

# Fit the data once when module is loaded
T0_V = DTc_V / Ti_V
p0 = [0.03, 0.01, 0.01, 0.01, 0.01, 0.0]
params, _ = curve_fit(correlation, (mue_V, Pe_V), T0_V, p0=p0)

# Unpack params
C0, C1, C4, C2, C3, C5 = params

def vortex_correlation(mue, Pe):
    """Calculate the fitted correlation value given mue and Pe."""
    return C0 * (mue ** C1) * (Pe ** C4) * (4 ** C2) * (0.155 ** C3) * (10 ** C5)

# Optional: also provide a function to get full cooling temp drop prediction
def predicted_DTc(mue, Pe):
    """Calculate predicted temperature drop DTc based on fitted correlation."""
    T0 = vortex_correlation(mue, Pe)
    return T0 * Ti_V

# Test the fit
if __name__ == "__main__":
    print(f"Fitted params: {params}")
    # Example prediction
    example_mue = 0.5
    example_Pe = 7.0
    print(f"Predicted DTc: {predicted_DTc(example_mue, example_Pe):.2f} K")
