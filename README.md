

# <h1 align="center">Consultora IT BROTHERS - Soluciones en Ciencia de Datos
 
## Cliente:
## <h1 align="center">E-Commerce Olist
<h1 align="center"><img src ='https://dnn65p9ixwrwn.cloudfront.net/uploads/2021/05/olist-gente-de-verdade.jpg' height = 300>


### Olist es una compañía brasileña prestadora de servicio e-commerce para PYMES que funciona como un marketplace, es decir, funciona como “tienda de tiendas” donde diferentes vendedores pueden ofrecer sus productos a consumidores finales. 
### Esta empresa nació para potenciar el comercio minorista digital y brindar oportunidades reales de crecimiento para pequeñas, medianas y grandes empresas. Existen para eliminar obstáculos y ayudar a los minoristas a vender más . Derriban barreras y transforman lo presencial en online, acelerando los resultados para todos los emprendedores que buscan su espacio en internet .

<h1 align="center"><img src ='https://i0.wp.com/qepd.news/wp-content/uploads/2020/11/olist.jpg?fit=513%2C342&ssl=1' height = 200>
    
    
# Planteo del Proyecto:
Olist, nos contrata como consultores externos para encontrar soluciones innovadoras que permitan a sus usuarios vender sus productos a un mayor número de clientes.

Para lograr este objetivo, nos disponibiliza sus datos periodo 2016-2018. 

Los archivos muestran diferentes dimensiones, estatus de la ordenes, precios, pagos, productos, performance de envios a los usuarios, e incluso reviews de los mismos escritos por diversos clientes.  

Asi mismo, se podra encontrar un archivo de geolocalizacion con todos los codigos postales de Brasil, junto con su latitud y longitud.

# OBJETIVO
- PRIMARIO 
    - Crear informacion de valor a Olist a través de los datos proporcionados, para la toma de
decisiones, en cuanto a la mejora del negocio del e-commerce, evaluando distintas áreas de la
empresa por ejemplo, sector ventas, registros de compras, lugares donde se llevan a cabo las
compras, entre otros.
- SECUNDARIO:
    - Elaborar un informe entendible para el cliente a través del uso de métricas y KPis,
    - Confeccionar datos que se ajusten a la realidad de la empresa,
    - Confeccionar un Data Lake o Data Warehouse que nos permita manejar los datos de forma transparente y correcta.
    - Determinar mediante modelos predictivos sucesos que beneficien a la empresa.

    
# Datos
- En este repositorio se encuentra la carpeta Datasets que son los archivos raw en formato CSV proporcionados por Olist
- Tambien se encuentra otra carpeta llamada Datasets_secundarios con archivos raw en formato CSV con comentarios de 
diferentes plataformas (Google review y Twitter).

<img src ='https://www.informatique-mania.com/wp-content/uploads/2020/12/Archivo-extension-CSV.jpg' height = 200><img src ='https://assets-global.website-files.com/602cf6148109ccfeb1d80c49/60d4509851d12743d030a9eb_5c11336dd43b9272273fb4ce_Google-Reviews.jpeg' height = 200><img src ='https://jimp.com.ar/wp-content/uploads/2017/04/twiterr.jpg' height = 200>
    
# Procesos
- Primer Semana:
   - Carga Delta de datos.
   - EDA -- (Analisis Exploratorio de Datos)
     En esta primera instancia, trabajando desde Visual Studio Code en un entorno de Python, se cargan los primeros archivos CSV 
     para identificar que tipo de datos se encuentran y la calidad de los mismos. Esto de detalla en un informe (IT-brothers.pdf) 
     que ademas contiene el resto de los procesos.
   - ETL -- (Extracción, Transformacion y Carga)
     Aqui teniendo en cuenta los objetivos planteados se procede a las transformaciones necesarias para que nos permite obtener
     datos limpios y normalizados. 
   - Creación de un diccionario de datos
   - Carga de datos a la nube de Google Cloud Plataform, donde se definirá un Data Lake o Data Warehouse.
 
 - Segunda semana:    
   - Con Google Cloud Functions, herramienta nativa de la plataforma, pretendemos automatizar los procesos anteriores utilizando cono disparador cada carga de archivos      nuevas en un *Bucket*.
   - Con la Plataforma de Google Cloud (de ahora en mas GCP), utilizando la herramienta Cloud Storage se establece varios Buckets. Estos Buckets permiten almacenar
     infromación, y destinamos uno para que la empresa deposite los archivos, otro lo destinamos a conformar el DATA-LAKE donde estara para ser consultados tantos los      archivos de la empresa Olist, asi como los que por nuestra investigacion y desarrollo sean pertinentes. Tambien dispondremos de un Bucket "Historial" donde los        archivos serán registrados en un documento Historial, que se usará para evaluar si ingresan nuevos archivos distintos o si simplemente son archivos ya cargados y      destinar los mismos al Bucket correspondiente del proceso automático. Dispondremos de un Bucket "ETL" para dejar estos archivos nuevos y que sean automaticamente      tratados y normalizados por las Cloud Functions para ser entregados al Bucket "Stage".
   - Creamos un DATA-WAREHOSE en BigQuery, herramienta de GCP, tomando esos archivos del Bucket "Stage" y creamos tablas para luego ser consultadas por medio de            lenguaje SQL. 
   
 - Tercer semana:
   - Aplicaremos la herramienta de Power BI para generar dashboards con analisis, metricas y KPIs.
   - Utilizaremos modelos de Machine Learning con motores de recomendación y/o análisis de sentimientos, ya sea para mejorar 
     proceso de ventas y/o posicionamiento de marca.
 
<img src ='https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1869px-Python-logo-notext.svg.png' height = 150><img src ='https://i.pinimg.com/originals/8c/59/60/8c5960af6cf46913129f7ef927229af7.png' height = 150><img src ='https://miro.medium.com/max/584/1*q4EVSAndlvgFLyR6ncc4Bg.png' height = 150>
