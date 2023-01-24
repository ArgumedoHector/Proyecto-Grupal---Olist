from google.cloud import bigquery

project_name = 'olist-374721'
bigquery_dataset = 'Datawarehouse'

schemas_id = {'customers': [
                bigquery.SchemaField("Id_customer", "STRING"),
                bigquery.SchemaField("Id_unique", "STRING"),
                bigquery.SchemaField("zip_code_prefix", "INTEGER"),
                bigquery.SchemaField("city", "STRING"),
                bigquery.SchemaField("state", "STRING"),],
                'geolocation':[
                bigquery.SchemaField("zip_code_prefix", "INTEGER"),
                bigquery.SchemaField("latitude", "FLOAT"),
                bigquery.SchemaField("longitude", "FLOAT"),
                bigquery.SchemaField("city", "STRING"),
                bigquery.SchemaField("state", "STRING"),
                bigquery.SchemaField("region", "STRING"),],
                'items':[
                bigquery.SchemaField("Id_order", "STRING"),
                bigquery.SchemaField("Id_item", "INTEGER"),
                bigquery.SchemaField("Id_product", "STRING"),
                bigquery.SchemaField("Id_seller", "STRING"),
                bigquery.SchemaField("shipping_limit_date", "TIMESTAMP"),
                bigquery.SchemaField("price", "FLOAT"),
                bigquery.SchemaField("freight_value", "FLOAT"),],
                'payments':[
                bigquery.SchemaField("Id_order", "STRING"),
                bigquery.SchemaField("payment_sequential", "INTEGER"),
                bigquery.SchemaField("payment_type", "STRING"),
                bigquery.SchemaField("payment_installments", "INTEGER"),
                bigquery.SchemaField("payment_value", "FLOAT"),],
                'reviews':[
                bigquery.SchemaField("Id_review", "STRING"),
                bigquery.SchemaField("Id_order", "STRING"),
                bigquery.SchemaField("review_score", "INTEGER"),
                bigquery.SchemaField("comment_title", "STRING"),
                bigquery.SchemaField("comment_message", "STRING"),
                bigquery.SchemaField("creation_date", "TIMESTAMP"),
                bigquery.SchemaField("answer_timestamp", "TIMESTAMP"),],
                'products':[
                bigquery.SchemaField("Id_product", "STRING"),
                bigquery.SchemaField("producto_category_name", "STRING"),
                bigquery.SchemaField("name_lenght", "FLOAT"),
                bigquery.SchemaField("description_lenght", "FLOAT"),
                bigquery.SchemaField("photos_quantity", "INTEGER"),
                bigquery.SchemaField("weight_g", "FLOAT"),
                bigquery.SchemaField("lenght_cm", "FLOAT"),
                bigquery.SchemaField("height_cm", "FLOAT"),
                bigquery.SchemaField("width_cm", "FLOAT"),],
                'sellers': [
                bigquery.SchemaField("Id_seller", "STRING"),
                bigquery.SchemaField("zip_code_prefix", "INTEGER"),
                bigquery.SchemaField("city", "STRING"),
                bigquery.SchemaField("state", "STRING"),],
                'product_category_name':[
                bigquery.SchemaField("product_category_name", "STRING"),
                bigquery.SchemaField("product_category_name_english", "STRING"),
                bigquery.SchemaField("product_category_name_spanish", "STRING"),],
                'orders':[
                bigquery.SchemaField("Id_order", "STRING"),
                bigquery.SchemaField("Id_customer", "STRING"),
                bigquery.SchemaField("order_status", "STRING"),
                bigquery.SchemaField("purchase_timestamp", "TIMESTAMP"),
                bigquery.SchemaField("order_approve_at", "TIMESTAMP"),
                bigquery.SchemaField("delivered_carrier_date", "TIMESTAMP"),
                bigquery.SchemaField("delivered_customer_date", "TIMESTAMP"),
                bigquery.SchemaField("estimated_delivery_date", "DATE"),]}

def mover_dataset_x(event,context):
    file = event
    file_name=file['name']   #se saca el nombre del archivo nuevo en el bucket ETL
    table_name = file_name.split(".")[0] # nombre del archivo sin el .csv
    print(f"Se detectó que se subió el archivo {file_name} en el bucket {file['bucket']}.")
    source_bucket_name = file['bucket'] #nombre del bucket donde esta el archivo

    # Construct a BigQuery client object.
    client = bigquery.Client()

    # TODO(developer): Set table_id to the ID of the table to create.
    # table_id = "your-project.your_dataset.your_table_name"

    source_path = "gs://"+source_bucket_name+"/"+file_name # ruta al archivo cargado en el bucket de stage
    table_id = project_name + "." + bigquery_dataset + "." + table_name 
    # table_id - ruta a la tabla a carga en big query: "nombre_del_proyecto"."nombre_de_la_base_de_datos"."nombre de la tabla"
    # cambiar nombre del proyecto y nombre de la base de datos en bigquery arriba (al inicio)  

    job_config = bigquery.LoadJobConfig(
        schema= schemas_id[table_name],
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        skip_leading_rows=1,
        # The source format defaults to CSV, so the line below is optional.
        source_format=bigquery.SourceFormat.CSV,
    )
    #poner ubicación de archivo customers
    uri = source_path

    load_job = client.load_table_from_uri(
        uri, table_id, job_config=job_config
    )  # Make an API request.

    load_job.result()  # Waits for the job to complete.

    destination_table = client.get_table(table_id)  # Make an API request.
    print("Loaded {} rows.".format(destination_table.num_rows))