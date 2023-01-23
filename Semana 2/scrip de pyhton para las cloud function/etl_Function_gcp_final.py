from datetime import datetime
from google.cloud.storage import Blob
from google.cloud import storage
import numpy as np
import string as string
import pandas as pd
import os
import gcsfs
from io import BytesIO
from deep_translator import GoogleTranslator
from googletrans import Translator
import emoji
import re


def etl(event, context):    #declaramos funcion que leera el bucket de ETL
    
    file = event
    source_file_name=file['name']   #se saca el nombre del archivo nuevo en el bucket ETL
    
    print(event)
    source_bucket_name = file['bucket'] #nombre del bucket donde esta el archivo
    print(f"Se detectó que se subió el archivo {source_file_name} al bucket {source_bucket_name}.")
    client = storage.Client(project="Olist")   #declara proyecto

    destination_bucket_name = 'olist_stage'  # bucket de destino datos normalizados y tratados
    destination_file_name=file['name']  # nombre del archivo en destino
   

    #Para el etl

    # Obtiene los buckets
    source_bucket = client.get_bucket(source_bucket_name)
    destination_bucket = client.get_bucket(destination_bucket_name)

    # Obtiene el objeto del archivo a extraer
    source_blob = source_bucket.get_blob(source_file_name)

    # Crea un objeto blob para el archivo de destino
    destination_blob = destination_bucket.blob(destination_file_name)
    print("Antes de leer con pandas")
    blop=source_bucket.blob(source_file_name)
    data=blop.download_as_string()
    df=pd.read_csv(BytesIO(data), encoding="utf-8", delimiter=',')

    # se evalua el nombre del archivo para proceder al ETL

    if "Geo" in source_file_name:
        Region={'PR':'Sur','RS':'Sur','SC':'Sur','SP':'Sudeste','MG':'Sudeste','RJ':'Sudeste','ES':'Sudeste','MT':'Centro oeste', 'MS':'Centro oeste', 'GO':'Centro oeste' , 'DF':'Centro oeste',
        'AC':'Norte', 'AP':'Norte','AM':'Norte','PA':'Norte', 'RO':'Norte','RR':'Norte', 'TO':'Norte', 	
        'AL':'Nordeste','BA':'Nordeste','CE':'Nordeste','MA':'Nordeste','PB':'Nordeste','PI':'Nordeste',
        'PE':'Nordeste','RN':'Nordeste','SE':'Nordeste'}
        #Creamos la función que los va a separar en regiones
        def get_region(state):
            return Region[state]
        df = df.drop_duplicates(subset='geolocation_zip_code_prefix', keep='first')
        df['geolocation_region'] = df['geolocation_state'].apply(get_region)
        df = df.rename(columns={'geolocation_zip_code_prefix':'zip_code_prefix', 'geolocation_city':'city', 'geolocation_state':'state', 'geolocation_lat':'latitude', 'geolocation_lng':'longitude', 'geolocation_region':'region'})
        df['city']= df['city'].str.replace('ã','a')
        df.to_csv('gs://olist_stage/geolocation.csv', index=False)

    elif "Customers" in source_file_name:
        df = df.rename(columns={'customer_id':'Id_customer','customer_unique_id':'Id_unique', 'customer_zip_code_prefix':'zip_code_prefix', 'customer_city':'city', 'customer_state':'state'})
        df.to_csv('gs://olist_stage/customers.csv', index=False)

    elif "items" in source_file_name:
        df = df.rename(columns={'order_id':'Id_order', 'order_item_id':'Id_item', 'product_id':'Id_product', 'seller_id':'Id_seller'})
        df['shipping_limit_date'] = pd.to_datetime(df['shipping_limit_date'])
        df.to_csv('gs://olist_stage/items.csv', index=False)

    elif "payments" in source_file_name:
        df = df.rename(columns={'order_id':'Id_order'})
        df.to_csv('gs://olist_stage/payments.csv', index=False)

    elif "review" in source_file_name:
        df['review_comment_message'].fillna('sem_comentarios',inplace=True)
        df['review_comment_title'].fillna('sem_titulo',inplace=True)
        RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)
        def strip_emoji(text):
            return RE_EMOJI.sub(r'', text)  
        for i in range(0,100):
            df['review_comment_message'][i]=strip_emoji(df['review_comment_message'][i])
            df['review_comment_title'][i]=strip_emoji(df['review_comment_title'][i])
        df['review_comment_message'] = df['review_comment_message'].str.replace('\r\n',' ')
        df['review_comment_message'] = df['review_comment_message'].apply(lambda text: emoji.demojize(text, delimiters=("", "")))
        df['review_comment_message'] = df['review_comment_message'].str.replace(';',',')
        df['review_comment_message'] = df['review_comment_message'].str.replace('"','')
        df['review_comment_message'] = df['review_comment_message'].str.replace('\\','')
        df['review_comment_title'] = df['review_comment_title'].str.replace('\r\n',' ')  
        df['review_comment_title'] = df['review_comment_title'].apply(lambda text: emoji.demojize(text, delimiters=("", "")))
        df['review_comment_title'] = df['review_comment_title'].str.replace(';',',')
        df['review_comment_title'] = df['review_comment_title'].str.replace('"','')
        df['review_comment_title'] = df['review_comment_title'].str.replace('\\','')
        df = df.rename(columns={'review_id': 'Id_review','order_id':'Id_order', 'review_comment_message':'comment_message', 'review_creation_date':'creation_date', 'review_comment_title':'comment_title', 'review_answer_timestamp':'answer_timestamp'})
        df['creation_date'] = pd.to_datetime(df['creation_date'])
        df['answer_timestamp'] = pd.to_datetime(df['answer_timestamp'])
        df.to_csv('gs://olist_stage/reviews.csv', index=False)

    elif "Orders" in source_file_name:
        df = df.rename(columns={'order_id':'Id_order','customer_id':'Id_customer', 'order_purchase_timestamp':'purchase_timestamp', 'order_delivered_carrier_date':'delivered_carrier_date', 'order_delivered_customer_date':'delivered_customer_date', 'order_estimated_delivery_date':'estimated_delivery_date'})
        df['purchase_timestamp'] = pd.to_datetime(df['purchase_timestamp'])
        df['order_approved_at'] = pd.to_datetime(df['order_approved_at'])
        df['delivered_carrier_date'] = pd.to_datetime(df['delivered_carrier_date'])
        df['delivered_customer_date'] = pd.to_datetime(df['delivered_customer_date'])
        df['estimated_delivery_date'] = pd.to_datetime(df['estimated_delivery_date'])
        df['order_approved_at'].fillna('None',inplace=True)
        df['delivered_carrier_date'].fillna('None',inplace=True)
        df['delivered_customer_date'].fillna('None',inplace=True)
        df.to_csv('gs://olist_stage/orders.csv', index=False)

    elif "category" in source_file_name:
        translator = GoogleTranslator(source="auto", target="es")
        df['product_category_name_spanish'] = df.product_category_name_english.apply(translator.translate)
        df.to_csv('gs://olist_stage/product_category_name.csv', index=False)  

    elif "Products" in source_file_name:
        df = df.rename(columns={'product_id':'Id_product', 'product_description_lenght':'description_length', 'product_name_lenght':'name_length', 'product_weight_g':'weight_g', 'product_length_cm':'length_cm', 'product_height_cm':'height_cm', 'product_width_cm':'width_cm', 'product_photos_qty':'photos_quantity'})
        df['product_category_name'].fillna('Sin dato',inplace=True)
        df['name_length'].fillna('Sin dato',inplace=True)
        df['description_length'].fillna('Sin dato',inplace=True)
        df['photos_quantity'].fillna('Sin dato',inplace=True)
        df['weight_g'].fillna('Sin dato',inplace=True)
        df['length_cm'].fillna('Sin dato',inplace=True)
        df['height_cm'].fillna('Sin dato',inplace=True)
        df['width_cm'].fillna('Sin dato',inplace=True)
        df.to_csv('gs://olist_stage/products.csv', index=False)

    elif "Sellers" in source_file_name:
        df = df.rename(columns={'seller_id':'Id_seller', 'seller_zip_code_prefix':'zip_code_prefix', 'seller_city':'city', 'seller_state':'state'})
        df.to_csv('gs://olist_stage/sellers.csv', index=False)
      
       
      
    return print(f"Archivo {source_file_name} del bucket {source_bucket_name} procesado con éxito.")
