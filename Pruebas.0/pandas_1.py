import warnings
warnings.filterwarnings('ignore')

# Módulos importantantes
import pandas as pd
#import numpy as np
#import scipy.signal as sig
#import matplotlib as mpl
#import matplotlib.pyplot as plt
#import scipy.io as sio

datos = {   'Nombre' : ['Franco', 'Clara', 'Javi', 'Cande', 'Maxi', 'Agus','Benito','Carlos','Leandro','Maria' ],
            'Nota'   : [8,2,3,7,5, 11 , 4, 2, 10, 5],
            'Materia': ['EA','SyH','SdC','TD','TC2', 'EA2','SyH2','SdC2','TD2','TC2'],
            'Deporte': ['Teni','Futb','Vole','Hand','Basq','Wate','Nata','Hock','Atle','Jaba'],
            'Edad'   : ['92','58','32','12','35','23','18','43','52','31']
         }
df_datos = pd.DataFrame(datos)
index = [ 2, 10, 6, 4, 8, 12, 0, 16, 14, 20]
df_datos = pd.DataFrame(datos, index)                 #Creo el data frame
print('\n')
print(datos)
print('\n')
print(df_datos)
print('\n')

df_datos.loc[1] = ['Fran','9','Maq','Natac','24']

df_modif = df_datos.replace( 'SyH', 'Med')
print(df_datos)
print('\n')
print(df_modif)
print('\n')

df_num = pd.DataFrame(df_datos)            #Creo un data frame igual
df_num['Nota'] = df_num.Nota.astype(int)
df_num['Edad'] = df_num.Edad.astype(int)
print(df_datos)
print('\n')
print(df_num)
print('\n')

print('\nPromedio de la Nota: ')
print( df_num['Nota'].mean())

print('\nCorrelación del DataFrame: ')
print( df_num.corr())

print('\nColumna Deportes y Materia del DataFrame: ')
print( df_num[['Deporte', 'Materia']])

print('\nSeleccionar un solo elemento, fila 2 columna Materia')
print( df_num.iloc[2]['Materia'])

print('\nSeleccionar la fila 1')
print( df_num.iloc[2][:])
