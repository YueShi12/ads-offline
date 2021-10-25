import gurobipy as gp
from gurobipy import GRB
from classes import *
import os

g = [None]  # global variables
patients = []
T = [] # define the timeslots as lists
timeslots = 100
hospitals = 100  # define the hospital numbers in advance


def readinput():
    f = open("designed-input.txt")
    g.append(int(f.readline()))  # processing time of the first shot
    g.append(int(f.readline()))  # tne is theprocessing time of the second shot
    g.append(int(f.readline()))  # the minimum gap between the first and the second shot
    g.append(int(f.readline()))  # the  number of patients
    # g[0] means p1
    # g[1] means p2
    # g[2] means g
    # g[3] means numbers of the patients

    for i in range():
        patientInput = f.readline()
        startI1, endI1, delay, lengthI2 = map(int, patientInput.split(","))
        patient = Patient(startI1, endI1, delay, lengthI2)
        patients.append(patient)


def model(patient):
    for i in range(timeslots):
        T.append(i)

    m = gp.models('model1')

    # Create Variables
    x_i_t = m.addVars([g[3], timeslots], vtype=GRB.BINARY, name='x_i_t')
    y_i_t = m.addVars([g[3], timeslots], vtype=GRB.BINARY, name='y_i_t')
    h_j = m.addVars([hospitals], vtype=GRB.BINARY, name="h_j")
    h_i_j = m.addVars([g[3], hospitals], vtype=GRB.BINARY, name="h_i_j")
    h_j_t = m.addVars([hospitals, timeslots], vtype=GRB.BINARY, name="h_j_t")

    # Set Objective function

    # Set Constraints for time
    # firstshot = m.addaddConstrs()
    m.addConstr(x_i_t.sum() == 1)
    m.addConstr(x_i_t * x_i_t >= patient.startIs * x_i_t)
    m.addConstr(x_i_t <= patient.endIs + 1 - g[0])
    m.addConstr(y_i_t - x_i_t <= g[0] + g[2] + patient.delay + patient.lengthI2 - g[1])
    m.addConstr((y_i_t - x_i_t) * y_i_t >= (g[0] + g[2] + patient.delay) * y_i_t)
    m.addConstr(y_i_t.sum() == 1)


readinput()


