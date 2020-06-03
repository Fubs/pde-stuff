import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation, cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from meshstuff import *
from algos import *

# L, W, H are in physical length units
# nd_density is nodes per unit length
L = 5
W = 5
nd_density = 3
duration = 3
stepsize = 0.001
steps = int(duration/stepsize)


five_pt_stencil = [[0,0],[1,0],[0,1],[-1,0],[0,-1]]
init_state = np.zeros((L*nd_density, W*nd_density))
# sets one of the nodes in the middle to 100
init_state[int(L*nd_density/2)][int(W*nd_density/2)] = 100

mesh = Mesh(init_state, five_pt_stencil)
mesh.nd_spacing = 1/nd_density

mesh.simulate(ftcs2d, steps, stepsize, debug=1)

# plot stuff
# colors are a bit messed up, it seems each grid cell shows the highest colormap value instead of current
fig, ax = plt.subplots()
ax.set_title("t = 0 sec")
colormap = cm.get_cmap('viridis')
grid = ax.pcolormesh(mesh.history[0])
fig.colorbar(grid)

def init():
    grid = ax.pcolormesh(mesh.history[0], cmap=colormap)
    ax.set_title("t = 0 sec")
    return grid,

def update(frame):
    grid = ax.pcolormesh(mesh.history[frame*10], cmap=colormap)
    ax.set_title(str(frame*20))
    return grid,

anim = animation.FuncAnimation(fig, update, frames=range(int(len(mesh.history)/20)), init_func=init, interval=10)

plt.show()











            
    
    





