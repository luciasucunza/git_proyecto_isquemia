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
pruebaRR.plotSerie()

#------------
pruebaSM = timeSerie('SlopeMax', matrixECG, SM[:,1], SM[:,0]  )
pruebaSM.plotSerie()

rectYpruebSM = pruebaSM.recorteY(25,30)
rectYpruebSM.plotSerie()

#------------
pruebaANG = timeSerie('Angle', matrixECG, ANG[:,1], ANG[:,0],  ANG[:,3], ANG[:,2], ANG[:,5], ANG[:,4] )
pruebaANG.plotSerie()

rectXpruebANG = pruebaANG.recorteX(0,20)
rectXpruebANG.plotSerie()
rectYpruebANG = rectXpruebANG.recorteY(4,5)
rectYpruebANG.plotSerie()


