import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from meshstuff import *
from algos import *

# L, W, H are in physical length units
# nd_density is nodes per unit length
L = 2
nd_density = 50
duration = 10
stepsize = 0.001
steps = int(duration/stepsize)


# each item in stencil is an offset, and will 
# be added to target index to find neighbors

three_pt_stencil = [[-1],[0],[1]]


# make initial state
#init_state = np.linspace(0, 100, L*nd_density)
init_state = np.zeros(L*nd_density)
mid = int(L*nd_density)/2
# set a section in the middle to 100 C
init_state[50:55] = 100


mesh1 = Mesh(init_state, three_pt_stencil)
mesh1.nd_spacing = 1/nd_density
mesh1.diffusivity = 0.001
mesh1.implicit_sim(ctcs1d, steps, stepsize)

mesh2 = Mesh(init_state, three_pt_stencil)
mesh2.nd_spacing = 1/nd_density
mesh2.diffusivity = 0.001
mesh2.explicit_sim(ftcs1d, steps, stepsize)


# plot stuff
fig = plt.figure()
ax = plt.axes(xlim=(0,L), ylim=(0, 100))

ax.set_xlabel('Position along object (m)')
ax.set_ylabel('Temperature (C)')
ax.set_title("t = 0 sec")

line, = ax.plot([], [], lw=2, label='Mesh1')
line2, = ax.plot([], [], lw=2, label='Mesh2')

def init():
    line.set_data([], [])
    line2.set_data([], [])
    return line, line2,

# only displays every tenth frame since animation is too slow otherwise
def animate(i):
    x = np.linspace(0,L,L*nd_density)
    y1 = mesh1.history[i*10]
    y2 = mesh2.history[i*10]
    line.set_data(x, y1)
    line2.set_data(x, y2)
    ax.set_title("t = {} sec".format(str(round(10 * i * stepsize, 2)).ljust(6)))
    return line, line2,

anim = animation.FuncAnimation(fig, animate, init_func=init, frames=int(len(mesh1.history)/10), interval=20)
plt.legend(loc='upper left')
plt.show()
    

            
    
    





