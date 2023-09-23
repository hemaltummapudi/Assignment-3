import statistics

class Task:
    def __init__(self, name, arrival_time, estimated_time, urgency):
        self.name = name
        self.arrival_time = arrival_time
        self.estimated_time = estimated_time
        self.urgency = urgency

def fcfs_scheduling(tasks):
    tasks.sort(key=lambda x: x.arrival_time)  # Sort by arrival time
    current_time = 0
    waiting_time = 0
    for task in tasks:
        if current_time < task.arrival_time:
            current_time = task.arrival_time
        waiting_time += current_time - task.arrival_time
        current_time += task.estimated_time
    return waiting_time / len(tasks)

def sjf_scheduling(tasks):
    tasks.sort(key=lambda x: (x.arrival_time, x.estimated_time))  # Sort by arrival time and estimated time
    current_time = 0
    waiting_time = 0
    for task in tasks:
        if current_time < task.arrival_time:
            current_time = task.arrival_time
        waiting_time += current_time - task.arrival_time
        current_time += task.estimated_time
    return waiting_time / len(tasks)

def ps_scheduling(tasks):
    tasks.sort(key=lambda x: (x.arrival_time, -x.urgency))  # Sort by arrival time and negative urgency (higher urgency first)
    current_time = 0
    waiting_time = 0
    for task in tasks:
        if current_time < task.arrival_time:
            current_time = task.arrival_time
        waiting_time += current_time - task.arrival_time
        current_time += task.estimated_time
    return waiting_time / len(tasks)

def rr_scheduling(tasks, time_quantum):
    tasks.sort(key=lambda x: x.arrival_time)  # Sort by arrival time
    current_time = 0
    waiting_time = 0
    total_tasks = len(tasks)  # Store the total number of tasks
    while tasks:
        task = tasks.pop(0)
        if current_time < task.arrival_time:
            current_time = task.arrival_time
        waiting_time += current_time - task.arrival_time
        if task.estimated_time <= time_quantum:
            current_time += task.estimated_time
        else:
            current_time += time_quantum
            tasks.append(Task(task.name, task.arrival_time, task.estimated_time - time_quantum, task.urgency))
    return waiting_time / total_tasks  # Calculate average based on the total number of tasks

# Example usage with specified input:
tasks = [
    Task("Task1", 0, 30, 3),
    Task("Task2", 10, 20, 5),
    Task("Task3", 15, 40, 2),
    Task("Task4", 20, 15, 4),
]

# Create a copy of tasks for SJF and PS to ensure they have the same input data
sjf_tasks = [Task(task.name, task.arrival_time, task.estimated_time, task.urgency) for task in tasks]
ps_tasks = [Task(task.name, task.arrival_time, task.estimated_time, task.urgency) for task in tasks]

fcfs_waiting_time = fcfs_scheduling(tasks)
sjf_waiting_time = sjf_scheduling(sjf_tasks)
ps_waiting_time = ps_scheduling(ps_tasks)
rr_waiting_time = rr_scheduling(tasks, 2)

# Determine the most efficient algorithm
efficiency_results = {
    "FCFS": fcfs_waiting_time,
    "SJF": sjf_waiting_time,
    "PS": ps_waiting_time,
    "RR": rr_waiting_time,
}

most_efficient_algorithm = min(efficiency_results, key=efficiency_results.get)

# Calculate the range of waiting times for fairness
waiting_times = [fcfs_waiting_time, sjf_waiting_time, ps_waiting_time, rr_waiting_time]
fairness_ranges = [max(waiting_times) - min(waiting_times)]

# Determine the most fair algorithm based on range
most_fair_algorithm = "All"  # Assume all algorithms are equally fair initially

for algorithm, waiting_time in zip(["FCFS", "SJF", "PS", "RR"], waiting_times):
    fairness_ranges.append(max(waiting_times) - min([waiting_time]))
    if min(fairness_ranges) == max(waiting_times) - min([waiting_time]):
        most_fair_algorithm = algorithm

print("FCFS Average Waiting Time:", fcfs_waiting_time)
print("SJF Average Waiting Time:", sjf_waiting_time)
print("PS Average Waiting Time:", ps_waiting_time)
print("RR Average Waiting Time:", rr_waiting_time)
print("Most Efficient Algorithm:", most_efficient_algorithm)
print("Most Fair Algorithm:", most_fair_algorithm)
