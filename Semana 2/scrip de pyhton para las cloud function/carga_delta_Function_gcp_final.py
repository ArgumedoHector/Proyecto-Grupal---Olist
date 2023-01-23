from datetime import datetime
from google.cloud.storage import Blob
from google.cloud import storage
import numpy as np
import string as string
import pandas as pd
import os
import gcsfs
from io import BytesIO

def carga_delta(event, context):
    """Triggered by a change to a Cloud Storage bucket.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    file = event
    source_file_name=file['name']
    print(f"Se detectó que se subió el archivo {source_file_name}.")
    print(event)
    source_bucket_name = file['bucket']

    client = storage.Client(project="Olist")

    destination_bucket_name = 'olist_datalake'
        
    now=datetime.now()
    suf=str(now.year)+"_"+str(now.month)+"_"+str(now.day)

    nombre = source_file_name.replace("olist_","")
    nombre = nombre.replace(".csv","")
    nombre = nombre.capitalize()

    destination_file_name= nombre+"__"+suf+".csv"

    
    lista_carga = ["Closed_deals_dataset","Customers_dataset","Geolocation_dataset","Marketing_qualified_leads_dataset",
                   "Order_items_dataset","Order_payments_dataset","Order_reviews_dataset","Orders_dataset",
                   "Product_category_name_translation","Products_dataset","Sellers_dataset"]

    if nombre in  lista_carga :

    #Para el datalake

            # Obtiene los buckets
            source_bucket = client.get_bucket(source_bucket_name)
            destination_bucket = client.get_bucket(destination_bucket_name)

            # Obtiene el objeto del archivo a extraer
            source_blob = source_bucket.get_blob(source_file_name)

            # Crea un objeto blob para el archivo de destino
            destination_blob = destination_bucket.blob(destination_file_name)

            # Copia el archivo desde el bucket origen al bucket destino
            destination_blob.upload_from_string(source_blob.download_as_string())

            #Para el ETL
            new=[]

            history_bucket_name = 'historia_cargas'
            history_bucket=client.get_bucket(history_bucket_name)
            filename=list(history_bucket.list_blobs(prefix=""))
            
            blop=history_bucket.blob("historia.csv")
            data=blop.download_as_string()
            df=pd.read_csv(BytesIO(data), encoding="utf-8",sep=",")
        
            sel = df[df["Fecha"]==suf]

            if sel.shape[0]==0:
                no_chosen=[]
            else:
                no_chosen=list(sel["Archivo"])

            print(f"Archivo en proceso {nombre}, lista prohibida {no_chosen}")

            if nombre not in no_chosen :  
                new.append([suf,nombre])

                destination_bucket_name = 'olist_extrlo'
                destination_bucket = client.get_bucket(destination_bucket_name)
                destination_blob = destination_bucket.blob(destination_file_name)
                destination_blob.upload_from_string(source_blob.download_as_string())

            new = pd.DataFrame(new)
            new.columns=df.columns
            df=pd.concat([df,new])
            print("Nuevo para historial : {new}")
            df.index = range(df.shape[0])
            df.to_csv('gs://historia_cargas/historia.csv',index=False)     
            
            
            return print(f"Archivo {source_file_name} del bucket {source_bucket_name} procesado con éxito.")
    else:
        print(f"Nombre de archivo no valido esta carga, ingresaste {source_file_name}")