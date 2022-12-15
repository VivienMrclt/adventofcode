import numpy as np
import re

# Variables to change to adapt to the example
# 10 and 20 for simple_input.txt
# 2000000 and 4000000 for simple_input.txt
y = 2000000
maxCoord = 4000000

sensors = []
with open('input.txt', 'r') as f:
    for line in f:
        result= re.search(r"Sensor at x=(\d+), y=(\d+): closest beacon is at x=(-?\d+), y=(-?\d+)", line)
        sensors.append([
            int(result.group(1)),
            int(result.group(2)),
            int(result.group(3)),
            int(result.group(4))])

def getCheckedSpots(y, filterOutBoundIntersections=False, verbose=False):
    line_intersections = []
    for s_x, s_y, b_x, b_y in sensors:
        distance_beacon = abs(s_x - b_x) + abs(s_y - b_y)
        distance_line = abs(s_y - y)
        if distance_beacon < distance_line:
            # The area covered by the sensor doesn't cross the line
            continue
        intersection_half_width = distance_beacon - distance_line
        candidate = [s_x - intersection_half_width, s_x + intersection_half_width]
        if filterOutBoundIntersections:
            if candidate[0] <= 0:
                if candidate[1] >= maxCoord:
                    # This intersection covers teh all search area
                    return [[0, maxCoord]]
                elif candidate[1] < 0:
                    # The intersection can be discarded. It's out of bounds
                    continue
                else:
                    # We can just crop this intersection
                    candidate[0] = 0
            elif candidate[1] >= maxCoord:
                if candidate[0] > maxCoord:
                    # The intersection can be discarded. It's out of bounds
                    continue
                else:
                    # We can just crop this intersection
                    candidate[1] = maxCoord
        line_intersections.append(candidate)
    
    # Order intersections by starting key 
    line_intersections = sorted(line_intersections, key=lambda x: x[0])
    if verbose:
        print('Here is the list of intersections with the line y={}: \
{}'.format(y, line_intersections))
    
    # This density metric was supposed to help for the second part of the problem
    # The false good idea was that the less dense (the less overlaps of sensor
    # detection area) the more likely the beacon the unchecked area will be there.
    # In the end it's not a good euristic but I kept the code
    density = sum([abs(x1 - x2) for (x1, x2) in line_intersections])

    # Filter overlaps
    checked_spots = []
    current_intersection = line_intersections[0]
    for i in range(1,len(line_intersections)):
        new_intersection = line_intersections[i]
        if new_intersection[0] > current_intersection[1] + 1:
            checked_spots.append(current_intersection)
            current_intersection = new_intersection
        elif new_intersection[1] <= current_intersection[1]:
            # The new intersection is contained by the current one
            continue
        else:
            # The right border of the new intersection extends the current one
            current_intersection[1] = new_intersection[1]
    checked_spots.append(current_intersection)

    if verbose:
        print('Here is the same list simplified: {}'.format(checked_spots))
    
    return checked_spots, density

checked_spots, _ = getCheckedSpots(y)

sumSpots = sum([abs(x1 - x2) for (x1, x2) in checked_spots])
print('In the row where y={}, {} positions cannot contain a \
beacon.'.format(y, sumSpots))

input('Press any key to continue to part 2')

def getUncheckedSpot(checkSpots):
    if len(checkSpots) == 1 and checkSpots[0][0] == 0 and\
       checkSpots[0][1] == maxCoord:
        return None
    if len(checkSpots) == 1:
        if checkSpots[0][0] == 1: return 0
        elif checkSpots[0][1] == maxCoord - 1: return maxCoord
        else:
            raise Exception('Only one non checked spot expected for \
{}'.format(checkSpots))
    elif len(checkSpots) == 2:
        if checkSpots[0][1] + 2 == checkSpots[1][0]:
            return checkSpots[0][1] + 1
        else:
            raise Exception('Only one non checked spot expected for \
{}'.format(checkSpots))
    else:
        raise Exception('Only one non checked spot expected for \
{}'.format(checkSpots))


# Let's try to find the line with unchecked block
# I wanted to use the density presented above as an euristic to guide the search
# but it didn't help. I actually used the opposite heuristic to have a result
# quicker. Menaning that I search in priority lines that seems to be in a quite
# densely checked area.

# This algorithm is a bit messy but it's inspired from dichotomy with the posibility to check everything by keeping in memory the other regions to split and check

b_x = None
b_y = None
regionTree = [[0, maxCoord]]
import time
import os
last_display = time.time() - 1
lineChecked = 0
while len(regionTree) > 0:
    if time.time() - last_display > 0.1:
        last_display = time.time()
        os.system('clear')
        print('Checked {:7>}/{} lines'.format(lineChecked, maxCoord))
    yMin = regionTree[-1][0]
    yMax = regionTree[-1][1]
    border_distance = yMax - yMin
    checkedSpotsMin, densityMin = getCheckedSpots(
            yMin,
            filterOutBoundIntersections=True)
    uncheckedSpot = getUncheckedSpot(checkedSpotsMin)
    lineChecked += 1
    if uncheckedSpot is not None:
        b_x = uncheckedSpot
        b_y = yMin
        break
    elif border_distance == 0:
        regionTree.pop()
        continue
    checkedSpotsMax, densityMax = getCheckedSpots(
            yMax,
            filterOutBoundIntersections=True)
    uncheckedSpot = getUncheckedSpot(checkedSpotsMax)
    lineChecked += 1
    if uncheckedSpot is not None:
        b_x = uncheckedSpot
        b_y = yMax
        break
    elif border_distance == 1:
        regionTree.pop()
        continue
    
    # We split this region in too
    regionTree.pop()
    yMiddle = yMin + border_distance // 2
    left = [yMin + 1, yMiddle]
    right = [yMiddle + 1, yMax - 1]
    if densityMin > densityMax:
        if border_distance > 2:
            regionTree.append(right)
        regionTree.append(left)
    else:
        regionTree.append(left)
        if border_distance > 2:
            regionTree.append(right)

print('Beacon found at position (x={}, y={})'.format(b_x, b_y))
print('The tuning frequency is thus {}'.format(b_x * 4000000 + b_y))

