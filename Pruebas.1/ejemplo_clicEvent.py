import matplotlib.pyplot as plt
import numpy as np  
import wfdb

#def pick_custom_hit():

def line_picker(line, mouseevent):

    
    if mouseevent.xdata is None:        #Si no esta dentro del eje X devuelve flase
        return False, dict()
    xdata = line.get_xdata()            #Se guardan los valoes de la señal en ese p
    ydata = line.get_ydata()
    
    maxd = 0.002
    d = np.sqrt( (xdata - mouseevent.xdata)**2 + (ydata - mouseevent.ydata)**2)
#Ind es un numpyarray que devuelve 
#Todo esto por si tocan màs de un punto
    ind, = np.nonzero(d <= maxd)

    if len(ind):
        pickx = xdata[ind]
        picky = ydata[ind]
        props = dict(ind=ind, pickx=pickx, picky=picky)
        return True, props
    else:
        return False, dict()

def onpick(event):
    print('onpick2 line:', event.pickx, event.picky)

#    fig, ax = plt.subplots()
#    ax.set_title('custom picker for line data')
#    line, = ax.plot(rand(100), rand(100), 'o', picker=line_picker)
#    fig.canvas.mpl_connect('pick_event', onpick2)
#    
def ploteo( time, signal):
    figur = plt.figure("TITULO DE LA PESTAÑA")  
    plt.plot(time, signal, 'o', picker=line_picker)
    figur.canvas.mpl_connect('pick_event', onpick)
    plt.show()   

cant_muestras = 100
signal, fields  = wfdb.io.rdsamp( '105', pb_dir='mitdb',     sampto = cant_muestras                     )
ecg_one_lead  = signal[:,0]
fs = fields['fs']
time            = np.arange(0, cant_muestras, 1) /fs

ploteo(time,ecg_one_lead)
