# %%
# %%
import gdown
import pandas as pd
import os
import warnings
warnings.filterwarnings("ignore")
from IPython.display import clear_output
import time
from datetime import datetime
import tqdm
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import string as string
from googletrans import Translator
from deep_translator import GoogleTranslator

# %% [markdown]
# Asegurarnos de estar en carpeta : Proyecto-Grupal---Olist sino la posees creala

# %%

#os.chdir("C:/Users/Ricardo/Desktop/Proyecto-Grupal---Olist/")

# %% [markdown]
# Revisando el directorio correcto y creando el directorio para el input al ETL. Se maneja el error en caso el directorio exista para no suspender el programa.

# %%

print(os.getcwd())
try:
    os.mkdir("ETL")
except FileExistsError as error:
    print("Directorio para ETL ya estaba creado.")

# %% [markdown]
# Accesando el link de drive 

# %%

url = "https://drive.google.com/drive/folders/14DFvVrsV6zIBH0ARnArBZdUhSXcf6OYh?usp=share_link"

print("conectando con Google drive y leyendo archivos ...")

files = gdown.download_folder(url, quiet=True, use_cookies=False)
files

# %% [markdown]
# Extraemos exclusivamente el nombre diferencial del archivo

# %%

nombres=[]
for file in files:
    lista = file.split("Datasets\\") 
    nombre = lista[1].replace("olist_","").replace(".csv","").replace("_dataset","").capitalize()
    nombres.append(nombre)
    
    

# %% [markdown]
# Entramos al bucle iterador de revisión de la data. Dentro de la transformación de fechas, el programa revisa si existe algún título de columna que contenga las palabras **date** o **stamp**, en caso de encontrarlas, se efectúa la transformación correspondiente a formato **datetime**.
# 
# Asimismo se consideran acumuladores de data en listas para obtener estadistcas del EDA.

# %%
nas=[]
sise=[]
regs=[]

for pos,file in enumerate(files) :
    
    data = pd.read_csv(file)
    
    print("\n")
    print("********************************")
    print(f"Carga de {nombres[pos]}")
    print("********************************")
    print("\n")

    print("Tamaño del dataset")
    print("------------------")
    regs.append(data.shape[0])
    print("\n")
    print(f"El dataset {nombres[pos]} contiene {data.shape[0]} filas y {data.shape[1]} columnas")
    print("\n")

    print("Muestreo de 10 registros aleatorios")
    print("-----------------------------------")
    print("\n")
    print(data.sample(10))
    print("\n")

    print("Columnas, tipo de datos y cantidad de no nulos")
    print("----------------------------------------------")
    print("\n")
    print(data.info())
    print("\n")
    
    print("Valores perdidos en el dataset :")
    print("--------------------------------")
    sise.append(data.size)
    nas.append(data.isna().sum(axis=0).sum())
    print("\n")
    print(data.isna().sum(axis=0))
    print("\n")
    print("+--------------------------------------+")
    print("| M A P A    D E    C A L O R   DE  NAs|")
    print("+--------------------------------------+")
    print("\n")
    plt.figure(figsize=(27,5))
    mapa = sns.heatmap(data.isna())
    plt.show()
    

    print("Revisión de algun campo fecha")
    print("------------------------------")
    print("\n")
    columnas = data.columns
    fecs = [col for col in columnas if "date" in col or "stamp" in col]
    for campo in fecs:
        data[campo]=pd.to_datetime(data[campo],errors="raise")

    if fecs :
        data.info()
    else:
        print(f"El archivo {nombres[pos]} no posee campos de tipo Date.")

   
    data.to_csv("ETL/"+nombres[pos]+".csv")
    print("\n")
    print("||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
    print("||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")



# %%

print("+-----------------------------------------+")
print("|          Estadisticas del EDA           |")
print("+-----------------------------------------+")
 
zippi=list(zip(nas,sise))
porc=[round(na/sise,2)*100 for (na,sise) in zippi]

fig,ax = plt.subplots()
sns.barplot(x=nombres,y=regs)
fig.autofmt_xdate(rotation=45)
plt.title("Cantidad de registros por Dataframe")
plt.xlabel("Dataframe")
plt.ylabel("# Registros")
plt.grid(True, color = "grey", linestyle = "--",alpha=0.4)
plt.show()

fig,ax = plt.subplots()
sns.barplot(x=nombres,y=porc)
fig.autofmt_xdate(rotation=45)
plt.title("Porcentaje de campos con NAs por Dataframe")
plt.xlabel("Dataframe")
plt.ylabel("% de Na's")
plt.grid(True, color = "grey", linestyle = "--",alpha=0.4)
plt.show()




