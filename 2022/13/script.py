from functools import cmp_to_key

# I was in a train without internet access when I did that do interpret the input
# file as lists.
# After checking I could have used json.loads or asp.literal_eval()
# Anyway, this works. I's a simple parser

def encapsulatedListParser(inputString):
    outputList = None
    listTree = []
    newNumber = ''
    for i, (c, pc) in enumerate(zip(inputString, [None, *inputString[:-1]])):
        if c == '[':
            if outputList is None:
                outputList = []
                listTree.append(outputList)
            else:
                listTree[-1].append([])
                listTree.append(listTree[-1][-1])
        elif c== ']':
            if len(listTree) == 0:
                raise Exception('Unexpected token {} at position {}'.format(c, i))
            else:
                if newNumber != '':
                    listTree[-1].append(int(newNumber))
                    newNumber = ''
                listTree.pop()
        elif c==',':
            if pc in [None, ',', '[']:
                raise Exception('Unexpected token {} at position {}'.format(c, i))
            if newNumber != '':
                listTree[-1].append(int(newNumber))
                newNumber = ''
        else:
            newNumber += c
    if len(listTree) != 0:
        raise Exception('Missing trailing \']\'')

    return outputList

### Importing and formating data

pairs = []
with open('input.txt', 'r') as f:
    newPair = []
    for i, line in enumerate(f):
        if line == '\n':
            if len(newPair) == 2:
                pairs.append(newPair)
            elif len(newPair) != 0:
                raise Exception('Too many messages for this pair - line {}'.format(i))
            newPair = []
        else:
            parsedList = encapsulatedListParser(line)
            newPair.append(parsedList)
    if len(newPair) == 2:
        pairs.append(newPair)

### Litle function to compare items of the message

"""
Returns -1 if left is smaller than right and 1 in the opposite case
(according to the definition stated in the problem description)
Returns 0 if the items are equal.
"""
def compareItems(left, right, verbose=False):
    assert(type(left)==list)
    assert(type(right)==list)
    if verbose:
        print('- Compare {} vs {}'.format(left, right))
    leftListTree = [left]
    rightListTree = [right]
    indexList = [0]
    while True:
        gap = '  ' * len(indexList)
        leftRanOut = indexList[-1] >= len(leftListTree[-1])
        rightRanOut = indexList[-1] >= len(rightListTree[-1])
        if leftRanOut and rightRanOut:
            # The length of the right Tree should be exactly the same
            if len(leftListTree) == 1:
                # We have checked all elements without having any difference
                return 0
            else:
                indexList.pop()
                indexList[-1] += 1
                leftListTree.pop()
                rightListTree.pop()
                continue
        elif leftRanOut:
            if verbose:
                print(gap + '- Left side rand out of items, so inputs are in \
right order')
            return -1
        elif rightRanOut:
            if verbose:
                print(gap + '- Right side rand out of items, so inputs are not \
in right order')
            return 1
        leftValue = leftListTree[-1][indexList[-1]]
        rightValue = rightListTree[-1][indexList[-1]]
        if verbose:
            print(gap + '- Compare {} vs {}'.format(leftValue, rightValue))
        if type(leftValue) == int and type(rightValue) == int:
            if leftValue < rightValue:
                if verbose:
                    print(gap + '- Left side is smaller, so inputs are in right \
order')
                return -1
            elif leftValue > rightValue:
                if verbose:
                    print(gap + '- Right side is smaller, so inputs are not in \
right order')
                return 1
            indexList[-1] += 1
        elif type(leftValue) == list and type(rightValue) == int:
            leftListTree.append(leftValue)
            rightListTree.append([rightValue])
            indexList.append(0)
            if verbose:
                print(gap + '- Mixed types; convert right to [{}] and retry \
comparison'.format(rightValue))
        elif type(leftValue) == int and type(rightValue) == list:
            leftListTree.append([leftValue])
            rightListTree.append(rightValue)
            indexList.append(0)
            if verbose:
                print(gap + '- Mixed types; convert left to [{}] and retry \
comparison'.format(leftValue))
        elif type(leftValue) == list and type(rightValue) == list:
            leftListTree.append(leftValue)
            rightListTree.append(rightValue)
            indexList.append(0)
        else:
            raise Exception('Unexpected type in inputs')

### Let's count how many pairs are in the right order

sumCorrectPairId = 0
for i, (left, right) in enumerate(pairs):
    pairId = i + 1
    verbose = True
    if verbose: print('== Pair {} =='.format(pairId))
    inRightOrder = compareItems(left, right, verbose=verbose) < 0
    if verbose: print('') # Jump a line
    if inRightOrder:
        sumCorrectPairId += pairId

print('The sum of ids of pair in right order is {}.'.format(sumCorrectPairId))


### Let's find the decoder key

allItems = [[[2]], [[6]]]
for left, right in pairs:
    allItems.append(left)
    allItems.append(right)

sortedList = sorted(allItems, key=cmp_to_key(compareItems))

with open('output.txt', 'w') as f:
    f.writelines([str(item) + '\n' for item in sortedList])

print('The decoder key is {}.'.format((sortedList.index([[2]]) + 1) * (sortedList.index([[6]]) + 1)))



