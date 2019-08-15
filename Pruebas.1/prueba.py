import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
import scipy.signal as sig

#%%
#------Apertura de la Señal-------
mat_struct = sio.loadmat('/home/luciasucunza/git_proyecto_isquemia/TP4_ecg.mat')

ecg_one_lead    = mat_struct['ecg_lead'].flatten()
qrs_detections  = mat_struct['qrs_detections'].flatten()
cant_muestras   = len(ecg_one_lead)
fs              = 1000 #Hz

time            = np.arange(0, cant_muestras, 1) /fs
time_qrs        = qrs_detections / fs


qrs = qrs_detections/fs
ecg = ecg_one_lead

ii = qrs[2]
zoom_region = np.arange( int((ii-0.4)*fs), int((ii+0.6)*fs), 1)

x = np.array( ecg[ zoom_region ], dtype = float )

    
ventDerivada_diff   =   np.diff( ecg[ zoom_region ] ) 
ventDerivada_diff   =   np.hstack([ ventDerivada_diff[0], ventDerivada_diff])     
ventDerivada_lfil   =   sig.lfilter( [1,0,-1], [1],  x)

#Ploteo
plt.figure('Pendiente')
plt.cla()
plt.plot( zoom_region/fs,   ecg[zoom_region]                                )
plt.plot( np.array([ii,ii]),          np.array([0, ecg[int(ii*fs)]]                ) )
plt.plot( zoom_region/fs,   ventDerivada_diff,  label=('Pendiente con Diff'     ) )
plt.plot( zoom_region/fs,   ventDerivada_lfil,  label=('Pendiente con lfilter'  ) )
plt.plot( zoom_region[np.argmax(ventDerivada_diff)]/fs , ventDerivada_diff.max(),'ro' )
plt.plot( zoom_region[np.argmax(ventDerivada_lfil)]/fs , ventDerivada_lfil.max(),'ro' )
plt.xlabel('time (s)')   
plt.ylabel('amplitude (mV)')           
plt.grid()
plt.legend()
plt.show()  



