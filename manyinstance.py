import gurobipy as gp
from gurobipy import GRB, quicksum
import time
import numpy
from classes import *

timeslots = 1000  # define the timeslots numbers in advance
hospitals = 10  # define the hospital numbers in advance
filename = []


def readinput(filename):
    patients = []
    g = []
    f = open(filename)
    g.append(int(f.readline()))  # processing time of the first shot
    g.append(int(f.readline()))  # tne is theprocessing time of the second shot
    g.append(int(f.readline()))  # the minimum gap between the first and the second shot
    g.append(int(f.readline()))  # the  number of patients
    # g[0] means p1
    # g[1] means p2
    # g[2] means g
    # g[3] means numbers of the patients

    for i in range(g[3]):
        patientInput = f.readline()
        startI1, endI1, delay, lengthI2 = map(int, patientInput.split(","))
        patient = Patient(startI1, endI1, delay, lengthI2)
        patients.append(patient)

    print(g[0], g[1], g[2], g[3])
    return patients, g, filename


def model(patients, g, filename):
    T = []
    for i in range(timeslots):
        T.append(int(i))

    T1 = numpy.asarray(T)
    m = gp.Model('model1')

    # # Create Variables
    x_i_t = m.addMVar((timeslots, g[3]), vtype=GRB.BINARY,
                      name='x_i_t')  # This variable is equal to 1 if patient i will have the fist shot at time t
    x_i_t = x_i_t.tolist()
    x_i_t = numpy.asarray(x_i_t)
    y_i_t = m.addMVar((timeslots, g[3]), vtype=GRB.BINARY,
                      name='y_i_t')  # This variable is equal to 1 if patient i will have the second shot at time t
    y_i_t = y_i_t.tolist()
    y_i_t = numpy.asarray(y_i_t)

    h_j = m.addMVar(hospitals, vtype=GRB.BINARY, name="h_j")  # This variable is equal to 1 if the hospital j is used.
    h_j = h_j.tolist()
    h_j = numpy.asarray(h_j)
    h_i_j_1 = m.addMVar((g[3], hospitals), vtype=GRB.BINARY,
                        name="h_i_j_1")  # This variable is equal to 1 if patient i is in hospital j for first shot
    h_i_j_1 = h_i_j_1.tolist()
    h_i_j_1 = numpy.asarray(h_i_j_1)
    h_i_j_2 = m.addMVar((g[3], hospitals), vtype=GRB.BINARY,
                        name="h_i_j_2")  # This variable is equal to 1 if patient i is in hospital j for second shot
    h_i_j_2 = h_i_j_2.tolist()
    h_i_j_2 = numpy.asarray(h_i_j_2)
    h_j_t = m.addMVar((hospitals, timeslots), vtype=GRB.BINARY,
                      name="h_j_t")  # The variable is equal to 1 if the hospital is used at time t
    h_j_t = h_j_t.tolist()
    h_j_t = numpy.asarray(h_j_t)

    # Set Constraints for time

    # every patient needs to have a first shot
    m.addConstrs((x_i_t[:, i].sum() == 1)
                 for i in range(g[3])
                 )

    # the first shot  is scheduled after the patient-dependent first available time slot
    m.addConstrs((T1 @ x_i_t[:, i] >= patients[i].startIs)
                 for i in range(g[3])
                 )
    # the  first  shot  which  is  scheduled  in  the  patient-dependent interval.
    m.addConstrs((T1 @ x_i_t[:, i] <= patients[i].endIs + 1 - g[0])
                 for i in range(g[3])
                 )
    # the second shot which is scheduled in the patient-dependent interval
    m.addConstrs((T1 @ y_i_t[:, j] + g[1] <= T1 @ x_i_t[:, j] + g[0] + g[2] + patients[j].delay + patients[j].lengthI2)
                 for j in range(g[3])
                 )
    #
    m.addConstrs((T1 @ y_i_t[:, j] >= g[0] + g[2] + patients[j].delay + T1 @ x_i_t[:, j])
                 for j in range(g[3])
                 )
    # every patient needs to have a second shot
    m.addConstrs((y_i_t[:, j].sum() == 1)
                 for j in range(g[3])
                 )

    # # Set Constraints for hospital
    # make every hospital we used to 1
    m.addConstrs((h_j[j] >= h_j_t[j][t])
                 for t in range(timeslots)
                 for j in range(hospitals)
                 )

    # if a patient i has it’s first shot scheduled in hospital j, all time slots starting at t, up to t + p1 should be marked as taken
    m.addConstrs((h_j_t[j][t + n] >= x_i_t[t][i] * h_i_j_1[i][j])
                 for i in range(g[3])
                 for n in range(g[0])
                 for t in range(timeslots - g[0])
                 for j in range(hospitals)

                 )
    # The same constraint is given for the second shot
    m.addConstrs((h_j_t[j][t + n] >= y_i_t[t][i] * h_i_j_2[i][j])
                 for i in range(g[3])
                 for n in range(g[1])
                 for t in range(timeslots - g[1])
                 for j in range(hospitals)
                 )
    # the total number of timeslots we marked is up to g[3]*(g[0]+g[1])
    m.addConstr(h_j_t.sum() <= x_i_t.sum() * g[0] + y_i_t.sum() * g[1])

    # every patient can only have one hospital for the first shot
    m.addConstrs((h_i_j_1[i].sum() == 1)
                 for i in range(g[3])
                 )
    # every patient can only have one hospital for the second shot
    m.addConstrs((h_i_j_2[i].sum() == 1)
                 for i in range(g[3])
                 )

    # for ever hospital at one timeslot can only deal with one patient
    m.addConstrs((quicksum(x_i_t[t + n][i] * h_i_j_1[i][j] + y_i_t[t + n][i] * h_i_j_2[i][j]for i in range(g[3]) for n in range(g[0]-1)) <= 1)
                 for t in range(timeslots - g[0])
                 for j in range(hospitals)
                 )
    m.addConstrs((quicksum(x_i_t[t + n][i] * h_i_j_1[i][j] + y_i_t[t + n][i] * h_i_j_2[i][j] for i in range(g[3]) for n in
        range(g[1]-1)) <= 1)
                 for t in range(timeslots - g[1])
                 for j in range(hospitals)
                 )


    m.setObjective(h_j.sum(), GRB.MINIMIZE)
    m.optimize()

    print('___________________hosipitail for the first shot______________________________________')
    for i in range(g[3]):
        for j in range(hospitals):
            if h_i_j_1[i][j].x >= 1:
                print('hospital location:', j, 'patient:', i)

    print('______________________hospital for the second shot___________________________________')
    for i in range(g[3]):
        for j in range(hospitals):
            if h_i_j_2[i][j].x >= 1:
                print('hospital location:', j, 'patient:', i)

    print('______________________time schedule for the first shot________________________________')
    for i in range(g[3]):
        for t in range(timeslots):
            if x_i_t[t][i].x >= 1:
                print('time slot:', t, 'patien:', i)
    print('______________________time schedule for the second shot_______________________________')
    for i in range(g[3]):
        for t in range(timeslots):
            if y_i_t[t][i].x >= 1:
                print('time slot:', t, 'patien:', i)
    print('_________________________________hospital we used_____________________________________')
    h_used = []
    for j in range(hospitals):
        if h_j[j].x >= 1:
            h_used.append(j)
            print(j)

    with open('Hospital_used.txt', 'a+') as f:
        f.writelines(filename + '   ' + str(h_used) + '\n')
    m.reset()


def main():
    #
    filename.append('10-1.txt')
    # filename.append('4-2.txt')
    # filename.append('4-4.txt')
    # filename.append('6-1.txt')
    # filename.append('5-3.txt')
    # filename.append('5-4.txt')
    # filename.append('6-1.txt')
    # filename.append('6-2.txt')
    # filename.append('6-3.txt')
    # filename.append('7-1.txt')
    # filename.append('7-2.txt')
    # filename.append('9.txt')
    # filename.append('10-3.txt')
    # filename.append('23.txt')
    # filename.append('25.txt')

    # filename.append('20.txt')
    # filename.append('23.txt')
    # filename.append('25.txt')# add the file name you copy this line mutil times
    time_used_total = []

    for file in filename:
        start_time = time.time()
        p, g, f = readinput(file)
        model(p, g, file)
        time_used = time.time() - start_time
        time_used_total.append(file + '   ' + str(time_used))

    with open('time.txt', 'a+') as f:
        for t in time_used_total:
            f.writelines(t + '\n')


main()
# p = readinput()
# model()
