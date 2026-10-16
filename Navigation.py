from utime import sleep_ms 
class Crossroads:
    def __init__(self, neighbours, occupied = False, rack = False):
        #neighbours are [north node, east node, south node, west node]
        self.neighbours = neighbours
        self.occupied = occupied #does this have a box?
        self.rack = rack #does this have somewhere to put a box?

class Navigator:
    def __init__(start, destination=None, orientation, robot, moving = False):
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

LWR1 = Crossroads([None, None, None, LWJ1], rack=True)
LWR2 = Crossroads([None, None, None, LWJ2], rack=True)
LWR3 = Crossroads([None, None, None, LWJ3], rack=True)
LWR4 = Crossroads([None, None, None, LWJ4], rack=True)
LWR5 = Crossroads([None, None, None, LWJ5], rack=True)
LWR5 = Crossroads([None, None, None, LWJ6], rack=True)

LER1 = Crossroads([None, LEJ1, None, None], rack=True)
LER2 = Crossroads([None, LEJ2, None, None], rack=True)
LER3 = Crossroads([None, LEJ3, None, None], rack=True)
LER4 = Crossroads([None, LEJ4, None, None], rack=True)
LER5 = Crossroads([None, LEJ5, None, None], rack=True)
LER6 = Crossroads([None, LEJ6, None, None], rack=True)

LWR1 = Crossroads([None, None, None, LWJ1], rack=True)
LWR2 = Crossroads([None, None, None, LWJ2], rack=True)
LWR3 = Crossroads([None, None, None, LWJ3], rack=True)
LWR4 = Crossroads([None, None, None, LWJ4], rack=True)
LWR5 = Crossroads([None, None, None, LWJ5], rack=True)
LWR5 = Crossroads([None, None, None, LWJ6], rack=True)


# we want the robot to have a start node and a destination node and to know what to do to get bw them
#this requires knowledge of robot orientation and the geometry of the paths coming out of the node
