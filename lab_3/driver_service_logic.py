from enum import Enum
import time
import random

# class RobotLocation():
#     def __init__(self, x:int, y: int):
#         self.x, self.y = 0 , 0 # initial pose

def generate_path():
    """
    Generates a path with a random number of poses that have random x and y coordinates. 
    Meant to represent the response of the path planner service.
    """
    length = random.randint(1, 10)
    path = []
    for _ in range(length):
        x = random.randint(0, 10)
        y = random.randint(0, 10)
        path.append((x, y))
    return path

# get the next pose in the randomly generated path
def next_pose(): 
    """
    Returns the next pose in the generated path.
    Meant to represent a future function in the driver node that iterates through the poses 
    in path and calls `go_to()` for each one.
    """
    try:
        next_pose = next(pose_iter)
        print(f"Next pose: {next_pose}")
        return next_pose
    except StopIteration:
        print("========== Path driven! ==========")
        return None

def turn_drive_sim():
    """
    Cycles through idle, turn, and drive states that will occur when using the turn-drive method of driving.
    Represents the core state machine in the driver node, mostly the function `go_to()`.
    """
    global state
    goal = next_pose()
    while goal is not None:  # runs the loop until the path returns nothing, considered blocking i think so odom updates would not work
        if state == "idle":
            print("velocity = 0")
            time.sleep(random.randint(0, 4))
            state = "turn"
        elif state == "turn":
            print("turning...")
            time.sleep(random.randint(0, 4))
            print("done turning")
            state = "drive"
        elif state == "drive":
            print(f"driving to {goal}")
            time.sleep(random.randint(0, 4))
            print("done driving")
            state = "idle"
            goal = next_pose()

# run ()
state = "idle" # initial robot state
path = generate_path() # generate path 
print(f"Generated path: {path}")
pose_iter = iter(path) # make path iterable
turn_drive_sim() # run simulation of state machine