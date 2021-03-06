import numpy as np
import numpy.linalg
from meshstuff import *

# finite difference coeffs from wikipedia
central_acc2_deriv2 = [1, -2, 1]
central_acc4_deriv2 = [-1/12, 4/3, -5/2, 4/3, -1/12]


# forward diff time, central diff space
def ftcs1d(mesh, stepsize):
    nextstate = np.zeros(np.shape(mesh.state))
    with np.nditer(mesh.state, flags=['multi_index']) as it:
        for x in it:
            idx, vals = mesh.neighbors(it.multi_index)
            laplacian = (vals[0] - 2*vals[1] + vals[2])
            # mesh.diffusivity defaults to 1 when creating mesh, but can be changed
            next_val = ((mesh.diffusivity * stepsize * laplacian)/ mesh.nd_spacing**2)  + vals[1]
            nextstate[it.multi_index] = next_val
    return nextstate

def ftcs2d(mesh, stepsize):
    nextstate = np.zeros(np.shape(mesh.state))
    with np.nditer(mesh.state, flags=['multi_index']) as it:
        for x in it:
            idx, vals = mesh.neighbors(it.multi_index)
            coefs = central_acc2_deriv2
            d2x = (coefs[0]*vals[1] + coefs[1]*vals[0] + coefs[2]*vals[3]) / mesh.nd_spacing**2
            d2y = (coefs[0]*vals[2] + coefs[1]*vals[0] + coefs[2]*vals[4]) / mesh.nd_spacing**2
            laplacian = d2x + d2y
            nextstate[it.multi_index] = (mesh.diffusivity * stepsize * laplacian) + vals[0]
    return nextstate

def burgers1d(mesh, stepsize):
    nextstate = np.zeros(np.shape(mesh.state))
    with np.nditer(mesh.state, flags=['multi_index']) as it:
        for x in it:
            idx, vals = mesh.neighbors(it.multi_index)
            const1 = stepsize/mesh.nd_spacing**2
            const2 = -stepsize/(2*mesh.nd_spacing)
            term1 = const1 * (vals[0] - 2*vals[1] + vals[2])
            term2 = const2 * vals[1] * (vals[2] - vals[0]) + vals[1]
            nextstate[it.multi_index] = term1 + term2
    return nextstate

def convection1d(mesh, stepsize):
    nextstate = np.zeros(np.shape(mesh.state))
    with np.nditer(mesh.state, flags=['multi_index']) as it:
        for x in it:
            idx, vals = mesh.neighbors(it.multi_index)
            const = mesh.conv_spd * stepsize / mesh.nd_spacing
            nextstate[it.multi_index] = vals[1] - const * (vals[1] - vals[0])
    return nextstate
    
# backwards diff time, central diff space
def btcs1d(mesh, stepsize):
    xstep = mesh.nd_spacing
    tstep = stepsize
    # tridiagonal coeff matrix
    # i've read that there's a faster way to solve
    # the linear system since its tridiagonal
    # TODO: figure that out
    r = (mesh.diffusivity * tstep)/(xstep**2)
    boundaryCoeff = 1 + 2*r
    emptyrow = np.zeros(np.size(mesh.state))
    coeffMatrix = np.copy(emptyrow)
    coeffMatrix[0] = boundaryCoeff
    coeffMatrix[1] = -r
    lastrow = np.copy(emptyrow)
    lastrow[-1] = boundaryCoeff
    lastrow[-2] = -r
    for n in range(np.size(mesh.state)-2):
        newrow = np.copy(emptyrow)
        newrow[n] = -r
        newrow[n+1] = 1 + 2*r
        newrow[n+2] = -r
        coeffMatrix = np.vstack([coeffMatrix, newrow])
    coeffMatrix = np.vstack([coeffMatrix, lastrow])
    currentState = np.copy(mesh.state)
    return numpy.linalg.solve(coeffMatrix, currentState)

# central diff time, central diff space (crank-nicolson method)
def ctcs1d(mesh, stepsize):
    r = (mesh.diffusivity * stepsize)/(mesh.nd_spacing**2)
    LBound = 1 + 2*r
    RBound = 1 - 2*r
    emptyrow = np.zeros(np.size(mesh.state))
    currentState = np.copy(mesh.state)
    # make left coeff matrix
    coeffMatrixL = np.copy(emptyrow)
    coeffMatrixL[0] = LBound
    coeffMatrixL[1] = -r
    lastrowL = np.copy(emptyrow)
    lastrowL[-1] = LBound
    lastrowL[-2] = -r
    for n in range(np.size(mesh.state)-2):
        newrow = np.copy(emptyrow)
        newrow[n] = -r
        newrow[n+1] = 1 + 2*r
        newrow[n+2] = -r
        coeffMatrixL = np.vstack([coeffMatrixL, newrow])
    coeffMatrixL = np.vstack([coeffMatrixL, lastrowL])
    # make right coeff matrix
    coeffMatrixR = np.copy(emptyrow)
    coeffMatrixR[0] = RBound
    coeffMatrixR[1] = r
    lastrowR = np.copy(emptyrow)
    lastrowR[-1] = RBound
    lastrowR[-2] = r
    for n in range(np.size(mesh.state)-2):
        newrow = np.copy(emptyrow)
        newrow[n] = r
        newrow[n+1] = 1 - 2*r
        newrow[n+2] = r
        coeffMatrixR = np.vstack([coeffMatrixR, newrow])
    coeffMatrixR = np.vstack([coeffMatrixR, lastrowR])
    # invert right coeff matrix and dot on left to make
    # coeffR . U(t+1) = coeffL . U(t)
    # into
    # coeffL^-1  . coeffR . U(t+1) = U(t)
    invR = numpy.linalg.inv(coeffMatrixR)
    M = numpy.dot(invR, coeffMatrixL)
    return numpy.linalg.solve(M, currentState)

    


    

    

    
    
    

