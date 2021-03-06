import numpy as np
import matplotlib.pyplot as plt 

class stream:
    """
    This class is the stream class. It holds the properties as as Tin, Tout, CP, index, Sin, Sout and type
    """

    #This is Delta Tmin=10
    deltaTmin = 10
    numberOfStream = 0

    #initialize properties of the streams: CP, Tin, Tout, Sin, Sout and label stream number
    def __init__(self,CP,actualTin,actualTout,number):
        
        """
        initialize the stream properties

        args:
            CP: sepcific heat capacity, float
            ActuallTin: inlet temperature, float
            actualTout: outlet temperature, float
            number: index of the stream, int
        """
        stream.numberOfStream += 1
        self.Tin = actualTin
        self.Tout = actualTout
        self.CP = CP
        self.number = number

        #Check if the stream is hot or cold
        if actualTin < actualTout:
            self.Sin = actualTin + self.deltaTmin / 2
            self.Sout = actualTout + self.deltaTmin / 2
            self.type = "cold"
        else:
            self.Sin = actualTin - self.deltaTmin / 2
            self.Sout = actualTout - self.deltaTmin / 2
            self.type = "hot"

class column:
    '''
    This class is the column class, It holds the properties of columns
    '''
    deltaTmin = 10
    def __init__(self,Treb,Tcond,Qreb,Qcond,number):
        self.Treb = Treb
        self.Tcond = Tcond
        self.number = number
        self.Sreb = Treb+self.deltaTmin/2
        self.Scond = Tcond -self.deltaTmin/2
        self.Qreb = Qreb
        self.Qcond = Qcond


def calculate_shifted_temperature_interval(streams):

    '''
    This function calculate the shifted temperture interval from the shifted inlet and out temperature.

    Args:
        streams: a list of class instant variable, list

    returns:
        returns shifted temperature interval, list
    '''

    temperature_interval = []
    for i in streams:
        if i.Sin not in temperature_interval:
            temperature_interval.append(i.Sin)
        if i.Sout not in temperature_interval:
            temperature_interval.append(i.Sout)
    temperature_interval = sorted(temperature_interval)[::-1]
    return temperature_interval

def caclulate_temperature_difference(temperature_interval):
    '''
    This function calculates the shifted temperature difference in each interval

    Args:
        temperature_interval: a list of shifted temperatuer

    Returns:
        list of temperature difference
    '''

    temperature_difference = []
    for i in np.arange(len(temperature_interval)-1):
        temperature_difference.append(temperature_interval[i]-temperature_interval[i+1])
    return(temperature_difference)

def does_interval_contain(coldorhot,interval_upper_bound,interval_lower_bound,Streamin,Streamout):
    '''
    This function checks if a certain stream occurs in a certain temperature interval

    Args:
        coldorhot: string, distinguish if a stream is hot or cold
        interval_upper_bound, interval_lower_bound: interval edges
        Streamin, Streamout: the inlet and outlet shifted temperatuer
    
    Returns:
        boolean, true if stream is part of the interval and false if not
    '''

    if coldorhot == 'hot':
        if Streamin >= interval_upper_bound and Streamout <= interval_lower_bound:
            return True
        else:
            return False
    if coldorhot == 'cold':
        if Streamout >= interval_upper_bound and Streamin <= interval_lower_bound:
            return True
        else:
            return False

def calculate_deltaCP(DeltaCP,streams,temperature_interval):
    '''
    This function calculate the CPhot - CPcold in each temperature difference

    Args:
        DeltaCP: list of CPH-CPC
        streams: list of instantce class variable
        temperature_interval: list of shifted temperature

    returns:
        DeltaCP
    '''

    for i in np.arange(len(temperature_interval)-1):
        currentCP = 0
        for j in streams:
            if does_interval_contain(j.type,temperature_interval[i],temperature_interval[i+1],j.Sin,j.Sout):
                if j.type == 'hot':
                    currentCP += j.CP
                if j.type == 'cold':
                    currentCP -= j.CP
            DeltaCP[i] = currentCP
    return DeltaCP

def calculate_heat_cascades(DeltaH):
    '''
    This function calculate the heat cascade before any adjustment

    Args:
        DeltaH: CPH-CPC, list
    
    returns:
        heat_cacade: list of heat at each shifted temperatuer, list
    '''

    heat_cascade = np.zeros(len(DeltaH)+1)
    for i in np.arange(len(heat_cascade)):
        for j in range(0,i):
            heat_cascade[i] += DeltaH[j]
    return heat_cascade

def adjust_heat_cascades(heat_cascade,temperature_interval):
    '''
    This function adjust the raw heat cascades and make sure all numbers are equal or bigger than zero.

    Args:
        heat_cascade: list
        temperature_interval: list
    return:
        Tpinch,Qpinch,Qhot,Qcold
    '''
    Qpinch = 0
    for i in np.arange(len(heat_cascade)):
        if heat_cascade[i] < 0:
            currentQ = -heat_cascade[i]
            Tpinch = temperature_interval[i]
            Qpinch += currentQ
            heat_cascade += currentQ
            currentQ = 0
    Qhot = heat_cascade[0]
    Qcold = heat_cascade[-1]
    return Tpinch,Qhot,Qcold

def grand_compositive_curve(heat,temperature):
    '''
    This function plot the grand compositive curve based on the heat casscatte and temperature
    '''
    plt.figure(figsize=(10,6))
    for i in range(len(heat)-1):
        plt.plot([heat[i],heat[i+1]],[temperature[i],temperature[i+1]],color = 'blue')
        #plt.plot([0,heat[i]],[temperature[i],temperature[i]],'r:')
    #plt.plot([0,heat[-1]],[temperature[-1],temperature[-1]],'r:')
    plt.xlim(0,max(heat))
    #plt.yticks(temperature)
    plt.title('Grand Compositive Curve')    

def insert_Q(i,temperature_interval,deltaH,rc,Q):
    try:
        temperature_interval.append(rc)
    except:
        temperature_interval = np.append(temperature_interval,rc)
    temperature_interval = sorted(temperature_interval,reverse=True)
    indexSreb = temperature_interval.index(rc)
    ratioUp = (temperature_interval[indexSreb-1]-rc)/(temperature_interval[indexSreb-1]-temperature_interval[indexSreb+1])
    ratioDown = -(temperature_interval[indexSreb+1]-rc)/(temperature_interval[indexSreb-1]-temperature_interval[indexSreb+1])
    indexDeltaH = indexSreb-1
    temperature_interval.insert(indexSreb,rc)
    deltaHUp = deltaH[indexDeltaH]*ratioUp
    deltaHDown = deltaH[indexDeltaH]*ratioDown
    deltaH = np.insert(deltaH,indexDeltaH,deltaHUp)
    deltaH = np.insert(deltaH,indexDeltaH+1,Q)
    deltaH = np.insert(deltaH,indexDeltaH+2,deltaHDown)
    deltaH = np.delete(deltaH,indexDeltaH+3)
    return temperature_interval,deltaH

def integrate_column(column,temperature_interval,deltaH):
    newTemperatureInt = temperature_interval
    newDeltaH = deltaH
    for i in column:
        if i.Sreb not in newTemperatureInt:
            # if i.Sreb < max(temperature_interval) and i.Sreb > min(temperature_interval):
            newTemperatureInt,newDeltaH = insert_Q(i,newTemperatureInt,newDeltaH,i.Sreb,-i.Qreb)
        else:
            index = temperature_interval.index(i.Sreb)
            newTemperatureInt = np.insert(temperature_interval,index,i.Sreb)
            newDeltaH = np.insert(deltaH,index,-i.Qreb)
        if i.Scond not in temperature_interval:
            newTemperatureInt,newDeltaH = insert_Q(i,newTemperatureInt,newDeltaH,i.Scond,i.Qcond)
        else:
            for j in range(len(newTemperatureInt)):
                if newTemperatureInt[j] == i.Scond:
                    index = j
                    break
            newTemperatureInt = np.insert(newTemperatureInt,index,i.Scond)
            newDeltaH = np.insert(newDeltaH,index,i.Qcond)
    return newTemperatureInt,newDeltaH

def main(streams,columns):
    '''
    The main function, change value here

    input stream in the order of stream(CP,Tin,Tout,index)
    '''
    temperatureInterval = calculate_shifted_temperature_interval(streams)
    #print('The shfited temperature interval is {}'.format(temperatureInterval))
    temperatureDifference = caclulate_temperature_difference(temperatureInterval)
    #print('The temperatuer difference is {}'.format(temperatureDifference))
    #initialize deltaCp and deltaH
    deltaCP = np.zeros(len(temperatureDifference))
    deltaH = np.zeros(len(temperatureDifference))
    deltaCP = calculate_deltaCP(deltaCP,streams,temperatureInterval)
    #print('The delta CP is {} '.format(deltaCP))
    for i in np.arange(len(deltaH)):
        deltaH[i] = (deltaCP[i]*temperatureDifference[i])
    #print('The deltaH is {}'.format(deltaH))
    #initialize heat cascades
    heatCascades = calculate_heat_cascades(deltaH)
    #print('The initial heat cascade is {}'.format(heatCascades))
    Tpinch,Qhot,Qcold = adjust_heat_cascades(heatCascades,temperatureInterval)
    #print('The adjusted heat cascade is {}'.format(heatCascades))
    print('Tpinch is {:.4g}C, Qhot is {:.4g}kw and Qcold is {:.4g}kw.'.format(Tpinch,Qhot,Qcold))
    #grand_compositive_curve(heatCascades,temperatureInterval)
    file = open('Heat_cascade.txt','w+')
    file.write('Temperature  deltaH  final_hc \n')
    file.write('{:8.4g}               {:5.4g}\n'.format(temperatureInterval[0],heatCascades[0]))
    for i in np.arange(0,len(temperatureInterval)-1):
        file.write('            {:6.4g}\n'.format(deltaH[i]))
        file.write('{:8.4g}               {:5.4g}\n'.format(temperatureInterval[i+1],heatCascades[i+1]))
    print('==============================')
    if columns != None:
        newTemperatureInt,newDeltaH = integrate_column(columns,temperatureInterval,deltaH)
        #print('The integrated column temperature interval is: {}'.format(newTemperatureInt))
        #print('The new delta H is: {}'.format(newDeltaH))
        newHeatCascades = calculate_heat_cascades(newDeltaH)
        #print('new HeatCascades is: {}'.format(newHeatCascades))
        newTpinch,newQhot,newQcold = adjust_heat_cascades(newHeatCascades,newTemperatureInt)
        #print('The adjusted heat cascade is {}'.format(newHeatCascades))
        print('Tpinch is {}C, Qhot is {}kw and Qcold is {}kw.'.format(newTpinch,newQhot,newQcold))
        #grand_compositive_curve(newHeatCascades,newTemperatureInt)
        #plt.show()
    #     file.write(' = = = = = = = = = = = = = = = = = \n')
    #     file.write('Temperature  deltaH  final_hc \n')
    #     file.write('{:8.4g}               {:5.4g}\n'.format(newTemperatureInt[0],newHeatCascades[0]))
    #     for i in np.arange(0,len(newTemperatureInt)-1):
    #         file.write('            {:6.4g}\n'.format(newDeltaH[i]))
    #         file.write('{:8.4g}               {:5.4g}\n'.format(newTemperatureInt[i+1],newHeatCascades[i+1]))
    # file.close()
    return newQhot


if __name__ == "__main__":
    stream.deltaTmin=10
    column.deltaTmin=10
    # stream_1 = stream(2,20,135,1)
    # stream_2 = stream(3,170,60,2)
    # stream_3 = stream(4,80,140,3)
    # stream_4 = stream(1.5,150,30,4)
    # column_1 = column(150,140,20,1)
    # stream_1 = stream(2,20,140,1)
    # stream_2 = stream(3,200,80,2)
    # stream_3 = stream(4,60,140,3)
    # stream_4 = stream(1.5,160,30,4)
    # column_1 = column(160,80,60,1)

    stream_1 = stream(2.44,35.5,450,1)
    stream_2 = stream(2.44,450,40,2)
    stream_3 = stream(1.23,40,75,3)
    stream_4 = stream(.52,35.5,20,4)
    stream_5 = stream(.66,104.5,70,5)
    stream_6 = stream(1.15,129.9,80,6)
    stream_7 = stream(3.26,183.2,80,7)
    stream_8 = stream(.12,249.3,25,8)
    stream_9 = stream(.11,80,25,9)
    stream_10 = stream(0.4,70,35,10)
    stream_11 = stream(4.47, 25, 100, 11)
    stream_12 = stream(2.13, 100, 120, 12)
    streams=[stream_1,stream_2,stream_3,stream_4,stream_5,stream_6,stream_7,stream_8,stream_9,stream_10,stream_11,stream_12]
    column_1 = column(129.9,35.5,95,35.7,1)
    column_2 = column(150.3,104.5,286.5,186.8,2)
    column_3 = column(249.3,183.2,2832,2552.7,3)
    column_4 = column(100, 100, 2406.9,0,4)
    columns = [column_1,column_2,column_3,column_4]
    main(streams,columns)
 