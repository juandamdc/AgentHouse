from ElementsEnvironment import Element, Obstacle, Child
from random import randint

class RobotBase(Element):
    def __init__(self):
        super().__init__(-1, -1, False)
        self.charged = False
        self.child = None

    def Move(self, environment):
       return self.MoveRobot(environment)

    def MoveRobot(self, environment, direction = -1):
        if direction == -1:
            direction = randint(1,4)

        if direction == 1:
            if self.row > 0 and (environment.field[self.row - 1][self.column] is None or not isinstance(environment.field[self.row - 1][self.column], Obstacle)):
                self.UpdateRow( self.row - 1)
                self.CheckChild(environment)
                return True
            else:
                return False
        elif direction == 2:
            if self.column < environment.columns - 1 and (environment.field[self.row][self.column + 1] is None or not isinstance(environment.field[self.row][self.column + 1], Obstacle)):
                self.UpdateColumn( self.column + 1)
                self.CheckChild(environment)
                return True
            else:
                return False
        elif direction == 3:
            if self.row < environment.rows - 1 and (environment.field[self.row + 1][self.column] is None or not isinstance(environment.field[self.row + 1][self.column], Obstacle)):
                self.UpdateRow( self.row + 1)
                self.CheckChild(environment)
                return True
            else:
                return False
        else:
            if self.column > 0 and (environment.field[self.row][self.column - 1] is None or not isinstance(environment.field[self.row][self.column - 1], Obstacle)):
                self.UpdateColumn( self.column - 1)
                self.CheckChild(environment)
                return True
            else:
                return False        
    
    def CheckChild(self, environment):
        if isinstance(environment.field[self.row][self.column], Child):
            self.charged = True
            self.child = environment.field[self.row][self.column]
            environment.field[self.row][self.column].free = False
            environment.field[self.row][self.column] = None

    def Clean(self, environment):
        environment.field[self.row][self.column] = None
        environment.cantDirtiness -= 1

    def DropChild(self, environment):
        self.child.platpen = True
        self.child = None
        self.charged = False
        environment.field[self.row][self.column].child = True
