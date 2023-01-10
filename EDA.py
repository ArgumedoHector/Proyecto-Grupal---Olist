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
from tqdm.notebook import tqdm
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import string as string

# %%
#asegurate de estar en carpeta : Proyecto-Grupal---Olist sino la posees creala
#os.chdir("C:/Users/Ricardo/Desktop/Proyecto-Grupal---Olist/")

# %%
#Revisando el directorio correcto
os.getcwd()

# %%

url = "https://drive.google.com/drive/folders/14DFvVrsV6zIBH0ARnArBZdUhSXcf6OYh?usp=share_link"

print("conectando con Google drive y leyendo archivos ...")

files = gdown.download_folder(url, quiet=True, use_cookies=False)
files

# %%
#Captura de los nombres de los archivos
nombres=[]
for file in files:
    lista = file.split("Datasets\\")
    nombre = lista[1].replace("olist_","").replace(".csv","").replace("_dataset","").capitalize()
    nombres.append(nombre)
    
    

# %%

for pos,file in enumerate(files) :
    
    data = pd.read_csv(file)
    print("\n")
    print("********************************")
    print(f"Carga de {nombres[pos]}")
    print("********************************")
    print("\n")

    print("Tamaño del dataset")
    print("------------------")
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
    print("\n")
    print(data.isna().sum(axis=0))
    print("\n")

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







