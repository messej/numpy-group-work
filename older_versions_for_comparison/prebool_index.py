#np lab
import numpy as np
import csv
from datetime import datetime

def read_date(val):
    val = val.split(sep='-')
    return val


def read_prices(csvfile, _strptime=datetime.strptime):
    with open(csvfile) as infile:
        header = infile.readline().strip().split(sep=',')
        h = {key:val for key , val in zip(header, range(2,len(header)+2))}
        h['Year'], h['Month'], h['Day'],  = range(3)
        full = infile.readlines()
        for i in range(len(full)):
            full[i] = full[i].strip().split(sep=',')
            full[i][:1] = read_date(full[i][0])
        return h, full

def gain_loss_column(data, dict_indices): #appends a column of gain/loss for each row
    new_list = []
    for line in range(len(data)):
        new_list.append(data[line][dict_indices['Close']] - data[line][dict_indices['Open']])
    dict_indices['GoL'] = 9
    return np.append(data.T, [new_list], axis = 0).T

csvfn = r"C:\Users\jesse\Documents\Into Data Analytics\SP500.csv"
h, full = read_prices(csvfn)
stuff = np.array(full, dtype='float')
stuff = gain_loss_column(stuff, h) 

# QUESTION 1:
print("QUESTION 1:============================================================")
max_col_values = np.amax(stuff, axis = 0)
maximum_GoL = tuple()
min_col_values = np.amin(stuff, axis = 0)
minimum_GoL = tuple()
maximum_vol = tuple()

partition_index = 0
partition_bool = False

for value in range(len(stuff)):
    if stuff[value][h['GoL']] == max_col_values[9]: # finds max gain and date
        maximum_GoL = (stuff[value][h['Year']],
                   stuff[value][h['Month']],
                   stuff[value][h['Day']],
                   stuff[value][h['GoL']])
    if stuff[value][h['GoL']] == min_col_values[9]: # finds max loss and date
        minimum_GoL = (stuff[value][h['Year']],
                   stuff[value][h['Month']],
                   stuff[value][h['Day']],
                   stuff[value][h['GoL']])
    if stuff[value][h['Volume']] == max_col_values[8]: # finds max volume and date
        maximum_vol = (stuff[value][h['Year']],
                   stuff[value][h['Month']],
                   stuff[value][h['Day']],
                   stuff[value][h['Volume']])
    if (stuff[value][h['Year']] == 2017) and (not partition_bool): # finds index of first occurrence of 2017
        partition_index = value
        partition_bool = not partition_bool
        

print(maximum_GoL)
print(minimum_GoL)

# QUESTION 2:
print("\nQUESTION 2:============================================================")
print(maximum_vol)

# QUESTION 3:
print("\nQUESTION 3:============================================================")
def monthly_avg(data, dict_indices):
    new_list = np.zeros((24, 10))
    new_index = 0
    counter = 0
    for item in range(len(data)):
        if data[item][dict_indices['Month']] == data[(item + 1) % len(data)][dict_indices['Month']]:
            counter += 1
            new_list[new_index] = new_list[new_index] + data[item]
        else:
            new_list[new_index] = new_list[new_index]/counter
            counter = 0
            new_index += 1
    return new_list
            
def monthly_avg_query(data, dict_indices, start_range, stop_range):
    new_list = np.zeros((24, 2))
    new_index = 0
    found = False
    month = data[0][dict_indices['Month']]
    for item in range(len(data)):
        value = data[item][dict_indices['Open']]
        if value >= start_range and value <= stop_range and not found:
            new_list[new_index][0], new_list[new_index][1] = data[item][dict_indices['Year']], data[item][dict_indices['Month']]
            new_index += 1
            month = data[item][dict_indices['Month']]
            found = not found
        elif month != data[item][dict_indices['Month']]:
            found = not found            
    return new_list    
    
partition = stuff[partition_index:,:]
monthly_avg_report = monthly_avg(partition, h)
print(monthly_avg_report)

monthly_query = monthly_avg_query(partition, h, 2630, 2640)
print(monthly_query)

# QUESTION 4:
print("\nQUESTION 4:============================================================")
def annual_avg(data, dict_indices):
    new_list = np.zeros((70, 10))
    new_index = 0
    counter = 0
    best_year = 0
    best_value = 0
    for item in range(len(data)):
        if data[item][dict_indices['Year']] == data[(item + 1) % len(data)][dict_indices['Year']]:
            counter += 1
            new_list[new_index] = new_list[new_index] + data[item]
        else:
            best_year = new_list[new_index][0]/counter if best_value < new_list[new_index][9]else best_year
            best_value = max(best_value, new_list[new_index][9])
            new_list[new_index] = new_list[new_index]/counter
            counter = 0
            new_index += 1
    return new_list, best_year

annual_avg_report, best_yearly = annual_avg(stuff, h)
print(annual_avg_report)
print(best_yearly)

# QUESTION 5:
print("\nQUESTION 5:============================================================")
def annual_avg(data, dict_indices):
    new_list = np.zeros((14, 10))
    new_index = 0
    counter = 0
    best_year = 0
    best_value = 0
    current_year = data[0][dict_indices['Year']] + 5
    for item in range(len(data)):
        if data[item][dict_indices['Year']] < current_year:
            counter += 1
            new_list[new_index] = new_list[new_index] + data[item]
        else:
            best_year = current_year - 5 if best_value < new_list[new_index][9] else best_year
            best_value = max(best_value, new_list[new_index][9])
            new_list[new_index] = new_list[new_index]/counter
            new_list[new_index][0] = current_year - 5 # this is the starting year for the timeframe. 
            counter = 0
            new_index += 1
            current_year += 5
    new_list[new_index][0] = current_year - 5
    return new_list, best_year

five_year_avg_report, best_five_yearly = annual_avg(stuff, h)
print(five_year_avg_report)
print(best_five_yearly)



















