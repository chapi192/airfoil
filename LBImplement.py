import numpy as np

# =============================================================================
#     node daigram:
#     8 1 2
#     7 0 3
#     6 5 4
#     for example, the 6th node is at -1, -1, as so the 6th entry in each array
#     should be that
# =============================================================================

def distance(x1, y1, x2, y2):
    return ( (x1 - x2)**2 + (y1 - y2)**2 )**0.5

class LatticeBolztman:
    def __init__(self, windowX, windowY):

        self.numberOfXCells = windowX
        self.numberOfYCells = windowY
        self.tau = 0.53 #viscocity timescale
        self.numberLattice = 9

        self.xVelocities = np.array([0, 0, 1, 1, 1, 0, -1 ,-1 ,-1])
        self.yVelocities = np.array([0, 1, 1, 0, -1, -1, -1, 0 ,1])
        self.velocityWeights = np.array([4/9, 1/9, 1/36, 1/9, 1/36, 1/9, 1/36, 1/9, 1/36])

        #note that "F" is the current state of the model. 3 dimensions: X and Y, nodal values
        self.F = np.ones((windowX, windowY, 9)) + np.abs(np.random.randn(windowX, windowY, 9))
        self.rho = np.sum(self.F, 2)

    def calculateInitial(self):

        #to move the fluid right we assign a rightward velocity to all particles.
        #This means node 3 will have a nonzero value
        self.F[:,:, 3] = 2.3

        #obstacle here is just a obstacle. TODO: make any boundry from selected shape
        self.obstacle = np.full((self.numberOfXCells, self.numberOfYCells), False)

        for x in range(0, self.numberOfXCells):
            for y in range(0, self.numberOfYCells):
                if(distance(self.numberOfXCells/2, self.numberOfYCells/2, x, y) < 13):
                    self.obstacle[x][y] = True


    def calcNext(self):

        # =============================================================================
        #     this section is for debugging. Note: if youre using this to debug, save yourself
        #     some headache and set the number of cells for x and y to be less than 5 each, and
        #     less than 5 iterations as well. This dumps the format of F: looping through the x
        #     cells and the acompanying y cells, where each x,y cell has 9 unique nodes for velocity.
        # =============================================================================

        # print('\n   Iteration:', iteration)
        # for i in range(0, len(F)):
        #     for j in range(0, len(F[i])):
        #         print(f'\n     At {i},{j}:\n', F[i][j])

        #streaming step.
        for i, cx, cy in zip(range(9), self.xVelocities, self.yVelocities):
            self.F[:, :, i] = np.roll(self.F[:, :, i], cx, axis = 1)
            self.F[:, :, i] = np.roll(self.F[:, :, i], cy, axis = 0)

        #finding obstacle collisions, and flipping velocities
        self.boundry = self.F[self.obstacle, :]
        self.boundry = self.boundry[:, [0, 5, 6, 7, 8, 1, 2, 3, 4]]

        #recover density and velocities from F
        self.rho = np.sum(self.F, 2)
        self.velX = np.sum(self.F * self.xVelocities, 2) / self.rho
        self.velY = np.sum(self.F * self.yVelocities, 2) / self.rho

        #nothing moves inside the object
        self.F[self.obstacle, :] = self.boundry
        self.velX[self.obstacle] = 0
        self.velY[self.obstacle] = 0

        #collision
        self.Feq = np.zeros(self.F.shape)
        for i, cx, cy, w in zip(range(9), self.xVelocities, self.yVelocities, self.velocityWeights):
            self.Feq[:, :, i] = self.rho * w * (1 + 3 * (cx*self.velX + cy*self.velY) + 9 * (cx*self.velX + cy*self.velY)**2 / 2 - 3 * (self.velX**2 + self.velY**2)/2)

        self.F = self.F + -(1/self.tau) * (self.F - self.Feq)

    # =============================================================================
    #    F is calculated so now it just needs to be displayed
    # =============================================================================