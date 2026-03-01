#===================== IMPORT PACKAGES ==============================

import pandas as pd
from tkinter.filedialog import askopenfilename
import re
import warnings
warnings.filterwarnings("ignore")
from sklearn import naive_bayes

#============================= DATA SELECTION ==============================

dataframe=pd.read_csv("C:/Users/EGC/CloudMe/Task Scheduling/Task Data.csv")

print("--------------------------------------")
print("Input Data ")
print("--------------------------------------")
print()

dataframe.columns =['Position','Instructions','Size','high_priority','Class','Server']

print(dataframe.head(20))

#============================= DATA PREPROCESSING ==============================

#=== CHECKING MISSING VALUES ====

print("--------------------------------------")
print("Checking Missing Values")
print("--------------------------------------")
print()
print(dataframe.isnull().sum())


#=== LABEL ENCODING ====

from sklearn import preprocessing

le = preprocessing.LabelEncoder()

print("--------------------------------------")
print("Before Label Encoding ")
print("--------------------------------------")
print()

print(dataframe['Instructions'] .head(10))

dataframe['Instructions'] = le.fit_transform(dataframe['Instructions'])

dataframe['Size'] = le.fit_transform(dataframe['Size'])

print("--------------------------------------")
print("Before Label Encoding ")
print("--------------------------------------")
print()

print(dataframe['Instructions'] .head(10))

#============================= TASK SCHEDULING ==============================

#===== ROUND ROBIN ==========

print("-----------------------------------------------")
print("Round Robin (Task Scheduling)")
print("-----------------------------------------------")
print()










class RoundRobin:

    def processData(self, no_of_processes):
        process_data = []
        for i in range(no_of_processes):
            temporary = []
            import random
            process_id=random.randint(0,10)
#            process_id = int(input("Enter Process ID: "))

            arrival_time = int(input(f"Enter Arrival Time for Process {process_id}: "))

            burst_time = int(input(f"Enter Burst Time for Process {process_id}: "))

            temporary.extend([process_id, arrival_time, burst_time, 0, burst_time])

            process_data.append(temporary)

        time_slice = int(input("Enter Time Slice: "))

        RoundRobin.schedulingProcess(self, process_data, time_slice)

    def schedulingProcess(self, process_data, time_slice):
        start_time = []
        exit_time = []
        executed_process = []
        ready_queue = []
        s_time = 0
        process_data.sort(key=lambda x: x[1])

        while 1:
            normal_queue = []
            temp = []
            for i in range(len(process_data)):
                if process_data[i][1] <= s_time and process_data[i][3] == 0:
                    present = 0
                    if len(ready_queue) != 0:
                        for k in range(len(ready_queue)):
                            if process_data[i][0] == ready_queue[k][0]:
                                present = 1

                    if present == 0:
                        temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][4]])
                        ready_queue.append(temp)
                        temp = []

                    if len(ready_queue) != 0 and len(executed_process) != 0:
                        for k in range(len(ready_queue)):
                            if ready_queue[k][0] == executed_process[len(executed_process) - 1]:
                                ready_queue.insert((len(ready_queue) - 1), ready_queue.pop(k))

                elif process_data[i][3] == 0:
                    temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][4]])
                    normal_queue.append(temp)
                    temp = []
            if len(ready_queue) == 0 and len(normal_queue) == 0:
                break
            if len(ready_queue) != 0:
                if ready_queue[0][2] > time_slice:

                    start_time.append(s_time)
                    s_time = s_time + time_slice
                    e_time = s_time
                    exit_time.append(e_time)
                    executed_process.append(ready_queue[0][0])
                    for j in range(len(process_data)):
                        if process_data[j][0] == ready_queue[0][0]:
                            break
                    process_data[j][2] = process_data[j][2] - time_slice
                    ready_queue.pop(0)
                elif ready_queue[0][2] <= time_slice:

                    start_time.append(s_time)
                    s_time = s_time + ready_queue[0][2]
                    e_time = s_time
                    exit_time.append(e_time)
                    executed_process.append(ready_queue[0][0])
                    for j in range(len(process_data)):
                        if process_data[j][0] == ready_queue[0][0]:
                            break
                    process_data[j][2] = 0
                    process_data[j][3] = 1
                    process_data[j].append(e_time)
                    ready_queue.pop(0)
            elif len(ready_queue) == 0:
                if s_time < normal_queue[0][1]:
                    s_time = normal_queue[0][1]
                if normal_queue[0][2] > time_slice:

                    start_time.append(s_time)
                    s_time = s_time + time_slice
                    e_time = s_time
                    exit_time.append(e_time)
                    executed_process.append(normal_queue[0][0])
                    for j in range(len(process_data)):
                        if process_data[j][0] == normal_queue[0][0]:
                            break
                    process_data[j][2] = process_data[j][2] - time_slice
                elif normal_queue[0][2] <= time_slice:

                    start_time.append(s_time)
                    s_time = s_time + normal_queue[0][2]
                    e_time = s_time
                    exit_time.append(e_time)
                    executed_process.append(normal_queue[0][0])
                    for j in range(len(process_data)):
                        if process_data[j][0] == normal_queue[0][0]:
                            break
                    process_data[j][2] = 0
                    process_data[j][3] = 1
                    process_data[j].append(e_time)
        t_time = RoundRobin.calculateTurnaroundTime(self, process_data)
        w_time = RoundRobin.calculateWaitingTime(self, process_data)
        RoundRobin.printData(self, process_data, t_time, w_time, executed_process)

    def calculateTurnaroundTime(self, process_data):
        total_turnaround_time = 0
        for i in range(len(process_data)):
            turnaround_time = process_data[i][5] - process_data[i][1]
            '''
            turnaround_time = completion_time - arrival_time
            '''
            total_turnaround_time = total_turnaround_time + turnaround_time
            process_data[i].append(turnaround_time)
        average_turnaround_time = total_turnaround_time / len(process_data)
        '''
        average_turnaround_time = total_turnaround_time / no_of_processes
        '''
        return average_turnaround_time

    def calculateWaitingTime(self, process_data):
        total_waiting_time = 0
        for i in range(len(process_data)):
            waiting_time = process_data[i][6] - process_data[i][4]
            '''
            waiting_time = turnaround_time - burst_time
            '''
            total_waiting_time = total_waiting_time + waiting_time
            process_data[i].append(waiting_time)
        average_waiting_time = total_waiting_time / len(process_data)
        '''
        average_waiting_time = total_waiting_time / no_of_processes
        '''
        return average_waiting_time

    def printData(self, process_data, average_turnaround_time, average_waiting_time, executed_process):
        process_data.sort(key=lambda x: x[0])
        '''
        Sort processes according to the Process ID
        '''
        print("P.ID  Arrival.T  Rem_Burst.T  Completed  Origl.Burst.T  Completion.T Turnaround.T Wait.T")
        for i in range(len(process_data)):
            for j in range(len(process_data[i])):

                print(process_data[i][j], end="		   ")
            print()

        print(f'Average Turnaround Time: {average_turnaround_time}')

        print(f'Average Waiting Time: {average_waiting_time}')

        print(f'Sequence of Processes: {executed_process}')


# ==== STEP 1 ---> 

# == No Of Servers ==
servers1=int(input("How Many Servers which we have?:"))



# ==== STEP 2 ---> 

# == No Of Processors ==
processors=int(input("How Many Processors which we have?:"))

# == Processors ID Generation ==

for i in range(0,processors):
    import random
    
    process_id=random.randint(0,50)
    print("The process ", i," ID =",process_id)

# arrival time =0

# ==== STEP 3 ---> 


# process burst time

burst_process=[]

for i in range(0,processors): 
    
    size=int(input("Enter the burst time (in kbs):"))
    burst_process.append(size)

# == total burst time for processors

prediction_cap=0
for i in burst_process:
    prediction_cap=prediction_cap+i
    
print("The total no.of burst time =",prediction_cap )    
print()    
    
# == CALCULATION ==

avg_val=prediction_cap/servers1
avg_val=round(avg_val)

print("Average Burst time :")
print()
print(avg_val)

# ==== STEP 4 ---> 


aa=(25/100)*avg_val
aa=round(aa)


print()
print("Capacity of Each Server is ")
cap_ser=avg_val + aa
print()
print(cap_ser)

# ==== STEP 5 ---> 

# == Round Robin





 # servers capacity
   
burst_server=[]

for i in range(servers1):
    size=int(input("Enter the capacity for server (in kbs):"))
    burst_server.append(size)
    

prediction_ser_cap=0
for i in burst_server:
    prediction_ser_cap=prediction_ser_cap+i
print(prediction_ser_cap)

# ==== STEP 6 ---> 



if prediction_cap>prediction_ser_cap:
    print("Task Allocated Successfully")
else:
    print("Need Servers")
    print()
    servers=int(input("How Many Servers?:"))
    final_ser=servers+servers1
    print()
    print("Total No.of servers",final_ser)
    print()
    avg_val=prediction_cap/final_ser
    avg_val=round(avg_val)
    
    print("Average Burst time :")
    print()
    print(avg_val)
    aa=(25/100)*avg_val
    aa=round(aa)
    
    
    print()
    print("Capacity of Each Server is ")
    cap_ser=avg_val + aa
    print()
    print(cap_ser)
    
    burst_server=[]

    for i in range(servers1):
        size=int(input("Enter the capacity for server (in kbs):"))
        burst_server.append(size)
        
    
    prediction_ser_cap=0
    for i in burst_server:
        prediction_ser_cap=prediction_ser_cap+i
    print(prediction_ser_cap)
    
if prediction_cap>prediction_ser_cap:
    print("Task Allocated Successfully")        

#=========================== DATA SPLITTING ====================================

x1=dataframe[['Position','Instructions','Size','high_priority','Class']]
y1=dataframe['Server']


from sklearn.model_selection import train_test_split 

X_train, X_test, y_train, y_test = train_test_split(x1, y1, test_size=0.25, random_state=0)

print("--------------------------------------")
print("Data Splitting           ")
print("--------------------------------------")
print()

print("Total no of data        :",dataframe.shape[0])
print("Total no of test data   :",X_test.shape[0])
print("Total no of train data  :",X_train.shape[0])


#========================== CLASSIFICATION ===================================

# ==== RANDOM FOREST ====

from sklearn.ensemble import RandomForestRegressor

rf = RandomForestRegressor(n_estimators = 100, random_state = 0)

rf.fit(X_train, y_train)  

pred_rf=rf.predict(X_test)

import numpy as np

pred_rf=np.round(pred_rf)


from sklearn import metrics

error=metrics.mean_absolute_error(y_test,pred_rf)

mse=metrics.mean_squared_error(y_test,pred_rf)

print("-------------------------------------------------------------")
print("Performance Analysis --- Random Foreest Regression           ")
print("-------------------------------------------------------------")
print()

Accuracy_rf=100-error

print("1. Accuracy =", Accuracy_rf,'%')
print()
print("2. MAE      =", error)
print()
print("3. MSE      =", mse)
print()


# ==== SUPPORT VECTOR REGRESSION ====

from sklearn.svm import SVR

svr_rbf = SVR(kernel='rbf', C=100, gamma=0.1, epsilon=.1)

svr_rbf.fit(X_train, y_train)  

pred_svr=svr_rbf.predict(X_test)

pred_svr=np.round(pred_svr)

error=metrics.mean_absolute_error(y_test,pred_svr)

mse=metrics.mean_squared_error(y_test,pred_svr)

print("-------------------------------------------------------------")
print("Performance Analysis --- Support Vector Regression           ")
print("-------------------------------------------------------------")
print()

Accuracy_svr=100-error

print("1. Accuracy =", Accuracy_svr,'%')
print()
print("2. MAE      =", error)
print()
print("3. MSE      =", mse)
print()


#=========== DISTRIBUTED =========================

for i in range(len(final_ser)):
#    print("Need Servers")
    
    print("Process ",i," have",processors[i],"kbs", "this allocates to ","Server",i)
    
#============================= ENCRYPPTION  ===============================


import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random
 
BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

print("-------------------------------------------------------------")
print("Encryption --> AES          ")
print("-------------------------------------------------------------")
print()


password = input("Enter password for encryption: ")
 
 
def encrypt(raw, password):
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    raw = pad(raw)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw))
 
 
def decrypt(enc, password):
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[16:]))

a="Work distributed"
#=== ENCRYPT ===
encrypted = encrypt(a, password)
print(encrypted)

import os.path

save_path = 'C:/Users/EGC/CloudMe/Task Scheduling/Encrypt/'

completeName = os.path.join(save_path, "enc_info.txt")         

file1 = open(completeName, "wb")

file1.write(encrypted)

file1.close()

#=== DECRYPT ===

password_dec = input("Enter password for Decryption: ")

if password==password_dec:
    decrypted = decrypt(encrypted, password)
    print(bytes.decode(decrypted))

    import os.path
    
    save_path = 'C:/Users/EGC/CloudMe/Task Scheduling/Decrypt/'
    
    completeName = os.path.join(save_path, "decrypt_info.txt")         
    
    file1 = open(completeName, "wb")
    
    file1.write(decrypted)
    
    file1.close()

else:
    print("Wrong Password!!")
    
#============================= COMPARISON GRAPH  ==============================

import matplotlib.pyplot as plt

vals=[Accuracy_rf,Accuracy_svr]
inds=range(len(vals))
labels=["RF ","SVR" ]
fig,ax = plt.subplots()
rects = ax.bar(inds, vals)
ax.set_xticks([ind for ind in inds])
ax.set_xticklabels(labels)
plt.title('Comparison graph')
plt.show()    






