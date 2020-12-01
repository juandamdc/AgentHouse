from random import random, randint


class Element:
    def __init__(self, row, column, canBeMoved):
        self.row = row
        self.column = column
        self.canBeMoved = canBeMoved

    def UpdateRow(self, newRow):
        self.row = newRow

    def UpdateColumn(self, newColumn):
        self.column = newColumn

    def Move(self, environment, direction = 1):
        return False

    def __str__(self):
        return 'E'


class Obstacle(Element):
    def __init__(self, row, column):
        super().__init__(row, column, True)

    def Move(self, environment, direction = 1):
        if direction == 1:  # Norte
            if self.row > 0 and not environment.isTheRobotLocation(self.row - 1, self.column) and (environment.field[self.row - 1][self.column] is None or (environment.field[self.row - 1][self.column].canBeMoved and environment.field[self.row - 1][self.column].Move(environment, 1))):
                environment.field[self.row][self.column] = None
                self.UpdateRow(self.row-1)
                environment.field[self.row][self.column] = self
                return True
            else:
                return False

        elif direction == 2:  # East
            if self.column < environment.columns - 1 and not environment.isTheRobotLocation(self.row, self.column + 1) and (environment.field[self.row][self.column + 1] is None or (environment.field[self.row][self.column + 1].canBeMoved and environment.field[self.row][self.column + 1].Move(environment, 2))):
                environment.field[self.row][self.column] = None
                self.UpdateColumn(self.column+1)
                environment.field[self.row][self.column] = self
                return True
            else:
                return False

        elif direction == 3:  # South
            if self.row < environment.rows - 1 and not environment.isTheRobotLocation(self.row + 1, self.column) and (environment.field[self.row + 1][self.column] is None or (environment.field[self.row + 1][self.column].canBeMoved and environment.field[self.row + 1][self.column].Move(environment, 3))):
                environment.field[self.row][self.column] = None
                self.UpdateRow(self.row+1)
                environment.field[self.row][self.column] = self
                return True
            else:
                return False

        else:   # West
            if self.column > 0 and not environment.isTheRobotLocation(self.row, self.column - 1) and (environment.field[self.row][self.column - 1] is None or (environment.field[self.row][self.column - 1].canBeMoved and environment.field[self.row][self.column - 1].Move(environment, 4))):
                environment.field[self.row][self.column] = None
                self.UpdateColumn(self.column-1)
                environment.field[self.row][self.column] = self
                return True
            else:
                return False

    def __str__(self):
        return 'O'


class Dirtiness(Element):
    def __init__(self, row, column):
        super().__init__(row, column, False)

    def Move(self, environment, direction = 1):
        return False

    def __str__(self):
        return 'D'


class Platpen(Element):
    def __init__(self, row, column):
        super().__init__(row, column, False)
        self.child = False

    def Move(self, environment, direction = 1):
        return False

    def __str__(self):
        return 'P'


class Child(Element):
    def __init__(self, row, column):
        super().__init__(row, column, False)
        self.free = True
        self.platpen = False

    def Move(self, environment, direction = 1):
        if self.free:
            is_moving = random()

            if is_moving > 0.5:
                direction = randint(1, 4)

                self.AddDirtiness(self.row, self.column, environment)

                if direction == 1:  # North
                    if self.row > 0  and not environment.isTheRobotLocation(self.row - 1, self.column) and (environment.field[self.row - 1][self.column] is None or (environment.field[self.row - 1][self.column].canBeMoved and environment.field[self.row - 1][self.column].Move(environment, 1))):
                        environment.field[self.row][self.column] = None
                        self.UpdateRow(self.row-1)
                        environment.field[self.row][self.column] = self
                        return True
                    else:
                        return False

                elif direction == 2:  # East
                    if self.column < environment.columns - 1 and not environment.isTheRobotLocation(self.row, self.column + 1) and (environment.field[self.row][self.column + 1] is None or (environment.field[self.row][self.column + 1].canBeMoved and environment.field[self.row][self.column + 1].Move(environment, 2))):
                        environment.field[self.row][self.column] = None
                        self.UpdateColumn(self.column+1)
                        environment.field[self.row][self.column] = self
                        return True
                    else:
                        return False

                elif direction == 3:  # South
                    if self.row < environment.rows - 1 and not environment.isTheRobotLocation(self.row + 1, self.column) and (environment.field[self.row + 1][self.column] is None or (environment.field[self.row + 1][self.column].canBeMoved and environment.field[self.row + 1][self.column].Move(environment, 3))):
                        environment.field[self.row][self.column] = None
                        self.UpdateRow(self.row+1)
                        environment.field[self.row][self.column] = self
                        return True
                    else:
                        return False

                else:   # West
                    if self.column > 0 and not environment.isTheRobotLocation(self.row, self.column - 1) and (environment.field[self.row][self.column - 1] is None or (environment.field[self.row][self.column - 1].canBeMoved and environment.field[self.row][self.column - 1].Move(environment, 4))):
                        environment.field[self.row][self.column] = None
                        self.UpdateColumn(self.column-1)
                        environment.field[self.row][self.column] = self
                        return True
                    else:
                        return False

            else:
                return False
        else:
            return False
    
    def AddDirtiness(self, xBeforeMovement, yBeforeMovement, environment):
        cantChilds = 1

        xs = [xBeforeMovement]
        if xBeforeMovement > 0:
            xs.append(xBeforeMovement - 1)
        if xBeforeMovement < environment.rows - 1:
            xs.append(xBeforeMovement + 1)

        ys = [yBeforeMovement]
        if yBeforeMovement > 0:
            ys.append(yBeforeMovement - 1)
        if yBeforeMovement < environment.columns - 1:
            ys.append(yBeforeMovement + 1)

        for x in xs:
            for y in ys:
                if isinstance(environment.field[x][y], Child) and (x != xBeforeMovement or y != yBeforeMovement):
                    cantChilds += 1

        if cantChilds == 1:
            rep = 1
        elif cantChilds == 2:
            rep = 2
        else:
            rep = 6

        for _ in range(rep):
            newDirtinessX = randint(-1, 1)
            newDirtinessY = randint(-1, 1)

            if environment.field[newDirtinessX][newDirtinessY] is None:
                environment.field[newDirtinessX][newDirtinessY] = Dirtiness(newDirtinessX, newDirtinessY)
                environment.cantDirtiness += 1


    def __str__(self):
        return 'C'