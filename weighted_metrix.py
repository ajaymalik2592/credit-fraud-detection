import numpy as np
import math
import csv
import random

data = []
i = 0

with open('creditcard.csv', "rt") as filereader:
    fil = csv.reader(filereader, delimiter= ' ' )

    for rows in fil:
        i+=1
        data.append(rows)

formated_data = []
for da in data[1:]:
    # if(i == 207):
    #     break
    # i+=1
    da = da[0]
    da = da.split(",")
    data_new = []
    j = 0
    for x in da:
        j += 1
        data_new.append(float(x))
        if(j == 30):
            break
    data_new.append(int(da[-1][1]))
    formated_data.append(data_new)


rows = 240000
cols = len(formated_data[0])


""" here onward analysis part on decision tree of the project, data set in list form easy to compute """


distributed , test_sample_labels,weight = [],[0, 0], []
ending = []
for x in range(cols):
    distributed.append([0, 0])
    weight.append([0,0])
    ending.append([0,0])


weight = weight[:-1]

test_rows = 200000

for x in range(int(test_rows)):

    for y in range(cols ):
        if(y != cols-1):
            distributed[y][formated_data[x][-1]] += formated_data[x][y]
        else:
            distributed[ y ][formated_data[x] [ -1 ]t  ]  += 1

fraud = distributed[cols-1][1]
normal = distributed[cols -1][0]

mean = []
standard_deviation = []

for x in range(cols - 1):
    mean.append([0, 0])
    standard_deviation.append([0, 0])

distributed = distributed[:-1]
index = 0
for x in distributed:
    mean[index][0] = distributed[index][0] / normal
    mean[index][1 ] = distributed[index] [1] / fraud
    index += 1


for x in range(int(test_rows)):

    for y in range(cols -1):
        if(formated_data[x][-1] == 0 ):
            standard_deviation[y][0] += pow(  mean[y][0] - formated_data[x][y], 2.0)
        else:
            standard_deviation[y][1] += pow(  mean[y][1] - formated_data[x][y], 2.0)

pi = math.pi
val = math.sqrt(2 * pi)
e  = math.e

def fun(a, b, c):
    return (pow(e, - (a- b)* (a- b) / (2 * c *c)) )/ (val * c)


for x in range(cols -1):
    standard_deviation[x][0] = math.sqrt(standard_deviation[x][0] / (normal - 1 ))

    standard_deviation[x][1] = math.sqrt(standard_deviation[x][1] / ( fraud -1 ))

aa = ['normal' , 'fraud']

tp, fn , fp, tn = 0, 0, 0, 0
output = []

total = [0, 0]
for row in formated_data[:test_rows]:
    sign = row[-1]
    total[sign] += 1
    pre = [0, 0]
    for index in range(cols - 1):
        pre[0] = fun(row[index], mean[index][0], standard_deviation[index][0])
        pre[1] = fun(row[index], mean[index][1], standard_deviation[index][1])

        if(pre[sign] > pre[not sign]):
            weight[index][sign]  += 1

        ending[index][sign] += pre[sign]



for x in range(cols - 1):
    weight[x][0] /= total[0]
    weight[x][1] /= total[1]
    ending[x][1] /= total[1]
    ending[x][0] /= total[0]
    print(weight[x])

i = 0
for x in weight :
    print(i ,x[1])
    i += 1



for index in range(test_rows, len(formated_data)):
    i = 0; j = 0
    ii = 1 ; jj = 1
    for x in range(1 , cols - 2):
        i2 = fun(formated_data[index][x], mean[x][0], standard_deviation[x][0]) * weight[x][0]
        j2 = fun(formated_data[index][x], mean[x][1], standard_deviation[x][1]) * weight[x][1]
        i1 = fun(formated_data[index][x], mean[x][0], standard_deviation[x][0])
        j1 = fun(formated_data[index][x], mean[x][1], standard_deviation[x][1])
        # # if (i1 != 0 and j1 != 0):
        # i *= i1
        # j *= j1
        ii *= i2
        jj *= j2

        if(i1 >= ending[x][0]):i+=1
        if(j1 >= ending[x][1]):j+=1

    if i > j:
        if(formated_data[index][-1] == 0 ):
            tn += 1
            # output.append(1)
        else:
            if(ii > jj) :
                fp += 1;output.append(0)
            else:tn += 1;output.append(1)

    else:

        # if (formated_data[index][29] > 2126):
        #     print("i ", i, " j ", j, " ", formated_data[index][-1])
        #     if(formated_data[index][-1] == 0):
        #         tn += 1
        #     else: fp += 1
        # else:
        if(formated_data[index][-1]):
            tp += 1
            output.append(1)

        else:
            if(ii < jj):
                fn += 1
            else:
                tn += 1

print(output)
print(tp , " ", fn)
print(fp , " ", tn)
print("recall  ",  tp * 100 / (tp + fp ))
print("accuracy  " ,  (tp + tn )* 100/ (len(formated_data) - test_rows) )