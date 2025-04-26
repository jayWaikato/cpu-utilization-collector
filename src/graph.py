from matplotlib import pyplot as pyp
import matplotlib.animation as animation
import json
from connection import devices
from datetime import datetime, timedelta

figures = {}
subplots = {}

def moving_average(data, window_size):
    return [sum(data[i:i+window_size])/window_size for i in range(len(data)-window_size+1)]

def time_to_seconds(time_str):
    """Convert time in 'HH:MM:SS' format to seconds since the start of the day."""
    time_obj = datetime.strptime(time_str, "%H:%M:%S")
    return time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second

def seconds_to_hm(seconds):
    """Convert seconds back to 'HH:MM' format."""
    time_obj = timedelta(seconds=seconds)
    # Format the time in HH:MM format
    return str(time_obj)[:5] 

# def seconds_to_time(seconds):
#     """Convert seconds back to 'HH:MM:SS' format."""
#     return str(timedelta(seconds=seconds))  # Use timedelta to convert seconds to HH:MM:SS

def initialize_figures(device_ips):
    for ip in device_ips:
        figures[ip] = pyp.figure()
        subplots[ip] = figures[ip].add_subplot(1,1,1)
    return (figures[ips] for ips in device_ips)

def animation_function(frame,w):

    for key,value in devices.items():
            
        x_axis = []
        y_axis = []
        cpu_data = []
        device = ""

        if key == w :

            device=value
            with open("C:\\Users\\jaych\\Downloads\\cpu.json","r") as read_data:
                
                data = json.load(read_data)
            if device in data:
                cpu_data = data[device]
                for key,value in cpu_data.items():
                    x_axis.append(time_to_seconds(key))
                    y_axis.append(float(value))
                
                window_size = 2# Define your window size (e.g., 5)
                smoothed_x = moving_average(x_axis, window_size)

                smoothed_x_time = [seconds_to_hm(s) for s in smoothed_x]


                print(value)

            subplot = subplots[device]
            subplot.set_title(f"{device}")
            subplot.plot(smoothed_x_time, y_axis[:len(smoothed_x_time)])

    return tuple(subplots[device] for device in devices.values())

# graph_animation1 = animation.FuncAnimation(figure1,animation_function,fargs=("10.10.10.2",),interval=10000,frames=10, cache_frame_data=False)
# graph_animation2 = animation.FuncAnimation(figure2,animation_function,fargs=("10.10.10.3",),interval=10000,frames=10, cache_frame_data=False)

# graph_animation3 = animation.FuncAnimation(figure3,animation_function,fargs=("10.10.10.4",),interval=10000,frames=10, cache_frame_data=False)
# pyp.show()               