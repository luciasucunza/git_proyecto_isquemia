import pandas as pd

#df = Una dataFrame importada de un archivo

# Identifica los datos nulos del DataFrame
#Devuekve yba natruz booleana, True para valores faltantes y False para valores no perdidos
print('\nDatos nulos en el DataFrame:')
print( df.isnull() )

# Muestra la cantidad de datos faltantes de cada columna
print('\nDatos nulos del DataFrame')
print( df.isnull().sum() )

# Elimino fila [dropna()] o columna [dropna(axis=1)] donde hay datos nulos
# Para rellenar los valores peridods se utiliza fd.filna(x)
print('\nReemplaza los valores perdidos por la media:')
print( fd.fillna(df.mean()) )




