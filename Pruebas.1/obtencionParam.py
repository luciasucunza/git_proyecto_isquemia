# Modulos importantantes
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
import pandas as pd

#%%
#------Apertura de la Señal-------
mat_struct = sio.loadmat('git_proyecto_isquemia/TP4_ecg.mat')

ecg_one_lead    = mat_struct['ecg_lead'].flatten()
qrs_detections  = mat_struct['qrs_detections'].flatten()
cant_muestras   = len(ecg_one_lead)
fs              = 1000 #Hz

time            = np.arange(0, cant_muestras, 1) /fs
time_qrs        = qrs_detections / fs

#%%
#------ Ploteo de ECG -------
plt.figure('Señales Obtenidas')

plt.plot(time, ecg_one_lead,     label='ECG'   )
plt.plot(time_qrs, ecg_one_lead[qrs_detections] ,     'ro'    )
plt.grid()
plt.legend()
plt.show()

#%%
#------ Ploteo de parametro-------
def plotParametro( tiempo, parametro ):
    plt.figure("Parametro")    
    plt.plot(tiempo, parametro-800000, 'ro' )
    plt.plot(time, ecg_one_lead,     label='ECG'   )
    plt.grid()
    plt.legend()
    plt.show()  
    
def plotParamDF( dataFram ):
    dataFram.plot( x= 'Tiempo', y='Param', grid=1)

    
#%%
#------ Ploteo de histograma-------
def plotHistograma( param, intervalo):
    plt.figure("Hist ograma")
    n, bins, patches = plt.hist(param, bins = intervalo, density=True )
    plt.xlabel('Smarts')
    plt.ylabel('Probability')
    plt.title('Histograma de la señal de error')
    plt.grid(True)
    plt.show()    
#%%
#------ Ploteo de UN SOLO VALOR del parametro UBICANDOLO en el ECG-------
# Esta funciòn se supone que sería el último paso de la cadena de ploteos cuando se elige un determinado valor
# Se la llamarìa desde la instancia, por lo tanto tendrìa acceso a saber de que ECG vengo, y una vez para cada parametro 
#que se haya seleccionado, por ejemplo si se trata de una instancia RR y quice seleccionar todo los RR = 701, quedando solo 2 que lo cumplan
# llamaria por cada uno una vez a esta funcion que me graficaria en cada caso los dos QRS que le dieron origen

#MUY IMPORTANTE PONER EL VECTOR DE TIEMPOS CORRECTO ASÌ SE ENTIENDE DE DONDE PROVIENE EL SEGMENTO DEL ECG

# LE TENGO QUE PASAR QUE SOY Y EL ECG, cuando esté dentro de la clase ya no porque se supone que serìan atributos
    
# Que grafique tambien el valor por el cual llamò la anteciòn?
    
#
#
def plotParamECG( dt, dx, tipo, fs, ecg):
    """
        Plotea un valor del parametro en el ECG, dependiendo de la naturaleza del mismo se realizan ciertas graficas adicionales
        Esta funcion formarìa parte de la clase pero solo la podrìa usar el padre? Porque solo la usa la primera instancia creada
        Al llamarla desde un objeto podrìa conocer:     - El "link" del ECG de donde viene (y la frecuencia de sampleo )
                                                        - El tipo de parametro del que viene
        Solo conciendo el indice se le podrìa pasar el valor del parametro y del tiempo, ya que serìa entrar en las columnas del data frame con eso
        En la clase que definimos, en el data frame cada valor tiene asociado un tiempo
        
        Parameters
        ----------
        dt :    int
            Tiempo en el que ocurre el parametro
        dx:     float
            Valor del parametro
        tipo:   str
            Nombre del tipo de parametro ("intervaloRR, "angulo", "pendienteMax")
        Notes
        -----
    """   
    if tipo ==          "intervaloRR":
        
        vent_inf_m = int((dt-1.2)*fs)
        vent_sup_m = int((dt+0.6)*fs) 
        
        zoom_region = np.arange( vent_inf_m, vent_sup_m, 1  )
        
        t_qrs1_m = int(dt*fs)                                                      #El +1 de dx esta porque si dx es impar me quedarìa un nunmero menos de vector, asì me queda de la misma longitud que fs*dx y las pares no me cambia
        t_qrs0_m = int((dt-dx)*fs)
        

        referencia = min( ecg[t_qrs0_m] , ecg[t_qrs1_m] )                       #Solo para que la recta RR me quede a un nivel que toque los dos
        
        
        t_rectas     = np.arange( t_qrs0_m, t_qrs1_m, 1 ) /fs 
        rectas       = np.zeros( int(dx*fs) )                                         #Grafico la recta sede la mitad de los QRS hasta cada QRS

        for i in np.arange(0, int(dx*fs), 1):
            rectas[i]  = referencia

        puntos       = np.matrix([ [dt,referencia] , [dt-dx,referencia] ])           
            
        plt.figure('Señales Obtenidas')
        plt.cla()
        plt.plot( zoom_region/fs,   ecg[zoom_region]                                                )
        plt.plot( t_rectas,         rectas,              label=('Intervalo: '   +str(dx)+   'ms')   )
        plt.plot( puntos[:,0],      puntos[:,1],    'ro',label=('Ocurrencia: '  +str(dt)+   'ms')   )
        plt.xlabel('time (s)')        
        plt.grid()
        plt.legend()
        plt.show()
    
    
    
    elif tipo ==        "PendienteMax":
        
        vent_inf_m = int((dt-0.4)*fs)
        vent_sup_m = int((dt+0.6)*fs)
        
        zoom_region = np.arange( vent_inf_m, vent_sup_m, 1)
        
        len_rec     = 0.01
        t_rectas    = np.arange( dt-len_rec, dt+len_rec, 1/fs)                  #Grafica la recta de la pendiente maxima a +-20ms de que ocurra
        rectas      = np.zeros( len(t_rectas) ) 
        
        for i in np.arange(0, len(t_rectas), 1):
          rectas[i]    = dx*(i-len(t_rectas)//2) + ( ecg[int(dt*fs)] -dt*dx  )
        
        puntos      = ( dt, ecg[int(dt*fs)] )                                                #Grafica el punto de la pendiente maxima             
            
        plt.figure('Señales Obtenidas')
        plt.cla()
        plt.plot( zoom_region/fs,   ecg[zoom_region]                                                 )
        plt.plot( t_rectas,         rectas,                 label=('Pendiente: '   +str(dx)      )   )
        plt.plot( puntos[0],        puntos[1],    'ro',     label=('Ocurrencia: '  +str(dt)+ 'ms')   )
        plt.xlabel('time (s)')        
        plt.grid()
        plt.legend()
        plt.show()  
        
    else:       #     "angulo"
         
        vent_inf_m = int((dt-0.4)*fs)
        vent_sup_m = int((dt+0.4)*fs)
        
        zoom_region = np.arange( vent_inf_m, vent_sup_m, 1)
                
        t_rectas    = np.arange( (dt-0.025)*fs, (dt+0.025)*fs, 1) /fs           #Grafica la recta de la pendiente maxima positiva
        rectas      = np.zeros( len(t_rectas) )     
        for i in np.arange(0, len(t_rectas), 1):
          rectas[i]    = dx*i + ( ecg[int(dt*fs)] -dt*dx  )
          
        t_rectas    = np.arange( (dt-0.025)*fs, (dt+0.025)*fs, 1) /fs           #Grafica la recta de la pendiente maxima negativa
        rectas      = np.zeros( len(t_rectas) ) 
        for i in np.arange(0, len(t_rectas), 1):
          rectas[i]    = -dx*i + ( ecg[int(dt*fs)] +dt*dx  )
       
        



#%%
#------Obtención de Parametros-------
def intervaloRR ( qrs ):
    """
        Obtiene los intervalos RR, devolviendo una matriz con el vector de tiempos y el de intevalos
        El tiempo es el tiempo del segundo QRS (para el primer latido el intervalo es 0)
        (tqrs0 = 0seg, tqrs2 = 25seg        => iRR0 = 25seg, tiRR0 = 25seg )
        
        Para el primer latido copia el RR del siguiente
    """
    len_qrs = len(qrs)
    result = np.array([     qrs,    np.hstack([  qrs[1]-qrs[0], qrs[1:len_qrs]-qrs[0:len_qrs-1]  ])    ])

    return result.transpose()


def pendienteMax ( ecg, qrs, fs ):
    """
        Obtiene los puntos de maxima pendiente a partir de la ubicación del complejo QRS con una ventana de +/-70 muestras
        Devuelve una matriz con el vector de tiempos en el que ocurre la maxima derivada y el valor de dicha derivada 
        Si para una ventana el maximo se mantiene para màs de una muestra devuelve la poscion del primero
        
        Para la primera muestra de cada ventana se copia el valor de la siguiente derivada
        Si bien en este caso no me afecta no tener valor porque tomo el maximo (lejos del limite inferior de la ventana)
        si me afecta el poscionamiento temporal del máximo (sin correjir se emciemtra una muestra antes del real)
                
    """
    
    result  = np.zeros( (len(qrs), 2) )
    i = 0
    
    for ii in qrs:
        
        ventDerivada    =   np.diff( ecg[ ii-70 : ii+70 ] )
        ventDerivada    =   np.hstack([ ventDerivada[0], ventDerivada ])           
        result[i,:]     =   [ np.argmax(ventDerivada)+ii-70 , ventDerivada.max() ]           
        i = i+1    
    
    return result
#%%
#------ PRUEBA DE FUNCIONES: INTERVALO RR------
fs = 1000

RR = intervaloRR(qrs_detections)
df_param =  {    'Tiempo'   : RR[:,0] / fs,
                 'Param'    : RR[:,1] / fs
                 }
df_param = pd.DataFrame( df_param )

#plotParametro( RR[:,0], RR[:,1] )                                              #Para Probar las funciones de Ploteo 
#plotParamDF( df_param )

#plotHistograma( RR[:,1], np.arange( 300, 1400, 10) )                           #Para Probar la funcion Histograma

plotParamECG( df_param.iloc[2]['Tiempo'], df_param.iloc[2]['Param'],"intervaloRR", fs, ecg_one_lead )    

#%%
#------ PRUEBA DE FUNCIONES: PENDIENTE MAXIMA------
fs = 1000

PM = pendienteMax(ecg_one_lead, qrs_detections, fs)
df_param =  {    'Tiempo'   : PM[:,0] / fs,
                 'Param'    : PM[:,1] 
                 }
df_param = pd.DataFrame( df_param )

plotParamECG( df_param.iloc[2]['Tiempo'], df_param.iloc[2]['Param'],"PendienteMax", fs, ecg_one_lead )    

#%%
#------ PRUEBA DE FUNCIONES: AGULO------


#%%
#------ MAS PRUEBAS------
dt =df_param.iloc[2]['Tiempo']
dx =df_param.iloc[2]['Param']
tipo= "PendienteMax"
fs = 1000
ecg= ecg_one_lead
qrs = qrs_detections

    