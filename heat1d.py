import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from meshstuff import *
from algos import *

### constants and parameters ###
# L, W, H are in physical length units
# nd_density is nodes per unit length
L = 2
nd_density = 50
duration = 10
stepsize = 0.001
steps = int(duration/stepsize)



#### make some initial states ###
init_state1 = np.zeros(L*nd_density)
init_state2 = np.zeros(L*nd_density)
init_state3 = np.zeros(L*nd_density)

# set a section in each to 100 C
mid = int(L*nd_density)//2
#init_state1[mid:mid+5] = 100
init_state1[mid] = 100
init_state2[mid-10] = 100
init_state3[mid+10] = 100





### make three meshes to compare algos ###  

# each item in stencil is an offset, and will 
# be added to target index to find neighbors
# changing this doesn't do anything right now, but I might use eventually
three_pt_stencil = [[-1],[0],[1]]

mesh1 = Mesh(init_state1, three_pt_stencil)
mesh1.nd_spacing = 1/nd_density
mesh1.diffusivity = 0.001 # diffusivity constants are just made up

mesh2 = Mesh(init_state2, three_pt_stencil)
mesh2.nd_spacing = 1/nd_density
mesh2.diffusivity = 0.001

mesh3 = Mesh(init_state3, three_pt_stencil)
mesh3.nd_spacing = 1/nd_density
mesh3.diffusivity = 0.001

# uncomment to make initial nodes have fixed values (like for a heat source/sink)
#mesh1.fixed = [(mid,)]
#mesh2.fixed = [(mid-10,)]
#mesh3.fixed = [(mid+10,)]




### now simulate each mesh using functions from algos.py ###

# ftcs is forward diff time, central diff space
# btcs is backward diff time, central diff space
# ctcs is central diff time, central diff space (crank-nicolson method)
# note ftcs is called with explicit_sim() and btcs/ctcs called with implicit_sim()
mesh1.explicit_sim(ftcs1d, steps, stepsize)
mesh2.implicit_sim(btcs1d, steps, stepsize)
mesh3.implicit_sim(ctcs1d, steps, stepsize)

# calling mesh.explicit_sim() or  mesh.implicit_sim() fills up the list mesh.history
# mesh.history[n] is an array representing the state after n time steps




### plot stuff ###
fig = plt.figure()
ax = plt.axes(xlim=(0,L), ylim=(0, 100))

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

# only displays every tenth frame since animation is too slow otherwise
def animate(i):
    x = np.linspace(0,L,L*nd_density)
    y1 = mesh1.history[i*10]
    y2 = mesh2.history[i*10]
    y3 = mesh3.history[i*10]
    line.set_data(x, y1)
    line2.set_data(x, y2)
    line3.set_data(x, y3)
    ax.set_title("t = {} sec".format(str(round(10 * i * stepsize, 2)).ljust(6)))
    return line, line2, line3,

anim = animation.FuncAnimation(fig, animate, init_func=init, frames=int(len(mesh1.history)/10), interval=20)
plt.legend(loc='upper left')
plt.show()
    

            
    
    





