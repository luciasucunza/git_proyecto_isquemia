import matplotlib.pyplot as plt
import numpy as np
import wfdb

def pick_custom_hit():
    def line_picker(line, mouseevent):
        """
        find the points within a certain distance from the mouseclick in
        data coords and attach some extra attributes, pickx and picky
        which are the data points that were picked
        """
        if mouseevent.xdata is None:
            return False, dict()
        xdata = line.get_xdata()
        ydata = line.get_ydata()
        maxd = 0.05
        d = np.sqrt(
            (xdata - mouseevent.xdata)**2 + (ydata - mouseevent.ydata)**2)

        d = np.sqrt( (xdata - mouseevent.xdata)**2 )


        ind, = np.nonzero(d <= maxd)
        if len(ind):
            pickx = xdata[ind]
            picky = ydata[ind]
            props = dict(ind=ind, pickx=pickx, picky=picky)
            return True, props
        else:
            return False, dict()

    def onpick2(event):
        print('onpick2 line:', event.pickx, event.picky)

    fig, ax = plt.subplots()
    ax.set_title('custom picker for line data')
    line, = ax.plot(time[0:1000], ecg_one_lead[0:1000],'o', picker=line_picker)
    fig.canvas.mpl_connect('pick_event', onpick2)
    
    
if __name__ == '__main__':
    pick_custom_hit()
    plt.show()
    
    
#%%
#------Apertura de la Señal y Anotaciones-------
cant_muestras = 60000                                   #cantidad de muestras

signal, fields  = wfdb.io.rdsamp( '105', pb_dir='mitdb',     sampto = cant_muestras                     )
ann             = wfdb.rdann(     '105', pb_dir='mitdb',     sampto = cant_muestras, extension = 'atr'   )

ecg_one_lead  = signal[:,0]
qrs_detections =   ann.sample
fs = fields['fs']

time            = np.arange(0, cant_muestras, 1) /fs
time_qrs        = qrs_detections / fs