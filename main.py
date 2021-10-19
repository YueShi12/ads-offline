import gurobipy as gp
from gurobipy import GRB
from classes import *
import os

g = [None]  # global variables
patients = []
timeslots = 100
def readinput():
    f = open("designed-input.txt")
    g.append(int(f.readline()))  # processing time of the first shot
    g.append(int(f.readline()))  # tne is theprocessing time of the second shot
    g.append(int(f.readline()))  # the minimum gap between the first and the second shot
    g.append(int(f.readline()))  # the  number of patients

    for i in range(g[3]):
        patientInput = f.readline()
        startI1, endI1, delay, lengthI2 = map(int, patientInput.split(","))
        patient = Patient(startI1, endI1, delay, lengthI2)
        patients.append(patient)
def model():
    m = gp.models('model1')
    x_i_t = m.addVars([g[3],timeslots],vtype=GRB.BINARY,name='ti1')
    y_i_t = m.addVars([g[3],timeslots],vtype=GRB.BINARY,name='ti2')
    firstshot = m.addaddConstrs()





readinput()


