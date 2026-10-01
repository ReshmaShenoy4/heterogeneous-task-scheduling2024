#!/usr/bin/env python3
from pulp import LpProblem, LpVariable, LpMinimize,lpSum,LpStatus,value
import matplotlib.pyplot as plt


def main():
    for_plot={}
    ## Provide the values here for NA and NB directly.
    for NA in range(4):
        for NB in range(1):
           if(NA>0 or NB>0):
                t = 11
                exe_tasksA      = [821,217,757,677,809,443,409,239,317,487,499]
                taskA           = [[LpVariable(f"task_procA{i}_{k}",cat="Binary") for k in range(NA)] for i in range(t)] # Whether task i assigned on processor kth instance of type A or not.
                deltaA          = [[[LpVariable(f"deltaA_{k}_{j}_{i}",cat="Binary") for i in range(NA)] for j in range(t)] for k in range(t)] # Comparison of 2 tasks on ith instance of typeA 
                start_timeA     = [[LpVariable(f"stA_{i}_{j}", lowBound=0, cat='Integer') for j in range(NA)] for i in range(t)]  #Start time of the processor    
                finish_timeA    = [[LpVariable("ftA_{i}_{j}", lowBound=0, cat="Integer") for j in range(NA)] for i in range(t)] # To be used in objective function
               

                exe_tasksB      = [577,337,569,359,401,269,577,197,227,761,347] 
                taskB           = [[LpVariable(f"task_procB{i}_{k}",cat="Binary") for k in range(NB)] for i in range(t)] # Whether task i assigned on processor kth instance of type A or not.
                deltaB          = [[[LpVariable(f"deltaB_{k}_{j}_{i}",cat="Binary") for i in range(NB)] for j in range(t)] for k in range(t)] # Comparison of 2 tasks on ith instance of typeA 
                start_timeB     = [[LpVariable(f"stB_{i}_{j}", lowBound=0, cat='Integer') for j in range(NB)] for i in range(t)]  #Start time of the processor    
                finish_timeB    = [[LpVariable("ftB_{i}_{j}", lowBound=0, cat="Integer") for j in range(NB)] for i in range(t)] # To be used in objective function
               
                fmax            = LpVariable("Fmax",lowBound=0,cat="Integer")
                problem         = LpProblem("Task_Scheduling",LpMinimize)  

                sumTA=[0]*11
                sumTB=[0]*11
                if(NA>0 and NB>0):
                    for i in range(t):
                        for j in range(NA):
                            sumTA[i] += taskA[i][j]
                        for j in range(NB):
                            sumTB[i] += taskB[i][j]
                        problem += (sumTA[i] + sumTB[i]==1)
                    #problem += fmaxA + fmaxB
                elif(NA==0 and NB>0):
                    for i in range(t):
                        for j in range(NB):
                            sumTB[i] += taskB[i][j]
                        problem += (sumTB[i]==1)
                elif(NB==0 and NA>0):
                    for i in range(t):
                        for j in range(NA):
                            sumTA[i] += taskA[i][j]
                        problem += (sumTA[i]==1)



                if(NA>0):
                # Constraint that a task should be assigned to any 1 instance of processor A.
                    # For an instance of a processor, assign only 1 task
                    #UA=sum(exe_tasksA)*2
                    UA=8000
                    if(NA<t):
                        for k in range(t):
                             for j in range(t):
                                 if(j!=k):
                                     for i in range(NA):
                                         problem += start_timeA[j][i] >= start_timeA[k][i] + exe_tasksA[k] - UA*(1-deltaA[k][j][i]) # - UA*(1-taskA[k][i]) - UA*(1-taskA[j][i]) #Task j is after Task k if true then delta [k][j]==1
                                         problem += start_timeA[k][i] >= start_timeA[j][i] + exe_tasksA[j] - UA*(1-deltaA[j][k][i]) #- UA*(1-taskA[k][i]) - UA*(1-taskA[j][i]) #Task k is after Task j if true, then delta[j][k]==1
                                         problem += (deltaA[k][j][i] + deltaA[j][k][i] == 1)
                    else:
                        sumPT = [0]*12
                        for i in range(NA):
                            for j in range(t):
                               sumPT[i] += taskA[j][i]
                            problem += (sumPT[i]<=1)

                    for p in range(NA):
                        problem += start_timeA[1][p]>=start_timeA[0][p]+ exe_tasksA[0] 
                        problem += start_timeA[4][p]>=start_timeA[0][p]+ exe_tasksA[0] 
                        problem += start_timeA[8][p]>=start_timeA[0][p]+ exe_tasksA[0]
                        problem += start_timeA[2][p]>=start_timeA[1][p]+ exe_tasksA[1] 
                        problem += start_timeA[5][p]>=start_timeA[4][p]+ exe_tasksA[4] 
                        problem += start_timeA[9][p]>=start_timeA[8][p]+ exe_tasksA[8] 

                        problem += start_timeA[3][p]>=start_timeA[2][p] + exe_tasksA[2] 

                        problem += start_timeA[6][p] >= start_timeA[5][p] + exe_tasksA[5] 
                        problem += start_timeA[10][p]>= start_timeA[9][p] + exe_tasksA[9] 
                        problem += start_timeA[7][p] >= start_timeA[6][p] + exe_tasksA[6] 

                        problem += start_timeA[8][p]+exe_tasksA[8]+100  >= start_timeA[9][p] 
                        problem += start_timeA[1][p]+exe_tasksA[1]+1000 >= start_timeA[3][p]
                        problem += start_timeA[5][p]+exe_tasksA[5]+750  >= start_timeA[7][p]


                    for i in range(t):
                        for j in range(NA):
                            #problem+=finish_timeA[i][j] == start_timeA[i][j] + exe_tasksA[i]
                            problem += fmax >= start_timeA[i][j] + exe_tasksA[i] - UA*(1-taskA[i][j])

                    #problem += fmaxA

                if(NB>0):
                    UB=sum(exe_tasksB)
                    #UB=10000
                    if(NB<t):
                        for k in range(t):
                             for j in range(t):
                                 if(j!=k):
                                     for i in range(NB):
                                         problem += start_timeB[j][i] >= start_timeB[k][i] + exe_tasksB[k] - UB*(1-deltaB[k][j][i]) #- UA*(1-taskA[k][i]) - UA*(1-taskA[j][i]) #Task j is after Task k if true then delta [k][j]==1
                                         problem += start_timeB[k][i] >= start_timeB[j][i] + exe_tasksB[j] - UB*(1-deltaB[j][k][i]) #- UA*(1-taskA[k][i]) - UA*(1-taskA[j][i]) #Task k is after Task j if true, then delta[j][k]==1
                                         problem += (deltaB[k][j][i] + deltaB[j][k][i] == 1)
                    else:
                        sumPTB = [0]*12
                        for i in range(NB):
                            for j in range(t):
                               sumPTB[i] += taskB[j][i]
                            problem += (sumPTB[i]<=1)

                    for p in range(NB):
                        problem += start_timeB[1][p]>=start_timeB[0][p]+ exe_tasksB[0] 
                        problem += start_timeB[4][p]>=start_timeB[0][p]+ exe_tasksB[0] 
                        problem += start_timeB[8][p]>=start_timeB[0][p]+ exe_tasksB[0]
                        problem += start_timeB[2][p]>=start_timeB[1][p]+ exe_tasksB[1] 
                        problem += start_timeB[5][p]>=start_timeB[4][p]+ exe_tasksB[4] 
                        problem += start_timeB[9][p]>=start_timeB[8][p]+ exe_tasksB[8] 

                        problem += start_timeB[3][p]>=start_timeB[2][p] + exe_tasksB[2] 

                        problem += start_timeB[6][p] >= start_timeB[5][p] + exe_tasksB[5] 
                        problem += start_timeB[10][p]>= start_timeB[9][p] + exe_tasksB[9] 
                        problem += start_timeB[7][p] >= start_timeB[6][p] + exe_tasksB[6] 

                        problem += start_timeB[8][p]+exe_tasksB[8]+100  >= start_timeB[9][p] 
                        problem += start_timeB[1][p]+exe_tasksB[1]+1000 >= start_timeB[3][p]
                        problem += start_timeB[5][p]+exe_tasksB[5]+750  >= start_timeB[7][p]


                    for i in range(t):
                        for j in range(NB):
                            problem += fmax >= start_timeB[i][j] + exe_tasksB[i]-UB*(1-taskB[i][j])


                problem += fmax 
                problem.solve()
                print("Status:", problem.status)
                #print(f"{value(fmaxB)}")
                print(f"{value(fmax)}")

                #for_plot[(NA,NB)]=((87*NA+151*NB),value(fmax))

    #print(for_plot)
    #points=list(for_plot.values())
    #points.sort()
    #print(points)
    #pareto_front = [points[1]]
#
    #for point in points[1:]:
    #    if point[1]<pareto_front[-1][1]:
    #        pareto_front.append(point)
#
    #x_all,y_all = zip(*points)
    #plt.scatter(x_all,y_all,color='blue',label="All points")
#
    #x_pareto,y_pareto = zip(*pareto_front)
    #plt.plot(x_pareto,y_pareto,color="blue",label="Pareto Front",linestyle="--",marker="o")
    #print(for_plot)
    #plt.xlabel("Total Cost of the platform")
    #plt.ylabel("Execution Time in ms")
    #plt.legend()
    #plt.grid()
    #plt.show() 
   ############################ PLOT ######################################################
   # colors = ['red', 'green', 'blue', 'orange', 'purple', 'cyan', 'magenta', 'yellow', 'pink', 'lime', 'teal']
   # plt.figure(figsize=(10, 10)) 
   # start_valB  = [[0 for _ in range(NB)] for _ in range(t)]
   # finish_valB = [[0 for _ in range(NB)] for _ in range(t)]
   # tp_valB     = [[0 for _ in range(NB)] for _ in range(t)]
#
   # start_valA  = [[0 for _ in range(NA)] for _ in range(t)]
   # finish_valA = [[0 for _ in range(NA)] for _ in range(t)]
   # tp_valA     = [[0 for _ in range(NA)] for _ in range(t)]
   # max_execA = 0
   # max_execB =0
   # #for i in range(t):
   # #    for j in range(NB):
   # #        tp_valB = value(taskB[i][j])
   # #        start_valB[i][j]  = value(start_timeB[i][j])  
   # #        finish_valB[i][j] = start_valB[i][j] + exe_tasksB[i]     
   # #        if(tp_valB==1):
   # #            print(f"For Task{i}, the processor assigned to B of instance {j}: Start time is {start_valB[i][j]} ")
   # #            exe_val = finish_valB[i][j]-start_valB[i][j]
   # #            #plt.barh(j,exe_val,left=start_valB[i][j], color=colors[i])
   # #            #plt.text(start_valB[i][j]+ exe_val/2,y=j,s=f"Task{i}",va='center',ha='center')
#
   # for i in range(t):
   #     for j in range(NA):
   #         tp_valA = value(taskA[i][j])
   #         start_valA[i][j]  = value(start_timeA[i][j])  
   #         finish_valA[i][j] = start_valA[i][j] + exe_tasksA[i]     
   #         if(tp_valA==1):
   #             print(f"For Task{i}, the processor assigned to A of instance {j}: Start time is {start_valA[i][j]} ")
   #             exe_val = finish_valA[i][j]-start_valA[i][j]
   #             plt.barh(j,exe_val,left=start_valA[i][j], color=colors[i])
   #             plt.text(start_valA[i][j]+ exe_val/2,y=j,s=f"Task{i}",va='center',ha='center')
##
   # max_execA = max(finish_valA[i][j] for i in range(t) for j in range(NA) if value(taskA[i][j]) == 1)
   # #max_execB = max(finish_valB[i][j] for i in range(t) for j in range(NB) if value(taskB[i][j]) == 1)
   # #plot_schedule(taskA, taskB, start_valA, start_valB, exe_tasksA, exe_tasksB, NA, NB)
   # print(max_execA)
   # for i in range(t):
   #     for j in range(NA):
   #         if(finish_valA[i][j]==max_execA and value(taskA[i][j])==1):
   #             processor=j
   #             print(processor)
   #             
   # plt.text(x=max_execA+350,y=processor,s=f"{max_execA} ",va='center',ha='center')
   # processors = [f"Processor {j}" for j in range(NA)]
   # plt.xlabel("Execution Time in ms")
   # plt.ylabel("Processor Number")
   # plt.legend()
   # plt.grid()
   # plt.yticks(range(NA), processors)  # Set processor names on y-axis
   # plt.show()
#



#def plot_schedule(taskA, taskB, start_timeA, start_timeB, exe_tasksA, exe_tasksB, NA, NB):
#    colors = [
#        'red', 'green', 'blue', 'orange', 'purple', 'cyan', 'magenta', 'yellow', 'pink', 'lime', 'teal'
#    ]
#    
#    plt.figure(figsize=(10, 6))
#    y_labels = []
#    y_positions = []
#    bar_colors = []
#
#    # Track the y-position for each processor
#    y_pos = 0
#
#    # Plot tasks assigned to Processor Type A
#    for j in range(NA):
#        y_labels.append(f"Processor A{j}")
#        for i in range(len(taskA)):
#            if value(taskA[i][j]) == 1:
#                start = value(start_timeA[i][j])
#                finish = start + exe_tasksA[i]
#                plt.barh(y_pos, finish - start, left=start, color=colors[i % len(colors)], edgecolor='black')
#                plt.text(
#                    start + (finish - start) / 2,
#                    y_pos,
#                    f"T{i}",
#                    color='white',
#                    ha='center',
#                    va='center'
#                )
#        y_positions.append(y_pos)
#        y_pos += 1
#
#    # Plot tasks assigned to Processor Type B
#    for j in range(NB):
#        y_labels.append(f"Processor B{j}")
#        for i in range(len(taskB)):
#            if value(taskB[i][j]) == 1:
#                start = value(start_timeB[i][j])
#                finish = start + exe_tasksB[i]
#                plt.barh(y_pos, finish - start, left=start, color=colors[i % len(colors)], edgecolor='black')
#                plt.text(
#                    start + (finish - start) / 2,
#                    y_pos,
#                    f"T{i}",
#                    color='white',
#                    ha='center',
#                    va='center'
#                )
#        y_positions.append(y_pos)
#        y_pos += 1
#
#    # Finalize the plot
#    plt.xlabel("Time")
#    plt.ylabel("Processors")
#    plt.title("Task Scheduling Visualization")
#    plt.yticks(y_positions, y_labels)
#    plt.grid(axis='x')
#    plt.show()



if __name__=="__main__":
    main()