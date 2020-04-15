

#importing libraries
import xlsxwriter
import alphashape
import sys
from descartes import PolygonPatch
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from tkinter import *
from tkinter.ttk import *
import tkinter as tk
from tkinter import filedialog
import os
from tkinter.filedialog import askopenfile
import matplotlib
import cProfile
import re
from pympler import classtracker, tracker
from memprof import memprof
from memory_profiler import profile
import math
import time, socket, sys
import ctypes
import pyautogui
from tkinter import messagebox  # Python 3
#import tkMessageBox as messagebox  # Python 2

#messagebox.showinfo("Title", "message")
#Creating GUI window
application_window = tk.Tk()
application_window.title("G-Code Analysis")
application_window.withdraw



# Build a list of tuples for each file type the file dialog should display
my_filetypes = [('all files', '.*'),('rich text format',".rtf")]
application_window.geometry("350x50")
#Counter for layer in the g-code
layer_counter = 1
#Path to store the excel sheet
path = "/Users/shivvyas/Desktop/3DPrint_Data" + str(layer_counter) + ".xlsx"
row = 0
column = 0

def connect_monitor():
    print("\nWelcome to G-Code Analysis\n")
    print("Initialising....\n")
    time.sleep(1)

    s = socket.socket()
    shost = socket.gethostname()
    ip = socket.gethostbyname(shost)
    print(shost, "(", ip, ")\n")
    host = "127.0.0.1"  # input(str("Enter server address: "))
    code = input(str("\nEnter your Authentication Code: "))
    name = "G-Code Analyser "
    port = 4008
    print("\nTrying to connect to ", host, "(", port, ")\n")
    #time.sleep(1)
    s.connect((host, port))
    print("Connected...\n")
    #s.send(name.encode())
    s.send(name.encode())
    #s_name = s.recv(1024)
    #s_name = s_name.decode()
    return s

#@profile
def write_and_plot(wbpath , lc , XV , YV , ZV, M_Flag , XN , YN , SOC, HOST):
    '''
    This function aims at writing the extracted information in the excel sheet and plotting it on the bases of geometric reasoning
    '''

    #message = input(str("Me : "))
    #s.send(message.encode())
    s= SOC
    s_name = HOST
    X_Values = XV
    Y_Values = YV
    Z_Values = ZV
    X_New = XN

    Y_New = YN
    #X_New  = X_New.append(X_Values)
    #Y_New = Y_New.append(Y_Values)
    layer_counter = lc
    workbook = xlsxwriter.Workbook(wbpath)
    worksheet = workbook.add_worksheet("My Sheet")
    pointer = 0
    row = 0
    column = 0
    print("\n")
    print("Layer Count : " + str(layer_counter))

    #Loop till all the values in the list and storing it in excel sheet.
    for data in X_Values:
        worksheet.write(row, column, X_Values[pointer])
        column = column + 1
        worksheet.write(row, column, Y_Values[pointer])
        column = column + 1
        worksheet.write(row, column, Z_Values[pointer])
        row = row + 1
        column = 0
        pointer = pointer + 1
    #Closing the excel sheet
    workbook.close()
    X_test1 = []
    Y_test1 = []
    Z_test1 = []
    X_angle = []
    Y_angle = []


    #Loop to remove the unecessary values in the list
    for value in range(len(X_Values)):
        if (X_Values[value] and Y_Values[value] != 'N/A'):
            X_test1.append(X_Values[value])
            #X_angle.append(X_New[value])
            Y_test1.append(Y_Values[value])
    for value in range(len(X_New)):
        if (X_New[value] and Y_New[value] != 'N/A'):
            X_angle.append(X_New[value])
            #X_angle.append(X_New[value])
            Y_angle.append(Y_New[value])


    z_temp = []
    vector_1 = []
    vector_2 = []
    angles = []
    V1 = []
    V2 = []
    shape = ""
    #print(X_New)
    #print("HEllp")
    for index in range(len(X_angle)):
        vector_1.insert(0, float(X_angle[index]))
        vector_1.insert(1, float(Y_angle[index]))

        #print(vector_1)
        #print(vector_2)
        V1.append(vector_1)
        V2.append(vector_2)
        vector_2= []
        vector_1 = []
        angles = []

    if(V1[0] == V1[len(V1)-1]):
        V1 = V1[:(len(V1) - 1)]
    for index in range(len(V1)):
        #a = np.array([int(V1[index][0]),int(V1[index][1])])
        a = np.array(V1[index])

        if((int(index) + 1) > (len(V1)-1)):
            #b = np.array([int(V1[0][0]),int(V1[0][1])])
            b = np.array(V1[0])
            c =  np.array(V1[1])
        else:
            if(((int(index) + 2) > (len(V1)-1))):
                b = np.array(V1[index + 1])
                c =  np.array(V1[0])
            else:#(((int(index) + 1) < (len(V1)-1)) and ((int(index) + 2) < (len(V1))-1)):
                b = np.array(V1[index + 1])
                c = np.array(V1[index +2])





        ba = a - b
        bc = c - b

        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.arccos(cosine_angle)
        #print(np.degrees(angle))#Plotting the figure
        angles.append(np.degrees(angle))


    Shape = ""
    print("Angeles are :")
    print(angles)
    sides = []
    #for num in range(len(angles)):
     #   sides[num] = V1[num]
    for values in range(len(V1)):
        p1 = V1[values]
        if((values + 1) > (len(V1)-1)):
            p2 = V1[0]
        else:
            p2 = V1[values + 1]
        distance = math.sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2))
        sides.append(float(distance))
     #   print(distance)
    #print(sides)

    print("Sides are : ")
    print(sides)
    count_side = 0
    if(len(angles) == 3):
        print("Triangle")
        message = (str("Triangle"))
        Shape = "Triangle"
        s.send(message.encode())
    elif(angles.count(90.0)==4):
        if(sides.count(sides[0]) == 4):
            print("Square")
            message = (str("Square"))
            s.send(message.encode())
            Shape = "Square"
        if (sides.count(sides[0]) == 2):
                print("Rectangle")
                message = (str("Rectangle"))
                s.send(message.encode())
                Shape = "Rectangle"

                #break
    #elif(angles.count(90.0)==2):
     #           #print("It is a rectangle")
      ##         message = (str("Rectangle"))
        #        s.send(message.encode())
        #if(count == 4 ):
         ### s.send(message.encode())


    elif(len(angles)  >= 4 ):
        print("A polygon with  " + str(len(angles)) + " sides.")
        message = (str("Polygon"))
        s.send(message.encode())
        Shape = "Polygon with "+str(len(angles))+" Sides."
    else:
        print("A random shape")
        message = (str("Random Shape"))
        s.send(message.encode())
        Shape = "Random Shape"

    message = s.recv(1024)
    message = message.decode()
    print(s_name, ":", message)

    if("Alert" in message):
        #pyautogui.alert('Wrong Sequence', "Alert")
        messagebox.showwarning("Warning","Wrong Sequence")
        #tk.messagebox.showwarning("Warning","Wrong Sequence",application_window)
        #print(V1)


    count_side = 0
    #print(np.degrees(angle))#Plotting the figure
    X_angle.clear()
    Y_angle.clear()




    for i in range(len(X_test1)):
        z_temp.append((1))
    fig = go.Figure(go.Scatter(x=X_test1, y=Y_test1))
    tittle_string = "Layer : " + str(layer_counter) + ".\n" + "It is a "+ Shape + ".\nThe angles are " + str(angles)+ ".\n The dimensions are " +str(sides) + ". The Co-Ordinates are " + str(V1)
    fig.update_layout(
        title= tittle_string)
    fig.update_layout()

    #Showing the figure
    #X_Values.c;
    fig.show()
    angles.clear()
    sides.clear()
    V1.clear()
    V2.clear()



#Function for taking files as input and storing all the values
def checkitout():
    s = connect_monitor()
    s_name = s.recv(1024)
    s_name = s_name.decode()

    print(s_name, " and Runtime Monitoring started \n [exit] to Runtime Monitoring \n\n")
    # time.sleep(2)
    # s_name = s.recv(1024)
    # s_name = s_name.decode()
    time.sleep(1)
    message = s.recv(1024)
    message = message.decode()
    print(s_name, ":", message)

    message = input(str("Me : "))
    s.send(message.encode())
    message = s.recv(1024)
    message = message.decode()
    print(s_name, ":", message)
    file1 = filedialog.askopenfilename(parent=application_window,
                                       initialdir=os.getcwd(),
                                       title="Please select a file:",
                                       filetypes=my_filetypes)

    X_Values = []
    Y_Values = []
    Z_Values = []
    X_new = []
    Y_new = []

    layer_counter = 1
    fig = plt.figure()
    file = open(file1)
    #Reading the file line by line
    for line in file:
        if ("layer" not in line and "M30" not in line):
            #print(line)
            #definig flag if a particular co-ordinate is not in the line
            trackx = False
            tracky = False
            trackz = False
            #Only if there is movement
            if ("G00" or "G01" in line):
                all = line[0:(len(line) - 1)].split(" ")
                for item in all:
                    if ("X" in item):
                        #If there are space is there remove it
                        if ("\\" in item):
                            a = item.split("\\")
                            X_Values.append(a[0][1:])
                            X_new.append(a[0][1:])

                        else:
                            X_Values.append(item[1:])
                            X_new.append(item[1:])
                        trackx = True
                    if ("Y" in item):
                        tracky = True
                        if ("\\" in item):
                            qp = item.split("\\")
                            Y_Values.append(qp[0][1:])
                            Y_new.append(qp[0][1:])
                        else:
                            Y_Values.append(item[1:])
                            Y_new.append(item[1:])
                    if ("Z" in item):
                        Z_Values.append(item[1:])
                        trackz = True
                if (trackx == False):
                    X_Values.append("N/A")
                    X_new.append("N/A")
                if (tracky == False):
                    Y_Values.append("N/A")
                    Y_new.append("N/A")
                if (trackz == False):
                    Z_Values.append("N/A")
        #End of the layer or end of the program
        elif ("layer" in line or "M30" in line):

            M_check = True
            #Calling the ploting function

            write_and_plot(path,layer_counter,X_Values,Y_Values,Z_Values,M_check,X_new,Y_new,s,s_name)
            #Incrementing the layer counter\
            X_new.clear()
            Y_new.clear()
            layer_counter = layer_counter + 1
    else:

            print("End of Program")
            message = (str("[exit]"))
            s.send(message.encode())
            #Running the profiler
            #cProfile.run('re.compile("foo|bar")')




#Attaching the button to the GUI
button = tk.Button(application_window,
                   text="Select G-Code",
                   fg="red",
                   command= checkitout )

button.pack(side=tk.TOP)

#Continuesly runnig the GUI
application_window.mainloop()
