import numpy as np

from matplotlib import pyplot

def distance(x1, y1, x2, y2):
    return ( (x1 - x2)**2 + (y1 - y2)**2 )**0.5

# =============================================================================
#     the cells are the permutations of the window itself. So the window could 
#     be larger in either direction, but it will still be divided into 400 by 
#     100 for the LB algo
# =============================================================================
numberOfXCells = 3
numberOfYCells = 2 

tau = 0.53 #kinematic viscocity/timescale

numberIterations = 2

numberLattice = 9

# =============================================================================
#     node daigram:   
#     8 1 2
#     7 0 3
#     6 5 4
#     for example, the 6th node is at -1, -1, as so the 6th entry in each array
#     should be that    
# =============================================================================

xVelocities = np.array([0, 0, 1, 1, 1, 0, -1 ,-1 ,-1])
yVelocities = np.array([0, 1, 1, 0, -1, -1, -1, 0 ,1])
velocityWeights = np.array([4/9, 1/9, 1/36, 1/9, 1/36, 1/9, 1/36, 1/9, 1/36])

# =============================================================================
#     initial conditions
# =============================================================================

#note that "F" is the current state of the model. 3 dimensions: X and Y, velocity
F = np.ones((numberOfXCells, numberOfYCells, numberLattice)) + np.random.randn(numberOfXCells, numberOfYCells, numberLattice)

#to move the fluid left we assign a rightward velocity to all particles. This means node 3 will have a nonzero value
F[:,:, 3] = 2.3

#obstacle here is just a cylander. TODO: make any boundry from selected shape
cylander = np.full((numberOfXCells, numberOfYCells), False)

for x in range(0, numberOfXCells):
    for y in range(0, numberOfYCells):
        if(distance(numberOfXCells/2, numberOfYCells/2, x, y) < 13):
            cylander[x][y] = True
            
# =============================================================================
#     main loop
# =============================================================================

for iteration in range(numberIterations):
    
# =============================================================================
#     this section is for debugging. Note: if youre using this to debug, save yourself 
#     some headache and set the number of cells for x and y to be less than 5 each, and
#     less than 5 iterations as well. This dumps the format of F: looping through the x
#     cells and the acompanying y cells, where each x,y cell has 9 unique nodes for velocity.    
# =============================================================================
    
    print('\n   Iteration:', iteration)
    for i in range(0, len(F)):
        for j in range(0, len(F[i])):
            print(f'\n     At {i},{j}:\n', F[i][j])

    #streaming step. 
    for i, cx, cy in zip(range(numberLattice), xVelocities, yVelocities):
        F[:, :, i] = np.roll(F[:, :, i], cx, axis = 1)
        F[:, :, i] = np.roll(F[:, :, i], cy, axis = 0)
        
    #finding cylander collisions, and flipping velocities
    boundry = F[cylander, :]
    boundry = boundry[:, [0, 5, 6, 7, 8, 1, 2, 3, 4]]
    
    #recover density and velocities from F
    rho = np.sum(F, 2)
    velX = np.sum(F * xVelocities, 2) / rho
    velY = np.sum(F * yVelocities, 2) / rho
    
    #nothing moves inside the object
    F[cylander, :] = boundry
    velX[cylander] = 0
    velY[cylander] = 0
    
    #collision
    Feq = np.zeros(F.shape)
    for i, cx, cy, w in zip(range(numberLattice), xVelocities, yVelocities, velocityWeights):
        Feq[:, :, i] = rho * w * (1 + 3 * (cx*velX + cy*velY) + 9 * (cx*velX + cy*velY)**2 / 2 - 3 * (velX**2 + velY**2)/2)
        
    F = F + -(1/tau) * (F - Feq)
    
# =============================================================================
#    F is calculated so now it just needs to be displayed     
# =============================================================================
