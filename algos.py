import numpy as np
import numpy.linalg
from meshstuff import *

# finite difference coeffs from wikipedia
central_acc2_deriv2 = [1, -2, 1]
central_acc4_deriv2 = [-1/12, 4/3, -5/2, 4/3, -1/12]


#in following algos, "it" is an iterator made by np.nditer
#vals is an array of neighboring values, with same index as stencil

# forward diff time, central diff space
def ftcs1d(mesh, it, stepsize):
    idx, vals = mesh.neighbors(it)
    coefs = central_acc2_deriv2
    laplacian = (coefs[0]*vals[0] + coefs[1]*vals[1] + coefs[2]*vals[2]) / mesh.nd_spacing**2
    # mesh.diffusivity defaults to 1 when creating mesh, but can be changed
    next_val = (mesh.diffusivity * stepsize * laplacian) + vals[1]
    return next_val

def ftcs2d(mesh, it, stepsize):
    idx, vals = mesh.neighbors(it)
    coefs = central_acc2_deriv2
    d2x = (coefs[0]*vals[1] + coefs[1]*vals[0] + coefs[2]*vals[3]) / mesh.nd_spacing**2
    d2y = (coefs[0]*vals[2] + coefs[1]*vals[0] + coefs[2]*vals[4]) / mesh.nd_spacing**2
    laplacian = d2x + d2y
    next_val = (mesh.diffusivity * stepsize * laplacian) + vals[0]
    return next_val

def ftcs3d(mesh, it, stepsize):
    idx, vals = mesh.neighbors(it)
    d2x = (vals[1] + vals[4] - 2 * vals[0])/ mesh.nd_spacing**2
    d2y = (vals[2] + vals[5] - 2 * vals[0])/ mesh.nd_spacing**2
    d2z = (vals[3] + vals[6] - 2 * vals[0])/ mesh.nd_spacing**2
    laplacian = d2x + d2y + d2z
    next_val = (mesh.diffusivity * stepsize * laplacian) + vals[0]
    return next_val
    
def btcs1d(mesh, stepsize):
    xstep = mesh.nd_spacing
    tstep = stepsize
    # tridiagonal coeff matrix
    # i've read that there's a faster way to solve
    # the linear system since its tridiagonal
    # TODO: figure that out
    r = (mesh.diffusivity * tstep)/(xstep**2)
    A = 1 + 2*r
    B = -r
    boundaryCoeff = A
    emptyrow = np.zeros(np.size(mesh.state))
    coeffMatrix = np.copy(emptyrow)
    coeffMatrix[0] = boundaryCoeff
    coeffMatrix[1] = B
    lastrow = np.copy(emptyrow)
    lastrow[-1] = boundaryCoeff
    lastrow[-2] = B
    for n in range(np.size(mesh.state)-2):
        newrow = np.copy(emptyrow)
        newrow[n] = B
        newrow[n+1] = A
        newrow[n+2] = B
        coeffMatrix = np.vstack([coeffMatrix, newrow])
    coeffMatrix = np.vstack([coeffMatrix, lastrow])
    currentState = np.copy(mesh.state)
    return numpy.linalg.solve(coeffMatrix, currentState)


    

    

    
    
    

