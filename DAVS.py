"""
Created on Fri Feb 14 10:13:59 2020
Analisis de DAVS de Rb85 y Rb87
Que hace:
    Carga los datos de un csv con pandas y los pasa a np
    Arma transformación para pasar de t a frec
    Plotea y superpone las frec teoricas
@author: Publico
"""
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.nonparametric.smoothers_lowess import lowess

#importo el csv en pandas porque es mas facil, lo transpongo y elijo columnas
fname = r'C:\Users\usuario\Documents\Labo_5\esp_laser\imanes2.csv'
df = pd.read_csv(fname, sep=" ",header=None)
datos = df.transpose()

t = np.array(datos[0])
v1 = np.array(datos[1])
v = v1 - np.mean(v1)
#------------------------------

#esto me suaviza la señal asi encuentro los picos sin ruido
suave = lowess(v, t, is_sorted=True, frac=0.015, it=0)
#voltaje suave y tiempo suave
vs = suave[:,1]
ts = suave [:,0]

#Busco los ceros
ceros = np.where(np.diff(np.signbit(vs)))[0]

"""
Asumimos que la longitud de onda crece con la corriente, entonces la frecuencia disminuye con la corriente.
En el grafico la frec va de mayor a menor
Hacemos coincidir con el primer y el ultimo pico las frec mas grandes y mas chicas, segun corresponda
con eso transformamos de t a frec
"""

f2 = 377.104391324
f1 = 377.112040486
tt = t[ceros]
t1 = tt[1] #lo elegi a mano porque ve otros que en realidad no son
t2 = tt[-2] 
A = (f1-f2)/(t1-t2)
B = f1- t1*A
frec = t*A + B

#------------------

plt.plot(frec, vs)
plt.plot(frec[ceros], v[ceros], "x")
plt.vlines(x= frec[ceros], ymax = v[ceros], ymin=np.min(v), linestyle='-')

plt.ylabel('Voltaje (V)', fontsize = 10) 
plt.xlabel('Frecuencia (Thz)', fontsize = 10)

teo85 = [377.109307192, 377.108945610, 377.106271460, 377.105909878]
teo87 = [377.112040486, 377.111226006, 377.105205804, 377.104391324]

for xc in teo85:
    plt.axvline(x=xc, color='m', linestyle=':')

for xc in teo87:
    plt.axvline(x=xc, color='c', linestyle=':')

"""
Un par de cosas que pueden malir sal:
    para definir la TL tomo el primer pico del grafico y le digo que es la frec mas grande, si eso no esta bien, la TL va a ser cualquier cosa
    por ahi no agarra todos los picos y hay que ponerlos a mano
"""