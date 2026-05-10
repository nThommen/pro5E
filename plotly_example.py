from pandapower.plotting.plotly import simple_plotly
from pandapower.networks import mv_oberrhein
import plotly.io as pio
pio.templates.default = "plotly_white"

net = mv_oberrhein()

simple_plotly(net)

