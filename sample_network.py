import numpy as np
import geojson
from pandapower.networks import mv_oberrhein
from pandapower.topology.create_graph import create_nxgraph
from pandapower.topology.graph_searches import calc_distance_to_bus, connected_components
from pandapower.plotting.simple_plot import simple_plot
from pandapower.run import runpp
from pandapower.plotting.plotting_toolbox import get_collection_sizes
from pandapower.plotting import create_line_collection, create_bus_collection, draw_collections, create_annotation_collection



# load example net (IEEE 9 buses)
net = mv_oberrhein()
# simple plot of net with existing geocoordinates or generated artificial geocoordinates
simple_plot(net, show_plot=True)
