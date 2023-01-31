import streamlit as st

st.title("API - Despliegue Modelos de Machine Learning - Analisis de Sentimiento")
st.markdown('***')

c1,c2 =st.columns([3,10])

#c2.image("logo_It.png")

c2.markdown("## IT - Brothers")
c2.markdown("##### Hector Argumedo  - Data Engineer / Data Analyst")
c2.markdown("##### Lucila Alonso    - Data Engineer / Data Analyst")
c2.markdown("##### Norberto Umbert  - Data Engineer / Data Analyst")
c2.markdown("##### Ricardo Talavera - Machine Learning Engineer / Data Analyst")
c2.markdown("##### José Jimenez     - Machine Learning Engineer / Data Analyst")

st.markdown('## Nociones Generales :')

st.markdown('''El presente endpoint, es exclusivo para las personas que posean las credenciales
de acceso obtenidas a través de Google Cloud. EL Endpoint en primer lugar solicitará al usuario 
que arrastre o a través del Browser señale el corespondiente archivo JSON de autorizaciones. 
EL Endpoint desarrolla dos puntos o etapas claramente marcadas :''')

st.markdown("### Sentimiento Archivo Externo")
st.markdown('''
1. Recepción de credenciales y autentificación del usuario con Google Clouds.
2. De estar el usuario correctamente autorizado, el endpoint solicitará el o los modelos a Google Cloud
3. Se solicitará al usuario el ingreso mediante arrastre o por browse, del archivo csv de comentarios.
4. Se emitirán las predicciones acerca del Sentimiento según el ejecutable del modelo o modelos escogidos.

''')

st.markdown('#### Archivo de Comentarios :')

st.markdown('''El archivo de comentarios deberá estar en formato CSV y el dataset deberá contener
una sola columna , conteniendo los comentarios. Se recomienda efectuar requests que no excedan los
5000 registros. Los comentarios pueden estar en cualquier idioma, el Endpoint maneja traductor 
universal y trasladará todo comentario en cualquier idioma registrado por Google hacia el idioma 
portugués.''')

st.markdown('#### Outputs :')
st.markdown('''El Endpoint emitirá dos gráficos de distribución : un diagrama de pie, un gráfico
de barras y un wordcloud de terminos negativos, todos con los resultados de sentimiento calculado. 
Asimismo el Endpoint generará un archivo csv con los comentarios procesados y su resultado correspondiente en cálculo de 
sentimiento, el archivo mencionado podrá ser bajado a solicitud del usuario.''')

st.markdown("### Sentimiento Redes Sociales")
st.markdown('''
1. Recepción de credenciales y autentificación del usuario con Google Clouds.
2. De estar el usuario correctamente autorizado, el endpoint solicitará el o los modelos a Google Cloud
3. Se solicitará al usuario decida por consultar la red social twitter y/o las busquedas de Google.
4. Se emitirán las predicciones acerca del Sentimiento según el ejecutable del modelo o modelos escogidos.''')

st.markdown('#### Red Social Twitter :')

st.markdown('''El acceso a la red social **Twitter**, será en tiempo real, la búsqueda  puede traer
muchos registros, por razones de procesamiento se restringen los requests a 1000 Tweets. 
El proceso de conexión a la red de twitter es interno, por lo que el usuario solo deberá escoger la
opción. El proceso interno entre otras cosas trasladará todo comentario en cualquier idioma 
registrado por Google hacia el idioma portugués.''')

st.markdown('#### Google :')

st.markdown('''Se tiene acceso también a las búsquedas de **Google**, con la diferencia, 
que las tablas de Google serán actualizadas cada 6 meses o a pedido del usuario. Las tablas actuales
se encuentran almacenadas en un bucket de Google Cloud. Son más de 10,000 registros, por tanto
por razones de procesamiento también se restringen los requests a 1000 registros. 
El proceso de conexión a Google Cloud es interno, por lo que el usuario solo deberá escoger la
opción. El proceso interno entre otras cosas trasladará todo comentario en cualquier idioma 
registrado por Google hacia el idioma portugués.''')