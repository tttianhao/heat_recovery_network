import numpy as np
import matplotlib.pyplot as plt


Tc=304.2
Th=60+273.15
#Vc=.094
Pc=73.83
#Qh=2856.4
#^kW, also does this underaccount, because it's not pulling all heat above 60°C
CompressRatio=2
R=.08314 
a=(27/64)*R**2*Tc**2/Pc
b=(1/8)*R*Tc/Pc
Vc = (3/8)*R*Tc/Pc
#find Volumes
V1=Vc*2/(CompressRatio+1)
V2=2*V1

#Builds Volume array
V=np.linspace(V1,V2, num=1000)

#Build isotherms
Phot= R*Th/(V-b)- a/(V**2)
Pcold= R*Tc/(V-b)- a/(V**2)

#Find Carnot Efficiency
effcarnot= 1-(Tc/Th)
print('efficiency is {}'.format(effcarnot))
print('=============================')
print('graph:')
#Build Temperature array
T=np.linspace(Tc,Th, num=1000)

#builds Graph

cvr = 0.655*(8.314/44.01)
def adia(V,b,Tc,cvr,Th):
    return (V-b)*(Tc/Th)**cvr+b

T2b = np.linspace(Tc,Th,1000)
VB = [V2]
previous_vb = V2
for i in range(0,len(T2b)-1):
    previous_Tc = T2b[i]
    current_Tc = T2b[i+1]
    current_vb = adia(previous_vb,b,previous_Tc,cvr,current_Tc)
    VB.append(current_vb)
    previous_vb = current_vb

T1a = np.linspace(Th,Tc,1000)
VA = [V1]
previous_va = V1
for i in range(0,len(T1a)-1):
    previous_Tc = T1a[i]
    current_Tc = T1a[i+1]
    current_va = adia(previous_va,b,previous_Tc,cvr,current_Tc)
    VA.append(current_va)
    previous_va = current_va

P1a= [R*j/(i-b)- a/(i**2) for i,j in zip(VA,T1a)]
P2b= [R*j/(i-b)- a/(i**2) for i,j in zip(VB,T2b)]

plt.plot(np.linspace(V1,VB[-1],1000), Phot,label=r'$T_H$')
plt.plot(np.linspace(VA[-1],V2,1000), Pcold,label=r'$T_C$')
plt.plot(VA,P1a,label='Adiabatic compression')
plt.plot(VB,P2b,label='Adiabatic expension')
plt.legend()
plt.xlabel('Volume/Liters')
plt.ylabel('Pressure/Bar')
plt.title('Carnot Engine at 60°C')
plt.show()

print('=============================')
for i,j in zip(['V1','VA','V2','VB'],[V1,VA[-1],V2,VB[-1]]):
    print('{} is {}'.format(i, j))

print('=============================')
integral = 0
int1 = 0
int2 = 0
for i in range(0,len(VA)-1):
    Phot= R*Th/(VA[i]-b)- a/(VA[i]**2)
    Phot2= R*Th/(VA[i+1]-b)- a/(VA[i+1]**2)
    int1 += (Phot - P1a[i])*(VA[i+1]-VA[i])
    int2 += (Phot2 - P1a[i])*(VA[i+1]-VA[i])

integral += (int1+int2)/2
int1 = 0
int2 = 0
V = np.linspace(VA[-1],VB[-1],1000)
for i in range(0,len(V)-1):
    Phot= R*Th/(V[i]-b)- a/(V[i]**2)
    Phot2= R*Th/(V[i+1]-b)- a/(V[i+1]**2)
    Pcold= R*Tc/(V[i]-b)- a/(V[i]**2)
    Pcold2= R*Tc/(V[i+1]-b)- a/(V[i+1]**2)
    int1 += (Phot - Pcold)*(V[i+1]-V[i])
    int2 += (Phot2 - Pcold2)*(V[i+1]-V[i])
integral += (int1+int2)/2

int1 = 0
int2 = 0
VB=VB[::-1]
P2b=P2b[::-1]
for i in range(0,len(VB)-1):
    Pcold= R*Tc/(VB[i]-b)- a/(VB[i]**2)
    Pcold2= R*Tc/(VB[i+1]-b)- a/(VB[i+1]**2)
    int1 += (P2b[i] - Pcold)*(VB[i+1]-VB[i])
    int2 += (P2b[i] - Pcold2)*(VB[i+1]-VB[i])
integral += (int1+int2)/2
print('Numerical solve work is {}'.format(integral))
print('=============================')
Qhana = R*Th*np.log((VB[0]-b)/(V1-b))
print('Analytical solve QH is {}'.format(Qhana))
print('Analytical solve Work is {}'.format(Qhana*effcarnot))