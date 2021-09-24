import math


# DESMOS https://www.desmos.com/calculator/zss45xap3f

# dummy points
points = [ [29.07,-5.394]]

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
    print((x**2 + y**2 - a1**2 - a2**2) / (2*a1*a2))
    q2 = math.acos((x**2 + y**2 - a1**2 - a2**2) / (2*a1*a2)) * sign(y) * -1
    q1 = math.atan(y / x) - math.atan( (a2 * math.sin(q2) /  (a1 + a2 * math.cos(q2)) ))

    q1 = (q1 * 180 / math.pi)
    q2 = (q2 * 180 / math.pi)

    return [q1,q1+q2] # The q2 angle calculated is relative to the x axis, so we must add q1 to have it relative to the joint


def display(points):

    print("Converting between given (x,y) points to degree values of Q1 and Q2, indicating the angles of the two joints.")

    for x,y in points:
        q1,q2 = findAngles(x,y)
        print("             (x,y)\t\t\tQ1\t\t    Q2")
        print("({},{})  \t {} \t {}".format(x,y,q1,q2))


display(points)
