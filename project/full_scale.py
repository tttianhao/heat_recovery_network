from project import *
import numpy as np
import matplotlib.pyplot as plt
capital = []
Qhotlist = []
for i in np.linspace(10,40,201):
    stream.deltaTmin=i
    column.deltaTmin=i
    #print(i)
    stream_1 = stream(24.4,35.5,450,1)
    stream_2 = stream(24.4,450,40,2)
    stream_3 = stream(12.3,40,75,3)
    stream_4 = stream(5.2,35.5,20,4)
    stream_5 = stream(6.6,104.5,70,5)
    stream_6 = stream(11.5,129.9,80,6)
    stream_7 = stream(32.6,183.2,80,7)
    stream_8 = stream(1.2,249.3,25,8)
    stream_9 = stream(1.1,80,25,9)
    stream_10 = stream(4,70,35,10)
    streams=[stream_1,stream_2,stream_3,stream_4,stream_5,stream_6,stream_7,stream_8,stream_9,stream_10]
    column_1 = column(129.9,35.5,950,357,1)
    column_2 = column(150.3,104.5,2865,1868,2)
    column_3 = column(249.3,183.2,28320,25527,3)
    columns = [column_1,column_2,column_3]
    Qhot = main(streams,columns)
    Qhotlist.append(Qhot)
    capital.append(12.5*10**6/i**0.05)
    #plt.plot(i,12.5*10**6/i**0.05,'ro')
annual = [i*0.15*24*300 for i in Qhotlist]
total = []
for i,j in zip(annual, capital):
    total.append(i+j)
print(total.index(min(total)))
print(np.linspace(10,40,201)[69])
plt.figure('total cost vs Tmin')
plt.plot(np.linspace(10,40,201), total,'o')
plt.title(r'total cost vs. $\Delta T_{min}$ for full-scale plant')
plt.xlabel(r'$\Delta T_{min}$ K')
plt.ylabel(r'total cost ')
plt.show()