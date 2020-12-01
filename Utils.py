
from ElementsEnvironment import Dirtiness
from random import randint
import math
import queue

def getFreePosition(environment, rows, columns):
    row = randint(0, rows - 1)
    column = randint(0, columns - 1)
    
    while not environment.field[row][column] is None or environment.isTheRobotLocation(row, column):
        row = randint(0, rows - 1)
        column = randint(0, columns - 1)

    return (row, column)


def childOutside(childrens):
    return any(child.free for child in childrens)


def closestPlatpen(row, column, environment):
    platpens = [(0, x) for x in range(environment.childsNumbers) if not environment.field[0][x].child]

    closest = None
    minDest = math.inf

    for platpen in platpens:
        if abs(platpen[0] - row) + abs(platpen[1] - column) < minDest:
            minDest = abs(platpen[0] - row) + abs(platpen[1] - column)
            closest = platpen
    
    return closest


def closestChild(row, column, environment):
    childs = [(child.row, child.column) for child in environment.childrens if child.free]

    closest = None
    minDist = math.inf

    for child in childs:
        if abs(child[0] - row) + abs(child[1] - column) < minDist:
            minDist = abs(child[0] - row) + abs(child[1] - column)
            closest = child

    return closest


def closestDirtiness(row, column, environment):
    visited = dict()
    toVisit = queue.deque()
    toVisit.append((row, column))

    while len(toVisit) > 0:
        (stepRow, stepColumn) = toVisit.popleft()
        if visited.get((stepRow, stepColumn), None) is None: 
            if isinstance(environment.field[stepRow][stepColumn], Dirtiness):
                break
            else:
                if stepRow - 1 > 0 and visited.get((stepRow - 1, stepColumn), None) is None:
                    toVisit.append((stepRow - 1, stepColumn))
                if stepRow < environment.rows - 1 and visited.get((stepRow + 1, stepColumn), None) is None:
                    toVisit.append((stepRow + 1, stepColumn))
                if stepColumn - 1 > 0 and visited.get((stepRow, stepColumn - 1), None) is None:
                    toVisit.append((stepRow, stepColumn - 1))
                if stepColumn < environment.columns - 1 and visited.get((stepRow, stepColumn + 1), None) is None:
                    toVisit.append((stepRow, stepColumn + 1))

            visited[(stepRow, stepColumn)] = True

    return (stepRow, stepColumn)


def directionToMove(xNow, yNow, xFinal, yFinal):
    if xNow < xFinal:
        return 3     # south
    elif xNow > xFinal:
        return 1     # north
    elif yNow < yFinal:
        return 2     # east
    elif yNow > yFinal:
        return 4     # west
    else:
        return 0

