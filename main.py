import gurobipy as gp
from gurobipy import GRB
import numpy
import scipy
from classes import *
import os

g = [None]  # global variables

T = []# define the timeslots as lists
timeslots = 100
hospitals = 100  # define the hospital numbers in advance


def readinput():
    patients = []
    f = open("designed-input.txt")
    g.append(int(f.readline()))  # processing time of the first shot
    g.append(int(f.readline()))  # tne is theprocessing time of the second shot
    g.append(int(f.readline()))  # the minimum gap between the first and the second shot
    g.append(int(f.readline()))  # the  number of patients
    # g[0] means p1
    # g[1] means p2
    # g[2] means g
    # g[3] means numbers of the patients

    for i in range(g[4]):
        patientInput = f.readline()
        startI1, endI1, delay, lengthI2 = map(int, patientInput.split(","))
        patient = Patient(startI1, endI1, delay, lengthI2)
        patients.append(patient)
    return patients


def model(patients):
    for i in range(timeslots):
        T.append(int(i))

    T1 = numpy.asarray(T)
    m = gp.Model('model1')



    # Create Variables
    x_i_t = m.addMVar((timeslots,g[4]), vtype=GRB.BINARY, name='x_i_t')
    y_i_t = m.addMVar((timeslots,g[4]), vtype=GRB.BINARY, name='y_i_t')

    h_j = m.addVars(100, vtype=GRB.BINARY, name="h_j")
    h_i_j = m.addMVars((hospitals, g[4]), vtype=GRB.BINARY, name="h_i_j")
    h_j_t = m.addMVars((timeslots,hospitals), vtype=GRB.BINARY, name="h_j_t")

    # Set Objective function

    # Set Constraints for time
    # firstshot = m.addaddConstrs()
    m.addConstrs((x_i_t[:,i].sum() == 1) for i in range(g[4]))
    m.addConstrs( (T1 @ x_i_t[:,i] >= patients[i].startIs) for i in range(g[4]) )
    m.addConstrs( (T1 @ x_i_t[:,i] <= patients[i].endIs + 1 - g[1]) for i in range(g[4]))
    m.addConstrs((T1@y_i_t[:,i] - T1@x_i_t[:,i] <= g[1] + g[3] + patients[i].delay + patients[i].lengthI2 - g[2]) for i in range(g[4]))
    m.addConstrs((T1@y_i_t[:,i] - T1@x_i_t[:,i] >= g[1] + g[3] + patients[i].delay) for i in range(g[4]))
    m.addConstrs((y_i_t[:,i].sum() == 1) for i in range(g[4]))

    # Set Constraints for hospital
   

    m.setObjective(x_i_t[:,1].sum(),GRB.MAXIMIZE)
    m.optimize()






p=readinput()
model(p)

