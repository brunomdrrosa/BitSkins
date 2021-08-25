import requests
import pyotp
import os

# Código de Autenticação de dois fatores
my_secret = os.getenv("my_secret")
my_token = pyotp.TOTP(my_secret)
CODE = my_token.now()

# Chaves API utilizadas
API_KEY_BITSKINS = os.getenv("API_KEY_BITSKINS")
API_KEY_USD_TO_BRL = os.getenv("API_KEY_USD_TO_BRL")

# Valor do US$ em BRL
api_real = requests.get(f"https://free.currconv.com/api/v7/convert?q=USD_BRL&compact=ultra&apiKey={API_KEY_USD_TO_BRL}")
usd_to_brl = api_real.json()
preco_brl = usd_to_brl["USD_BRL"]

# Checar o saldo da conta no BitSkins
saldo = requests.get(f"https://bitskins.com/api/v1/get_account_balance/?api_key={API_KEY_BITSKINS}&code={CODE}")
checar_saldo_usuario = saldo.json()
saldo_usd = float(checar_saldo_usuario["data"]["available_balance"])
saldo_usuario_brl = saldo_usd * preco_brl
print(f"Você tem na sua conta R$ {saldo_usuario_brl:.2f}")