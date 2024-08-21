

# Class representing a process with necessary attributes
class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid  # Process ID
        self.arrival_time = arrival_time  # Arrival time of the process
        self.burst_time = burst_time  # Burst time of the process
        self.remaining_time = burst_time  # Remaining burst time, initially same as burst time
        self.completion_time = 0  # Completion time of the process
        self.turnaround_time = 0  # Turnaround time of the process
        self.waiting_time = 0  # Waiting time of the process
        self.response_time = -1  # Response time, -1 indicates not yet started

# Function to read processes from a file
def read_processes(file_name):
    processes = []
    with open(file_name, 'r') as file:
        for line in file:
            if line.strip():
                pid, arrival_time, burst_time = line.strip().split()
                processes.append(Process(pid, int(arrival_time), int(burst_time)))
    return processes

# Function to simulate Round-Robin scheduling
def round_robin_scheduling(processes, quantum):
    time = 0  # Current time
    gantt_chart = []  # Gantt chart to store the process execution sequence
    ready_queue = []  # Ready queue for processes
    process_index = 0  # Index for tracking processes
    n = len(processes)  # Number of processes
    
    while True:
        # Add all processes that have arrived to the ready queue
        while process_index < n and processes[process_index].arrival_time <= time:
            ready_queue.append(processes[process_index])
            process_index += 1
        
        # If ready queue is empty and there are more processes, advance time
        if not ready_queue and process_index < n:
            time = processes[process_index].arrival_time
            continue
        
        # If no more processes to execute, break
        if not ready_queue:
            break
        
        current_process = ready_queue.pop(0)  # Get the next process in the ready queue
        
        # Set the response time if it's the first execution
        if current_process.response_time == -1:
            current_process.response_time = time - current_process.arrival_time
        
        # Execute the current process for the quantum time or remaining time, whichever is smaller
        execution_time = min(quantum, current_process.remaining_time)
        gantt_chart.append((current_process.pid, time, time + execution_time))
        
        time += execution_time
        current_process.remaining_time -= execution_time
        
        # Add newly arrived processes to the ready queue during the execution
        while process_index < n and processes[process_index].arrival_time <= time:
            ready_queue.append(processes[process_index])
            process_index += 1
        
        # If process is not finished, add it back to the ready queue
        if current_process.remaining_time > 0:
            ready_queue.append(current_process)
        else:
            current_process.completion_time = time
            current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
            current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
    
    return gantt_chart

# Function to calculate average metrics
def calculate_metrics(processes):
    total_turnaround_time = sum(p.turnaround_time for p in processes)
    total_waiting_time = sum(p.waiting_time for p in processes)
    total_response_time = sum(p.response_time for p in processes)
    n = len(processes)
    avg_turnaround_time = total_turnaround_time / n
    avg_waiting_time = total_waiting_time / n
    avg_response_time = total_response_time / n
    return avg_turnaround_time, avg_waiting_time, avg_response_time

# Function to display results
def display_results(processes, gantt_chart, avg_turnaround_time, avg_waiting_time, avg_response_time):
    print("Gantt Chart:")
    for entry in gantt_chart:
        print(f"{entry[0]}|", end="")
    print()
    
    # Print the metrics for each process
    print(f"{'Process':<10}{'Arrival Time':<15}{'Turnaround Time':<20}{'Waiting Time':<15}{'Response Time':<15}")
    for process in processes:
        print(f"{process.pid:<10}{process.arrival_time:<15}{process.turnaround_time:<20}{process.waiting_time:<15}{process.response_time:<15}")
    
    # Print the average metrics
    print(f"Average Response Time: {avg_response_time:.2f}")
    print(f"Average Waiting Time: {avg_waiting_time:.2f}")
    print(f"Average Turnaround Time: {avg_turnaround_time:.2f}")

# Main function to run the program
def main():
    file_name = input("Enter the filename: ")
    quantum = int(input("Enter the quantum time period (in milliseconds): "))
    
    processes = read_processes(file_name)
    processes.sort(key=lambda p: p.arrival_time)
    
    gantt_chart = round_robin_scheduling(processes, quantum)
    
    avg_turnaround_time, avg_waiting_time, avg_response_time = calculate_metrics(processes)
    
    display_results(processes, gantt_chart, avg_turnaround_time, avg_waiting_time, avg_response_time)

if __name__ == "__main__":
    main()