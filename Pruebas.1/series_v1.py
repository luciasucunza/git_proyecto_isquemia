# Modulos importantantes
import wfdb
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
import pandas as pd


class timeSerie:
    def __init__(self, ):
            dataFrame   = pd.DataFrame( {    'Tiempo_QRS'    : ANG[:,0],
                                             'ECG'           : ANG[:,1],
                                             'IntervaloRR'   : ANG[:,1], 
                                             'PendienteMax'  : ANG[:,2], 
                                             'PendienteMin'  : ANG[:,3], 
                                             'Tiempo_PMax'   : ANG[:,4], 
                                             'Tiempo_PMin'   : ANG[:,5], 
                                             'Angulo'        : ANG[:,3], 
                                             'Tiempo_Angulo' : ANG[:,4]
                                             } )
            fields = {    'fs'  : ANG[:,0],
                      'sig_len' : ANG[:,0],    
                      'units'   : ANG[:,1]
                }
            
    def plotSerie():  
    """
    Graficar una serie con datos alrededor 
    """    
        
    def plotCombination():  
    """
    Deberìa ser capaz de graficar la combinaciòn de dos series que le pasen
    (?) serìa mejor qe directamente se llame AnguloVSRR, etc 
    """
    
    def plotInspection( df, tipo, fs, ecg):
    """
    Estos serìan los que ya hice, solo ser llamaria desde un "clic" en una plotSerie o plotCombination
    Podria ponerle los  "__" para marcar que solo se llama desde otra si me tocan un clic
    """
    
    def media():
    """
    Calcula la media de una sola serie de valores (puede llamarse desde otras funciones)
    """    
    def filter_1():
    """
    Pueden haber màs de estas funciones que permitan realizar disitnots filtrados:
            - Descartar todos los valores por fuera de un cierto intervalo (pasado por el usuario)
    """    
        
    
    