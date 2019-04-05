#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 11:03:40 2019

@author: luciasucunza
"""

import pandas as pd
import wfdb
import matplotlib.pyplot as plt
import numpy as np


class ECGClase:
    def __init__(self, num_ECG, dataBase='MIT', ti=0, tf=20000  ):
        if dataBase == 'MIT' : 
            signals, fields = wfdb.io.rdsamp( num_ECG, pb_dir='mitdb', sampfrom = ti, sampto = tf)
            datos = {   'Signal' : signals[:,0],
                        'Time'   : np.arange( ti, tf, 1 ) / fields.get('fs')
                    }
            self.df_signal  = pd.DataFrame( datos )             

        else:
            print("ERRROR: Formato Incompatible")
            
#    def plot(self, ti=self.df_signal.loc[0,'Time'], tf=self.df_signal.index.max() ):
        #Algo para tomar el ultimo valor de la serie

#Tomar desde una cierta posicion del index  a otra, por ejemplo de 0 a50s
#Capaz lo mejor es que el tiempo sea una columna nueva 
#NO puedo tomar una parte del dataFrame diciendole anda de este valor de indeice a este        
        


ECG = ECGClase('101')
plt.grid()
plt.plot( ECG.df_signal.loc[:,'Time'], ECG.df_signal.loc[:,'Signal'] )

ECG2 = ECGClase('101', 'M', ti = 10000, tf = 50000)

ECG.df_signal.mean()
ECG2.df_signal.mean()


