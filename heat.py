import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from meshstuff import *
from algos import *

# L, W, H are in physical length units
# nd_density is nodes per unit length
L = 1
W = 1
H = 1
nd_density = 200
duration = 10
stepsize = 0.0001
steps = int(duration/stepsize)


# each item in stencil is an offset, and will 
# be added to target index to find neighbors

# for 1d
three_pt_stencil = [[-1],[0],[1]]

# for 2d
#five_pt_stencil = [[0,0],[1,0],[0,1],[-1,0],[0,-1]]

# for 3d
# seven_pt_stencil = [[0,0,0],[1,0,0],[0,1,0],[0,0,1],[-1,0,0],[0,-1,0],[0,0,-1]]

# make initial state
#init_state = np.linspace(0, 100, L*nd_density)
init_state = np.zeros(L*nd_density)

mesh1 = Mesh(init_state, three_pt_stencil)
mesh1.nd_spacing = 1/nd_density
mesh1.diffusivity = 0.0008
mesh1.simulate(ftcs1d, steps, stepsize)

mesh2 = Mesh(init_state, three_pt_stencil)
mesh2.nd_spacing = 1/nd_density
mesh2.diffusivity = .022
mesh2.simulate(ftcs1d, steps, stepsize)


# plot stuff
fig = plt.figure()
ax = plt.axes(xlim=(0,L), ylim=(0, 100))

ax.set_xlabel('Position along object (m)')
ax.set_ylabel('Temperature (C)')
ax.set_title("t = 0 sec")

# reference temperatures
roomtemp = ax.plot(np.arange(L+1), np.ones(L+1)*22, lw=2)
roomtemp = ax.plot(np.arange(L+1), np.ones(L+1)*60, lw=2)
line, = ax.plot([], [], lw=2)
line2, = ax.plot([], [], lw=2)

def init():
    line.set_data([], [])
    line2.set_data([], [])
    return line, line2,

def animate(i):
    x = np.linspace(0,L,L*nd_density)
    y1 = mesh1.history[i*10]
    y2 = mesh2.history[i*10]
    line.set_data(x, y1)
    line2.set_data(x, y2)
    ax.set_title("t = {} sec".format(str(round(10 * i * stepsize, 2)).ljust(6)))
    return line, line2,

anim = animation.FuncAnimation(fig, animate, init_func=init, frames=int(len(mesh1.history)/10), interval=1)
plt.show()
    

            
    
    





