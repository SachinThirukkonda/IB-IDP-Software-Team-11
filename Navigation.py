from utime import sleep_ms 
class Crossroads:
    def __init__(self, neighbours, occupied = False, rack = False):
        #neighbours are [north node, east node, south node, west node]
        self.neighbours = neighbours
        self.occupied = occupied #does this have a box?
        self.rack = rack #does this have somewhere to put a box?

class Navigator:
    def __init__(self, start, orientation, robot, destination=None, moving = False):
        # 0-north, 1-east, 2-south, 3-west
        self.start = start
        self.destination = destination
        self.orientation = orientation
        self.robot = robot
        self.moving = moving

    def Orient(self):
        #find difference between own orientation and location of destination
        dest_orientation = self.start.neighbours.index(self.destination)
        #we now find the difference between the two; 
        # if we get 1 or -3, we know we need to turn right
        # if we get -1 or 3, we know we need to turn left
        # if we get +-2, we know we need to do a 180
        delta_orientation = (dest_orientation - self.orientation) % 4
        if delta_orientation == 0:
            return
        if delta_orientation == 1:
            #turn left
            self.robot.Turn(-1)
        if delta_orientation == 2:
            #do a 180
            self.robot.one_eighty_degree_turn()
        if delta_orientation == 3:
            #turn right
            self.robot.Turn(1)
    
    def NavStep(self):
        self.Orient()
        self.robot.Forward_Until_Node(80)


#map
# |-             -|
# |-             -| naming system - lower - L__, upper -U__
# |-             -|                 east - _E_, west - _W_
# |-             -|                 racks - __R_, junctions - __J_, boxes __B_
# |-             -|                 then number north-to-south
# |-             -|
# |               |
# |-B           B-|
# |               |
# |-B           B-|
# |     ┌-┰-┐     |	
# L-----+-┸-+-----┘

lwr1 = Crossroads([None, None, None, lw1], rack=True)
lwr2 = Crossroads([None, None, None, lw2], rack=True)
lwr3 = Crossroads([None, None, None, lw3], rack=True)
lwr4 = Crossroads([None, None, None, lw4], rack=True)
lwr5 = Crossroads([None, None, None, lw5], rack=True)
lwr6 = Crossroads([None, None, None, lw6], rack=True)

ler1 = Crossroads([None, lej1, None, None], rack=True)
ler2 = Crossroads([None, lej2, None, None], rack=True)
ler3 = Crossroads([None, lej3, None, None], rack=True)
ler4 = Crossroads([None, lej4, None, None], rack=True)
ler5 = Crossroads([None, lej5, None, None], rack=True)
ler6 = Crossroads([None, lej6, None, None], rack=True)

uwr1 = Crossroads([None, None, None, lwj1], rack=True)
uwr2 = Crossroads([None, None, None, lwj2], rack=True)
uwr3 = Crossroads([None, None, None, lwj3], rack=True)
uwr4 = Crossroads([None, None, None, lwj4], rack=True)
uwr5 = Crossroads([None, None, None, lwj5], rack=True)
uwr6 = Crossroads([None, None, None, lwj6], rack=True)


# we want the robot to have a start node and a destination node and to know what to do to get bw them
#this requires knowledge of robot orientation and the geometry of the paths coming out of the node

