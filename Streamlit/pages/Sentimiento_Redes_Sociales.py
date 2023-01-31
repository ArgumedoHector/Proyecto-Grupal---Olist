import snscrape.modules.twitter as sntwitter
import base64
import streamlit as st
import warnings
import joblib
from sklearn.ensemble import VotingClassifier
from tempfile import TemporaryFile
warnings.filterwarnings("ignore")
from google.oauth2 import service_account
from google.cloud import storage
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from io import StringIO
import json
import os
import pandas as pd
from deep_translator import GoogleTranslator
import PIL.Image
import re
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import style
from textblob import TextBlob
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer,SnowballStemmer
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
import time
import datetime as time2
from sklearn.metrics import accuracy_score,classification_report,confusion_matrix,ConfusionMatrixDisplay
stop_words = {'a', 'ao', 'aos', 'aquela', 'aquelas', 'aquele', 'aqueles', 'aquilo', 'as', 'até',
 'com', 'como', 'da', 'das', 'de', 'dela', 'delas', 'dele', 'deles', 'depois', 'do', 'dos', 'e',
 'ela', 'elas', 'ele', 'eles', 'em', 'entre', 'era', 'eram', 'essa', 'essas', 'esse', 'esses',
 'esta', 'estamos', 'estar', 'estas', 'estava', 'estavam', 'este', 'esteja', 'estejam', 'estejamos',
 'estes', 'esteve', 'estive', 'estivemos', 'estiver', 'estivera', 'estiveram', 'estiverem',
 'estivermos', 'estivesse', 'estivessem', 'estivéramos', 'estivéssemos', 'estou', 'está',
 'estávamos', 'estão', 'eu', 'foi', 'fomos', 'for', 'fora', 'foram', 'forem', 'formos', 'fosse',
 'fossem', 'fui', 'fôramos', 'fôssemos', 'haja', 'hajam', 'hajamos', 'havemos', 'haver', 'hei',
 'houve', 'houvemos', 'houver', 'houvera', 'houveram', 'houverei', 'houverem', 'houveremos',
 'houveria', 'houveriam', 'houvermos', 'houverá', 'houverão', 'houveríamos', 'houvesse',
 'houvessem', 'houvéramos', 'houvéssemos', 'há', 'hão', 'isso', 'isto', 'já', 'lhe', 'lhes', 'mais',
 'mas', 'me', 'mesmo', 'meu', 'meus', 'minha', 'minhas', 'muito', 'na', 'nas', 'nem', 'no', 'nos',
 'nossa', 'nossas', 'nosso', 'nossos', 'num', 'numa', 'não', 'nós', 'o', 'os', 'ou', 'para', 'pela',
 'pelas', 'pelo', 'pelos', 'por', 'qual', 'quando', 'que', 'quem', 'se', 'seja', 'sejam', 'sejamos',
 'sem', 'ser', 'serei', 'seremos', 'seria', 'seriam', 'será', 'serão', 'seríamos', 'seu', 'seus',
 'somos', 'sou', 'sua', 'suas', 'são', 'só', 'também', 'te', 'tem', 'temos', 'tenha', 'tenham',
 'tenhamos', 'tenho', 'terei', 'teremos', 'teria', 'teriam', 'terá', 'terão', 'teríamos', 'teu',
 'teus', 'teve', 'tinha', 'tinham', 'tive', 'tivemos', 'tiver', 'tivera', 'tiveram', 'tiverem',
 'tivermos', 'tivesse', 'tivessem', 'tivéramos', 'tivéssemos', 'tu', 'tua', 'tuas', 'tém', 'tínhamos',
 'um', 'uma', 'você', 'vocês', 'vos', 'à', 'às', 'é', 'éramos'}

c1,c2 =st.columns([3,10])

#c2.image("Logo_It.png")


st.title("Sentimiento en Redes Sociales")
st.markdown('***')

st.markdown("## Ingreso de Credenciales")

uploaded_file = st.file_uploader("Choose your json credentials")
if uploaded_file is not None:

    if uploaded_file.name[-5:] == ".json":
            bytes_data = json.load(uploaded_file)
            
            with open('data.json', 'w') as file:
                json.dump(bytes_data, file, indent=4)
            
            st.write("Starting authentication ... ")
            
            storage_client = storage.Client.from_service_account_json("data.json")
            
            bucket =storage_client.get_bucket("exit_model")

            st.write("authentication confirmed ...")
            

            blob = bucket.blob("log.joblib")

            with TemporaryFile() as temp_file:
                blob.download_to_file(temp_file)
                temp_file.seek(0)
                log=joblib.load(temp_file)

            blob = bucket.blob("vect.joblib")

            with TemporaryFile() as temp_file:
                blob.download_to_file(temp_file)
                temp_file.seek(0)
                vect=joblib.load(temp_file)

            blob = bucket.blob("svm.joblib")

            with TemporaryFile() as temp_file:
                blob.download_to_file(temp_file)
                temp_file.seek(0)
                svm=joblib.load(temp_file)

            blob = bucket.blob("MNB.joblib")

            with TemporaryFile() as temp_file:
                blob.download_to_file(temp_file)
                temp_file.seek(0)
                MNB=joblib.load(temp_file)

            blob = bucket.blob("RF.joblib")

            with TemporaryFile() as temp_file:
                blob.download_to_file(temp_file)
                temp_file.seek(0)
                RF=joblib.load(temp_file)

            blob = bucket.blob("ensamble.joblib")

            with TemporaryFile() as temp_file:
                blob.download_to_file(temp_file)
                temp_file.seek(0)
                ensamble=joblib.load(temp_file)

            st.write("Modelos cargados, vectorización cargada ...")
            

            st.write(":heavy_minus_sign:" * 32)

            st.markdown("## Modelos disponibles :")

            a=st.checkbox("Regresión Logistica Multinomial")
            b=st.checkbox("Maquina de Soporte Vectorial")
            c=st.checkbox("Naive Bayes Multinomial")
            d=st.checkbox("Random Forest")
            e=st.checkbox("Ensamble")

            if not (a or b or c or d or e):
                a=True
                b=True
                c=True
                d=True
                e=True

            st.write(":heavy_minus_sign:" * 32)

            st.markdown("## Fuentes disponibles de consulta :")

            opc = st.radio("Elija la fuente :", ("Acceso en tiempo real a Twitter (1000 tweets)",
             "Acceso a tablas batch de Google (1000 comentarios)"))
            

            if opc== "Acceso en tiempo real a Twitter (1000 tweets)":
                st.write("Descargando tweets en tiempo real ...")
                query="Olist"
                usu=["olistbr","olistnigeria","cpubipolar","gpubipolar","rambipolar"]
                tweets=[]
                con=0

                for tweet in sntwitter.TwitterSearchScraper(query).get_items():
                    if query in tweet.content and tweet.user.username not in usu:
                        con+=1
                        tweets.append([tweet.date, tweet.user.username, tweet.content, tweet.lang])
                    if con == 100:
                        break
                
                st.write("Se descargaron ",con," tweets")

                data= pd.DataFrame(tweets, columns=["Date", "User", "Tweet", "Lang"])

                percent_complete=0
                my_bar = st.progress(0)
                st.write("Cleaning, translating ...")
                time0= time2.datetime.now()

                for i,tweet in enumerate(data["Tweet"]):

                    delta = round(1/len(data["Tweet"]),3)
                    percent_complete = percent_complete + delta
                    if percent_complete >1:
                        percent_complete = 1
                    dif = time2.datetime.now()-time0
                    time.sleep(dif.seconds)
                    my_bar.progress(percent_complete)

                    text=data["Tweet"].iloc[i]
                    text=text.lower()
                    #re.sub(cadena a buscar, con la que se reemplaza, cadena leida)
                    url= ('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
                    menciones='@[\w\-]+'
                    hashtag='#[\w\-]+'
                    caracteres_especiales=r'\W'
                    caracter_individual=r'\s+[a-zA-Z]\s+'
                    caracter_individual_inicio=r'\^[a-zA-Z]\s+'
                    varios_espacios = r'\s+'
                    numeros='[0-9]+'
                    prefijo_b=r'^b\s+'
                    text=re.sub(url,' ',text)
                    text=re.sub(menciones,' ',text)
                    text=re.sub(hashtag,' ',text)
                    text=re.sub(caracteres_especiales,' ',text)
                    text=re.sub(caracter_individual_inicio,' ',text)
                    text=re.sub(caracter_individual,' ',text)
                    text=re.sub(varios_espacios,' ',text)
                    text=re.sub(numeros,' ',text)
                    text=re.sub(prefijo_b,' ',text)
                        
                    translator = GoogleTranslator(source="auto", target="pt")
                    text = translator.translate(text)
                    #stop_words = set(stopwords.words('portuguese'))
                    text_tokens=word_tokenize(text)
                    filtered_text=[w for w in text_tokens if not w in stop_words]
                        
                    data["Tweet"].iloc[i]= " ".join(filtered_text)
                    time0= time2.datetime.now()        
                    
                stemmer= PorterStemmer()
                def steaming(text):
                    text= stemmer.stem(text)
                    return text

                data["Tweet"]=data["Tweet"].apply(lambda x : steaming(x))

                data=data[data["User"]!="olistbr"]
                data=data[data["User"]!="olistnigeria"]
                data=data[data["User"]!="cpubipolar"]
                data=data[data["User"]!="gpubipolar"]
                data=data[data["User"]!="rambipolar"]

                largo=[len(s) for s in data["Tweet"]]
                data["largo"]=largo
                data=data[data["largo"]>2]
                data.drop(["largo"],axis=1,inplace = True)
                
                st.write(":heavy_minus_sign:" * 32)

                st.markdown("## Predicción de Sentimiento de Marca Olist en Tweeter...")
                
                X=data["Tweet"]
                X=vect.transform(X)

                def sentiment(polar):
                    if polar ==0:
                        return("Negative")
                    elif polar ==1:
                        return("Neutral")
                    else:
                        return("Positive")

                if a:
                        ypred_log = log.predict(X)
                        data["Sentimiento_log"]=ypred_log
                        
                        st.markdown("### Resultados Regresión Logistica Multinomial")

                        fig, (ax2,ax3) = plt.subplots(1,2,figsize=(15,5))
                        colors=("yellowgreen","red","gold")                      
                        
                        wp={"linewidth":2,"edgecolor":"black"}
                        tags= data["Sentimiento_log"].value_counts()
                        orden=tags.index
                        if len(data["Sentimiento_log"].unique())==2:
                            explode = (0.1,0.1)
                            
                        else:
                            explode = (0.1,0.1,0.1)

                        ax2.pie(x=tags,explode=explode,colors=colors,labels=orden,
                                autopct='%1.1f%%',shadow=True,startangle=90,wedgeprops= wp)
                        ax2.set_title("Distribution of Sentiments for Olist - LOG")
                        
                        negative=data[data["Sentimiento_log"]=="Negative"]
                        text_neg= " ".join ([word for word in negative["Tweet"]])
                        wordcloud= WordCloud(max_words=500,width=1600,height=800).generate(text_neg)
                        ax3.imshow(wordcloud,interpolation="bilinear")
                        ax3.axis("off")
                        ax3.set_title("Negative Comments - LOG", fontsize=19)

                        st.pyplot(fig)

                if b:
                        ypred_svm = svm.predict(X)
                        data["Sentimiento_svm"]=ypred_svm
                        data["Sentimiento_svm"]=data["Sentimiento_svm"].apply(sentiment)

                        st.markdown("### Resultados Maquina de Soporte Vectorial")

                        fig, (ax2,ax3) = plt.subplots(1,2,figsize=(15,5))
                        colors=("yellowgreen","red","gold")
                                                
                        
                        wp={"linewidth":2,"edgecolor":"black"}
                        tags= data["Sentimiento_svm"].value_counts()
                        orden=tags.index
                        if len(data["Sentimiento_svm"].unique())==2:
                            explode = (0.1,0.1)
                            
                        else:
                            explode = (0.1,0.1,0.1)

                        ax2.pie(x=tags,explode=explode,colors=colors,labels=orden,
                                autopct='%1.1f%%',shadow=True,startangle=90,wedgeprops= wp)
                        ax2.set_title("Distribution of Sentiments for Olist - SVM")
                        
                        negative=data[data["Sentimiento_svm"]=="Negative"]
                        text_neg= " ".join ([word for word in negative["Tweet"]])
                        wordcloud= WordCloud(max_words=500,width=1600,height=800).generate(text_neg)
                        ax3.imshow(wordcloud,interpolation="bilinear")
                        ax3.axis("off")
                        ax3.set_title("Negative Comments - SVM", fontsize=19)

                        st.pyplot(fig)


                if c:
                        ypred_MNB = MNB.predict(X)
                        data["Sentimiento_mnb"]=ypred_MNB
                        data["Sentimiento_mnb"]=data["Sentimiento_mnb"].apply(sentiment)

                        st.markdown("### Resultados Multinomial Naive Bayes")

                        fig, (ax2,ax3) = plt.subplots(1,2,figsize=(15,5))
                        colors=("yellowgreen","red","gold")
                                                
                        wp={"linewidth":2,"edgecolor":"black"}
                        tags= data["Sentimiento_mnb"].value_counts()
                        orden=tags.index
                        if len(data["Sentimiento_mnb"].unique())==2:
                            explode = (0.1,0.1)
                            
                        else:
                            explode = (0.1,0.1,0.1)

                        ax2.pie(x=tags,explode=explode,colors=colors,labels=orden,
                                autopct='%1.1f%%',shadow=True,startangle=90,wedgeprops= wp)
                        ax2.set_title("Distribution of Sentiments for Olist - MNB")
                        
                        negative=data[data["Sentimiento_mnb"]=="Negative"]
                        text_neg= " ".join ([word for word in negative["Tweet"]])
                        wordcloud= WordCloud(max_words=500,width=1600,height=800).generate(text_neg)
                        ax3.imshow(wordcloud,interpolation="bilinear")
                        ax3.axis("off")
                        ax3.set_title("Negative Comments - MNB", fontsize=19)

                        st.pyplot(fig)

                if d:
                        ypred_RF = RF.predict(X)
                        data["Sentimiento_rf"]=ypred_RF
                        data["Sentimiento_rf"]=data["Sentimiento_rf"].apply(sentiment)

                        st.markdown("### Resultados Random Forest")

                        fig, (ax2,ax3) = plt.subplots(1,2,figsize=(15,5))
                        colors=("yellowgreen","red","gold")
                                                
                        wp={"linewidth":2,"edgecolor":"black"}
                        tags= data["Sentimiento_rf"].value_counts()
                        orden=tags.index
                        if len(data["Sentimiento_rf"].unique())==2:
                            explode = (0.1,0.1)
                            
                        else:
                            explode = (0.1,0.1,0.1)

                        ax2.pie(x=tags,explode=explode,colors=colors,labels=orden,
                                autopct='%1.1f%%',shadow=True,startangle=90,wedgeprops= wp)
                        ax2.set_title("Distribution of Sentiments for Olist - RF")
                        
                        negative=data[data["Sentimiento_rf"]=="Negative"]
                        text_neg= " ".join ([word for word in negative["Tweet"]])
                        wordcloud= WordCloud(max_words=500,width=1600,height=800).generate(text_neg)
                        ax3.imshow(wordcloud,interpolation="bilinear")
                        ax3.axis("off")
                        ax3.set_title("Negative Comments - RF", fontsize=19)

                        st.pyplot(fig)

                if e:
                        
                        ypred_ens = ensamble.predict(X)
                        data["Sentimiento_ens"]=ypred_ens
                        data["Sentimiento_ens"]=data["Sentimiento_ens"].apply(sentiment)
                        
                        st.markdown("### Resultados Ensamble")

                        fig, (ax2,ax3) = plt.subplots(1,2,figsize=(15,5))
                        colors=("yellowgreen","red","gold")
                        
                        
                      
                        wp={"linewidth":2,"edgecolor":"black"}
                        tags= data["Sentimiento_ens"].value_counts()
                        orden=tags.index
                        if len(data["Sentimiento_ens"].unique())==2:
                            explode = (0.1,0.1)
                            
                        else:
                            explode = (0.1,0.1,0.1)

                        ax2.pie(x=tags,explode=explode,colors=colors,labels=orden,
                                autopct='%1.1f%%',shadow=True,startangle=90,wedgeprops= wp)
                        ax2.set_title("Distribution of Sentiments for Olist - ENS")
                        
                        negative=data[data["Sentimiento_ens"]=="Negative"]
                        text_neg= " ".join ([word for word in negative["Tweet"]])
                        wordcloud= WordCloud(max_words=500,width=1600,height=800).generate(text_neg)
                        ax3.imshow(wordcloud,interpolation="bilinear")
                        ax3.axis("off")
                        ax3.set_title("Negative Comments - ENS", fontsize=19)

                        st.pyplot(fig)

                st.markdown("# --> Predicción Finalizada de Olist en Tweeter <--")
                st.write(data)
                
                if st.button("Download CSV"):
                        csv = data.to_csv(index=False)
                        b64 = base64.b64encode(csv.encode()).decode()  # encode CSV file as base64
                        href = f'<a href="data:file/csv;base64,{b64}" download="tweets.csv">Download CSV file</a>'
                        st.markdown(href, unsafe_allow_html=True)


                

                st.write(":heavy_minus_sign:" * 32)

            if opc == "Acceso a tablas batch de Google (1000 comentarios)" :

                st.write("Conectando con Google Cloud y leyendo archivos del bucket de Machine Learning ...")
                bucket =storage_client.get_bucket("exit_model")
                nombres=[]
                filename=list(bucket.list_blobs(prefix="google_files/google"))
                vez=0
                for name in filename:
                    vez+=1
                    blop=bucket.blob(name.name)
                    nombre=name.name.replace("google_files/","")
                    df=blop.download_to_filename(nombre)
                    df=pd.read_csv(nombre)
                    nombres.append(nombre)
                    if vez == 1:
                        google_df=df
                    else:
                        google_df=pd.concat([google_df,df])

                for file in nombres:
                    os.remove(file)

                # eliminamos registros duplicados
                google_df.drop_duplicates(inplace=True)

                # eliminar columnas que no sirven para nuestro analisis de sentiminetos
                google_df.drop(columns=['WEBjve href','NBa7we src','eaLgGf src','hCCjke src','hCCjke src 2'], inplace=True)
                google_df.drop(columns=['hCCjke src 3','hCCjke src 4','hCCjke src 5'], inplace=True)
                google_df.drop(columns=['dSlJg src','dSlJg src 2'], inplace=True)
                google_df.drop(columns=['pkWtMe','w8nwRe', 'znYl0'], inplace=True)

                # quitamos indice distorsionado
                google_df=google_df.reset_index(drop=True)

                # llenamos NaN con vacios 
                google_df['wiI7pd']=google_df['wiI7pd'].fillna('')

                # convertimos toad la columna de comentarios a string
                google_df['wiI7pd']=google_df['wiI7pd'].apply(str)

                # se pasa todos los comentarios a minusculas
                for i in range(0, 4567):
                    google_df.loc[i,'wiI7pd']=google_df.loc[i,'wiI7pd'].lower()

                # quitamos el texto repetido de los comentarios
                texto='(traducción de google) '
                for i in range(0, 4567):
                    if texto in google_df.loc[i,'wiI7pd']:
                        google_df.loc[i,'wiI7pd']=google_df.loc[i,'wiI7pd'].replace(texto,'')


                percent_complete=0
                my_bar = st.progress(0)
                st.write("Cleaning, translating ...")
                time0= time2.datetime.now()

                google_df=google_df.head(100)

                for i,goog in enumerate(google_df["wiI7pd"]):

                    delta = round(1/len(google_df["wiI7pd"]),3)
                    percent_complete = percent_complete + delta
                    if percent_complete >1:
                        percent_complete = 1
                    dif = time2.datetime.now()-time0
                    time.sleep(dif.seconds)
                    my_bar.progress(percent_complete)

                    text=google_df["wiI7pd"].iloc[i]
                    text=text.lower()
                    #re.sub(cadena a buscar, con la que se reemplaza, cadena leida)
                    url= ('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
                    menciones='@[\w\-]+'
                    hashtag='#[\w\-]+'
                    caracteres_especiales=r'\W'
                    caracter_individual=r'\s+[a-zA-Z]\s+'
                    caracter_individual_inicio=r'\^[a-zA-Z]\s+'
                    varios_espacios = r'\s+'
                    numeros='[0-9]+'
                    prefijo_b=r'^b\s+'
                    text=re.sub(url,' ',text)
                    text=re.sub(menciones,' ',text)
                    text=re.sub(hashtag,' ',text)
                    text=re.sub(caracteres_especiales,' ',text)
                    text=re.sub(caracter_individual_inicio,' ',text)
                    text=re.sub(caracter_individual,' ',text)
                    text=re.sub(varios_espacios,' ',text)
                    text=re.sub(numeros,' ',text)
                    text=re.sub(prefijo_b,' ',text)
                        
                    translator = GoogleTranslator(source="auto", target="pt")
                    text = translator.translate(text)
                    #stop_words = set(stopwords.words('portuguese'))
                    text_tokens=word_tokenize(text)
                    filtered_text=[w for w in text_tokens if not w in stop_words]
                        
                    google_df["wiI7pd"].iloc[i]= " ".join(filtered_text)
                    time0= time2.datetime.now()   

                largo=[len(s) for s in google_df["wiI7pd"]]
                google_df["largo"]=largo
                google_df=google_df[google_df["largo"]>2]
                google_df.drop(["largo"],axis=1,inplace = True)     
                    
                stemmer= PorterStemmer()
                def steaming(text):
                    text= stemmer.stem(text)
                    return text

                google_df["wiI7pd"]=google_df["wiI7pd"].apply(lambda x : steaming(x))


                st.write(":heavy_minus_sign:" * 32)

                st.markdown("## Predicción de Sentimiento de Marca Olist en Google...")

                X=google_df["wiI7pd"]
                X=vect.transform(X)
              
                def sentiment(polar):

                    if polar ==0:
                        return("Negative")
                    elif polar ==1:
                        return("Neutral")
                    else:
                        return("Positive")

                if a:
                        ypred_log = log.predict(X)
                        google_df["Sentimiento_log"]=ypred_log
                        
                        st.markdown("### Resultados Regresión Logistica Multinomial")

                        fig, (ax2,ax3) = plt.subplots(1,2,figsize=(15,5))
                        colors=("yellowgreen","red","gold")
                                                
                        
                        wp={"linewidth":2,"edgecolor":"black"}
                        tags= google_df["Sentimiento_log"].value_counts()
                        orden=tags.index
                        if len(google_df["Sentimiento_log"].unique())==2:
                            explode = (0.1,0.1)
                            
                        else:
                            explode = (0.1,0.1,0.1)

                        ax2.pie(x=tags,explode=explode,colors=colors,labels=orden,
                                autopct='%1.1f%%',shadow=True,startangle=90,wedgeprops= wp)
                        ax2.set_title("Distribution of Sentiments for Olist - LOG")
                        
                        negative=google_df[google_df["Sentimiento_log"]=="Negative"]
                        text_neg= " ".join ([word for word in negative["wiI7pd"]])
                        wordcloud= WordCloud(max_words=500,width=1600,height=800).generate(text_neg)
                        ax3.imshow(wordcloud,interpolation="bilinear")
                        ax3.axis("off")
                        ax3.set_title("Negative Comments - LOG", fontsize=19)

                        st.pyplot(fig)

                if b:
                        ypred_svm = svm.predict(X)
                        google_df["Sentimiento_svm"]=ypred_svm
                        google_df["Sentimiento_svm"]=google_df["Sentimiento_svm"].apply(sentiment)

                        st.markdown("### Resultados Maquina de Soporte Vectorial")

                        fig, (ax2,ax3) = plt.subplots(1,2,figsize=(15,5))
                        colors=("yellowgreen","red","gold")
                                                
                        
                        wp={"linewidth":2,"edgecolor":"black"}
                        tags= google_df["Sentimiento_svm"].value_counts()
                        orden=tags.index
                        if len(google_df["Sentimiento_svm"].unique())==2:
                            explode = (0.1,0.1)
                            
                        else:
                            explode = (0.1,0.1,0.1)

                        ax2.pie(x=tags,explode=explode,colors=colors,labels=orden,
                                autopct='%1.1f%%',shadow=True,startangle=90,wedgeprops= wp)
                        ax2.set_title("Distribution of Sentiments for Olist - SVM")
                        
                        negative=google_df[google_df["Sentimiento_svm"]=="Negative"]
                        text_neg= " ".join ([word for word in negative["wiI7pd"]])
                        wordcloud= WordCloud(max_words=500,width=1600,height=800).generate(text_neg)
                        ax3.imshow(wordcloud,interpolation="bilinear")
                        ax3.axis("off")
                        ax3.set_title("Negative Comments - SVM", fontsize=19)

                        st.pyplot(fig)


                if c:
                        ypred_MNB = MNB.predict(X)
                        google_df["Sentimiento_mnb"]=ypred_MNB
                        google_df["Sentimiento_mnb"]=google_df["Sentimiento_mnb"].apply(sentiment)

                        st.markdown("### Resultados Multinomial Naive Bayes")

                        fig, (ax2,ax3) = plt.subplots(1,2,figsize=(15,5))
                        colors=("yellowgreen","red","gold")
                                                
                        wp={"linewidth":2,"edgecolor":"black"}
                        tags= google_df["Sentimiento_mnb"].value_counts()
                        orden=tags.index
                        if len(google_df["Sentimiento_mnb"].unique())==2:
                            explode = (0.1,0.1)
                            
                        else:
                            explode = (0.1,0.1,0.1)

                        ax2.pie(x=tags,explode=explode,colors=colors,labels=orden,
                                autopct='%1.1f%%',shadow=True,startangle=90,wedgeprops= wp)
                        ax2.set_title("Distribution of Sentiments for Olist - MNB")
                        
                        negative=google_df[google_df["Sentimiento_mnb"]=="Negative"]
                        text_neg= " ".join ([word for word in negative["wiI7pd"]])
                        wordcloud= WordCloud(max_words=500,width=1600,height=800).generate(text_neg)
                        ax3.imshow(wordcloud,interpolation="bilinear")
                        ax3.axis("off")
                        ax3.set_title("Negative Comments - MNB", fontsize=19)

                        st.pyplot(fig)

                if d:
                        ypred_RF = RF.predict(X)
                        google_df["Sentimiento_rf"]=ypred_RF
                        google_df["Sentimiento_rf"]=google_df["Sentimiento_rf"].apply(sentiment)

                        st.markdown("### Resultados Random Forest")

                        fig, (ax2,ax3) = plt.subplots(1,2,figsize=(15,5))
                        colors=("yellowgreen","red","gold")
                                                
                        wp={"linewidth":2,"edgecolor":"black"}
                        tags= google_df["Sentimiento_rf"].value_counts()
                        orden=tags.index
                        if len(google_df["Sentimiento_rf"].unique())==2:
                            explode = (0.1,0.1)
                            
                        else:
                            explode = (0.1,0.1,0.1)

                        ax2.pie(x=tags,explode=explode,colors=colors,labels=orden,
                                autopct='%1.1f%%',shadow=True,startangle=90,wedgeprops= wp)
                        ax2.set_title("Distribution of Sentiments for Olist - RF")
                        
                        negative=google_df[google_df["Sentimiento_rf"]=="Negative"]
                        text_neg= " ".join ([word for word in negative["wiI7pd"]])
                        wordcloud= WordCloud(max_words=500,width=1600,height=800).generate(text_neg)
                        ax3.imshow(wordcloud,interpolation="bilinear")
                        ax3.axis("off")
                        ax3.set_title("Negative Comments - RF", fontsize=19)

                        st.pyplot(fig)

                if e:
                        
                        ypred_ens = ensamble.predict(X)
                        google_df["Sentimiento_ens"]=ypred_ens
                        google_df["Sentimiento_ens"]=google_df["Sentimiento_ens"].apply(sentiment)
                        
                        st.markdown("### Resultados Ensamble")

                        fig, (ax2,ax3) = plt.subplots(1,2,figsize=(15,5))
                        colors=("yellowgreen","red","gold")
                                                
                        wp={"linewidth":2,"edgecolor":"black"}
                        tags= google_df["Sentimiento_ens"].value_counts()
                        orden=tags.index
                        if len(google_df["Sentimiento_ens"].unique())==2:
                            explode = (0.1,0.1)
                            
                        else:
                            explode = (0.1,0.1,0.1)

                        ax2.pie(x=tags,explode=explode,colors=colors,labels=orden,
                                autopct='%1.1f%%',shadow=True,startangle=90,wedgeprops= wp)
                        ax2.set_title("Distribution of Sentiments for Olist - ENS")
                        
                        negative=google_df[google_df["Sentimiento_ens"]=="Negative"]
                        text_neg= " ".join ([word for word in negative["wiI7pd"]])
                        wordcloud= WordCloud(max_words=500,width=1600,height=800).generate(text_neg)
                        ax3.imshow(wordcloud,interpolation="bilinear")
                        ax3.axis("off")
                        ax3.set_title("Negative Comments - ENS", fontsize=19)

                        st.pyplot(fig)

                st.markdown("# --> Predicción Finalizada de Olist en Google <--")
                st.write(google_df)
                
                if st.button("Download CSV"):
                        csv = google_df.to_csv(index=False)
                        b64 = base64.b64encode(csv.encode()).decode()  # encode CSV file as base64
                        href = f'<a href="data:file/csv;base64,{b64}" download="google.csv">Download CSV file</a>'
                        st.markdown(href, unsafe_allow_html=True)



                st.write(":heavy_minus_sign:" * 32)  

                



            os.remove("data.json")




                                   

    else:
        st.write("Archivo de Credenciales debe ser de tipo JSON")                