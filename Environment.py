from ElementsEnvironment import *
from Utils import *
from RobotBase import RobotBase

class Environment:
    def __init__(self, rows, columns, dirtinessPorcent, obstaclePorcent, childsNumber, change):
        self.rows = rows
        self.columns = columns
        self.field = [ [None for _ in range(columns)] for _ in range(rows)]
        self.dirtinessPorcent = dirtinessPorcent
        self.obstaclePorcent = obstaclePorcent
        self.childsNumbers = childsNumber
        self.change = change

        self.robot = RobotBase()
        self.childrens = []
        self.cantObstacles = 0
        self.cantDirtiness = 0
        self.cantFree = rows * columns
        self.InitialScenario()


    def InitialScenario(self):
        # ubicar los corrales
        for i in range(0, self.childsNumbers):
            self.field[0][i] = Platpen(0,i)

        # ubicar los obstaculos
        self.cantObstacles = 0
        while (self.cantObstacles / (self.rows * self.columns - 2 * self.childsNumbers - 1)) * 100 < self.obstaclePorcent:
            (row, column) = getFreePosition(self, self.rows, self.columns)
            self.field[row][column] = Obstacle(row, column)
            self.cantObstacles += 1

        self.cantFree = self.rows * self.columns - 2 * self.childsNumbers - self.cantObstacles - 1

        # ubicar la suciedad
        self.cantDirtiness = 0
        while (self.cantDirtiness / self.cantFree) * 100 < self.dirtinessPorcent:
            (row, column) = getFreePosition(self, self.rows, self.columns)
            self.field[row][column] = Dirtiness(row, column)
            self.cantDirtiness += 1

        # ubicar los ninnos
        cant_child = 0
        while cant_child != self.childsNumbers:
            (row, column) = getFreePosition(self, self.rows, self.columns)
            child = Child(row, column)
            self.childrens.append(child)
            self.field[row][column] = child
            cant_child += 1



    def Run(self, robot):
        # ubicando al robot
        (row, column) = getFreePosition(self, self.rows, self.columns)
        robot.row = row
        robot.column = column
        self.robot = robot


        # running
        t = 0
        while self.CondSteps(t) and not self.CondFiredRobot() and not self.CondJobDone():
            robot.Move(self)

            for child in self.childrens:
                if child.free:
                    child.Move(self)

            t += 1
            
            # print(f"Despues del turno: {t}")
            # print(self)
            
            if t % self.change == 0:
                self.EnvironmentChange()
                # print("despues del cambio")
                # print(self)


        if not self.CondSteps(t):
            endStatus = 0
        elif self.CondFiredRobot():
            endStatus = 1
        else:
            endStatus = 2

        return (endStatus, self.DirtinessPorcent())
        


    def DirtinessPorcent(self):
        return (self.cantDirtiness / self.cantFree) * 100

    def CondSteps(self, t):
        return t < self.change * 100

    def CondFiredRobot(self):
        return self.DirtinessPorcent() >= 60

    def CondJobDone(self):
        return all( child.platpen for child in self.childrens) and self.DirtinessPorcent() == 0 

    def EnvironmentChange(self):
        for row in range(self.rows):
            for column in range(self.columns):
                if self.field[row][column] is None or isinstance(self.field[row][column], Platpen):
                    continue
                else:
                    (newRow, newColumn) = getFreePosition(self, self.rows, self.columns)
                    self.field[row][column].UpdateRow(newRow)
                    self.field[row][column].UpdateColumn(newColumn)
                    self.field[newRow][newColumn] = self.field[row][column]
                    self.field[row][column] = None

    def isTheRobotLocation(self, row, column):
        if self.robot is None:
            return False
        elif row == self.robot.row and column == self.robot.column:
            return True
        else:
            return False


    def __str__(self):
        rep = ''

        for row in range(self.rows):
            for column in range(self.columns):
                if self.field[row][column] is None:
                    rep += '_ '
                else:
                    rep += str(self.field[row][column]) + ' '

            rep += '\n'

        rep += f'Robot: {self.robot.row} {self.robot.column}'

        return rep