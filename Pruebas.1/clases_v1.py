import pandas as pd
import wfdb
import numpy as np
#%%
class ECGClass:
    def __init__(self, num_ECG, dataBase='MIT', ti=0, tf=20000  ):
        
        self.__dataBase__ = dataBase
        
        if dataBase == 'MIT' :
            signals, fields = wfdb.io.rdsamp( num_ECG, pb_dir='mitdb', sampfrom = ti, sampto = tf)
            ann = wfdb.rdann(     num_ECG, pb_dir='mitdb', sampfrom = ti, sampto = tf, extension = 'atr'   )
            
            self.signal = signals[:,0]
            self.qrs    = ann.sample
            self.fs     = fields['fs']
            self.len    = len(self.signal)
            self.time   = np.arange( ti, tf, 1 ) / self.fs
            self.dfsignal  = pd.DataFrame({     'Signal' : self.signal,
                                                'Time'   : self.time
                                                })
        else:
            print("ERRROR: Formato Incompatible")

# Aca voy a cambiar para solo delvolver el valor de los intervalos, la ocurrencia no tiene sentido porque son los QRS, me parece
    def intervalRR (self):
        len_qrs = len(self.qrs)
        qrs = self.qrs/self.fs
        return np.hstack([  qrs[1]-qrs[0], qrs[1:len_qrs]-qrs[0:len_qrs-1]  ])

# Este lo voy a dejar igual porque el tiempo de ocurrencia si me sirve para despues poder graficar fachero
# Tendría que ver si es mejor el tiempo de ocurrencia o el offset respecto al QRS ( no es muyy importante la diferencia)
    def slopeMax (self):
        result  = np.zeros( (len(self.qrs), 2) )
        fs      = self.fs
        i = 0

        for ii in self.qrs:
            zoom_region     = np.arange(  ii-np.around(0.07*fs), ii+np.around(0.07*fs), 1, int )
            ventDerivada    =   np.diff( self.signal[ zoom_region ] ) * 0.4
            ventDerivada    =   np.hstack([ ventDerivada[0], ventDerivada ])
            result[i,:]     =   [ zoom_region[np.argmax(ventDerivada)]/fs, ventDerivada.max() *fs ]
            i = i+1

        return result
    
# Este lo voy a dejar igual porque el tiempo de ocurrencia si me sirve para despues poder graficar fachero
    def angle (self):
        result  = np.zeros( (len(self.qrs), 6) )
        i = 0
        for ii in self.qrs:

            zoom_region = np.arange( ii-np.around(0.07*self.fs), ii+np.around(0.07*self.fs), 1, int)

            ventDerivada    =   np.diff( self.signal[ zoom_region ] )
            ventDerivada    =   np.hstack([ ventDerivada[0], ventDerivada ])

            m1 = ventDerivada.max() *self.fs
            t1 = zoom_region[np.argmax(ventDerivada)]/self.fs
            b1 = self.signal[int(t1*self.fs)] - t1* m1
            m2 = ventDerivada.min() *self.fs
            t2 = zoom_region[np.argmin(ventDerivada)]/self.fs
            b2 = self.signal[int(t2*self.fs)] - t2*m2

            result[i,0] = (b2-b1)     / (m1-m2)
            result[i,1] = np.arctan( np.abs((m1-m2) / (0.4*(6.25+m1*m2))) ) *180 / np.pi

            result[i,2] = t1
            result[i,3] = m1
            result[i,4] = t2
            result[i,5] = m2

            i = i+1

        return result

#%%

ECG = ECGClass('105')

RR  = ECG.intervalRR()
ANG = ECG.angle()
SM  = ECG.slopeMax()

#plotParamECG( df_param_RR.iloc[10],"intervaloRR", ECG.fs(), ECG.ecg() )
