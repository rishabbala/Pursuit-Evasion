import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d

########    Making the voronoi diagram with scipy   ########

# make up data points
points = np.array([[282, 339], [67, 442], [462, 356], [370, 435], [185, 5]])


# compute Voronoi tesselation
vor = Voronoi(points)

# plot
voronoi_plot_2d(vor)

# colorize
plt.show()
