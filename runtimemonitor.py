# server.py
import time, socket, sys
import smtplib
#server = smtplib.SMTP('smtp.gmail.com', 587)
#server.login("shivvyas3030@gmail.com", "Shiv12345")
#msg ="Wrong Sequence"
print("\nWelcome to Run-Time Monitor for 3D Printers\n")
print("Initialising....\n")
time.sleep(1)

s = socket.socket()
host = "127.0.0.1"
ip = socket.gethostbyname(host)
port = 4008


s.bind((host, port))
print(host, "(", ip, ")\n")
code = input(str("Enter your Authentication Code: "))

name = "Runtime Monitor"

s.listen(1)
print("\nWaiting for G-Code Analyzer...\n")
conn, addr = s.accept()
print("Received connection from ", addr[0], "(", addr[1], ")\n")

s_name = conn.recv(1024)
s_name = s_name.decode()
print(s_name, "has connected to the Runtime Monitor\nEnter [exit] to exit monitoring room\n")
conn.send(name.encode())
time.sleep(2)
#sequence = (input("Enter Your desired sequence").split(" "))
#print(sequence)
message = "Send Your desired sequence"
conn.send(message.encode())
message = conn.recv(1024)
message = message.decode()


sequence = str(message).split(" ")
print(sequence)
length = len(sequence)
counter = 0
#print(sequence.index("Triangle"))

#print(sequence.index("Rectangle"))
print("Length" + str(length))
First_Flag = False
Flag = False
#message = input(str("Me : "))
#conn.send(message.encode())
while True:
    #message = input(str("Me : "))

    if((First_Flag == False) and (Flag == False)):
        message = "Okay"
        conn.send(message.encode())
        print("\n")
        First_Flag == True
        time.sleep(1)
        counter = 0
    elif((counter <= length) and (Flag == True)):
        if(String1 == String2):
            message = "Okay"
            conn.send(message.encode())
            print("\n")
            counter = counter +1
            Flag = False
            #time.sleep(1)
        if(not(String1 == String2)):
            print("(" + sequence[counter].lower() + "!=" +  message.lower() + ")")
            message = "Alert --> Wrong Sequence"
            conn.send(message.encode())
            print("\n")
            #server.sendmail("shivvyas3030@gma.com", "svyas2019@my.fit.edu", msg)
            counter = counter +1
            Flag = False
            #time.sleep(1)
    elif(counter > length):
            message = "Number of Layers is more than you desired sequence"
            conn.send(message.encode())
            print("\n")
            counter = counter + 1
            Flag = False
            #time.sleep(1)
    elif(message == "[exit]"):
        message = "G-Code Analysis Stopped!"
        conn.send(message.encode())
        print("\n")
        Flag = False
        #time.sleep(1)
        break
    else:

        message = "Waiting for your response"
        conn.send(message.encode())
        print("\n")
        #time.sleep(1)
        #break


        #conn.send(message.encode())
    time.sleep(1)
    message = conn.recv(1024)
    message = message.decode()
    Flag = True
    String1 = (sequence[counter]).lower()
    String2 = message.lower()
    #counter = counter + 1

    print(length)
    print(s_name, ":", message)

