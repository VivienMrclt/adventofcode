import numpy as np
import os
import time

paths = []
with open('input.txt', 'r') as f:
    for line in f:
        paths.append([[int(c) for c in p.split(',')] for p in line.split(' -> ')])

xMin = paths[0][0][0]
xMax = xMin
yMin = paths[0][0][1]
yMax = yMin
yMin = 0 # The sand origin is in 0

for path in paths:
    for point in path:
        if point[0] > xMax:
            xMax = point[0]
        elif point[0] < xMin:
            xMin = point[0]
        if point[1] > yMax:
            yMax = point[1]
        elif point[1] < yMin:
            yMin = point[1]

xDigit = len(str(xMax))
yDigit = len(str(yMax))

xDim = xMax - xMin + 1
yDim = yMax - yMin + 1

fieldSymbols = ['.', '#', 'O', '+', '~']

def printField(field):
    # Print the x coord lines
    for d in range(xDigit - 1, -1, -1):
        line = ' ' * yDigit
        p = 10 ** d
        for i in range(xDim):
            x = xMin + i
            q, mod = divmod(x, p)
            if i == 0 or i == xDim - 1 or mod == 0:
                line += str(q % 10)
            else:
                line += ' '
        print(line)

    # Print field lines
    powers = [10 ** p for p in range(yDigit - 1, -1, -1)]
    for j in range(yDim):
        line = ''
        y = j + yMin
        # For each line start with the y coord columns
        for p in powers:
            q, mod = divmod(y, p)
            if j == 0 or j == yDim - 1 or mod == 0:
                line += str(q % 10)
            else:
                line += ' '
        # Then print the field line
        for i in range(xDim):
            line += fieldSymbols[field[i,j]]
        print(line)

# The sand origin
origin = (500, 0)

# Creating the field and filling it with the origin and the rocks
field = np.zeros((xDim, yDim), dtype=int)
field[origin[0] - xMin, origin[1] - yMin] = 3
for path in paths:
    for (x1, y1), (x2, y2) in zip(path[:-1], path[1:]):
        i1 = x1 - xMin
        j1 = y1 - yMin
        i2 = x2 - xMin
        j2 = y2 - yMin
        field[min(i1, i2):max(i1, i2) + 1, min(j1, j2):max(j1, j2) + 1] = 1

# Make the sand rain

def simulateSandFalling(field):
    originInSimu = (origin[0] - xMin, origin[1] - yMin)
    animation = False
    equilibrium = False
    sandUnits = 0
    lastMessageUpdate = time.time() - 1
    while not equilibrium:
        pos = originInSimu
        trail = []
        resting = False
        sandUnits += 1
        if not animation:
            # Limiting the message refreshing rate
            if time.time() - lastMessageUpdate > 0.1:
                os.system('clear')
                print('Simulated {:5>} sand units.'.format(sandUnits))
                lastMessageUpdate = time.time()
        done = False
        while not done:
            candidatePositions = [
                    (pos[0], pos[1] + 1),
                    (pos[0] - 1, pos[1] + 1),
                    (pos[0] + 1, pos[1] + 1)]
            
            resting = True
            for cp in candidatePositions:
                if cp[0] < 0 or cp[0] >= xDim or cp[1] < 0 or cp[1] >= yDim:
                    equilibrium = True
                    field[tuple(np.array(trail).T)] = 4
                    resting = False
                    done = True
                    break
                if field[cp] == 0:
                    trail.append(cp)
                    if animation: 
                        field[cp] = 2
                        if field[pos] == 2: # To filter the case when pos is origin
                            field[pos] = 0
                    pos = cp
                    resting = False
                    break
            if resting:
                field[pos] = 2
                done = True
            if animation:
                time.sleep(0.01)
                os.system('clear')
                printField(field)
        if pos == originInSimu:
            equilibrium = True
    os.system('clear')
    print('Simulated {:5>} sand units.'.format(sandUnits))
    return sandUnits

# Let's discard the sand unit that falls in the void
sandUnitsPart1 = simulateSandFalling(field) - 1
printField(field)

print()
print('Once all {} units of sand shown above have come to rest, all further \
sand flows out the bottom, falling into the endless void'.format(sandUnitsPart1))

input('Type any key to continue to part 2 of the problem')

# Let's remove the trail we traced during the first part to show sand going
# to the void
field[field == 4] = 0

# We can consider that we don't need to create a base larger than twice its
# distance to the sand origin.
yBase = yMax + 2
xBase1 = 500 - yBase
xBase2 = 500 + yBase

# Let's rescale the simulation grid before tracing the base
xDiffLeft = xMin - xBase1
xDiffRight = xBase2 - xMax

if xDiffLeft > 0:
    field = np.concatenate([np.zeros((xDiffLeft, yDim), dtype=int), field])
if xDiffRight > 0:
    field = np.concatenate([field, np.zeros((xDiffRight, yDim), dtype=int)])

# Update simulation dimensions related to x
xMin = min(xBase1, xMin)
xMax = max(xBase2, xMax)
xDim = xMax - xMin + 1
xDigit = len(str(xMax))

# Adding the two new bottom layers
field = np.concatenate([field, np.zeros((xDim, 2), dtype=int)], axis=1)

# Update simulation dimensions related to y
yMax = yBase
yDim = yMax - yMin + 1
yDigit = len(str(yMax))

# Let's add the base
field[:, yDim - 1] = 1

# Let's relaunch the simulation where we left of

sandUnitsPart2 = simulateSandFalling(field)
printField(field)

print()
print('The sand stops falling after {} units of sand come to rest.'.format(sandUnitsPart1 + sandUnitsPart2))
