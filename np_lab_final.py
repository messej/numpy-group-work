#np lab
#Group Members: Britani Prescott, Jesse Hankins, Jesse Raines,
#               Kearsten Collins, Liu Yu, Sipei Chen, Vince Kovich
import numpy as np
"""
#totally should have used this
class DurationSummary:
    def __init__(self, data, start_date, end_date, partition_size):
        self.full_data = data
        self.data = self.set_data(data, start_date, end_date)
        self.partitions = self.set_partitions(partition_size)
    def set_data(self, data, start_date, end_date):
        pass
    def set_partitions(self, partition_size):
        pass
    def summary(self):
        print("Everything!")
    def Q1_2_3(self):
        print('Highest daily gain: ')
        print('Highest daily loss: ')
        print('Highest daily volume: ')
    def repartition(self, start_date, end_date, partition_size):
        self.data = self.set_data(self.full_data, start_date, end_date)
        self.partitions = self.set_partitions(partition_size)
"""
        

def read_date(val):
    val = val.split(sep='-')
    return val        

def read_prices(csvfile):
    with open(csvfile) as infile:
        header = infile.readline().strip().split(sep=',')
        h = {key:val for key , val in zip(header, range(2,len(header)+2))}
        h['Year'], h['Month'], h['Day'],  = range(3)
        full = infile.readlines()
        times = []
        for i in range(len(full)):
            full[i] = full[i].strip().split(sep=',')
            times.append(full[i][0])
            full[i][:1] = read_date(full[i][0])
        return h, times, full

def gain_loss_column(data, dict_indices): #appends a column of gain/loss for each row
    new_list = []
    for line in range(len(data)):
        new_list.append(data[line][dict_indices['Close']] - data[line][dict_indices['Open']])
    dict_indices['Gain or Loss'] = 9
    return np.append(data.T, [new_list], axis = 0).T
#########################################################################################
#Example full path: csvfn = r"D:\programs\data\SP500.csv"
csvfn = r"SP500.csv"
h, tt, full = read_prices(csvfn)
stuff = np.array(full, dtype='float')
times = np.array(tt, dtype='datetime64')
stuff = gain_loss_column(stuff, h) 

def all_between(data, times, start, end):
    return data[(times>=start) & (times<end)]

def make_time(year, month, day):
    return np.datetime64(f'{int(year)}-{int(month):02d}-{int(day):02d}')

def add_time(date, Year, Month, *args):
    new_year = int(str(date).split(sep = '-')[0]) + Year
    month = int(str(date).split(sep = '-')[1]) + Month
    new_month = (month-1)%12 + 1
    new_year += (month-1)//12
    return np.datetime64(f'{new_year}-{new_month:02d}-01')

def delta_to_int(delta): 
    #Converts time delta to a number representing number of days
    return int(str(delta).split()[0])

months = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun',
          7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}


# QUESTION 1:
print("\nQUESTION 1:============================================================")
max_col_values = np.amax(stuff, axis = 0)
maximum_GoL = tuple()
min_col_values = np.amin(stuff, axis = 0)
"""
max_info = stuff[stuff[:,9]==max_col_values[9]].flatten()
vol_info = stuff[stuff[:,8]==max_col_values[8]].flatten()
min_info = stuff[stuff[:,9]==min_col_values[9]].flatten()
"""
max_info = stuff[ stuff[:,h['Gain or Loss']] == max_col_values[h['Gain or Loss']] ].flatten()
vol_info = stuff[ stuff[:,h['Volume']]       == max_col_values[h['Volume']]       ].flatten()
min_info = stuff[ stuff[:,h['Gain or Loss']] == min_col_values[h['Gain or Loss']] ].flatten()

def Q1(vals, kind):
    print(f"{int(vals[h['Year']])}-{int(vals[h['Month']]):02d}-{int(vals[h['Day']]):02d}",
             ": ", kind, ": ", f"{vals[h[kind]]}")

Q1(max_info, "Gain or Loss")
Q1(min_info, "Gain or Loss")

# QUESTION 2:
print("\nQUESTION 2:============================================================")
Q1(vol_info, "Volume")

# QUESTION 3:
print("\nQUESTION 3:============================================================")
Q3set = stuff[times>=np.datetime64('2017-01-01')]
def partition(data, times, start_date, end_date, partition_size, L = []):
    #partitions subset of data
    #subset range is [start_date, end_date)
    #partition_size is a tuple (Year, Month)
    date_step = delta_to_int(add_time(start_date, *partition_size) - start_date)
    total_time = delta_to_int(end_date - start_date)
    num_parts = int(np.ceil(total_time/date_step))
    L = np.full((num_parts,date_step,10), np.NaN)
    for i in range(num_parts):
        next_date = add_time(start_date, *partition_size)
        part = all_between(data, times, start_date, next_date)
        L[i][:part.shape[0], :part.shape[1]] = part
        start_date = next_date
    return L
st = np.datetime64('2017-01-01')
en = np.datetime64('2019-01-01')
Q3 = partition(stuff, times, st, en, (0,1))
#ex = Q3[0].mean(axis=0)
def report(data, pos):
    #generates report for the pos'th partition of data
    sum_part_col = np.nansum(data, axis = 1)
    part_GoL = list(sum_part_col[:,h['Gain or Loss']])
    max_GoL = max(part_GoL)
    max_pos = part_GoL.index(max_GoL)
    
    vals = np.nanmean(data[pos],axis = 0)
    
    #data = data[~np.isnan(data[:,0,0]),~np.isnan(data[0,:,0]),~np.isnan(data[0,0,:])]
    data = data[~np.isnan(data[:,0,0]),:,:]
    data = data[:,~np.isnan(data[0,:,0]),:]
    #print(data[:,:,:3])
    
    
    d1 = make_time(*data[pos,0,:3])
    d2 = make_time(*data[pos,data.shape[1]-1,:3])
    
    d3 = make_time(*data[max_pos,0,:3])
    d4 = make_time(*data[max_pos,data.shape[1]-1,:3])
    print("Example report for", d1, "to", d2)
    print(f"""\tAverage Open:       {vals[h['Open']]:f}
        Average Close:      {vals[h['Close']]:f}
        Average Volume:     {vals[h['Volume']]:e}
        Average Gain/Loss:  {vals[h['Gain or Loss']]:f}
        Most Profitable:    [{d3:} to {d4:}]: {max_GoL}\n""")
report(Q3,0)
#print(Q3[0])
#print(len(Q3))
def query(data, high, low):
    data = data[~np.isnan(data[:,0,0]),:,:]
    data = data[:,~np.isnan(data[0,:,0]),:]
    x = data[(low < data[:,0,h['Open']])&(data[:,0,h['Open']] < high)]
    print("Months that open between", high, "and", low, "\n [YYYY,   MM]")
    print(x[:,0,:2])
query(Q3,2650,2620)
# QUESTION 4:
print("\nQUESTION 4:============================================================")
st = np.datetime64('1950-01-01')
en = np.datetime64('2019-01-01')
Q4 = partition(stuff, times, st, en, (1,0))
report(Q4,0)


# QUESTION 5:
print("\nQUESTION 5:============================================================")

st = np.datetime64('1950-01-01')
en = np.datetime64('2019-01-01')
Q5 = partition(stuff, times, st, en, (5,0))
report(Q5,0)



