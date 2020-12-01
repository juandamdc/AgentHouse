from Environment import *
from Robot1 import Robot1
from Robot2 import Robot2

def CalEst(rows, columns, dirtinessPorcent, obstaclePorcent, childNumber, changeT, robot, rep = 30):
    est = dict()
    est['timeout'] = 0
    est['fired'] = 0
    est['job done'] = 0
    est['accumDirtiness'] = 0

    for _ in range(rep):
        env = Environment(rows, columns, dirtinessPorcent, obstaclePorcent, childNumber, changeT)
        (status, porcent) =  env.Run(robot)
        
        if status == 0:
            est['timeout'] += 1
        elif status == 1:
            est['fired'] += 1
        else:
            est['job done'] += 1

        est['accumDirtiness'] += porcent
    
    est['accumDirtiness'] = est['accumDirtiness'] / rep
    return est


result = CalEst(12, 12, 20, 20, 10, 150, Robot2())
for key in result.keys():
    print(f'{key}: {result[key]}')
