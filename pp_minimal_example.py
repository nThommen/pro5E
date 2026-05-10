import pandapower as pp
import matplotlib.pyplot as plt
import pandapower.topology as top

def pf_print_results(net):
    pp.runpp(net)
    print("Bus Results:")
    print(net.res_bus)
    print("\nLine Results:")
    print(net.res_line)
    print("\nTransformer Results:")
    print(net.res_trafo)

net = pp.create_empty_network(name="Rural_Test")

bus1 = pp.create_bus(net, vn_kv=20, name="Bus 1")
bus2 = pp.create_bus(net, vn_kv=0.4, name="Bus 2")
bus3 = pp.create_bus(net, vn_kv=0.4, name="Bus 3")

pp.create_ext_grid(net, bus=bus1, vm_pu=1.02, name="Grid Connection")
pp.create_load(net, bus=bus3, p_mw=0.01, q_mvar=0.005, name="Load")

pp.create_transformer(net, hv_bus=bus1, lv_bus=bus2, std_type="0.4 MVA 20/0.4 kV", name="Trafo")
pp.create_line(net, from_bus=bus2, to_bus=bus3, length_km=0.3, name="Line",std_type="NAYY 4x50 SE")



"""pf_print_results(net)

net.trafo.at[net.trafo.index[0], "tap_pos"] = -2
pp.runpp(net)
pf_print_results(net)"""

pp.create_switch(net, bus=bus3, element=net.line.index[0], et="l", name="Switch", closed=False)

print(top.unsupplied_buses(net))

net.switch.at[net.switch.index[0], "closed"] = True
print(top.unsupplied_buses(net))

#pp.plotting.simple_plot(net, show_plot=True)
#pf_print_results(net)