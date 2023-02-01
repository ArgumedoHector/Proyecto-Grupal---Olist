

# <h1 align="center">Consultora IT BROTHERS - Soluciones en Ciencia de Datos
 
## Cliente:
## <h1 align="center">E-Commerce Olist
<h1 align="center"><img src ='https://dnn65p9ixwrwn.cloudfront.net/uploads/2021/05/olist-gente-de-verdade.jpg' height = 300>


### Olist es una compañía brasileña prestadora de servicios de e-commerce para PYMES que funciona como un marketplace, es decir, funciona como “tienda de tiendas” donde diferentes vendedores pueden ofrecer sus productos a consumidores finales. 
### Esta empresa nació para potenciar el comercio minorista digital y brindar oportunidades reales de crecimiento para pequeñas, medianas y grandes empresas. Existen para eliminar obstáculos y ayudar a los minoristas a vender más. Derriban barreras y transforman lo presencial en online, acelerando los resultados para todos los emprendedores que buscan su espacio en internet .

<h1 align="center"><img src ='https://i0.wp.com/qepd.news/wp-content/uploads/2020/11/olist.jpg?fit=513%2C342&ssl=1' height = 200>
    
    
# Planteo del Proyecto:
Olist, nos contrata como consultores externos para encontrar soluciones innovadoras que permitan a sus usuarios vender sus productos a un mayor número de clientes.

Para lograr este objetivo, nos disponibiliza sus datos del período 2016 al 2018. 

Los archivos muestran diferentes dimensiones, estatus de la órdenes, precios, pagos, productos, performance de envíos a los usuarios, e incluso reviews de los mismos escritos por diversos clientes.  

Así mismo, se puede encontrar un archivo de geolocalización con todos los códigos postales de Brasil, junto con su latitud y longitud.

# OBJETIVO
- PRIMARIO 
    - Crear información de valor a Olist a través de los datos proporcionados, para la toma de
decisiones, en cuanto a la mejora del negocio del e-commerce, evaluando distintas áreas de la
empresa por ejemplo, sector ventas, registros de compras, lugares donde se llevan a cabo las
compras, entre otros.
- SECUNDARIO:
    - Confeccionar datos que se ajusten a la realidad de la empresa.
    - Confeccionar un Data Lake y un Data Warehouse que nos permita manipular los datos de forma transparente y correcta.
    - Elaborar un informe entendible para el cliente a través del uso de métricas y KPis.
    - Determinar mediante modelos predictivos sucesos que beneficien a la empresa.

    
# Datos
- En este repositorio se encuentra la carpeta Datasets que son los archivos raw en formato CSV proporcionados por Olist
- También se encuentra otra carpeta llamada Datasets_secundarios con archivos raw en formato CSV con comentarios de diferentes plataformas (Google review y Twitter).

<img src ='https://www.informatique-mania.com/wp-content/uploads/2020/12/Archivo-extension-CSV.jpg' height = 200><img src ='https://assets-global.website-files.com/602cf6148109ccfeb1d80c49/60d4509851d12743d030a9eb_5c11336dd43b9272273fb4ce_Google-Reviews.jpeg' height = 200><img src ='https://jimp.com.ar/wp-content/uploads/2017/04/twiterr.jpg' height = 150>
    
# Procesos
- Primer Semana:
   - Carga Delta de datos.
   - EDA -- (Analisis Exploratorio de Datos)
     En esta primera instancia, trabajando desde Visual Studio Code en un entorno de Python, se cargaron los primeros archivos CSV para identificar que tipo de datos se encuentran y la calidad de los mismos. Esto se detalla en el informe "IT-brothers.pdf" que además contempla el resto de los procesos.
   - ETL -- (Extracción, Transformación y Carga)
     Teniendo en cuenta los objetivos planteados se procedió a las transformaciones necesarias para que nos permita obtener datos limpios y normalizados. 
   - Creación de un diccionario de datos.
   - Carga de datos a la nube de Google Cloud Plataform, para comenzar la definición de la estructura de almacenamiento.  

 <img src ='https://miro.medium.com/max/1200/1*Ptv1_9wX9O2Rm2IBklyufw.png' height = 250> <img src ='https://sarasanalytics.com/wp-content/uploads/2022/07/ETL-using-Python.jpg' height = 250>
 
 - Segunda semana:    
   - En la Plataforma de Google Cloud (de ahora en más GCP), utilizando la herramienta Cloud Storage se estableció la estructura de Buckets. Estos Buckets permiten almacenar infromación en la nube. Destinamos uno llamado "raw" para que la empresa deposite los archivos. Otro para conformar el DATA-LAKE para almacenamiento de datos no relacionales. También se dispuso de un Bucket "Historial" donde los archivos son registrados en un documento "Historial", que se usa para evaluar si ingresan archivos distintos o si simplemente son archivos ya cargados. En caso de estar repetido, se lo descarta y sino prosigue con el proceso automatizado del flujo del dato. 
   Creamos dos buckets más para disponibilizar los datos en un Data Warehouse. El primer bucket fue llamado "extrl" que es donde llegan los datos del bucket "raw", y un bucket "staging" que es donde se ubican los archivos transformados y normalizados, listos para ser utilizados para el objetivo definido. 
   - Con Google Cloud Functions, herramienta nativa de la plataforma, se automatizaron los procesos de carga delta, movimiento de datos, y normalización, desarrollados entre los buckets y finalmente la carga a Big Query, usando como disparador una carga nueva de archivos en cada *Bucket*.
   - Creamos un DATA-WAREHOSE en BigQuery, herramienta de GCP, tomando esos archivos del Bucket "Stage" y generando tablas para ser consultadas por medio de lenguaje SQL. 
   - Link del video que resume el movimiento de los archivos: https://youtu.be/MtjFQ8BEaMk
   
<img src ='https://i.pinimg.com/originals/8c/59/60/8c5960af6cf46913129f7ef927229af7.png' height = 150> <img src ='https://miro.medium.com/max/584/1*q4EVSAndlvgFLyR6ncc4Bg.png' height = 150> <img src ='https://usercentrics.com/wp-content/uploads/2021/03/Google-BigQuery.png' height = 150>

 - Tercer semana:
   - Aplicamos la herramienta de Power BI para generar dashboards con análisis, métricas y KPIs.
   - Nuestro dashboard puede ser accedido por medio de Power BI Online con una cuenta de usuario que se dispone para el cliente. De todas maneras subimos a este repositorio el archivo descargable para que sea abierto por Power BI Desktop. LINK:https://github.com/ArgumedoHector/Proyecto-Grupal---Olist/blob/main/Semana%203/Dashboard%20Proyecto%20Olist.pbix
   - Generamos una API de consulta con FastAPI que luego dockerizamos y desplegamos utilizando Cloud Run, una herramienta nativa de GCP. LINK DE PRUEBA: https://datalake-ltanlhfs7q-uc.a.run.app/docs
   - Dejamos link a la documentacion de la API: https://github.com/ArgumedoHector/Proyecto-Grupal---Olist/blob/main/Semana%203/API%20de%20consulta.pdf
   - Preprocesamiento de datos para análisis de Machine Learning
   

<img src ='https://bharatsraj.com/wp-content/uploads/2021/05/fastapi.png' height = 150> <img src ='https://datascientest.com/es/wp-content/uploads/sites/7/2020/10/power-bi-logo-1.jpg' height = 150>


- Cuarta semana :
   - Utilizamos modelos de Machine Learning con motores de análisis de sentimientos, ya sea para mejorar proceso de ventas y/o posicionamiento de marca.
   - Se crearon varios modelos de aprendizaje: Regresión Logística Multinomial, Máquina de Soporte Vectorial, Naive Bayes Multinomial, Random Forest, y Ensamble. 
   - Los modelos de Machine Learning se desplegaron desde Streamlit. Link: https://argumedohector-proyecto-grupal---olist-streamlitmain-9lwyyz.streamlit.app/
   - Dejamos el link a la documentación de la app de Streamlit: https://github.com/ArgumedoHector/Proyecto-Grupal---Olist/blob/main/Semana%204/Streamlit%20-%20guia%20de%20uso.pdf
 
<img src ='https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1869px-Python-logo-notext.svg.png' height = 200> <img src ='https://www.fsm.ac.in/blog/wp-content/uploads/2022/08/ml-e1610553826718.jpg' height = 200> <img src ='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT-8aMOv8h5F-tVRP7LGodjG0BzAZK27_v0wh1WJ1HFcnIZiH04oW23tuCVUI_7tQdEsGI&usqp=CAU' height = 200>
 
 
# Worflow:
 ![image](https://user-images.githubusercontent.com/109697217/215760213-c90720b3-7b88-48d3-93e6-5c7afbebb526.png)
 
 
# Modelo de Machine Learning:
 - Con la tabla provista por Olist “olist_order_reviews_dataset.csv” que tiene utilizables cerca de 41000 registros, la usamos de base para armar el modelo ya que contiene comentarios y una calificación de la experiencia del usuario. 
 - Usando Python y librerías como NLTK, procedimos a la limpieza de los comentarios: eliminando usuarios, hashtags, caracteres especiales, números, URLs, etc.
 - Tokenizamos, sacamos las stopwords, y realizamos la derivación. 
 - Con el scoring, realizamos la polarización clasificando en “Positivo”, “Neutro”, y “Negativo”.
 - Para alimentar los modelos de Machine Learning, realizamos la vectorización de los comentarios, utilizando unigramas, para luego realizar el entrenamiento.
 - Seleccionamos los modelos de categorización de Regresión Logística Multinomial, SVM, Naive Bayes, Random Forest, y un modelo de Ensamble que pondera entre los 4 modelos seleccionados y toma una opción intermedia. 
 - Contando con el entrenamiento apropiado, testeamos con la propia base de Olist y con bases externas como Twitter y Google Reviews. 
 - Desplegamos en la herramienta Streamlit los modelos de machine learning para que el usuario pueda realizar sus análisis, brindando la opción de traer una base de datos propia o seleccionando alguna red social en particular.
 - Actualmente se encuentra cargada Google Reviews, y Twitter en forma demostrativa.  
 
 ![workflow ml](https://user-images.githubusercontent.com/109697217/215772679-fb794cd6-0a16-47ba-8507-bc2c7bc7b79a.jpeg)

