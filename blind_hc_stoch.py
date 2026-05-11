import pandas as pd
import pandapower as pp
import simbench as sb
import matplotlib.pyplot as plt
import seaborn as sns

from pandapower.plotting.plotly import pf_res_plotly
from numpy.random import default_rng

# Load a desired network (simbench for now)
def load_network():
    net = sb.get_simbench_net('1-LV-urban6--1-no_sw')
    return net

# Maximum number of PV systems at end of planning horizon should be 80% of the number of load points in the network
def get_pv_number(net):
    buses = 0
    for i in net.bus.index:
        buses += 1
    print("Number of buses: ", buses)
    pv_number = int(buses * 0.8)
    print("Maximum number of PV systems: ", pv_number)
    return pv_number

# Create array reflecting the number of PV systems in each year of the planning horizon
def get_pv_array(planning_horizon, pv_number):
    pv_array = []
    for i in range(planning_horizon):
        pv_array.append(int(pv_number / planning_horizon * (i + 1)))
    print("PV array: ", pv_array)
    return pv_array

# Check for network violations and return the number of violations for each year of the planning horizon
def check_violations(net, max_voltage, max_line_loading, max_transformer_loading):
    violation = False
    voltage_violations = 0
    line_loading_violations = 0
    transformer_loading_violations = 0
    for i in net.bus.index:
        if net.res_bus.vm_pu[i] > max_voltage:
            voltage_violations += 1
            violation = True
    for i in net.line.index:
        if net.res_line.loading_percent[i] > max_line_loading * 100:
            line_loading_violations += 1
            violation = True
    for i in net.trafo.index:
        if net.res_trafo.loading_percent[i] > max_transformer_loading * 100:
            transformer_loading_violations += 1
            violation = True
    print("Voltage violations: ", voltage_violations)
    print("Line loading violations: ", line_loading_violations)
    print("Transformer loading violations: ", transformer_loading_violations)
    return voltage_violations, line_loading_violations, transformer_loading_violations, violation


# Set the boundary conditions for the optimization problem and the max network parameters
rng = default_rng(seed=42)  # For reproducibility
max_voltage = 1.03 # Maximum bus voltage in p.u.
max_line_loading = 1.0 # Maximum line loading in p.u.
max_transformer_loading = 1.0 # Maximum transformer loading in p.u.
pv_size = 0.035 # Size of each PV system in MW
planning_horizon = 10

# Number of iterations for the stochastic optimization
iterations = 2

# Set up pandas dataframe to store the results
results_df = pd.DataFrame(columns=['Year', 'Installed', 'Voltage_Violations', 'Line_Loading_Violations', 'Transformer_Loading_Violations'])

# Distribute the PV systems randomly in the network for each year of the planning horizon and run power flow calculations
for i in range(planning_horizon):
    print("Year: ", i + 1)
    for j in range(iterations):
        net = load_network()
        pv_max_number = get_pv_number(net)
        pv_current_number = get_pv_array(planning_horizon, pv_max_number)[i]
        if pv_current_number == 0:
            print("No PV systems to place this year")
        else:
            available_buses = net.bus.index.to_numpy()
            random_buses = rng.choice(available_buses, size=pv_current_number, replace=False)
            print("Which buses: ", random_buses)
            # Randomly distribute PV systems in the network without repeats in the same iteration
            for bus in random_buses:
                pp.create_sgen(net, bus, p_mw=pv_size, q_mvar=0.0)
        pp.runpp(net)
        check_violations(net, max_voltage, max_line_loading, max_transformer_loading)
        if check_violations(net, max_voltage, max_line_loading, max_transformer_loading)[3] == True:
            results_df.loc[i] = {'Year': i + 1, 'Installed': pv_current_number*pv_size, 'Voltage_Violations': check_violations(net, max_voltage, max_line_loading, max_transformer_loading)[0], 'Line_Loading_Violations': check_violations(net, max_voltage, max_line_loading, max_transformer_loading)[1], 'Transformer_Loading_Violations': check_violations(net, max_voltage, max_line_loading, max_transformer_loading)[2]}

results_df.to_csv('results.csv', index=False)
# Boxplot of installed PV capacity for each year of the planning horizon
plt.rc('xtick', labelsize=18)    # fontsize of the tick labels
plt.rc('ytick', labelsize=18)    # fontsize of the tick labels
plt.rc('legend', fontsize=18)    # fontsize of the tick labels
plt.rc('axes', labelsize=20)    # fontsize of the tick labels
plt.rcParams['font.size'] = 20
sns.set_style("whitegrid", {'axes.grid' : False})
fig, ax = plt.subplots(figsize=(10,5))
sns.boxplot(results_df.Installed, width=.1, ax=ax, orient="v")
ax.set_ylabel("Installed Capacity [MW]")
plt.show()