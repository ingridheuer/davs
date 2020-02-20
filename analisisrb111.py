# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 10:13:59 2020
Analisis de espectro de absorción del RB
Que hace:
    Carga los datos de un csv con pandas y los pasa a np
    Endereza el grafico
    Busca los picos
    Arma transformación para pasar de t a frec
    Plotea y superpone las frec teoricas
@author: Publico
"""
from matplotlib import pyplot as plt
import numpy as np
from scipy.signal import find_peaks
import pandas as pd
from statsmodels.nonparametric.smoothers_lowess import lowess

#importo el csv en pandas porque es mas facil, lo transpongo y elijo columnas
fname = r'C:\Users\usuario\Documents\Labo_5\esp_laser\imanes1.csv'
df = pd.read_csv(fname, sep=" ",header=None)
datos = df.transpose()

t = np.array(datos[0])
v1 = np.array(datos[1])
#------------------------------

#busco la pendiente para enderezar el grafico
m = (v1[-1] - v1[0])/(t[-1] - t[0])
#voltaje derecho:
v = v1-m*t

#esto me suaviza la señal asi encuentro los picos sin ruido
suave = lowess(v, t, is_sorted=True, frac=0.025, it=0)
#voltaje suave y tiempo suave
vs = suave[:,1]
ts = suave [:,0]

#Busco los picos y los grafico. Si no pongo los parametros no me devuelve el dict
peaks, _ = find_peaks(-vs, height=0, prominence=0.0001)  #Cambiar prominence si no agarra todos los picos
  
"""
Asumimos que la longitud de onda crece con la corriente, entonces la frecuencia disminuye con la corriente.
En el grafico la frec va de mayor a menor
Hacemos coincidir con el primer y el ultimo pico las frec mas grandes y mas chicas, segun corresponda
con eso transformamos de t a frec
"""

f2 = 377.1045949440209
f1 = 377.1120404866318
tt = t[peaks]
t1 = tt[0]
A = -3.614915879020313 #esto quedo de un analisis anterior
B = f1- t1*A
frec = t*A + B
#------------------

plt.plot(frec, -v)
plt.plot(frec[peaks], -v[peaks], "x")
plt.vlines(x= frec[peaks], ymax = -v[peaks], ymin=np.min(-v), linestyle='-')

#para poner piquitos a mano. esta medio choto pero es lo que hay
abs1 = np.abs(frec - 377.10439) #poner acá la frecuencia aproximada
abs2 = np.abs(frec - 377.111)
index1 = abs1.argmin()
index2 = abs2.argmin()
p1 = frec[index1]
p2 = frec[index2]
y1 = -v[index1]
y2 = -v[index2]
p = ([p1,p2])
y = ([y1,y2])

plt.plot(p,y, "x")
plt.vlines(x=p, ymax = y, ymin=np.min(-v), linestyle='-')

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