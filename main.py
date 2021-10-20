import gurobipy as gp
from gurobipy import GRB
import numpy
import scipy
from classes import *
import os

p1 = 0  # global variables
p2 = 0
gap = 0
n = 0
T = []  # define the timeslots as lists
timeslots = 100
hospitals = 100  # define the hospital numbers in advance

patients = []


def readinput():
    f = open("designed-input.txt")
    p1 = int(f.readline())  # processing time of the first shot
    p2 = int(f.readline())  # tne is theprocessing time of the second shot
    gap = int(f.readline())  # the minimum gap between the first and the second shot
    n = int(f.readline())  # the  number of patients
    # g[0] means p1
    # g[1] means p2
    # g[2] means g
    # g[3] means numbers of the patients

    for i in range(n):
        patientInput = f.readline()
        startI1, endI1, delay, lengthI2 = map(int, patientInput.split(","))
        patient = Patient(startI1, endI1, delay, lengthI2)
        patients.append(patient)
    for i in range(n):
        print(patients[i].endIs)
    return patients


def model():
    for i in range(timeslots):
        T.append(int(i))

    T1 = numpy.asarray(T)
    m = gp.Model('model1')

    # Create Variables
    x_i_t = m.addMVar((timeslots, 15), vtype=GRB.BINARY, name='x_i_t')
    y_i_t = m.addMVar((timeslots, 15), vtype=GRB.BINARY, name='y_i_t')
    #
    # h_j = m.addMVar(100, vtype=GRB.BINARY, name="h_j")
    h_i_j = m.addMVar((15, hospitals), vtype=GRB.BINARY, name="h_i_j")
    h_j_t = m.addMVar((timeslots, hospitals), vtype=GRB.BINARY, name="h_j_t")

    # Set Objective function

    # Set Constraints for time
    # firstshot = m.addaddConstrs()
    m.addConstrs((x_i_t[:, i].sum() == 1) for i in range(15))

    m.addConstrs((T1 @ x_i_t[:, i] >= patients[i].startIs) for i in range(15))
    # # print(T1@x_i_t[:,0])
    m.addConstrs((T1 @ x_i_t[:, i] <= patients[i].endIs + 1 - 2) for i in range(15))
    #
    m.addConstrs((T1 @ y_i_t[:, j] + 3 <= T1 @ x_i_t[:, j] + 2 + 1 + patients[j].delay + patients[j].lengthI2) for j in
                 range(15))
    #
    m.addConstrs((T1 @ y_i_t[:, j] >= 2 + 1 + patients[j].delay + T1 @ x_i_t[:, j]) for j in range(15))
    m.addConstrs((y_i_t[:, j].sum() == 1) for j in range(15))
    #
    # # # Set Constraints for hospital
    # m.addConstrs((h_j[j] - h_j_t[t][j] >= 0) for t in range(100) for j in range(100))
    # m.addConstrs((h_j_t[t + g[1]][j] >= h_i_j[i][j] @ x_i_t[t][i])
    #              for i in range(g[4])
    #              for t in range(90)
    #              for j in range(100)
    #              )
    # m.addConstrs((h_j_t[t + g[1]][j] >= h_i_j[i][j] @ y_i_t[t][i])
    #              for i in range(g[4])
    #              for t in range(90)
    #              for j in range(100)
    #              )
    #

    m.setObjective(T1 @ y_i_t[:, 9], GRB.MINIMIZE)
    m.optimize()
    # m.computeIIS()


    # for i in range(g[4]):
    #     for t in range(100):
    #         print(x_i_t[t][i])
    # print(x_i_t.sum())


p = readinput()
model()
