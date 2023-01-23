from google.cloud import bigquery,storage
import os
import re
import datetime
import json 
import gcsfs
from google.cloud.storage import Blob
from io import BytesIO
import pandas as pd

# hay que traer el dataset para ingestarlo en la funcion
# hay que extraer del dataset el nombre para ingestarlo en la funcion
def mover_dataset_x(event,context):
    file = event
    file_name=file['name']   #se saca el nombre del archivo nuevo en el bucket ETL
    print(f"Se detectó que se subió el archivo {file_name} en el bucket {file['bucket']}.")
    source_bucket_name = file['bucket'] #nombre del bucket donde esta el archivo

    client = storage.Client(project="Olist")
    client2 = bigquery.Client()
     # Obtiene los buckets
    source_bucket = client.get_bucket(source_bucket_name)
    
    # Obtiene el objeto del archivo a extraer
    source_blob = source_bucket.get_blob(file_name)

    # Crea un objeto blob para el archivo de destino
    
    blop=source_bucket.blob(file_name)
    data=blop.download_as_string()
    df=pd.read_csv(BytesIO(data), encoding="utf-8", sep=',')
    ##############################
    
    dataset = df

    dataset = bigquery.Dataset(dataset)
    #dataset.location = "europe-west3"
    dataset = client2.create_dataset(dataset)

    dataset = client2.dataset(dataset)

    job_config = bigquery.LoadJobConfig()

    #job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND

    #job_config.schema_update_options = [
    #    bigquery.SchemaUpdateOption.ALLOW_FIELD_ADDITION]
    # esquema de la tabla que va a contener el dataset
    
    if file_name == "customers.csv":

            job_config.schema = [
            bigquery.SchemaField("Id_customer", "STRING"),
            bigquery.SchemaField("Id_unique", "STRING"),
            bigquery.SchemaField("zip_code_prefix", "INTEGER"),
            bigquery.SchemaField("city", "STRING"),
            bigquery.SchemaField("state", "STRING"),]


    elif file_name=="geolocation.csv":

            job_config.schema = [
            bigquery.SchemaField("zip_code_prefix", "INTEGER"),
            bigquery.SchemaField("latitude", "GEOGRAPHY"),
            bigquery.SchemaField("longitude", "GEOGRAPHY"),
            bigquery.SchemaField("city", "STRING"),
            bigquery.SchemaField("state", "STRING"),
            bigquery.SchemaField("region", "STRING"),]

    elif file_name=="items.csv":

            job_config.schema = [
            bigquery.SchemaField("Id_order", "STRING"),
            bigquery.SchemaField("Id_item", "INTEGER"),
            bigquery.SchemaField("Id_product", "STRING"),
            bigquery.SchemaField("Id_seller", "STRING"),
            bigquery.SchemaField("shipping_limit_date", "TIMESTAMP"),
            bigquery.SchemaField("price", "FLOAT"),
            bigquery.SchemaField("freight_value", "FLOAT"),]

    elif file_name=="payments.csv":

            job_config.schema = [
            bigquery.SchemaField("Id_order", "STRING"),
            bigquery.SchemaField("payment_sequential", "INTEGER"),
            bigquery.SchemaField("payment_type", "STRING"),
            bigquery.SchemaField("payment_installments", "INTEGER"),
            bigquery.SchemaField("payment_value", "FLOAT"),]

    elif file_name=="reviews.csv":

            job_config.schema = [
            bigquery.SchemaField("Id_review", "STRING"),
            bigquery.SchemaField("Id_order", "STRING"),
            bigquery.SchemaField("review_score", "INTEGER"),
            bigquery.SchemaField("comment_title", "STRING"),
            bigquery.SchemaField("comment_message", "STRING"),
            bigquery.SchemaField("creation_date", "TIMESTAMP"),
            bigquery.SchemaField("answer_timestamp", "TIMESTAMP"),]


    elif file_name=="products.csv":

            job_config.schema = [
            bigquery.SchemaField("Id_product", "STRING"),
            bigquery.SchemaField("producto_category_name", "STRING"),
            bigquery.SchemaField("name_lenght", "FLOAT"),
            bigquery.SchemaField("description_lenght", "FLOAT"),
            bigquery.SchemaField("photos_quantity", "INTEGER"),
            bigquery.SchemaField("weight_g", "FLOAT"),
            bigquery.SchemaField("lenght_cm", "FLOAT"),
            bigquery.SchemaField("height_cm", "FLOAT"),
            bigquery.SchemaField("width_cm", "FLOAT"),]


    elif file_name=="sellers.csv":

            job_config.schema = [
            bigquery.SchemaField("Id_seller", "STRING"),
            bigquery.SchemaField("zip_code_prefix", "INTEGER"),
            bigquery.SchemaField("city", "STRING"),
            bigquery.SchemaField("state", "STRING"),]


    elif file_name=="product_category_name.csv":

            job_config.schema = [
            bigquery.SchemaField("product_category_name", "STRING"),
            bigquery.SchemaField("product_category_name_english", "STRING"),
            bigquery.SchemaField("product_category_name_spanish", "STRING"),]

    else:

            file_name=="orders.csv"

            job_config.schema = [
            bigquery.SchemaField("Id_order", "STRING"),
            bigquery.SchemaField("Id_customer", "STRING"),
            bigquery.SchemaField("order_status", "STRING"),
            bigquery.SchemaField("purchase_timestamp", "TIMESTAMP"),
            bigquery.SchemaField("order_approve_at", "TIMESTAMP"),
            bigquery.SchemaField("delivered_carrier_date", "TIMESTAMP"),
            bigquery.SchemaField("delivered_customer_date", "TIMESTAMP"),
            bigquery.SchemaField("estimated_delivery_date", "TIMESTAMP"),]

    job_config.skip_leading_rows = 1
    job_config.source_format = bigquery.SourceFormat.CSV
    uri = "gs://olist_stage/" + str(file_name)

    load_job = client.load_table_from_uri(
        uri, dataset_ref.table(dataset), job_config=job_config) 
    print("Starting job {}".format(load_job.job_id))

    load_job.result()
    print("Job finished.")

    destination_table = client.get_table(dataset.table(dataset))
    print("Loaded {} rows.".format(destination_table.num_rows))