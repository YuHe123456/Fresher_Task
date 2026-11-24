import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

m_dry = 50.0 # kg, mass with no propellant
m_prop = 11.20 # kg, propellant mass at ignition (all burnt by end of thrust curve)
d = 0.177 # m, reference diameter

rail_length = 12.0 # m
rail_elevation = 84.0 # deg, up from horizontal (90 = vertical)
rail_heading = 90.0 # deg, clockwise from north (90 = tilted towards east)

h_site = 0.0 # m above sea level
g = 9.81 # m/s^2

thrust_curve = pd.read_csv('Data/thrust_curve.csv')

def rk4(f, t0, y0, t_end, h):

    t_values = np.arange(t0, t_end + h, h) # Creates array of times with gap h from t to t_end
    y_values = np.zeros(len(t_values))

    y_values[0] = y0

    for i in range(1,len(t_values)):
        t = t_values[i-1]
        y = y_values[i-1]

        y_values[i] = y_values[i-1] + rk4_step(f, t, y, h)

    
    return t_values,y_values

# # Example usage: solve dy/dt = -2y with y(0) = 1
# def f(t, y):
#     return -2.0 * t**2

# t, y = rk4(f, -1, 1, 1, 0.1)

def rk4_step(f, t, y, h):

    k1 = f(t,y) # Original gradient at t,y
    k2 = f(t + (h * 0.5), y + (h * 0.5) * k1) # New gradient at t + h/2, y0 + h/2 * k1
    k3 = f(t + (h * 0.5), y + (h * 0.5) * k2) # New gradient at t + h/2, t0 + h/2 * k2
    k4 = f(t + h, y + h * k3) # New gradient at t + h, t0 + h(k3)

    weighted_y_increase = (h/6) * (k1 + 2*(k2) + 2*(k3) + k4)

    return weighted_y_increase

def find_total_impulse():

    global thrust_curve

    time_values = np.array(thrust_curve['time_s'])
    thrust_values = np.array(thrust_curve['thrust_N'])

    time_intervals = time_values[1:] - time_values[:-1]
    thrust_interval_values = (thrust_values[1:] + thrust_values[:-1]) / 2 

    total_impulse = np.sum(time_intervals * thrust_interval_values) # Trapezium rule to estimate area

    return total_impulse

def interp_thrust(time,position): # Returns thrust at a given time elapsed

    global thrust_curve
    global total_impulse

    time_values = thrust_curve['time_s']
    thrust_values = thrust_curve['thrust_N']

    return np.interp(time, time_values, thrust_values) 

total_impulse = find_total_impulse()
position_0 = 0
velocity_0 = 0 
mass_0 = m_dry + m_prop

state_vector = [position_0, velocity_0, mass_0]

# dV/dt = ( d thrust / d t ) / mass 
# Create velocity curve 

time_values, impulse_values = rk4(interp_thrust, 0, 0, 5.5, 0.1)


plt.plot(time_values, impulse_values)

plt.show()


# 

# State vector: (Position, Velocity, Mass, phi)
