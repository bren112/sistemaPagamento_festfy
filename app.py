# app.py ou um arquivo de configuração
import os
import mercadopago
from dotenv import load_dotenv  # Biblioteca para ler o .env

# Carrega as variáveis do arquivo .env
load_dotenv()

# Configura o SDK do Mercado Pago com o Access Token
sdk = mercadopago.SDK(os.getenv("MP_ACCESS_TOKEN"))

# A partir daqui, você pode usar o objeto 'sdk' para fazer requisições à API.