# %% [markdown]
# Importamos las librerías necesarias para el proceso de extracción, transformación y carga y luego extraemos los csv correspondientes.

# %%
import pandas as pd
from deep_translator import GoogleTranslator
from googletrans import Translator

# %%
Closed_deals = pd.read_csv("Closed_deals.csv")
Customers = pd.read_csv("Customers.csv")
Geolocation = pd.read_csv("Geolocation.csv")
Marketing = pd.read_csv("Marketing_qualified_leads.csv")
Order_items = pd.read_csv("Order_items.csv")
Order_payments = pd.read_csv("Order_payments.csv")
Order_reviews = pd.read_csv("Order_reviews.csv")
Orders = pd.read_csv("Orders.csv")
Product_category_name_translation = pd.read_csv("Product_category_name_translation.csv")
Products = pd.read_csv("Products.csv")
Sellers = pd.read_csv("Sellers.csv")

# %% [markdown]
# Observamos que dentro del csv de closed deals hay columnas que no van a ser necesarias para nuestro análisis, por lo tanto las eliminamos.

# %%
Closed_deals.info()

# %%
Closed_deals = Closed_deals.drop(['has_company', 'has_gtin', 'average_stock', 'declared_product_catalog_size'], axis=1)

# %% [markdown]
# Ahora, a los valores nulos de las columnas cualitativas los rellenamos por "unknown" (desconocido), ya que va a resultar más adecuado para nuestro análisis.

# %%
Closed_deals['business_segment'].fillna('unknown', inplace=True)
Closed_deals['lead_type'].fillna('unknown', inplace=True)
Closed_deals['lead_behaviour_profile'].fillna('unknown', inplace=True)
Closed_deals['business_type'].fillna('unknown', inplace=True)

# %% [markdown]
# Dentro del csv 'Geolocation', creamos a una columna nueva donde nos ubique a qué región pertenece el Estado.

# %%
Region={'PR':'Sur','RS':'Sur','SC':'Sur','SP':'Sudeste','MG':'Sudeste','RJ':'Sudeste','ES':'Sudeste','MT':'Centro oeste', 'MS':'Centro oeste', 'GO':'Centro oeste' , 'DF':'Centro oeste',
 'AC':'Norte', 'AP':'Norte','AM':'Norte','PA':'Norte', 'RO':'Norte','RR':'Norte', 'TO':'Norte', 	
'AL':'Nordeste','BA':'Nordeste','CE':'Nordeste','MA':'Nordeste','PB':'Nordeste','PI':'Nordeste',
'PE':'Nordeste','RN':'Nordeste','SE':'Nordeste',}

def get_region(state):
    return Region[state]

Geolocation['geolocation_region'] = Geolocation['geolocation_state'].apply(get_region)

# %%
Geolocation

# %% [markdown]
# Eliminación de datos duplicados.

# %%
Closed_deals = Closed_deals.drop_duplicates()
Customers = Customers.drop_duplicates()
Geolocation = Geolocation.drop_duplicates()
Marketing = Marketing.drop_duplicates()
Order_items = Order_items.drop_duplicates()
Order_payments = Order_payments.drop_duplicates()
Order_reviews = Order_reviews.drop_duplicates()
Orders = Orders.drop_duplicates()
Product_category_name_translation = Product_category_name_translation.drop_duplicates()
Products = Products.drop_duplicates()
Sellers = Sellers.drop_duplicates()

# %% [markdown]
# Creamos una nueva columna en español para las sucursales latinoamericanas.

# %%
#le aplicamos la traducción a la columna product_category_name_english
translator = GoogleTranslator(source="auto", target="es")
Product_category_name_translation['product_category_name_spanish'] = Product_category_name_translation.product_category_name_english.apply(translator.translate)

print(Product_category_name_translation)


