from ElementsEnvironment import Dirtiness, Platpen
from Utils import childOutside, closestChild, closestDirtiness, closestPlatpen, directionToMove
from RobotBase import RobotBase

class Robot1(RobotBase):
    def __init__(self):
        super().__init__()
    
    def Move(self, environment, direction = 1):
        if not self.charged and childOutside(environment.childrens):
            closest = closestChild(self.row, self.column, environment)
            directionMove = directionToMove(self.row, self.column, closest[0], closest[1])
            return self.MoveRobot(environment, directionMove)
        elif not self.charged and not environment.field[self.row][self.column] is None and isinstance(environment.field[self.row][self.column], Dirtiness):
            self.Clean(environment)
            return True
        elif not self.charged:
            closest = closestDirtiness(self.row, self.column, environment)
            directionMove = directionToMove(self.row, self.column, closest[0], closest[1])
            return self.MoveRobot(environment, directionMove)
        elif self.charged and not environment.field[self.row][self.column] is None and isinstance(environment.field[self.row][self.column], Platpen):
            self.DropChild(environment)
            return True
        elif self.charged:
            closest = closestPlatpen(self.row, self.column, environment)
            directionMove = directionToMove(self.row, self.column, closest[0], closest[1])
            return self.MoveRobot(environment, directionMove)
        else:
            return self.MoveRobot(environment)
