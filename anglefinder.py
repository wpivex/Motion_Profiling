import math
import csv

# DESMOS https://www.desmos.com/calculator/zss45xap3f

stepNum = 20 # number of steps between points
points = [ [20, 10], [29.07,-5.394], [30, 20] ] # list of x,y positions along desired path

a1 = 22.0 # length of arm 1 
a2 = 14.0 # length of arm 2 (inches)
y_offset = 8.0 # a little vertical gap above the joint (inches)

# 1 if positive/0, -1 if negative
def sign(x):
    if x < 0:
        return -1
    return 1

def findAngles(x,y):
    #print("Finding angle for ({},{})".format(x,y))

    # adjust for offset
    y -= y_offset
    
    # in radians, angles q1 and q2
    q2 = math.acos((x**2 + y**2 - a1**2 - a2**2) / (2*a1*a2)) * sign(y) * -1
    q1 = math.atan(y / x) - math.atan( (a2 * math.sin(q2) /  (a1 + a2 * math.cos(q2)) ))

    q1 = (q1 * 180 / math.pi)
    q2 = (q2 * 180 / math.pi)

    return [q1,q1+q2] # The q2 angle calculated is relative to the x axis, so we must add q1 to have it relative to the joint

def getPath(p1, p2):
    x_incr = (p2[0] - p1[0]) / stepNum
    y_incr = (p2[1] - p1[1]) / stepNum
    path_points = []
    for i in range(stepNum):
        path_points.append([p1[0] + ((i+1) * x_incr), p1[1] + ((i+1) * y_incr)])
    return path_points

def getFullPath(points):
    first = points.pop(0)
    first_point = findAngles(first[0], first[1])
    full_path = [first_point]
    for x,y in points:
        q1,q2 = findAngles(x,y)
        short_path = getPath(full_path[-1], [q1, q2])
        full_path += short_path
    return full_path

def display(points):

    print("Converting between given (x,y) points to degree values of Q1 and Q2, indicating the angles of the two joints.")

    print_array = [["(x,y)", "Q1", "Q2"]]
    for x, y in points:
        q1, q2 = findAngles(x, y)
        print_array.append(["("+str(x)+","+str(y)+")", str(q1), str(q2)])

    for p in print_array:
        print("{: >20} {: >20} {: >20}".format(*p))

def export(points):
    # have array of angle pairs, being the angle for the left then right joints, respectively
    with open('motion_profile.csv', 'w', newline='') as csvfile:
        pathwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        full_path = getFullPath(points)
        for x, y in full_path:
            pathwriter.writerow([x, y])

display(points)
export(points)
