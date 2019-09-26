from clases_v1 import ECGClass
from series_v1 import timeSerie

#%%     PRUEBA ECGCLASS
ECG = ECGClass('105')

RR  = ECG.intervalRR()
ANG = ECG.angle()
SM  = ECG.slopeMax()


#%%     PRUEBA TIME SERIE

pruebaRR = timeSerie('IntervalRR', ECG.fs, ECG, RR, ECG.qrs/ECG.fs)
pruebaRR.plotSerieECG()

pruebaSM = timeSerie('SlopeMax', ECG.fs, ECG, SM[:,1], SM[:,0]  )
pruebaSM.plotSerieECG()

pruebaANG = timeSerie('Angle', ECG.fs, ECG, ANG[:,1], ANG[:,0],  ANG[:,3], ANG[:,2], ANG[:,5], ANG[:,4] )
pruebaANG.plotSerieECG()

