import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from meshstuff import *
from algos import *

L = 1
nd_density = 70
duration = 5
stepsize = 0.0001
steps = int(duration/stepsize)

three_pt_stencil = [[-1],[0],[1]]

init_state = np.ones(L*nd_density)
mid = int(L*nd_density)//2
init_state[12] = 10
init_state[11] = 20
init_state[10] = 100
init_state[9] = 75
init_state[8] = 30
init_state[7] = 10

mesh1 = Mesh(init_state, three_pt_stencil)
mesh1.nd_spacing = 1/nd_density
mesh1.simulate(burgers1d, steps, stepsize)


# plot stuff
fig = plt.figure()
ax = plt.axes(xlim=(0,L), ylim=(0, 100))

ax.set_xlabel('Position along object (m)')
ax.set_ylabel('Mesh value')
ax.set_title("t = 0 sec")

line, = ax.plot([], [], lw=2, label='Mesh1')

def init():
    line.set_data([], [])
    return line,

def animate(i):
    x = np.linspace(0,L,L*nd_density)
    y1 = mesh1.history[i]
    line.set_data(x, y1)
    ax.set_title("t = {} sec".format(str(round(10 * i * stepsize, 2)).ljust(6)))
    return line,

anim = animation.FuncAnimation(fig, animate, init_func=init, frames=int(len(mesh1.history)), interval=20)
plt.legend(loc='upper left')
plt.show()
    

            
    
    





