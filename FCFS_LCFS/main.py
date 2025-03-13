import random
import numpy as np
import matplotlib.pyplot as plt
import sys

top = 0
arrivals = []
burst_times = []
n = 10

completion_times = []
turn_around_times = []
waiting_times = []
time = 0

completion_times2 = []
turn_around_times2 = []
waiting_times2 = []
time2 = 0


# Random number generator, adds entry and execution times to the lists arrivals and burst_times
def generator(number):
    for i in range(number):
        arrivals.append(random.randrange(0, 20))  # Modify the range if needed
        burst_times.append(random.randrange(0, 20))


# Sorting function for FCFS (First-Come, First-Served)
# The process with the smallest arrival time will be first (bubble sort)
def sortingFCFS(number, arr, burst):
    for i in range(number):
        for j in range(0, number - i - 1):
            if arr[j] > arr[j + 1]:
                burst[j], burst[j + 1] = burst[j + 1], burst[j]
                arr[j], arr[j + 1] = arr[j + 1], arr[j]


# Sorting function for LCFS (Last-Come, First-Served)
# The process with the largest arrival time will be first
def sortingLCFS(number, arr, burst):
    for i in range(number):
        for j in range(0, number - i - 1):
            if arr[j] < arr[j + 1]:
                burst[j], burst[j + 1] = burst[j + 1], burst[j]
                arr[j], arr[j + 1] = arr[j + 1], arr[j]


# Function to calculate completion time for different cases
def ct(number, arr, burst, complet_t):
    tm = arr[0] + burst[0]
    complet_t.append(tm)
    for i in range(1, number):
        if tm > arr[i]:
            completion_time = tm + burst[i]
            complet_t.append(completion_time)
            tm = completion_time

        elif tm == arr[i]:
            completion_time = tm + burst[i]
            complet_t.append(completion_time)
            tm = completion_time

        elif tm < arr[i]:
            completion_time = arr[i] + burst[i]
            complet_t.append(completion_time)
            tm = completion_time


# Function to calculate turnaround time for each process
def ta(number, complet_t, turna, arr):
    for i in range(number):
        turna.append(int(complet_t[i] - arr[i]))


# Function to calculate waiting time for each process
def wt(number, turn_ar, burst, waitt):
    for i in range(number):
        waitt.append(int(turn_ar[i] - burst[i]))


# Function to calculate and display average turnaround and waiting time
def average(number, turn_ar, wait_t):
    avg_turnaround = sum(turn_ar) / number
    avg_waiting = sum(wait_t) / number
    print(f"Average Turnaround Time: {avg_turnaround:.2f}")
    print(f"Average Waiting Time: {avg_waiting:.2f}")


# Function to display sorted results
def display(number, arr, burst, complet_t, turn_ar, wait_t):
    print("Process | Arrival | Burst | Completion | Turnaround | Wait |")
    for i in range(number):
        print(f"   {i+1}   |   {arr[i]}  |    {burst[i]}  |    {complet_t[i]}  |    {turn_ar[i]}  |   {wait_t[i]}   |  ")


print("\nComparison of FCFS and LCFS for 10 processes with arrival time \nfrom range 0-20 and burst time from range 0-20")
print("\nFCFS")

# Generate process times once for both algorithms
generator(n)
sortingFCFS(n, arrivals, burst_times)
ct(n, arrivals, burst_times, completion_times)
ta(n, completion_times, turn_around_times, arrivals)
wt(n, turn_around_times, burst_times, waiting_times)
display(n, arrivals, burst_times, completion_times, turn_around_times, waiting_times)
average(n, turn_around_times, waiting_times)

print("\nLCFS")
sortingLCFS(n, arrivals, burst_times)
ct(n, arrivals, burst_times, completion_times2)
ta(n, completion_times2, turn_around_times2, arrivals)
wt(n, turn_around_times2, burst_times, waiting_times2)
display(n, arrivals, burst_times, completion_times2, turn_around_times2, waiting_times2)
average(n, turn_around_times2, waiting_times2)


# Data for charts
fcfs_avg_turnaround = round(np.mean(turn_around_times), 2)
fcfs_avg_waiting = round(np.mean(waiting_times), 2)
fcfs_completion = completion_times[-1]

lcfs_avg_turnaround = round(np.mean(turn_around_times2), 2)
lcfs_avg_waiting = round(np.mean(waiting_times2), 2)
lcfs_completion = completion_times2[-1]


# Function to generate comparison chart for average turnaround and waiting time
def plot_comparison_bar(data_fcfs, data_lcfs, title, ylabel):
    x = np.arange(len(data_fcfs))
    width = 0.35

    fig, ax = plt.subplots()
    fcfs_bars = ax.bar(x - width / 2, data_fcfs, width, label='FCFS')
    lcfs_bars = ax.bar(x + width / 2, data_lcfs, width, label='LCFS')

    ax.set_xlabel('')
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(['Avg Turnaround Time', 'Avg Waiting Time', 'Completion Time'])
    ax.legend()

    # Adding labels to bars
    def add_labels(bars):
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')

    add_labels(fcfs_bars)
    add_labels(lcfs_bars)

    fig.tight_layout()
    plt.show()


# Generate comparison chart
plot_comparison_bar(
    [fcfs_avg_turnaround, fcfs_avg_waiting, fcfs_completion],
    [lcfs_avg_turnaround, lcfs_avg_waiting, lcfs_completion],
    'Comparison of FCFS and LCFS for 10 processes with arrival time\nfrom range 0-20 and burst time from range 0-20',
    'Values'
)
