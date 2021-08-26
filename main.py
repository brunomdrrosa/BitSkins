from logo import logo
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

# Menu do programa
def menu():
    print(logo)
    print("=== MENU ===")
    print("1. Checar saldo da conta")
    print("2. Checar sua última ordem de compra")
    print("3. Fechar o programa")
    opcao_menu = input("Digite uma opção do menu:\n")

    # Checar saldo da conta do BitSkins
    if opcao_menu == "1":
        saldo = requests.get(f"https://bitskins.com/api/v1/get_account_balance/?api_key={API_KEY_BITSKINS}&code={CODE}")
        checar_saldo_usuario = saldo.json()
        saldo_usd = float(checar_saldo_usuario["data"]["available_balance"])
        saldo_usuario_brl = saldo_usd * preco_brl
        print(f"Você tem R$ {saldo_usuario_brl:.2f} na sua conta")
        menu()

    # Checar a última ordem de compra
    if opcao_menu == "2":
        ordens = requests.get(f"https://bitskins.com/api/v1/get_buy_order_history/?api_key={API_KEY_BITSKINS}&page=1&app_id=730&code={CODE}")
        ordens_json = ordens.json()
        nome_skin = ordens_json["data"]["orders"][0]["market_hash_name"]
        preco_skin = ordens_json["data"]["orders"][0]["price"]
        print(f"Sua última ordem de compra foi {nome_skin} por $ {preco_skin}")

    # Sair do programa
    if opcao_menu == "3":
        exit()

menu()