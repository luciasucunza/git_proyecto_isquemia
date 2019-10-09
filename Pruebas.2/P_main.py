from ecg_class import ECGClass
from series_v2 import timeSerie
import numpy as np

#%%     PRUEBA ECGCLASS
ECG = ECGClass('105')

RR  = ECG.intervalRR()
ANG = ECG.angle()
SM  = ECG.slopeMax()


#%%     PRUEBA TIME SERIE

matrixECG = np.column_stack((ECG.time, ECG.signal)) 

#------------
pruebaRR = timeSerie('IntervalRR', matrixECG, RR, ECG.qrs/ECG.fs)
pruebaRR.recorteX(0,20)
pruebaRR.recorteY(0.6,0.9)
pruebaRR.plotSerie()

#------------
pruebaSM = timeSerie('SlopeMax', matrixECG, SM[:,1], SM[:,0]  )
pruebaSM.plotSerie()

pruebaSM.recorteY(25,30)
pruebaSM.plotSerie()

#------------
pruebaANG = timeSerie('Angle', matrixECG, ANG[:,1], ANG[:,0],  ANG[:,3], ANG[:,2], ANG[:,5], ANG[:,4] )

pruebaANG.recorteX(0,20)
pruebaANG.recorteY(4,60)
pruebaANG.plotSerie()