# Modulos importantantes
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
##
"""
            ALGUNA FORMA DE PONER POR EJEMPLO UNITIS["ANGLE"] Y ME DEVUELVA "º", ASÍ CON LAS 3
            
            
            En todas las gráficas se pueden hacer mejoras, para mostrar más datos
"""
##
def buscar( A, Cx, Xi, Ci):
    """
    ¡¡¡¡¡¡¡¡¡¡¡¡¡¡POSIBLEMENTE ESTO YA EXISTA!!!!!!!!!!!!!!
    
    El valor de la matriz "A" que esta en la columna "Cx" y la fila que corresponda al valor "Xi" de la columna "Ci"
    """
    j = 0
    for i in A[:,Ci]:
        if i == Xi:
            return A[j,Cx]
        else:
            j = j+1
def devolverVector( A, Cx, Xi, Xd, Ci):
    """
    ¡¡¡¡¡¡¡¡¡¡¡¡¡¡POSIBLEMENTE ESTO YA EXISTA!!!!!!!!!!!!!!
    
    Devuleve un vector de la columna "Cx" de la matriz "A" que vaya de la fila que corresponda al valor Xi de la columna "Ci" hasta la fila que corresponda al valor Xf de la columna "Ci" 
    """
    j = 0
    for i in A[:,Ci]:
        if i == Xi:
            break
        else:
            j = j+1
    
    for i in A[:,Ci]:
        aux = 
        if i == Xf:
            break
        else:
            j = j+1
    

def picker_handler( line, mouseevent):
    """
    Tendrìa que ver dos cosas:          - Ahora si toca dos puntos agarra el primero arbitrariamente (MENU)
                                        - El valor de maxd es funcion de dt que es igual en todos los parametros que grafico ahora, PUEDE QUE EN ALGUN MOMENTO JODA 
    """

    if mouseevent.xdata is None:        
        return False, dict()
    
    xdata = line.get_xdata()           
    ydata = line.get_ydata()    
    maxd = 0.3
    d = abs(xdata - mouseevent.xdata)
#    d = np.sqrt( (xdata - mouseevent.xdata)**2 + (ydata - mouseevent.ydata)**2 )
    
    #Si se seleccionan dos puntos arbitrariamente me quedo con uno de los dos
    #Aca podrìa hacer distintas cosas como:     -NINGUNO    -MENU PARA ELEGIR CUAL
    ind, = np.nonzero(d <= maxd)
    if len(ind):
        pickx = xdata[ind[0]]
        picky = ydata[ind[0]]
        props = dict(ind=ind, pickx=pickx, picky=picky)
        return True, props
    else:
        return False, dict()

    
class timeSerie:
    """
    TYPE PARAM TIENE QUE SER O "Angle" "SlopeMax" "IntervalRR",  "Filt" "Resampled" "Median"
    Para el angulo primero se pasa la màxima y despues la minima
    
    Tendría que ver la mejor forma de tratar el None o chequear que las cosas sean strings o ese tipo de cosas
    """
    def __init__(self,  typeParam   = None, 
                        origin      = None,           
                        param       = None,      t_param = None, 
                        param_aux1  = None,      t_param_aux1 = None, 
                        param_aux2  = None,      t_param_aux2 = None  
                 ):
        
#        if typeParam is None: 
        self.type       = typeParam
        self.__origin__ = origin
        self.dataFrame  = pd.DataFrame({   'Time'      : t_param,
                                             typeParam  : param
                                             })
    
        if typeParam == 'Angle':
            self.units                      = "º"
            self.dataFrame['SlopeMax']      = param_aux1
            self.dataFrame['TimeSlopeMax']  = t_param_aux1   
            self.dataFrame['SlopeMin']      = param_aux2
            self.dataFrame['TimeSlopeMin']  = t_param_aux2   
            
        elif typeParam == 'IntervalRR':
            self.units    = "s"
            
        elif typeParam == 'SlopeMax':
            self.dataFrame['TimeSlopeMax']  = t_param_aux1  
            self.units    = "mm/mm"
          
        
    """
    Grafica la serie
    """
    def plotSerie(self):
        fig = plt.figure( 'TimeSerie: ' + self.type + ' plot')
        plt.cla()
        plt.plot( self.dataFrame['Time'],  self.dataFrame[ self.type ], 'go', picker=picker_handler)
        fig.canvas.mpl_connect('pick_event',  self.__plotInspection__)
        plt.grid()
        
    """
    Grafica la serie y la serie que le dio origen
    """
    def plotSerieVsOrig( self ): 
        if isinstance(self.__origin__, np.ndarray):
            fig = plt.figure( 'TimeSerie: ' + self.type + ' vs Origin')
            plt.cla()
            
            ax1 = plt.subplot(211)
            plt.plot( self.__origin__[:,0],  self.__origin__[:,1])
            plt.setp(ax1.get_xticklabels(), fontsize=6)
            plt.grid()
            
            ax2 = plt.subplot(212, sharex=ax1)
            plt.plot( self.dataFrame['Time'],  self.dataFrame[ self.type ], 'go', picker=picker_handler)
            plt.setp(ax2.get_xticklabels(), fontsize=6)
            fig.canvas.mpl_connect('pick_event',  self.__plotInspection__)
            plt.grid()
            
        elif isinstance(self.__origin__, timeSerie): 
            fig = plt.figure( 'TimeSerie: ' + self.type + ' vs Origin')
            plt.cla()
            
            ax1 = plt.subplot(211)
            plt.plot( self.__origin__.dataFrame['Time'],  self.__origin__.dataFrame[self.__origin__.type] )
            plt.setp(ax1.get_xticklabels(), fontsize=6)
            plt.grid()
            
            ax2 = plt.subplot(212, sharex=ax1)
            plt.plot( self.dataFrame['Time'],  self.dataFrame[ self.type ], 'go', picker=picker_handler)
            plt.setp(ax2.get_xticklabels(), fontsize=6)
            fig.canvas.mpl_connect('pick_event',  self.__plotInspection__)
            plt.grid()
                      
        else:
            print('Origen no conocido')
            self.plotSerie()
     
    def __plotInspection__(self,event):
        """
        Estos serìan los que ya hice, solo ser llamaria desde un "clic" en una plotSerie o plotCombination
        Podria ponerle los  "__" para marcar que solo se llama desde otra si me tocan un clic
        """ 
        if   self.type == 'IntervalRR':
             self.__plotItemRR__( self.__origin__, event.pickx, event.picky )
            
        elif self.type == 'SlopeMax':
             self.__plotItemSlope__( self.__origin__, event.pickx, event.picky )
            
        elif self.type == 'Angle':
             self.__plotItemAngle__( self.__origin__, event.pickx, event.picky )

       
    def __plotItemRR__ (self,originECG, dt, dy):
        """
        Esto debería ver que es mejor si poner el funciones aca adentro o por fuera
        """
        fs = 360
        zoom_region = np.arange( (dt-1.2)*fs, (dt+0.6)*fs, 1, int  )
            
        referencia  = min( buscar(originECG, 1, dt, 0),  buscar(originECG, 1, dt-dy, 0) )
        t_rectas    = np.arange( dt-dy, dt, dy/2 ) 
        rectas      = np.full( 3, referencia )                                 
        puntos      = np.matrix([ [dt,referencia] , [dt-dy,referencia] ])           
                
        #Ploteo
        plt.figure('Inspection: Intervalo RR')
        plt.cla()
        plt.plot( zoom_region/fs,  originECG[zoom_region,1]                                                )
        plt.plot( t_rectas,             rectas,                  label=('Intervalo: '   +str(np.round(dy,4))+   's')   )
        plt.plot( puntos[:,0],          puntos[:,1],      'ro'  ,label=('Ocurrencia: '  +str(np.round(dt,4))+   's')   )
        plt.xlabel('time (s)')  
        plt.ylabel('amplitude (mV)')      
        plt.grid()
        plt.legend()
        plt.show()
        
    def __plotItemSlope__ (self, dt, dy ):
    #Defino la ventana que se va a graficar y la longitud de la recta        
        zoom_region = np.arange( int((dt-0.4)*self.fs), int((dt+0.6)*self.fs), 1)    
        len_rec     = 0.01
        
        #Recta con valor de pendiente maxima que pasa por el punto 
        t_rectas    = np.arange( dt-len_rec, dt+len_rec, 1/self.fs)
        rectas      = np.zeros( len(t_rectas) ) 
        for i in np.arange(0, len(t_rectas), 1):
          rectas[i]    = dy/0.4/self.fs*(t_rectas[i])*self.fs + ( self.__origin__.signal[int(dt*self.fs)] -dt/self.fs*dy/0.4*self.fs )
          #  0.4 = mv2mm/s2mm
        
        #Punto de la pendiente maxima 
        puntos      = ( dt, self.__origin__.signal[int(dt*self.fs)] )                                                            
            
        #Ploteo
        plt.figure('Inspection: Pendiente Máxima')
        plt.cla()
        plt.plot( zoom_region/self.fs,   self.__origin__.signal[zoom_region]                                                 )
        plt.plot( t_rectas,         rectas,                 label=('Pendiente: '   +str(np.round(dy,4))      )   )
        plt.plot( puntos[0],        puntos[1],    'ro',     label=('Ocurrencia: '  +str(np.round(dt,4))+ 's')   )
        plt.xlabel('time (s)')   
        plt.ylabel('amplitude (mV)')           
        plt.grid()
        plt.legend()
        plt.show()  
        
    def __plotItemAngle__ (self, dt, dy ):
    
#        i = DE ALGUNA FORMA ENCONTRAR EL i CON DT QUE NO SE REPITE NUNCA
        i = self.dataFrame[self.dataFrame['Time']==dt].index
        i = i[0]
        
        dt1 = self.dataFrame.iloc[i]['TimeSlopeMax']
        dt2 = self.dataFrame.iloc[i]['TimeSlopeMin']
        m1  = self.dataFrame.iloc[i]['SlopeMax']
        m2  = self.dataFrame.iloc[i]['SlopeMin'] 
        
        fs = self.fs
        #Defino la ventana que se va a graficar  
        zoom_region = np.arange( (dt1-0.4)*fs, (dt2+0.4)*fs, 1, int)   
                
        
        #Recta con valor de pendiente maxima , dibido m1 por la frecuencia para pasarlo a muestras dx/(dt*fs)
        t_rectas1    = np.arange( dt1-np.around(0.005*fs)/fs, dt+np.around(0.005*fs)/fs,  1/fs)
        rectas1      = np.zeros( len(t_rectas1) ) 
        for i in np.arange(0, len(t_rectas1), 1):
          rectas1[i]    = m1/fs*(t_rectas1[i])*fs + ( self.__origin__.signal[int(dt1*fs)] -dt1/fs*m1*fs )
        
        #Recta con valor de pendiente minima
        t_rectas2    = np.arange( dt-np.around(0.005*fs)/fs,  dt2+np.around(0.005*fs)/fs, 1/fs)    
        rectas2      = np.zeros( len(t_rectas2) ) 
        for i in np.arange(0, len(t_rectas2), 1):
          rectas2[i]    = m2/fs*(t_rectas2[i])*fs + ( self.__origin__.signal[int(dt2*fs)] -dt2/fs*m2*fs )
        
        
        punto1      = ( dt1, self.__origin__.signal[int(dt1*fs)] )    
        punto2      = ( dt2, self.__origin__.signal[int(dt2*fs)] )    
        #Ploteo
        plt.figure('Inspection: Pendiente Máxima y Minima que forman el angulo')
        plt.cla()
        plt.plot( zoom_region/fs,   self.__origin__.signal[zoom_region]                                                            )
        plt.plot( t_rectas1,         rectas1,                 label=('Pendiente Positiva: '   +str(np.round(m1,4))+'('+str(np.round(dt1,4))+'s)')   )
        plt.plot( t_rectas2,         rectas2,                 label=('Pendiente Negativa: '   +str(np.round(m2,4))+'('+str(np.round(dt2,4))+'s)')   )
        plt.plot( punto1[0],        punto1[1],    'ro',       label=('Ocurrencia: '           +str(np.round(dt,4))+'s'  )   )
        plt.plot( punto2[0],        punto2[1],    'ro',       label=('Angulo: '               +str(np.round(dy,4))+'º')   )
        plt.xlabel('time (s)')      
        plt.ylabel('amplitude (mV)')  
#        plt.xlim(6.8,7.4)
        plt.grid()
        plt.legend()
        plt.show()              
    
    def media(self):
        """
        Calcula la media de una sola serie de valores (puede llamarse desde otras funciones)
        """   
        medianSerie = np.median( self.dataFrame[self.type] )
        print( medianSerie )
        
        rect       = np.full( len(self.dataFrame['Time']), medianSerie )  

        #Ploteo
        plt.figure('Media TimeSerie:' + self.type + ' plot' )
        plt.cla()
        plt.plot( self.dataFrame['Time'],  self.dataFrame[ self.type ], 'go'    )
        plt.plot( self.dataFrame['Time'],  rect,                        '-.'    )
        plt.xlabel('time (s)')        
        plt.grid()
        plt.legend()
        plt.show()                               

#%%
"""
     FUNCIONES A DESARROLLAR    
"""
#    def plotCombination():  
#    """
#    Deberìa ser capaz de graficar la combinaciòn de dos series que le pasen
#    (?) serìa mejor qe directamente se llame AnguloVSRR, etc 
#    """
#            
#    def resampling:
#        """
#        Resamplea la serie de datos a otra frecuencia pasada como parametro, generando otra instancia de la clase donde __origin__ va a ser la serie que le dio origen
#        """
#    
#    def filter_1():
#    """
#    Pueden haber màs de estas funciones que permitan realizar disitnots filtrados:
#            - Descartar todos los valores por fuera de un cierto intervalo (pasado por el usuario)
#    """    
#        
#    
#    