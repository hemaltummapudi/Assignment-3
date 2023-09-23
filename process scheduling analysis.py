class Process:
    def __init__(self, arrival_time, burst_time, priority):
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.waiting_time = 0
        self.turnaround_time = 0


def calculate_combined_metric(avg_waiting_time, avg_turnaround_time):
    return avg_waiting_time + avg_turnaround_time


def fcfs(processes):
    n = len(processes)
    processes.sort(key=lambda x: x.arrival_time)
    
    time = 0
    for process in processes:
        if time < process.arrival_time:
            time = process.arrival_time
        process.waiting_time = time - process.arrival_time
        process.turnaround_time = process.waiting_time + process.burst_time
        time += process.burst_time
    
    total_waiting_time = sum(process.waiting_time for process in processes)
    total_turnaround_time = sum(process.turnaround_time for process in processes)
    avg_waiting_time = total_waiting_time / n
    avg_turnaround_time = total_turnaround_time / n
    
    return avg_waiting_time, avg_turnaround_time


def sjf(processes):
    n = len(processes)
    processes.sort(key=lambda x: (x.arrival_time, x.burst_time))
    waiting_time = [0] * n
    turnaround_time = [0] * n
    remaining_time = [process.burst_time for process in processes]

    time = 0
    while True:
        done = True
        for i in range(n):
            if remaining_time[i] > 0 and processes[i].arrival_time <= time:
                done = False
                chosen_process = i
                break
        
        if done:
            break

        min_burst_time = min(remaining_time)
        if remaining_time[chosen_process] == min_burst_time:
            time += min_burst_time
            waiting_time[chosen_process] = time - processes[chosen_process].arrival_time - processes[chosen_process].burst_time
            turnaround_time[chosen_process] = time - processes[chosen_process].arrival_time
            remaining_time[chosen_process] = 0
        else:
            time += 1
            remaining_time[chosen_process] -= 1
    
    total_waiting_time = sum(waiting_time)
    total_turnaround_time = sum(turnaround_time)
    avg_waiting_time = total_waiting_time / n
    avg_turnaround_time = total_turnaround_time / n

    return avg_waiting_time, avg_turnaround_time


def priority_scheduling(processes):
    n = len(processes)
    processes.sort(key=lambda x: (x.arrival_time, x.priority))
    waiting_time = [0] * n
    turnaround_time = [0] * n

    for i in range(1, n):
        waiting_time[i] = waiting_time[i - 1] + processes[i - 1].burst_time
        turnaround_time[i] = waiting_time[i] + processes[i].burst_time

    total_waiting_time = sum(waiting_time)
    total_turnaround_time = sum(turnaround_time)
    avg_waiting_time = total_waiting_time / n
    avg_turnaround_time = total_turnaround_time / n

    return avg_waiting_time, avg_turnaround_time


def round_robin(processes, time_quantum):
    n = len(processes)
    waiting_time = [0] * n
    turnaround_time = [0] * n
    remaining_time = [process.burst_time for process in processes]

    time = 0
    while True:
        done = True
        for i in range(n):
            if remaining_time[i] > 0:
                done = False
                if remaining_time[i] <= time_quantum:
                    time += remaining_time[i]
                    waiting_time[i] = time - processes[i].arrival_time - processes[i].burst_time
                    turnaround_time[i] = time - processes[i].arrival_time
                    remaining_time[i] = 0
                else:
                    time += time_quantum
                    remaining_time[i] -= time_quantum
        
        if done:
            break

    total_waiting_time = sum(waiting_time)
    total_turnaround_time = sum(turnaround_time)
    avg_waiting_time = total_waiting_time / n
    avg_turnaround_time = total_turnaround_time / n

    return avg_waiting_time, avg_turnaround_time


# Example usage:
if __name__ == "__main__":
    processes = [
        Process(0, 24, 3),
        Process(4, 3, 1),
        Process(5, 3, 4),
        Process(6, 12, 2),
    ]

    time_quantum = 4

    algorithms = [
        ("FCFS", fcfs(processes)),
        ("SJF", sjf(processes)),
        ("Priority Scheduling", priority_scheduling(processes)),
        ("Round Robin", round_robin(processes, time_quantum))
    ]

    min_combined_metric = float('inf')
    best_algorithm = ""

    for algo_name, (avg_waiting_time, avg_turnaround_time) in algorithms:
        combined_metric = calculate_combined_metric(avg_waiting_time, avg_turnaround_time)
        print(f"{algo_name}: Avg Waiting Time: {avg_waiting_time:.2f}, Avg Turnaround Time: {avg_turnaround_time:.2f}, Combined Metric: {combined_metric:.2f}")
        
        if combined_metric < min_combined_metric:
            min_combined_metric = combined_metric
            best_algorithm = algo_name

    print(f"\nThe most suitable algorithm is: {best_algorithm}")
