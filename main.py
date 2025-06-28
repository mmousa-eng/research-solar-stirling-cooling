from performance_plots import plot_I_vs_P_by_wind, plot_I_vs_P_by_Tamb
from performance_plots import plot_Pe_vs_DTc
from performance_plots import plot_I_vs_CC_by_Pe
from performance_plots import plot_I_vs_CC_by_mue
from performance_plots import plot_I_vs_CC_by_Ta
from performance_plots import plot_I_vs_CC_by_V
from performance_plots import plot_I_vs_eta_tot_by_Ta, plot_I_vs_eta_tot_by_V

# I vs P
plot_I_vs_P_by_wind()
plot_I_vs_P_by_Tamb()

# Pe vs DTc
plot_Pe_vs_DTc()

# I vs CC - Pes
plot_I_vs_CC_by_Pe()

# I vs CC - mues
plot_I_vs_CC_by_mue()

# I vs CC - by Ta
plot_I_vs_CC_by_Ta()

# I vs CC - by V
plot_I_vs_CC_by_V()

# I vs eta_tot - by Ta
plot_I_vs_eta_tot_by_Ta()

# I vs eta_tot - by V
plot_I_vs_eta_tot_by_V()