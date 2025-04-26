import sys
import time
from ip_file_validity import ip_file_valid
from ip_addr_validity import ip_addr_valid
from ip_reachability import ip_reach
from connection import ssh_connection
from create_threads import create_threads
from graph import animation_function,initialize_figures
from matplotlib import pyplot as plt
import matplotlib.animation as animation

ip_list = ip_file_valid()

try:
    ip_addr_valid(ip_list)
except KeyboardInterrupt:
    print("program closed by user")
    sys.exit()

try:
    ip_reach(ip_list)
except KeyboardInterrupt:
    print("program closed by user")
    sys.exit()
    
counter = 0
while counter<1:
    create_threads(ip_list,ssh_connection)
    time.sleep(3)
    counter+=1

switches = ["arista1","arista2","arista3"]
figures = initialize_figures(switches)

def animate(frame, ip):

    return animation_function(frame, w=ip)  # Pass the correct IP

x=  1
animations = {}
for figure in figures:
    x+=1
    animations[x] = animation.FuncAnimation(figure, animate, fargs=(f"10.10.10.{x}",), frames=100, interval=1000, repeat=False)


plt.show()







