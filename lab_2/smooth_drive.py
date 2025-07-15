# for lab2 extra credit smooth drive

"""
PID controller

Output = (Proportional Gain * Error) + 
        (Integral Gain * Integral of Error) + 
        (Derivative Gain * Derivative of Error)

error = target - current

for this particular purpose, euclidian distance to target is what is used for "distance remaining" or error
"""