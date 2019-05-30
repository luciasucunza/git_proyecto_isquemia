# Modulos importantantes
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio

#%%
#------Apertura de la Señal-------
mat_struct = sio.loadmat('git_proyecto_isquemia/TP4_ecg.mat')

ecg_one_lead = mat_struct['ecg_lead']
ecg_one_lead = ecg_one_lead.flatten()
qrs_detections = mat_struct['qrs_detections']
cant_muestras = len(ecg_one_lead)
 
ecg_qrs_detections = np.zeros( cant_muestras ) 
ecg_qrs_detections[qrs_detections] = ecg_one_lead[qrs_detections]
#%%
#------ Ploteo de ECG -------
plt.figure('Señales Obtenidas')

plt.plot(ecg_one_lead,     label='ECG'   )
plt.plot(qrs_detections, ecg_one_lead[qrs_detections] ,     'ro'    )
plt.grid()
plt.axis([-10, 100010, -12000, 32000])
plt.legend()
plt.show()

#%%
#------ Ploteo de parametro-------
def plotParametro( tiempo, parametro ):
    plt.figure("Parametro")    
    plt.plot(tiempo, parametro, 'ro' )
    plt.grid()
    plt.legend()
    plt.show()  
#%%
#------ Ploteo de parametro-------
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
    #dx esta en ms, entonces ver si esta bien pensando o poner la fs
    
    if tipo ==          "intervaloRR":
        zoom_region = np.array([dt-0.8, dt+0.8])
        
        t_rectas  = np.arange( (dt-dx//2)*fs, (dt-(dx+1)//2)*fs, 1 ) /fs        #El +1 de dx esta porque si dx es impar me quedarìa un nunmero menos de vector, asì me queda de la misma longitud que fs*dx y las pares no me cambia
        rectas       = np.zeros( dx*fs )                                      #Grafico la recta sede la mitad de los QRS hasta cada QRS
        for i in np.arange(1, dx*fs, 1):
            rectas  = dx
        
        puntos       = [ [dt-dx//2,ecg[dt-dx//2]] , [dt+dx//2,ecg[dt+dx//2]] ]   #Grafica los puntos de los dos QRS qe lo definen
     
    
    elif tipo ==        "PendienteMax":
        zoom_region = np.array([dt-0.4, dt+0.4])
        
        t_rectas    = np.arange( (dt-0.025)*fs, (dt+0.025)*fs, 1) /fs           #Grafica la recta de la pendiente maxima a +-25ms de que ocurra
        rectas      = np.zeros( len(t_rectas) ) 
        for i in t_rectas:
          rectas    = dx*i+(ecg[dt]-dt*dx)
        
        puntos      = [ dt, dx ]                                                #Grafica el punto de la pendiente maxima
            
        
    else:       #     "angulo"
        zoom_region = np.array([dt-0.4, dt+0.4])
        
        t_rectas    = np.arange( (dt-0.025)*fs, (dt+0.025)*fs, 1) /fs           #Grafica la recta de la pendiente maxima positiva
        rectas      = np.zeros( len(t_rectas) ) 
        for i in t_rectas:
          rectas    = dx*i+(ecg[dt]-dt*dx)
        
        t_rectas    = np.arange( (dt-0.025)*fs, (dt+0.025)*fs, 1) /fs           #Grafica la recta de la pendiente maxima negativa
        rectas      = np.zeros( len(t_rectas) ) 
        for i in t_rectas:
          rectas    = -dx*i+(ecg[dt]+dt*dx)
       
        
        
        
    plt.figure('Señales Obtenidas')
    plt.plot( zoom_region,  ecg[zoom_region/fs],    label='ECG'     )
    plt.plot( t_rectas,     rectas,                 label='Rectas'   )
    plt.plot( puntos[:,0],   puntos[:,1],            label='Puntos'   )
    plt.grid()
    plt.legend()
    plt.show()


#%%
#------Obtención de Parametros-------
def intervaloRR ( qrs ):
    """
        Obtiene los intervalos RR, devolviendo una matriz con el vector de tiempos y el de intevalos
        El tiempo es tiempo de medio entre los dos QRS truncado 
        (tqrs0 = 0seg, tqrs2 = 25seg        => iRR0 = 25seg, tiRR0 = 12seg )
    """
    matriz = np.zeros( (len(qrs), 2) )
    for i in np.arange(1, len(qrs), 1 ):
        matriz[i, 0] = (qrs[i] + qrs[i-1]) //2
        matriz[i, 1] = qrs[i] - qrs[i-1]
        
    return matriz

#%%
#------ Pruebas ------

B = intervaloRR(qrs_detections)

plt.figure("Prueba")
plotParametro(B[:,0], B[:,1])
plt.grid()
plt.show()

plotHistograma( A, np.arange( 200, 1500, 10) )