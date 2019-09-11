# Modulos importantantes
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

##
"""
            ALGUNA FORMA DE PONER POR EJEMPLO UNITIS["ANGLE"] Y ME DEVUELVA "º", ASÍ CON LAS 3
"""
##
def picker_handler( line, mouseevent):
    """
    Tendrìa que ver dos cosas:
            - Ahora si toca dos puntos agarra el primero arbitrariamente
            - El valor de maxd es funcion de dt que es igual en todos los parametros que grafico ahora, pero habrìa que ver si esto sigue bien para otras cosazs
                podrìa querer expresarlo en funcion de FS por lo que la deberìa definir adentro
                pero 1/fs es muy chico porque lo que me importa es la distancia entre latidos que esl algo pseudo constante
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
    TYPE PARAM TIENE QUE SER O "Angle" "SlopeMax" "IntervalRR"
    Para el angulo primero se pasa la màxima y despues la minima
    """
    def __init__(self, typeParam = None, fs = None, sig_origin= None, param = None, 
                 t_param = None, param_aux1 = None, t_param_aux1 = None  , param_aux2 = None, 
                 t_param_aux2 = None  
                 ):
        
#        if typeParam is None: 
        self.__origin__  = sig_origin
        self.dataFrame   = pd.DataFrame({   'Time'      : t_param,
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
          
        self.fs     = fs
        self.type   = typeParam
        
    """
    Graficar una serie con datos alrededor 
    """
    def plotSerieECG( self ): 
        fig = plt.figure( 'TimeSerie: ' + self.type + 'plot')
        plt.cla()
        
        ax1 = plt.subplot(211)
        plt.plot( self.__origin__.time,  self.__origin__.signal)
        plt.setp(ax1.get_xticklabels(), fontsize=6)
        plt.grid()
        
        ax2 = plt.subplot(212, sharex=ax1)
        plt.plot( self.dataFrame['Time'],  self.dataFrame[ self.type ], 'go', picker=picker_handler)
        plt.setp(ax2.get_xticklabels(), visible=False)
        fig.canvas.mpl_connect('pick_event',  self.__plotInspection__)
        plt.grid()
        
     
    def __plotInspection__(self,event):
        """
        Estos serìan los que ya hice, solo ser llamaria desde un "clic" en una plotSerie o plotCombination
        Podria ponerle los  "__" para marcar que solo se llama desde otra si me tocan un clic
        """ 
        if   self.type == 'IntervalRR':
             self.__plotItemRR__( event.pickx, event.picky )
            
        elif self.type == 'SlopeMax':
             self.__plotItemSlope__( event.pickx, event.picky )
            
        elif self.type == 'Angle':
             self.__plotItemAngle__( event.pickx, event.picky )

       
    def __plotItemRR__ (self, dt, dy):
        """
        Esto debería ver que es mejor si poner el funciones aca adentro o por fuera
        """
        zoom_region = np.arange( (dt-1.2)*self.fs, (dt+0.6)*self.fs, 1, int  )
        
        referencia = min( self.__origin__.signal[int(dt*self.fs)] , self.__origin__.signal[int((dt-dy)*self.fs)] )              #Solo para que la recta RR me quede a un nivel que toque los dos
        t_rectas     = np.arange( dt-dy, dt, 1/self.fs ) 
        rectas       = np.full( len(t_rectas), referencia )                                 
        puntos       = np.matrix([ [dt,referencia] , [dt-dy,referencia] ])           
                
        #Ploteo
        plt.figure('Inspection: Intervalo RR')
        plt.cla()
        plt.plot( zoom_region/self.fs,  self.__origin__.signal[zoom_region]                                                )
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
        
    
            
#%%     PRUEBA TIME SERIE

pruebaRR = timeSerie('IntervalRR', ECG.fs, ECG, RR, ECG.qrs/ECG.fs)
pruebaRR.plotSerieECG()


#Tengo que revisar el quilombo de tiempo que hice para lo de la escala
pruebaSM = timeSerie('SlopeMax', ECG.fs, ECG, SM[:,1], SM[:,0]  )
pruebaSM.plotSerieECG()


#Tengo que revisar el quilombo de tiempo que hice para lo de la escala
pruebaANG = timeSerie('Angle', ECG.fs, ECG, ANG[:,1], ANG[:,0],  ANG[:,3], ANG[:,2], ANG[:,5], ANG[:,4] )
pruebaANG.plotSerieECG()

    

            
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
#    def media():
#    """
#    Calcula la media de una sola serie de valores (puede llamarse desde otras funciones)
#    """    
#    def filter_1():
#    """
#    Pueden haber màs de estas funciones que permitan realizar disitnots filtrados:
#            - Descartar todos los valores por fuera de un cierto intervalo (pasado por el usuario)
#    """    
#        
#    
#    