from box import box
from collections import deque

class Crossroads:
    def __init__(self, name, neighbours, occupied = False, rack = False):
        #neighbours are [north node, east node, south node, west node]
        self.neighbours = neighbours
        self.occupied = occupied #does this have a box?
        self.rack = rack #does this have somewhere to put a box?
        self.name = name
        self.label = name.split()

    def Update_neighbours(self, new_neighbours):
        self.neighbours = new_neighbours

class Navigator:
    def __init__(self, start, orientation, robot, destination=None, moving = False):
        # 0-north, 1-east, 2-south, 3-west
        self.start = start
        self.destination = destination
        self.orientation = orientation
        self.robot = robot
        self.moving = moving

        def Update_neighbours(self, new_neighbours):
            self.neighbours = new_neighbours

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

    def FollowRoute(self, route):
        routeCopy = route
        #set start to first node in route and destination to second
        self.start = routeCopy.pop()
        self.destination = routeCopy.pop()
        #now loop through until route is empty:
        while len(routeCopy >= 0):
            #go to next node
            self.NavStep()
            #current node is now old destination
            self.start = self.destination
            #new destination is start of remaining route
            self.destination = routeCopy.pop()
        #at the end of this loop, route will be empty but we won't have gone to the last node. so
        self.NavStep() #do the final step


#map
# |-             -|
# |-             -| naming system - lower - L__, upper -U__
# |-             -|                 east - _E_, west - _W_, central - _C_
# |-             -|                 racks - __R_, junctions - __J_, boxes __B_
# |-             -|                 then number north-to-south
# |-             -|
# |               |
# |-B           B-|
# |               |
# |-B           B-|
# |     ┌-┰-┐     |	
# L-----+-┸-+-----┘

#DECLARING NODES

# lower west junctions
lwj1 = Crossroads("lwj1", [])
lwj2 = Crossroads("lwj2", [])
lwj3 = Crossroads("lwj3", [])
lwj4 = Crossroads("lwj4", [])
lwj5 = Crossroads("lwj5", [])
lwj6 = Crossroads("lwj6", [])
lwj7 = Crossroads("lwj7", [])
lwj8 = Crossroads("lwj8", [])
lwj9 = Crossroads("lwj9", [])

# lower east junctions
lej1 = Crossroads("lej1", [])
lej2 = Crossroads("lej2", [])
lej3 = Crossroads("lej3", [])
lej4 = Crossroads("lej4", [])
lej5 = Crossroads("lej5", [])
lej6 = Crossroads("lej6", [])
lej7 = Crossroads("lej7", [])
lej8 = Crossroads("lej8", [])
lej9 = Crossroads("lej9", [])

# upper junctions
ucj1 = Crossroads("ucj1", [])
ucj2 = Crossroads("ucj2", [])
ucj3 = Crossroads("ucj3", [])
ucj4 = Crossroads("ucj4", [])
ucj5 = Crossroads("ucj5", [])
ucj6 = Crossroads("ucj6", [])

# specials
strt = Crossroads("strt", [])
crse = Crossroads("crse", [])
crsw = Crossroads("crsw", [])
ende = Crossroads("ende", [])
endw = Crossroads("endw", [])
endu = Crossroads("endu", [])  # End of upper part
lccj = Crossroads("lccj", [])  # Just north of start
lcej = Crossroads("lcej", [])  # Just northeast of start
lcwj = Crossroads("lcwj", [])  # Just northwest of start

# lower west racks
lwr1 = Crossroads("lwr1", [None, None, None, lwj1], rack=True)
lwr2 = Crossroads("lwr2", [None, None, None, lwj2], rack=True)
lwr3 = Crossroads("lwr3", [None, None, None, lwj3], rack=True)
lwr4 = Crossroads("lwr4", [None, None, None, lwj4], rack=True)
lwr5 = Crossroads("lwr5", [None, None, None, lwj5], rack=True)
lwr6 = Crossroads("lwr6", [None, None, None, lwj6], rack=True)

# lower west boxes
lwb1 = Crossroads("lwb1", [], occupied=True)
lwb2 = Crossroads("lwb2", [], occupied=True)

# lower east racks
ler1 = Crossroads("ler1", [None, lej1, None, None], rack=True)
ler2 = Crossroads("ler2", [None, lej2, None, None], rack=True)
ler3 = Crossroads("ler3", [None, lej3, None, None], rack=True)
ler4 = Crossroads("ler4", [None, lej4, None, None], rack=True)
ler5 = Crossroads("ler5", [None, lej5, None, None], rack=True)
ler6 = Crossroads("ler6", [None, lej6, None, None], rack=True)

# lower east boxes
leb1 = Crossroads("leb1", [], occupied=True)
leb2 = Crossroads("leb2", [], occupied=True)

# upper west racks
uwr1 = Crossroads("uwr1", [], rack=True)
uwr2 = Crossroads("uwr2", [], rack=True)
uwr3 = Crossroads("uwr3", [], rack=True)
uwr4 = Crossroads("uwr4", [], rack=True)
uwr5 = Crossroads("uwr5", [], rack=True)
uwr6 = Crossroads("uwr6", [], rack=True)

# upper east racks
uer1 = Crossroads("uer1", [], rack=True)
uer2 = Crossroads("uer2", [], rack=True)
uer3 = Crossroads("uer3", [], rack=True)
uer4 = Crossroads("uer4", [], rack=True)
uer5 = Crossroads("uer5", [], rack=True)
uer6 = Crossroads("uer6", [], rack=True)


#CONNECTING NODES
#lower western racks
lwr1.Update_neighbours([None, None, None, lwj1])
lwr2.Update_neighbours([None, None, None, lwj2])
lwr3.Update_neighbours([None, None, None, lwj3])
lwr4.Update_neighbours([None, None, None, lwj4])
lwr5.Update_neighbours([None, None, None, lwj5])
lwr6.Update_neighbours([None, None, None, lwj6])
#lower western boxes
lwb1.Update_neighbours([None, None, None, lwj7])
lwb2.Update_neighbours([None, None, None, lwj8])
#lower eastern racks
ler1.Update_neighbours([None, lej1, None, None])
ler2.Update_neighbours([None, lej2, None, None])
ler3.Update_neighbours([None, lej3, None, None])
ler4.Update_neighbours([None, lej4, None, None])
ler5.Update_neighbours([None, lej5, None, None])
ler6.Update_neighbours([None, lej6, None, None])
#lower eastern boxes
leb1.Update_neighbours([None, lej7, None, None])
leb2.Update_neighbours([None, lej8, None, None])

#lower western junctions
lwj1.Update_neighbours([endw, lwr1, lwj2, None])
lwj2.Update_neighbours([lwj1, lwr2, lwj3, None])
lwj3.Update_neighbours([lwj2, lwr3, lwj4, None])
lwj4.Update_neighbours([lwj3, lwr4, lwj5, None])
lwj5.Update_neighbours([lwj4, lwr5, lwj6, None])
lwj6.Update_neighbours([lwj5, lwr6, lwj7, None])
lwj7.Update_neighbours([lwj6, lwb1, lwj8, None])
lwj8.Update_neighbours([lwj7, lwb2, crsw, None])
lwj9.Update_neighbours([lcwj, strt, None, crsw])

#lower eastern junctions
lej1.Update_neighbours([ende, None, lej2, ler1])
lej2.Update_neighbours([lej1, None, lej3, ler2])
lej3.Update_neighbours([lej2, None, lej4, ler3])
lej4.Update_neighbours([lej3, None, lej5, ler4])
lej5.Update_neighbours([lej4, None, lej6, ler5])
lej6.Update_neighbours([lej5, None, lej7, ler6])
lej7.Update_neighbours([lej6, None, lej8, leb1])
lej8.Update_neighbours([lej7, None, crse, leb2])
lej9.Update_neighbours([lcej, crse, None, strt])

#upper junctions
ucj1.Update_neighbours([endu, uer1, ucj2, uwr1])
ucj2.Update_neighbours([ucj1, uer2, ucj3, uwr2])
ucj3.Update_neighbours([ucj2, uer3, ucj4, uwr3])
ucj4.Update_neighbours([ucj3, uer4, ucj5, uwr4])
ucj5.Update_neighbours([ucj4, uer5, ucj6, uwr5])
ucj6.Update_neighbours([ucj5, uer6, lccj, uwr6])

#upper western junctions
uwr1.Update_neighbours([None, ucj1, None, None])
uwr2.Update_neighbours([None, ucj2, None, None])
uwr3.Update_neighbours([None, ucj3, None, None])
uwr4.Update_neighbours([None, ucj4, None, None])
uwr5.Update_neighbours([None, ucj5, None, None])
uwr6.Update_neighbours([None, ucj6, None, None])

#upper eastern junctions
uer1.Update_neighbours([None, None, None, ucj1])
uer2.Update_neighbours([None, None, None, ucj2])
uer3.Update_neighbours([None, None, None, ucj3])
uer4.Update_neighbours([None, None, None, ucj4])
uer5.Update_neighbours([None, None, None, ucj5])
uer6.Update_neighbours([None, None, None, ucj6])

#corners
crsw.Update_neighbours([lwj8, lwj9, None, None])
crse.Update_neighbours([lej8, None, None, lej9])

#specials
endw.Update_neighbours([None, None, lwj1, None])
ende.Update_neighbours([None, None, lej1, None])
endu.Update_neighbours([None, None, ucj1, None])
strt.Update_neighbours([lccj, lej9, None, lwj9])

lccj.Update_neighbours([ucj6, lcej, strt, lcwj])    
lcej.Update_neighbours([None, None, lej9, lccj])   
lcwj.Update_neighbours([None, lccj, lwj9, None])

# we want the robot to have a start node and a destination node and to know what to do to get bw them
#this requires knowledge of robot orientation and the geometry of the paths coming out of the node

def find_route(strt, end):

    queue = deque([strt])
    came_from = {strt: None}

    while queue:
        node = queue.popleft()
        if node == end: 
            break
        
        for nxt in node.neighbours():
            if nxt is not None and nxt not in came_from:
                came_from[nxt] = node
                queue.append(nxt)

    route = []
    node = end

    while node is not None:
        route.append(node)
        node = came_from[node]
    
    route.reverse
    return route
