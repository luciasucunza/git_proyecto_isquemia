# Modulos importantantes
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
##
"""
            ALGUNA FORMA DE PONER POR EJEMPLO UNITIS["ANGLE"] Y ME DEVUELVA "º", ASÍ CON LAS 3
            En todas las gráficas se pueden hacer mejoras, para mostrar más datos
"""
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
                        param_aux2  = None,      t_param_aux2 = None,
                        abstraLevel = 1,
                        origIndex   = None
                 ):
        
#        if typeParam is None: 
        self.type       = typeParam
        self.__origin__ = origin
        self.__level__  = abstraLevel 
        
        if typeParam == 'Angle':
            self.units    = "º"
        elif typeParam == 'IntervalRR':
            self.units    = "s"            
        elif typeParam == 'SlopeMax':
            self.units    = "mm/mm"        
        
        if type(param) == pd.core.frame.DataFrame:
            self.dataF  = param
        else:
            self.dataF  = pd.DataFrame({   'Time'      : t_param,
                                             typeParam  : param
                                             })   
            if typeParam == 'Angle':
                self.dataF['SlopeMax']      = param_aux1
                self.dataF['TimeSlopeMax']  = t_param_aux1   
                self.dataF['SlopeMin']      = param_aux2
                self.dataF['TimeSlopeMin']  = t_param_aux2   
                
            elif typeParam == 'SlopeMax':
                self.dataF['TimeSlopeMax']  = t_param_aux1  
                

    def plotSerie(self, interes = None ):
        fig = plt.figure( 'TimeSerie: ' + self.type + ' plot' + ' (' + str(self.__level__) + ')')
        plt.cla()
        plt.plot( self.dataF['Time'],  self.dataF[ self.type ], 'go', picker=picker_handler)
        
        if interes != None:               
            for i in interes:
#                plt.plot( self.dataF.loc[ self.dataF['Time']==i ][ 'Time' ],  self.dataF.loc[ self.dataF['Time']==i ][ self.type ], 'ro' )
                plt.plot( self.dataF.iloc[i]['Time'],  self.dataF.iloc[i][self.type], 'ro' )
        
        fig.canvas.mpl_connect('pick_event',  self.__plotInspection__)
        plt.xlabel('time (s)')   
        plt.ylabel(self.units)
        plt.grid()
        

    def plotSerieVsOrig( self ): 
        if isinstance(self.__origin__, np.ndarray):
            fig = plt.figure( 'TimeSerie: ' + self.type + ' vs Origin')
            plt.cla()
            
            ax1 = plt.subplot(211)
            plt.plot( self.__origin__[:,0],  self.__origin__[:,1])
            plt.setp(ax1.get_xticklabels(), fontsize=6)
            plt.grid()
            
            ax2 = plt.subplot(212, sharex=ax1)
            plt.plot( self.dataF['Time'],  self.dataF[ self.type ], 'go', picker=picker_handler)
            plt.setp(ax2.get_xticklabels(), fontsize=6)
            fig.canvas.mpl_connect('pick_event',  self.__plotInspection__)
            
            plt.grid()
            
        elif isinstance(self.__origin__, timeSerie): 
            fig = plt.figure( 'TimeSerie: ' + self.type + ' vs Origin')
            plt.cla()
            
            ax1 = plt.subplot(211)
            plt.plot( self.__origin__.dataF['Time'],  self.__origin__.dataF[self.__origin__.type] )
            plt.setp(ax1.get_xticklabels(), fontsize=6)
            plt.grid()
            
            ax2 = plt.subplot(212, sharex=ax1)
            plt.plot( self.dataF['Time'],  self.dataF[ self.type ], 'go', picker=picker_handler)
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
        if self.__level__ == 1:
            if   self.type == 'IntervalRR':  
                 self.__plotItemRR__( self.__origin__, event.pickx, event.picky )
                
            elif self.type == 'SlopeMax':
                 self.__plotItemSlope__( self.__origin__, event.pickx, event.picky )
                
            elif self.type == 'Angle':
                 self.__plotItemAngle__( self.__origin__, event.pickx, event.picky )
        else:
            self.__origin__.plotSerie( interes = self.dataF.loc[ self.dataF['Time']==event.pickx ][ 'iOrigin' ] )

       
    
    def __plotItemRR__ (self,originECG, dt, dy):
        """
        Esto debería ver que es mejor si poner el funciones aca adentro o por fuera
        """
        referencia  = min( originECG[ originECG[:,0] == dt, 1 ], originECG[ originECG[:,0] == dt-dy, 1 ] )[0]                            
        puntos      = np.array([ [dt,referencia] , [dt-dy,referencia] ])           
                
        #ZoomRegion
        timeZR = originECG[ np.bitwise_and( originECG[:,0] >= dt-1.2,  originECG[:,0] <= dt+0.6), 0 ] 
        ecgZR  = originECG[ np.bitwise_and( originECG[:,0] >= dt-1.2,  originECG[:,0] <= dt+0.6), 1 ]
        
        #Ploteo
        plt.figure('Inspection: Intervalo RR')
        plt.cla()
        plt.plot( timeZR,       ecgZR                                                                   )
        plt.plot( puntos[:,0],  puntos[:,1],            label=('Ocurrencia: '+str(np.round(dt,4))+'s')  )
        plt.plot( puntos[:,0],  puntos[:,1],    'ro',   label=('Ocurrencia: '+str(np.round(dt,4))+'s')  )
        plt.xlabel('time (s)')  
        plt.ylabel('amplitude (mV)')      
        plt.grid()
        plt.legend()
        plt.show()
        
        
    def __plotItemSlope__ (self, originECG, dt, dy ):

        #Punto de pendiente maxima 
        punto      = ( dt, originECG[ originECG[:,0] == dt, 1 ] )                                                            
            
        #Recta con valor de pendiente maxima que pasa por el punto 
        len_rec     = 0.01
        t_rectas    = np.array( [ dt - len_rec, dt + len_rec ] )        
        rectas      = np.array( [ punto[1] - dy/0.4*len_rec, punto[1] + dy/0.4*len_rec] )
        
        #ZoomRegion
        timeZR = originECG[ np.bitwise_and( originECG[:,0] >= dt-0.4,  originECG[:,0] <= dt+0.6), 0 ] #zoom_region/self.fs
        ecgZR  = originECG[ np.bitwise_and( originECG[:,0] >= dt-0.4,  originECG[:,0] <= dt+0.6), 1 ] #self.__origin__.signal[zoom_region] 
        
        #Ploteo
        plt.figure('Inspection: Pendiente Máxima')
        plt.cla()
        plt.plot( timeZR,       ecgZR                                                                   )
        plt.plot( t_rectas,     rectas,                 label=('Pendiente: ' +str(np.round(dy,4))    )  )
        plt.plot( punto[0],     punto[1],    'ro',      label=('Ocurrencia: '+str(np.round(dt,4))+'s')  )
        plt.xlabel('time (s)')   
        plt.ylabel('amplitude (mV)')           
        plt.grid()
        plt.legend()
        plt.show()  
        
        
    def __plotItemAngle__ (self, originECG, dt, dy ):
    
#        i = DE ALGUNA FORMA ENCONTRAR EL i CON DT QUE NO SE REPITE NUNCA, ver alguna forma mejor
#        Ojo que filas no es lo mismo que indice
        i = self.dataF[self.dataF['Time']==dt].index
        i = i[0]
        aux = self.dataF.loc[i]
        dt1 = aux[:]['TimeSlopeMax']
        dt2 = aux[:]['TimeSlopeMin']
        m1  = aux[:]['SlopeMax']
        m2  = aux[:]['SlopeMin'] 


        #Puntos de pendiente maxima 
        punto1      = ( dt1, originECG[ originECG[:,0] == dt1, 1 ] )    
        punto2      = ( dt2, originECG[ originECG[:,0] == dt1, 1 ] )  
        
        #Recta con valor de pendiente maxima que pasa por el punto 
        len_rec     = 0.005
        
        t_rectas1    = np.array( [ dt1 - len_rec,                           dt  + len_rec                       ] )        
        rectas1      = np.array( [ punto1[1] - m1/0.4*len_rec,              punto1[1] + m1/0.4*(dt-dt1+len_rec) ] )
        t_rectas2    = np.array( [ dt  - len_rec,                           dt2 + len_rec                       ] )        
        rectas2      = np.array( [ punto2[1] - m2/0.4*(dt2-dt+len_rec),     punto2[1] + m2/0.4*len_rec          ] )
      
        #ZoomRegion
        timeZR = originECG[ np.bitwise_and( originECG[:,0] >= dt1-0.4,  originECG[:,0] <= dt2+0.4), 0 ] 
        ecgZR  = originECG[ np.bitwise_and( originECG[:,0] >= dt1-0.4,  originECG[:,0] <= dt2+0.4), 1 ]
        
        #Ploteo
        plt.figure('Inspection: Pendiente Máxima y Minima que forman el angulo')
        plt.cla()
        plt.plot( timeZR,       ecgZR                                                                   )
        plt.plot( t_rectas1,         rectas1,                 label=('Pendiente Positiva: '   +str(np.round(m1,4))+'('+str(np.round(dt1,4))+'s)')   )
        plt.plot( t_rectas2,         rectas2,                 label=('Pendiente Negativa: '   +str(np.round(m2,4))+'('+str(np.round(dt2,4))+'s)')   )
        plt.plot( punto1[0],        punto1[1],    'ro',       label=('Ocurrencia: '           +str(np.round(dt,4))+'s'  )   )
        plt.plot( punto2[0],        punto2[1],    'ro',       label=('Angulo: '               +str(np.round(dy,4))+'º')   )
        plt.xlabel('time (s)')      
        plt.ylabel('amplitude (mV)')  
        plt.grid()
        plt.legend()
        plt.show()              
        
        
    def media(self):
        """
        Calcula la media de una sola serie de valores (puede llamarse desde otras funciones)
        """   
        medianSerie = np.median( self.dataF[self.type] )
        print( medianSerie )
        
        rect       = np.full( len(self.dataF['Time']), medianSerie )  

        #Ploteo
        plt.figure('Media TimeSerie:' + self.type + ' plot' )
        plt.cla()
        plt.plot( self.dataF['Time'],  self.dataF[ self.type ], 'go'    )
        plt.plot( self.dataF['Time'],  rect,                        '-.'    )
        plt.xlabel('time (s)')        
        plt.grid()
        plt.legend()
        plt.show()


    def recorteX(self, lInf, lSup):
        if lInf == lSup:
            print('Los limites deben ser diferentes')
        else:
            self.dataF = self.dataF.loc[ (self.dataF['Time']>lInf) & (self.dataF['Time']<lSup) ]
            
        
    def recorteY(self, lInf, lSup):
        if lInf == lSup:
            print('Los limites deben ser diferentes')
        else:
            self.dataF = self.dataF.loc[ (self.dataF[self.type]>lInf) & (self.dataF[self.type]<lSup) ]


    def recorteRoI(self, label):       
            self.dataF = self.dataF.loc[ self.dataF['RoI'] == label ]    
#            recX = timeSerie(   typeParam   = self.type, 
#                    origin      = self,           
#                    param       = self.dataF.loc[ self.dataF['RoI'] == label ],
#                    abstraLevel = self.__level__  +1
#                    )
#            recX.dataF['iOrigin'] = self.dataF['Time']
#            return recX
#            

        
    def roi_time(self, label, tInf = None, tSup = None):
        
        #Si no pasan tiempos limites entonces es por metodo gráfico la elección
        #Estaría bueno que en lugar de poner el nombre desde la funcion salte una pestañita despues de tocar dos puntos
        if tInf == None:
            if tSup == None:                 
                
                i = 2*len(label) + 1
                
                plt.figure( 'TimeSerie: ' + self.type + ' plot' + ' (' + str(self.__level__) + ')')
                plt.cla()
                plt.plot( self.dataF['Time'],  self.dataF[ self.type ], 'go')
                plt.xlabel('time (s)')   
                plt.ylabel(self.units)
                plt.grid()
                
                x = plt.ginput(i, timeout = 0)
                                    
                plt.close()
                print (x)
                
            else:
                self.dataF.loc[self.dataF['Time'] < tSup, 'RoI']  = label
        else:
            if tSup == None:
                self.dataF.loc[self.dataF['Time'] > tInf, 'RoI']  = label
            else:                
#                self.dataF.loc[ (self.dataF['Time'] > 2) & (self.dataF['Time'] < 7), 'RoI' ]  = 'das'
                self.dataF.loc[ (self.dataF['Time'] > tInf) & (self.dataF['Time'] < tSup), 'RoI' ]  = label
                
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
#    def showRoI(self):
#    """
#        Que muestre cuales son las roi qe hay en el momento
#    """

# De esta forma al recortar genero otra instancia

#            SI QUISIERA HACER UNA NUEVA INSTANCIA Y NO PISAR
#            recX = timeSerie(   typeParam   = self.type, 
#                                origin      = self,           
#                                param       = self.dataF.loc[ (self.dataF['Time']>lInf) & (self.dataF['Time']<lSup) ],
#                                abstraLevel = self.__level__  +1
#                                )
#            return recX
            