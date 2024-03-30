# Ahmad Hamdan 1210241
import matplotlib.pyplot as plt


# ganttChart = [Process Name, Run Start, Run Duration]
# Plot Gantt chart
def ganttChart(ganttChartData, title):
    fig, gnt = plt.subplots()

    gnt.set_title(title)
    gnt.set_xlabel("Time Unit")
    gnt.set_ylabel("Processes")

    process_indices = {
        process_id: i + 1
        for i, process_id in enumerate(
            (P1[0], P2[0], P3[0], P4[0], P5[0], P6[0], P7[0])
        )
    }

    for i, (process_id, start_time, burst_time) in enumerate(ganttChartData):
        gnt.broken_barh(
            [(start_time, burst_time)],
            (process_indices[process_id] - 0.5, 1),
            facecolors=("darkcyan"),
        )

    y_ticks = range(1, 8)
    gnt.set_yticks(y_ticks)
    gnt.set_yticklabels((P1[0], P2[0], P3[0], P4[0], P5[0], P6[0], P7[0]))
    gnt.set_ylim(0.5, 7.5)

    x_ticks = range(0, timeLimit, 5)
    gnt.set_xticks(x_ticks)
    gnt.set_xlim(0, timeLimit - 1)

    gnt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.show()


# First Come First Served
def firstComeFirstServed():
    # Declaring variables
    readyQueue = []
    waitQueue = []
    processing = []
    ganttChartData = []
    processingTime = 0
    sumWaitTime = 0
    sumTurnAroundTime = 0

    # Simulating time units
    for time in range(timeLimit):
        processingTime += 1

        # Time calculations
        for process in readyQueue:
            process[5] += 1
            process[6] += 1
        for process in waitQueue:
            process[6] += 1

        # If the process arrives, send it to the ready queue
        for arrivingProcess in Processes:
            if arrivingProcess[1] == time:
                readyQueue.append(arrivingProcess)

        # If the come back after time has finished, return to the ready queue
        waitQueueTemp = waitQueue.copy()
        for waitQueueProcess in waitQueueTemp:
            waitQueueProcess[7] += 1            
            if waitQueueProcess[7] == waitQueueProcess[3]:
                waitQueue.remove(waitQueueProcess)
                readyQueue.append(waitQueueProcess)


        # If the CPU is ready to receive, pop the first process in the ready queue
        if not processing and readyQueue:
            processing = readyQueue.pop(0)
            processingTime = 0

        # If the process has finished working, send it to the wait queue
        if processing:
            if processingTime == processing[2] or time == timeLimit - 1:
                waitQueue.append(processing)
                ganttChartData.append(
                    (
                        processing[0],
                        time - processingTime,
                        processingTime,
                    )
                )
                sumTurnAroundTime += processingTime
                processing[7] = 0
                processing = []

        # If the CPU is empty, pop the first process in the ready queue
        if not processing and readyQueue and time != timeLimit - 1:
            processing = readyQueue.pop(0)
            sumWaitTime += processing[5]
            sumTurnAroundTime += processing[6]
            processingTime = 0
            processing[5] = 0
            processing[6] = 0

    # Checking if any processes didn't work
    inactiveProcesses = 0
    for process in Processes:
        if process[5] == timeLimit - 1 - process[1]:
            inactiveProcesses += 1

    print("\n\n\033[1mFirst Come First Served Scheduling:\033[0m")
    print(
        "  Average waiting time =", sumWaitTime / (len(Processes) - inactiveProcesses)
    )
    print(
        "  Average turn around time =",
        sumTurnAroundTime / (len(Processes) - inactiveProcesses),
        "\n\n",
    )
    ganttChart(ganttChartData, "First Come First Served Scheduling")


# Shortest Job First
def shortestJobFirst():
    # Declaring variables
    readyQueue = []
    waitQueue = []
    processing = []
    ganttChartData = []
    processingTime = 0
    sumWaitTime = 0
    sumTurnAroundTime = 0

    # Simulating time units
    for time in range(timeLimit):
        processingTime += 1

        # Time calculations
        for process in readyQueue:
            process[5] += 1
            process[6] += 1
        for process in waitQueue:
            process[6] += 1

        # If the process arrives, send it to the ready queue
        for arrivingProcess in Processes:
            if arrivingProcess[1] == time:
                readyQueue.append(arrivingProcess)

        # If the CPU is ready to receive, pop the first process in the ready queue
        if not processing and readyQueue and time != timeLimit - 1:
            processing = min(readyQueue, key=lambda process: process[2])
            readyQueue.remove(processing)
            sumWaitTime += processing[5]
            sumTurnAroundTime += processing[6]
            processingTime = 0
            processing[5] = 0
            processing[6] = 0

        # If the process has finished working, send it to the wait queue
        if processing:
            if processingTime == processing[2] or time == timeLimit - 1:
                waitQueue.append(processing)
                ganttChartData.append(
                    (
                        processing[0],
                        time - processingTime,
                        processingTime,
                    )
                )
                sumTurnAroundTime += processingTime
                processing[7] = 0
                processing = []

        # If the come back after time has finished, return to the ready queue
        waitQueueTemp = waitQueue.copy()
        for waitQueueProcess in waitQueueTemp:
            if waitQueueProcess[7] == waitQueueProcess[3]:
                waitQueue.remove(waitQueueProcess)
                readyQueue.append(waitQueueProcess)
            else:
                waitQueueProcess[7] += 1

        # If the CPU is ready to receive, pop the first process in the ready queue
        if not processing and readyQueue and time != timeLimit - 1:
            processing = min(readyQueue, key=lambda process: process[2])
            readyQueue.remove(processing)
            sumWaitTime += processing[5]
            sumTurnAroundTime += processing[6]
            processingTime = 0
            processing[5] = 0
            processing[6] = 0

    # Checking if any processes didn't work
    inactiveProcesses = 0
    for process in Processes:
        if process[5] == timeLimit - 1 - process[1]:
            inactiveProcesses += 1

    print("\033[1mShortest Job First Scheduling:\033[0m")
    print(
        "  Average waiting time =",
        sumWaitTime / (len(Processes) - inactiveProcesses),
    )
    print(
        "  Average turn around time =",
        sumTurnAroundTime / (len(Processes) - inactiveProcesses),
        "\n\n",
    )
    ganttChart(ganttChartData, "Shortest Job First Scheduling")


# Shortest Remaining Time First
def shortestRemainingTimeFirst():
    # Declaring variables
    readyQueue = []
    waitQueue = []
    processing = []
    ganttChartData = []
    currentProcessRunningTime = 0
    sumWaitTime = 0
    sumTurnAroundTime = 0

    # Simulating time units
    for time in range(timeLimit):
        if processing:
            currentProcessRunningTime += 1
            processing[8] += 1

        # Time calculations
        for process in readyQueue:
            process[5] += 1
            process[6] += 1
        for process in waitQueue:
            process[6] += 1

        # If the process arrives, send it to the ready queue
        for process in Processes:
            if process[1] == time:
                readyQueue.append(process)

        # Processes that finished their come back after time go back to the ready queue
        if waitQueue:
            waitQueueTemp = waitQueue.copy()
            for process in waitQueueTemp:
                process[7] += 1
                if process[3] == process[7]:
                    process[7] = 0
                    waitQueue.remove(process)
                    readyQueue.append(process)

        # Sort the ready queue based on the remaining time
        readyQueue = sorted(
            readyQueue, key=lambda readyQueue: readyQueue[2] - readyQueue[8]
        )

        # If the process has finished working, send it to the wait queue
        if processing:
            if processing[2] == processing[8] or time == timeLimit - 1:
                ganttChartData.append(
                    (
                        processing[0],
                        time - currentProcessRunningTime,
                        currentProcessRunningTime,
                    )
                )
                sumWaitTime += processing[5]
                sumTurnAroundTime += processing[6]
                sumTurnAroundTime += currentProcessRunningTime
                processing[5] = 0
                processing[6] = 0
                processing[8] = 0
                waitQueue.append(processing)
                currentProcessRunningTime = 0
                processing = []

        # If the CPU is ready to receive, pop the first process in the ready queue
        if readyQueue:
            if processing:
                if processing[2] - processing[8] > readyQueue[0][2]:
                    sumTurnAroundTime += processing[8]
                    ganttChartData.append(
                        (
                            processing[0],
                            time - currentProcessRunningTime,
                            currentProcessRunningTime,
                        )
                    )
                    readyQueue.append(processing)
                    processing = readyQueue.pop(0)
                    sumWaitTime += processing[5]
                    sumTurnAroundTime += processing[6]
                    processing[5] = 0
                    processing[6] = 0
                    currentProcessRunningTime = 0
            else:
                if time != timeLimit - 1:
                    processing = readyQueue.pop(0)
                    sumWaitTime += processing[5]
                    sumTurnAroundTime += processing[6]
                    processing[5] = 0
                    processing[6] = 0
                    currentProcessRunningTime = 0

    inactiveProcesses = 0
    for process in Processes:
        if process[5] == timeLimit - 1 - process[1]:
            inactiveProcesses += 1

    print("\033[1mShortest Remaining Time First Scheduling:\033[0m")
    print(
        "  Average waiting time =",
        sumWaitTime / (len(Processes) - inactiveProcesses),
    )
    print(
        "  Average turn around time =",
        sumTurnAroundTime / (len(Processes) - inactiveProcesses),
        "\n\n",
    )
    ganttChart(ganttChartData, "Shortest Remaining Time First Scheduling")


# Round Robin with q = 5
def roundRobin():
    # Declaring variables
    readyQueue = []
    waitQueue = []
    processing = []
    ganttChartData = []
    currentProcessRunningTime = 0
    sumWaitTime = 0
    sumTurnAroundTime = 0

    # Simulating time units
    for time in range(timeLimit):
        if processing:
            processing[8] += 1
            currentProcessRunningTime += 1

        # Time calculations
        for process in readyQueue:
            process[5] += 1
            process[6] += 1
        for process in waitQueue:
            process[6] += 1

        # If the process arrives, send it to the ready queue
        for arrivingProcess in Processes:
            if arrivingProcess[1] == time:
                readyQueue.append(arrivingProcess)

        # Processes that finished their come back after time go back to the ready queue
        if waitQueue:
            waitQueueTemp = waitQueue.copy()
            for process in waitQueueTemp:
                process[7] += 1
                if process[3] == process[7]:
                    process[7] = 0
                    waitQueue.remove(process)
                    readyQueue.append(process)

        # If the processing process finish processing, send it to the wait queue
        if processing:
            if processing[2] == processing[8]:
                ganttChartData.append(
                    (
                        processing[0],
                        time - currentProcessRunningTime,
                        currentProcessRunningTime,
                    )
                )
                sumWaitTime += processing[5]
                sumTurnAroundTime += processing[6]
                sumTurnAroundTime += currentProcessRunningTime
                processing[5] = 0
                processing[6] = 0
                processing[8] = 0
                currentProcessRunningTime = 0
                waitQueue.append(processing)
                processing = []

        # If the CPU is ready to receive, pop the first process in the ready queue
        if readyQueue:
            if currentProcessRunningTime == 5:
                readyQueue.append(processing)
                ganttChartData.append(
                    (
                        processing[0],
                        time - currentProcessRunningTime,
                        currentProcessRunningTime,
                    )
                )
                sumTurnAroundTime += currentProcessRunningTime
                if time != timeLimit - 1:
                    processing = readyQueue.pop(0)
                    sumWaitTime += processing[5]
                    sumTurnAroundTime += processing[6]
                    processing[5] = 0
                    processing[6] = 0
                    currentProcessRunningTime = 0

            # If the CPU is empty, pop the first process in the ready queue
            if not processing:
                processing = readyQueue.pop(0)
                sumWaitTime += processing[5]
                sumTurnAroundTime += processing[6]
                processing[5] = 0
                processing[6] = 0
                currentProcessRunningTime = 0

    # Checking if any processes didn't work
    inactiveProcesses = 0
    for process in Processes:
        if process[5] == timeLimit - 1 - process[1]:
            inactiveProcesses += 1

    print("\033[1mRound Robin Scheduling:\033[0m")
    print(
        "  Average waiting time =",
        sumWaitTime / (len(Processes) - inactiveProcesses),
    )
    print(
        "  Average turn around time =",
        sumTurnAroundTime / (len(Processes) - inactiveProcesses),
        "\n\n",
    )
    ganttChart(ganttChartData, "Round Robin Scheduling")


# Preemptive Priority Scheduling with aging
def preemptivePriority():
    # Declaring variables
    readyQueue = []
    waitQueue = []
    processing = []
    ganttChartData = []
    currentProcessRunningTime = 0
    sumWaitTime = 0
    sumTurnAroundTime = 0

    # Simulating time units
    for time in range(timeLimit):
        if processing:
            processing[8] += 1
            currentProcessRunningTime += 1

        # Time calculations
        for process in readyQueue:
            process[5] += 1
            process[6] += 1
        for process in waitQueue:
            process[6] += 1

        # Aging for processes in the ready queue
        for process in readyQueue:
            process[9] += 1
            if process[9] == 5:
                if process[4] + process[10] > 0:
                    process[10] -= 1
                process[9] = 0

        # If the process arrives, send it to the ready queue
        for arrivingProcess in Processes:
            if arrivingProcess[1] == time:
                readyQueue.append(arrivingProcess)

        # Processes that finished their come back after time go back to the ready queue
        if waitQueue:
            waitQueueTemp = waitQueue.copy()
            for waitQueueProcess in waitQueueTemp:
                waitQueueProcess[7] += 1
                if waitQueueProcess[3] == waitQueueProcess[7]:
                    waitQueueProcess[7] = 0
                    waitQueueProcess[8] = 0
                    waitQueueProcess[9] = 0
                    waitQueueProcess[10] = 0
                    readyQueue.append(waitQueueProcess)
                    waitQueue.remove(waitQueueProcess)

        # Sort the ready queue based on the priority
        if readyQueue:
            minReadyQueue = min(
                readyQueue, key=lambda process: process[4] + process[10]
            )

        # If the processing process finish processing, send it to the wait queue
        if processing:
            if processing[2] == processing[8] or time == timeLimit - 1:
                ganttChartData.append(
                    (
                        processing[0],
                        time - currentProcessRunningTime,
                        currentProcessRunningTime,
                    )
                )
                sumWaitTime += processing[5]
                sumTurnAroundTime += processing[6]
                sumTurnAroundTime += currentProcessRunningTime
                processing[5] = 0
                processing[6] = 0
                processing[7] = 0
                processing[8] = 0
                waitQueue.append(processing)
                currentProcessRunningTime = 0
                processing = []

        # If the CPU is ready to receive, pop the first process in the ready queue
        if readyQueue:
            if processing:
                if (
                    processing[4] + processing[10]
                    > minReadyQueue[4] + minReadyQueue[10]
                ):
                    sumTurnAroundTime += processing[8]
                    ganttChartData.append(
                        (
                            processing[0],
                            time - currentProcessRunningTime,
                            currentProcessRunningTime,
                        )
                    )
                    processing[9] = 0
                    processing[10] = 0
                    readyQueue.append(processing)
                    if time != timeLimit - 1:
                        processing = minReadyQueue
                        readyQueue.remove(minReadyQueue)
                        sumWaitTime += processing[5]
                        sumTurnAroundTime += processing[6]
                        processing[5] = 0
                        processing[6] = 0
                        currentProcessRunningTime = 0
            else:
                if time != timeLimit - 1:
                    processing = minReadyQueue
                    readyQueue.remove(minReadyQueue)
                    sumWaitTime += processing[5]
                    sumTurnAroundTime += processing[6]
                    processing[5] = 0
                    processing[6] = 0
                    processing[9] = 0
                    currentProcessRunningTime = 0

    # Checking if any processes didn't work
    inactiveProcesses = 0
    for process in Processes:
        if process[5] == timeLimit - 1 - process[1]:
            inactiveProcesses += 1

    print("\033[1mPreemptive Priority Scheduling:\033[0m")
    print(
        "  Average waiting time =",
        sumWaitTime / (len(Processes) - inactiveProcesses),
    )
    print(
        "  Average turn around time =",
        sumTurnAroundTime / (len(Processes) - inactiveProcesses),
        "\n\n",
    )
    ganttChart(ganttChartData, "Preemptive Priority Scheduling")


# Non Preemptive Priority Scheduling with aging
def nonPreemptivePriority():
    # Declaring variables
    readyQueue = []
    waitQueue = []
    processing = []
    ganttChartData = []
    currentProcessRunningTime = 0
    sumWaitTime = 0
    sumTurnAroundTime = 0

    # Simulating time units
    for time in range(timeLimit):
        if processing:
            processing[8] += 1
            currentProcessRunningTime += 1

        # Time calculations
        for process in readyQueue:
            process[5] += 1
            process[6] += 1
        for process in waitQueue:
            process[6] += 1

        # Aging for processes in the ready queue
        for process in readyQueue:
            process[9] += 1
            if process[9] == 5:
                if process[4] + process[10] > 0:
                    process[10] -= 1
                process[9] = 0

        # If the process arrives, send it to the ready queue
        for arrivingProcess in Processes:
            if arrivingProcess[1] == time:
                readyQueue.append(arrivingProcess)

        # Processes that finished their come back after time go back to the ready queue
        if waitQueue:
            waitQueueTemp = waitQueue.copy()
            for waitQueueProcess in waitQueueTemp:
                waitQueueProcess[7] += 1
                if waitQueueProcess[3] == waitQueueProcess[7]:
                    waitQueueProcess[7] = 0
                    waitQueueProcess[8] = 0
                    waitQueueProcess[9] = 0
                    waitQueueProcess[10] = 0
                    readyQueue.append(waitQueueProcess)
                    waitQueue.remove(waitQueueProcess)

        # Sort the ready queue based on the priority
        if readyQueue:
            minReadyQueue = min(
                readyQueue, key=lambda process: process[4] + process[10]
            )
        # If the processing process finish processing, send it to the wait queue
        if processing:
            if processing[2] == processing[8] or time == timeLimit - 1:
                ganttChartData.append(
                    (
                        processing[0],
                        time - currentProcessRunningTime,
                        currentProcessRunningTime,
                    )
                )
                sumWaitTime += processing[5]
                sumTurnAroundTime += processing[6]
                sumTurnAroundTime += currentProcessRunningTime
                processing[5] = 0
                processing[6] = 0
                processing[7] = 0
                processing[8] = 0
                waitQueue.append(processing)
                currentProcessRunningTime = 0
                processing = []

        # If the CPU is ready to receive, pop the first process in the ready queue
        if readyQueue:
            if not processing:
                if time != timeLimit - 1:
                    processing = minReadyQueue
                    readyQueue.remove(minReadyQueue)
                    sumWaitTime += processing[5]
                    sumTurnAroundTime += processing[6]
                    processing[5] = 0
                    processing[6] = 0
                    processing[9] = 0
                    currentProcessRunningTime = 0

    # Checking if any processes didn't work
    inactiveProcesses = 0
    for process in Processes:
        if process[5] == timeLimit - 1 - process[1]:
            inactiveProcesses += 1

    print("\033[1mNon-Preemptive Priority Scheduling:\033[0m")
    print(
        "  Average waiting time =",
        sumWaitTime / (len(Processes) - inactiveProcesses),
    )
    print(
        "  Average turn around time =",
        sumTurnAroundTime / (len(Processes) - inactiveProcesses),
        "\n\n",
    )
    ganttChart(ganttChartData, "Non-Preemptive Priority Scheduling")


"""
[0]: {       ProcessNum                 }
[1]: {       Arrival time               }
[2]: {       Burst time                 }
[3]: {       Comes back after           }
[4]: {       Priority                   }
[5]: {       Waiting Time               }
[6]: {       Turn Around Time           }
[7]: {       Keep track of wait time    }
[8]: {       Keep track of burst time   }
[9]: {       Keep track of aging time   }
[10]:{       Fake priority for aging    }
"""
# Example processes list
P1 = ["P1", 0, 10, 0, 2, 0, 0, 0, 0, 0, 0]
P2 = ["P2", 2, 8, 0, 1, 0, 0, 0, 0, 0, 0]
P3 = ["P3", 3, 3, 0, 3, 0, 0, 0, 0, 0, 0]
P4 = ["P4", 10, 4, 0, 2, 0, 0, 0, 0, 0, 0]
P5 = ["P5", 12, 1, 0,3, 0, 0, 0, 0, 0, 0]
P6 = ["P6", 15, 4, 0, 1, 0, 0, 0, 0, 0, 0]

Processes = [P1, P2, P3, P4, P5, P6]
timeLimit = 201
#firstComeFirstServed()
for process in Processes:
    process[5] = 0
    process[6] = 0
    process[7] = 0
    process[8] = 0
shortestJobFirst()
for process in Processes:
    process[5] = 0
    process[6] = 0
    process[7] = 0
    process[8] = 0
#shortestRemainingTimeFirst()
for process in Processes:
    process[5] = 0
    process[6] = 0
    process[7] = 0
    process[8] = 0
#roundRobin()
for process in Processes:
    process[5] = 0
    process[6] = 0
    process[7] = 0
    process[8] = 0
preemptivePriority()
for process in Processes:
    process[5] = 0
    process[6] = 0
    process[7] = 0
    process[8] = 0
    process[9] = 0
    process[10] = 0
nonPreemptivePriority()
