import pandapower as pp
import simbench as sb
from pandapower.plotting.plotly import pf_res_plotly
from numpy.random import default_rng

"""def get_simbench_codes():
    print(sb.collect_all_simbench_codes())
    return"""

# Set the boundary conditions for the optimization problem and the max network parameters
rng = default_rng(seed=42)  # For reproducibility
max_voltage = 1.3 # Maximum bus voltage in p.u.
max_line_loading = 1.0 # Maximum line loading in p.u.
max_transformer_loading = 1.0 # Maximum transformer loading in p.u.

# Planning horizon in years
planning_horizon = 10

# Check for network violations and return the number of violations for each year of the planning horizon
def check_violations(net):
    voltage_violations = 0
    line_loading_violations = 0
    transformer_loading_violations = 0
    for i in net.bus.index:
        if net.res_bus.vm_pu[i] > max_voltage:
            voltage_violations += 1
    for i in net.line.index:
        if net.res_line.loading_percent[i] > max_line_loading * 100:
            line_loading_violations += 1
    for i in net.trafo.index:
        if net.res_trafo.loading_percent[i] > max_transformer_loading * 100:
            transformer_loading_violations += 1
    print("Voltage violations: ", voltage_violations)
    print("Line loading violations: ", line_loading_violations)
    print("Transformer loading violations: ", transformer_loading_violations)
    return voltage_violations, line_loading_violations, transformer_loading_violations

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

net = sb.get_simbench_net('1-LV-urban6--1-no_sw')

get_pv_number(net)
pv_array = get_pv_array(planning_horizon, get_pv_number(net))

# Number of iterations for the stochastic optimization
iterations = 100
"""
# Distribute the PV systems randomly in the network for each year of the planning horizon and run power flow calculations
for i in range(planning_horizon):
    print("Year: ", i + 1)
    for j in range(iterations):
        random_bus = rng.choice(net.bus.index)
        # Randomly distribute PV systems in the network
        pp.create_sgen(net, random_bus, p_mw=0.035, q_mvar=0.0)
        print("Which bus: ", random_bus)
        # Run power flow calculation
        #pp.runpp(net)
        # Check for network violations
        #check_violations(net)

"""
pp.runpp(net)
pf_res_plotly(net)

print("Array of buses: ", net.bus.index)