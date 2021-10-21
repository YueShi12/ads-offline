import gurobipy as gp
from gurobipy import GRB, quicksum
import numpy
import scipy
from classes import *
import os

g = [] # global variables

T = []  # define the timeslots as lists
timeslots = 100
hospitals = 100  # define the hospital numbers in advance

patients = []


def readinput():
    f = open("designed-input.txt")
    g.append( int(f.readline())  )# processing time of the first shot
    g.append( int(f.readline())  )# tne is theprocessing time of the second shot
    g.append( int(f.readline())  )# the minimum gap between the first and the second shot
    g.append(int(f.readline() ) )# the  number of patients
    # g[0] means p1
    # g[1] means p2
    # g[2] means g
    # g[3] means numbers of the patients

    for i in range(g[3]):
        patientInput = f.readline()
        startI1, endI1, delay, lengthI2 = map(int, patientInput.split(","))
        patient = Patient(startI1, endI1, delay, lengthI2)
        patients.append(patient)

    print(g[0],g[1],g[2],g[3])
    return patients


def model():
    for i in range(timeslots):
        T.append(int(i))

    T1 = numpy.asarray(T)
    m = gp.Model('model1')

    # Create Variables
    x_i_t = m.addMVar((timeslots, g[3]), vtype=GRB.BINARY, name='x_i_t')
    y_i_t = m.addMVar((timeslots, g[3]), vtype=GRB.BINARY, name='y_i_t')

    h_j = m.addMVar(hospitals, vtype=GRB.BINARY, name="h_j")
    h_i_j_1 = m.addMVar((g[3], hospitals), vtype=GRB.BINARY, name="h_i_j")
    h_i_j_2 = m.addMVar((g[3], hospitals), vtype=GRB.BINARY, name="h_i_j")
    h_j_t = m.addMVar((timeslots, hospitals), vtype=GRB.BINARY, name="h_j_t")

    # Set Constraints for time

    m.addConstrs((x_i_t[:, i].sum() == 1) for i in range(g[3]))

    m.addConstrs((T1 @ x_i_t[:, i] >= patients[i].startIs) for i in range(g[3]))
    # # print(T1@x_i_t[:,0])
    m.addConstrs((T1 @ x_i_t[:, i] <= patients[i].endIs + g[2] - g[0]) for i in range(g[3]))
    #
    m.addConstrs((T1 @ y_i_t[:, j] + g[1] <= T1 @ x_i_t[:, j] + g[0] + g[2] + patients[j].delay + patients[j].lengthI2) for j in
                 range(g[3]))
    #
    m.addConstrs((T1 @ y_i_t[:, j] >= g[0] + g[2] + patients[j].delay + T1 @ x_i_t[:, j]) for j in range(g[3]))
    m.addConstrs((y_i_t[:, j].sum() == 1) for j in range(g[3]))
    #
    # # # Set Constraints for hospital
    m.addConstrs((h_j[j] - h_j_t[t][j] >= 0) for t in range(timeslots) for j in range(hospitals))

    m.addConstrs((h_j_t[t + g[0]][j] >= x_i_t[t] @ h_i_j_1[:,j])
                 for i in range(g[3])
                 for t in range(timeslots-g[0])
                 for j in range(hospitals)
                 )
    m.addConstrs((h_j_t[t + g[1]][j] >= y_i_t[t] @ h_i_j_2[:,j])
                 for i in range(g[3])
                 for t in range(timeslots-g[1])
                 for j in range(hospitals)
                 )

    m.addConstrs((h_i_j_1[i].sum() == 1) for i in range(g[3]))
    m.addConstrs((h_i_j_2[i].sum() == 1) for i in range(g[3]))
    m.addConstrs((quicksum(x_i_t[t+n][i] * h_i_j_1[i][j] for n in range(p[0]) for j in range(hospitals))<=1)
                 for t in range(timeslots)
                 for i in range(g[3])
                 )
    m.addConstrs((quicksum(y_i_t[t+n][i] * h_i_j_2[i][j] for n in range(p[1]) for j in range(hospitals))<=1)
                 for t in range(timeslots)
                 for i in range(g[3])
                 )






    m.setObjective(h_j.sum(), GRB.MINIMIZE)
    m.optimize()
    # m.computeIIS()


    # for i in range(g[4]):
    #     for t in range(100):
    #         print(x_i_t[t][i])
    # print(x_i_t.sum())


p = readinput()
model()
