import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def rk4(f, t0, t_end, y0, h):

    t_values = np.arange(t0, t_end + h, h) # Creates array of times with gap h from t to t_end
    y_values = np.zeros(len(t_values))

    y_values[0] = y0

    for i in range(1,len(t_values)):
        t = t_values[i-1]
        y = y_values[i-1]

        y_values[i] = y_values[i-1] + rk4_step(f, t, y, h)

    
    return t_values,y_values

def rk4_step(f, t, y, h):

    k1 = f(t,y) # Original gradient at t,y
    k2 = f(t + (h * 0.5), y + (h * 0.5) * k1) # New gradient at t + h/2, y0 + h/2 * k1
    k3 = f(t + (h * 0.5), y + (h * 0.5) * k2) # New gradient at t + h/2, t0 + h/2 * k2
    k4 = f(t + h, y + h * k3) # New gradient at t + h, t0 + h(k3)

    weighted_y_increase = (h/6) * (k1 + 2*(k2) + 2*(k3) + k4)

    return weighted_y_increase

# Example usage: solve dy/dt = -2y with y(0) = 1

def f(t, y): # Function represents dy/dt 

    global force
    global mass 

    return force / mass
    

t, y = rk4(f, 0, 3, 1, 0.1)

plt.plot(t,y)
plt.show()


force = 5 # N = m * dv/dt 
mass = 1 # N 
v_0 = 0 
r_0 = 0 

state_vector = [r_0, v_0]

