#imports
import matplotlib.pyplot as plt
import sys

# NOTE 
#       Grind amount and speed over time
#  |                                         |
# S|                                         | A
# P|                                         | M
# E|                                         | O
# E|                                         | U
# P|                                         | N
#  |                                         | T
#  +-----------------------------------------+
#                   TIME                        

# Data format:
# runtime (s); speed (rpm); amount (g)
# 0; 200; 0
# 1:00; 200; 0.0
# 2:00; 192; 0.6
# 3:00; 197; 1.2
# 4:00; 190; 1.8
# . . .


def plotter(data: set, data2: set):
    
    # Subplot so we can have dual Y-axis with shared X
    fig, ax = plt.subplots(figsize = (16, 6))
    
    # Based on empirical data I determined that if rpm drops below 200, PWM duty cycle ~50%, 
    # the motor will most likely stall and it wont start turning unless it is reversed manually
    # Thus, I set critical limit that shows the low bound of dynamic speed control 
    critical_limit = 200

    ax.plot(data["runtime (s)"], data["speed (rpm)"], "orange", linestyle="--", label="Full Throttle Speed")
    ax.plot(data2["runtime (s)"], data2["speed (rpm)"], "b", marker="*", linestyle="solid", label="Dynamic Speed")
    
    ax.axhline(critical_limit, color="r", label="Speed low bound")

    ax.set_xlabel("Runtime (s)")
    ax.set_ylabel("Speed (RPM)")
    ax.legend(loc="upper left", bbox_to_anchor=(0,1.15))
   
    ax1 = ax.twinx()

    ax1.plot(data["runtime (s)"], data["amount (g)"], "orange", linestyle=":", label="Full Throttle Gain")
    ax1.plot(data2["runtime (s)"], data2["amount (g)"], "b", marker="*", linestyle="-.", label="Dynamic Gain")
    ax1.set_ylabel("Amount (g)")
    ax1.legend(loc="upper right", bbox_to_anchor=(1,1.15))


    plt.show()
    

def sc_reader(filename: str):
    # Set
    data = {}

    with open(filename, "r") as f:
        # Read all lines
        lines = f.readlines()
        header = lines.pop(0).strip()
        kt, ks, ka = header.split(";")
        data[kt] = []
        data[ks] = []
        data[ka] = []
        # Parse data
        for l in lines:
            # Remove '\n'
            strp = l.strip()
            t, s, a = strp.split(";")
            data[kt].append(int(t))
            data[ks].append(int(s))
            data[ka].append(float(a))

    return data

if __name__=="__main__":
    if len(sys.argv) < 3:
        print("./prog <file1> <file2>")
        exit(0)

    d1 = sc_reader(sys.argv[1])
    d2 = sc_reader(sys.argv[2])
    
    plotter(d1, d2)

