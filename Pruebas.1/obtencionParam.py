# Modulos importantantes
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
import pandas as pd

#%%
#------Apertura de la Señal-------
mat_struct = sio.loadmat('/home/luciasucunza/git_proyecto_isquemia/TP4_ecg.mat')

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
def plotParamECG( df, tipo, fs, ecg):
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
    dt = df['Tiempo']
    dx = df['Param']
    if tipo ==          "intervaloRR":
        
        #Defino la ventana que se va a graficar
        zoom_region = np.arange( int((dt-1.2)*fs), int((dt+0.6)*fs), 1  )
        
        
        referencia = min( ecg[int(dt*fs)] , ecg[int((dt-dx)*fs)] )              #Solo para que la recta RR me quede a un nivel que toque los dos
        t_rectas     = np.arange( dt-dx, dt, 1/fs ) 
        rectas       = np.full( int(dx*fs), referencia )                                 
        puntos       = np.matrix([ [dt,referencia] , [dt-dx,referencia] ])           
                
        #Ploteo
        plt.figure('Intervalo RR')
        plt.cla()
        plt.plot( zoom_region/fs,   ecg[zoom_region]                                                )
        plt.plot( t_rectas,         rectas,              label=('Intervalo: '   +str(dx)+   'ms')   )
        plt.plot( puntos[:,0],      puntos[:,1],    'ro',label=('Ocurrencia: '  +str(dt)+   'ms')   )
        plt.xlabel('time (s)')        
        plt.grid()
        plt.legend()
        plt.show()
    
    
    
    elif tipo ==        "PendienteMax":
        
        #Defino la ventana que se va a graficar y la longitud de la recta        
        zoom_region = np.arange( int((dt-0.4)*fs), int((dt+0.6)*fs), 1)    
        len_rec     = 0.01
        
        #Recta con valor de pendiente maxima que pasa por el punto 
        t_rectas    = np.arange( dt-len_rec, dt+len_rec, 1/fs)
        rectas      = np.zeros( len(t_rectas) ) 
        for i in np.arange(0, len(t_rectas), 1):
          rectas[i]    = dx*fs*(t_rectas[i])*fs + ( ecg[int(dt*fs)] -dt*fs*dx*fs )
        
        #Punto de la pendiente maxima 
        puntos      = ( dt, ecg[int(dt*fs)] )                                                            
            
        #Ploteo
        plt.figure('Pendiente Máxima')
        plt.cla()
        plt.plot( zoom_region/fs,   ecg[zoom_region]                                                 )
        plt.plot( t_rectas,         rectas,                 label=('Pendiente: '   +str(dx)      )   )
        plt.plot( puntos[0],        puntos[1],    'ro',     label=('Ocurrencia: '  +str(dt)+ 'ms')   )
        plt.xlabel('time (s)')        
        plt.grid()
        plt.legend()
        plt.show()  
        
    else:       #     "angulo"
        
        dt1 = df['t_m1']
        dt2 = df['t_m2']
        m1  = df['m1']
        m2  = df['m2'] 
        
        #Defino la ventana que se va a graficar  
        zoom_region = np.arange( int((dt1-0.4)*fs), int((dt2+0.4)*fs), 1)   
                
        
        #Recta con valor de pendiente maxima 
        t_rectas1    = np.arange( dt1-0.005, dt1+0.018,  1/fs)
        rectas1      = np.zeros( len(t_rectas1) ) 
        for i in np.arange(0, len(t_rectas1), 1):
          rectas1[i]    = m1*fs*(t_rectas1[i])*fs + ( ecg[int(dt1*fs)] -dt1*fs*m1*fs )
        
        #Recta con valor de pendiente minima
        t_rectas2    = np.arange( dt2-0.018,  dt2+0.005, 1/fs)    
        rectas2      = np.zeros( len(t_rectas2) ) 
        for i in np.arange(0, len(t_rectas2), 1):
          rectas2[i]    = m2*fs*(t_rectas2[i])*fs + ( ecg[int(dt2*fs)] -dt2*fs*m2*fs )
        
        
        punto1      = ( dt1, ecg[int(dt1*fs)] )    
        punto2      = ( dt2, ecg[int(dt2*fs)] )    
        #Ploteo
        plt.figure('Pendiente Máxima y Minima que forman el angulo')
        plt.cla()
        plt.plot( zoom_region/fs,   ecg[zoom_region]                                                            )
        plt.plot( t_rectas1,         rectas1,                 label=('Pendiente Positiva: '   +str(m1)      )   )
        plt.plot( t_rectas2,         rectas2,                 label=('Pendiente Negativa: '   +str(m2)      )   )
        plt.plot( punto1[0],        punto1[1],    'ro',       label=('Ocurrencia: '           +str(np.round(dt,2))+'ms' )   )
        plt.plot( punto2[0],        punto2[1],    'ro',       label=('Angulo: '               +str(np.round(dx,2))+'rad')   )
        plt.xlabel('time (s)')        
        plt.grid()
        plt.legend()
        plt.show()  
        



#%%
#------Obtención de Parametros-------
def intervaloRR ( qrs, fs = 1 ):
    """
        Obtiene los intervalos RR, devolviendo una matriz con el vector de tiempos y el de intevalos
        El tiempo es el tiempo del segundo QRS (para el primer latido el intervalo es 0)
        (tqrs0 = 0seg, tqrs2 = 25seg        => iRR0 = 25seg, tiRR0 = 25seg )
        
        Para el primer latido copia el RR del siguiente
        
        Si la frecuencia de muestreo es 1 quiere decir que o está muestreda
    """
    len_qrs = len(qrs)
    qrs = qrs/fs
    result = np.array([     qrs,    np.hstack([  qrs[1]-qrs[0], qrs[1:len_qrs]-qrs[0:len_qrs-1]  ])    ])

    return result.transpose()


def pendienteMax ( ecg, qrs, fs = 1 ):
    """
        Obtiene los puntos de maxima pendiente a partir de la ubicación del complejo QRS con una ventana de +/-70 muestras
        Devuelve una matriz con el vector de tiempos en el que ocurre la maxima derivada y el valor de dicha derivada 
        Si para una ventana el maximo se mantiene para màs de una muestra devuelve la poscion del primero
        
        Para la primera muestra de cada ventana se copia el valor de la siguiente derivada
        Si bien en este caso no me afecta no tener valor porque tomo el maximo (lejos del limite inferior de la ventana)
        si me afecta el poscionamiento temporal del máximo (sin correjir se emciemtra una muestra antes del real)
                
    """
    qrs = qrs/fs
    
    result  = np.zeros( (len(qrs), 2) )
    i = 0
    
    for ii in qrs:
        
        ventDerivada    =   np.diff( ecg[ int((ii-0.07)*fs) : int((ii+0.07)*fs) ] )
        ventDerivada    =   np.hstack([ ventDerivada[0], ventDerivada ])     /fs
        result[i,:]     =   [ np.argmax(ventDerivada)/fs+ii-0.07 , ventDerivada.max() ]           
        i = i+1    
    
    return result



def angulo ( ecg, qrs, fs = 1):
    """
        Obtiene el angulo formado por la pendiente maxima y la minima de cada complejo QRS
        
        angulo = arctg( (m2-m1) / (1+m1*m2) )
        
        Si: Y1 = m1 * t + (ecg[t1]-t1*m1)
            Y2 = m2 * t + (ecg[t2]-t2*m2)
            Pinterseccion = ( (ecg[t1]-t1*m1)-(ecg[t2]-t2*m2)  ;  (ecg[t2]-t2*m2)*m1 - (ecg[t1]-t1*m1)*m2 )
       
        En la primera columna devuelve el timpo de intersección
        En la segunda columna devuleve el valor del angulo (si es positivo hacia arriba si es - hacia abajo)
        En la tercera columna devuleve el valor el tiempo de ocurrencia de la pendiente maxima
        En la cuarta  columna devuleve el valor de la pendiente maxima
        En la quinta  columna devuleve el valor el tiempo de ocurrencia de la pendiente minima
        En la sexta   columna devuleve el valor de la pendiente minima
        
        
        Otra opcion serìa sacar la 4,5 y 6 y reemplazar en la tercera por 
#        result[i,2] = (a*d-b*c) / (a-b)
        Es la poscion en el eje Y de la interecciòn (donde graficar el angulo)
                      
    """
    qrs = qrs/fs
    
    
    result  = np.zeros( (len(qrs), 6) )
    i = 0
    
    for ii in qrs:
        
        ventDerivada    =   np.diff( ecg[ int((ii-0.07)*fs) : int((ii+0.07)*fs) ] )
        ventDerivada    =   np.hstack([ ventDerivada[0], ventDerivada ])     /fs

        a = ventDerivada.max()
        c = ecg[np.argmax(ventDerivada)] - np.argmax(ventDerivada) * a
        b = ventDerivada.min()
        d = ecg[np.argmin(ventDerivada)] - np.argmin(ventDerivada) * b
        
        result[i,0] = (d-c)     / (a-b) + ii
        result[i,1] = np.arctan( np.abs(a-b) / (1+a*b) )
        
        result[i,2] = np.argmax(ventDerivada)/fs + ii-0.07
        result[i,3] = a
        result[i,4] = np.argmin(ventDerivada)/fs + ii-0.07
        result[i,5] = b
                     
        i = i+1   
    
    return result

#%%
#------ PRUEBA DE FUNCIONES: INTERVALO RR------
fs = 1000

RR = intervaloRR(qrs_detections,fs)
df_param =  {    'Tiempo'   : RR[:,0],
                 'Param'    : RR[:,1]
                 }
df_param = pd.DataFrame( df_param )

plotParamECG( df_param.iloc[2],"intervaloRR", fs, ecg_one_lead )  

#%%
#------ PRUEBA DE FUNCIONES: PENDIENTE MAXIMA------
fs = 1000

PM = pendienteMax(ecg_one_lead, qrs_detections,fs )
df_param =  {    'Tiempo'   : PM[:,0],
                 'Param'    : PM[:,1] 
                 }
df_param = pd.DataFrame( df_param )

plotParamECG( df_param.iloc[2],"PendienteMax", fs, ecg_one_lead )    

#%%
#------ PRUEBA DE FUNCIONES: AGULO------

ANG = angulo(ecg_one_lead, qrs_detections, fs )
df_param =  {    'Tiempo'   : ANG[:,0],
                 'Param'    : ANG[:,1], 
                 't_m1'     : ANG[:,2], 
                 'm1'       : ANG[:,3], 
                 't_m2'     : ANG[:,4], 
                 'm2'       : ANG[:,5]
                 }
df_param = pd.DataFrame( df_param )

plotParamECG( df_param.iloc[2],"Angulo", fs, ecg_one_lead )    
   