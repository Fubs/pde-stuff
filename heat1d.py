import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from meshstuff import *
from algos import *

### constants and parameters ###
# L is in physical length units
# nd_density is nodes per unit length
L = 1
nd_density = 100
duration = 10
stepsize = 0.001
steps = int(duration/stepsize)



#### make initial state ###
init_state = 20*np.ones(L*nd_density)

# set left edge to 100 C
init_state[0] = 100

### make three meshes to compare algos ###  

# each item in stencil is an offset, and will 
# be added to target index to find neighbors
# this is the only stencil that works with the 1d algorithms right now
three_pt_stencil = [[-1],[0],[1]]

mesh1 = Mesh(init_state, three_pt_stencil)
mesh1.nd_spacing = 1/nd_density
mesh1.diffusivity = 0.001 # diffusivity constants are just made up

mesh2 = Mesh(init_state, three_pt_stencil)
mesh2.nd_spacing = 1/nd_density
mesh2.diffusivity = 0.001

mesh3 = Mesh(init_state, three_pt_stencil)
mesh3.nd_spacing = 1/nd_density
mesh3.diffusivity = 0.001

# this makes left boundary nodes have fixed values (like a heat source)
mesh1.fixed = [(0,)]
mesh2.fixed = [(0,)]
mesh3.fixed = [(0,)]




### now simulate each mesh using functions from algos.py ###

# ftcs is forward diff time, central diff space
# btcs is backward diff time, central diff space
# ctcs is central diff time, central diff space (crank-nicolson method)
# note ftcs is called with explicit_sim() and btcs/ctcs called with implicit_sim()
print("running ftcs")
mesh1.explicit_sim(ftcs1d, steps, stepsize)
print("running btcs")
mesh2.implicit_sim(btcs1d, steps, stepsize)
print("running ctcs")
mesh3.implicit_sim(ctcs1d, steps, stepsize)

# to make sim pause and display values after each step, you can add debug=1 like this
# mesh1.explicit_sim(ftcs1d, steps, stepsize, debug=1)
# then press enter to increment step when you run program





### plot stuff ###
fig = plt.figure()
ax = plt.axes(xlim=(0,L), ylim=(20, 100))

ax.set_xlabel('Position along object (m)')
ax.set_ylabel('Temperature (C)')
ax.set_title("t = 0 sec")

line, = ax.plot([], [], lw=2, label='ftcs')
line2, = ax.plot([], [], lw=2, label='btcs')
line3, = ax.plot([], [], lw=2, label='ctcs')

def init():
    line.set_data([], [])
    line2.set_data([], [])
    line3.set_data([], [])
    return line, line2, line3,

# calling mesh.explicit_sim() or  mesh.implicit_sim() fills up the list mesh.history
# mesh.history[n] is an array representing the state after n time steps
def animate(i):
    x = np.linspace(0,L,L*nd_density)
    y1 = mesh1.history[i]
    y2 = mesh2.history[i]
    y3 = mesh3.history[i]
    line.set_data(x, y1)
    line2.set_data(x, y2)
    line3.set_data(x, y3)
    ax.set_title("t = {} sec".format(str(round(i * stepsize, 2)).ljust(6)))
    return line, line2, line3,

anim = animation.FuncAnimation(fig, animate, init_func=init, frames=len(mesh1.history), interval=20)
plt.legend(loc='upper left')
plt.show()
    

            
    
    





