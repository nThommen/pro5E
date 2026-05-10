import pandas as pd
from numpy.random import default_rng
import matplotlib.pyplot as plt
import seaborn as sns

from pandapower.run import runpp
from pandapower.create import create_sgen
from pandapower.networks import mv_oberrhein

rng = default_rng(0)

def violations(net):
    runpp(net)
    if net.res_line.loading_percent.max() > 100:
        return (True, "Line \n Overloading")
    elif net.res_trafo.loading_percent.max() > 75:
        return (True, "Transformer \n Overloading")
    elif net.res_bus.vm_pu.max() > 1.04:
        return (True, "Voltage \n Violation")
    else:
        return (False, None)
    
def chose_bus(net):
    return rng.choice(net.load.bus.values)

def get_plant_size_mw():
    return rng.normal(loc=0.5, scale=0.05)

def load_network():
    return mv_oberrhein(scenario="generation")


iterations = 50
results = pd.DataFrame(columns=["installed", "violation"])

for i in range(iterations):
    net = load_network()
    installed_mw = 0
    while 1:
        violated, violation_type = violations(net)
        if violated:
            results.loc[i] = [installed_mw, violation_type]
            break
        else:
            plant_size = get_plant_size_mw()
            create_sgen(net, chose_bus(net), p_mw=plant_size, q_mvar=0)
            installed_mw += plant_size

#matplotlib inline
plt.rc('xtick', labelsize=18)    # fontsize of the tick labels
plt.rc('ytick', labelsize=18)    # fontsize of the tick labels
plt.rc('legend', fontsize=18)    # fontsize of the tick labels
plt.rc('axes', labelsize=20)    # fontsize of the tick labels
plt.rcParams['font.size'] = 20

sns.set_style("whitegrid", {'axes.grid' : False})
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10,5))
ax = axes[0]
sns.boxplot(results.installed, width=.1, ax=ax, orient="v")
ax.set_ylabel("Installed Capacity [MW]")

ax = axes[1]
#ax.axis("equal")
results.violation.value_counts().plot(kind="pie", ax=ax,  autopct=lambda x:"%.0f %%"%x)
ax.set_ylabel("")
ax.set_xlabel("")
sns.despine()
plt.tight_layout()
plt.show()