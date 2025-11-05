# teste_mp.py - VERSÃO CORRIGIDA
import os
import mercadopago
from dotenv import load_dotenv

# 1. Carregar variáveis do .env
load_dotenv()

# 2. Configurar SDK
try:
    sdk = mercadopago.SDK(os.getenv("MP_ACCESS_TOKEN"))
    print("✅ SDK configurado com sucesso!")
except Exception as e:
    print(f"❌ Erro ao configurar SDK: {e}")
    exit()

# 3. Fazer uma requisição simples para testar
try:
    print("🔍 Testando conexão com a API...")
    
    # FORMA CORRETA: Criar uma preferência de pagamento de teste
    preference_data = {
        "items": [
            {
                "title": "Ingresso Teste",
                "quantity": 1,
                "unit_price": 10.50,
                "currency_id": "BRL",
            }
        ],
        "back_urls": {
            "success": "https://www.seusite.com/success",
            "failure": "https://www.seusite.com/failure",
            "pending": "https://www.seusite.com/pending"
        },
        "auto_return": "approved",
    }
    
    # Criar a preferência
    preference_result = sdk.preference().create(preference_data)
    
    # Verificar se deu certo
    if preference_result["status"] in [200, 201]:
        print("✅ Conexão com API do Mercado Pago: OK!")
        print("✅ Preferência de pagamento criada com sucesso!")
        print(f"✅ ID da Preferência: {preference_result['response']['id']}")
        print(f"✅ URL do Checkout: {preference_result['response']['init_point']}")
        
        print("\n🎉 Tudo funcionando perfeitamente!")
        print("💡 Dica: Abra a URL do checkout no navegador para testar o fluxo de pagamento")
        
    else:
        print(f"❌ Erro na API: Status {preference_result['status']}")
        print(f"   Mensagem: {preference_result.get('response', {}).get('message', 'Erro desconhecido')}")
        
except Exception as e:
    print(f"❌ Erro ao fazer requisição: {e}")
    print("\n💡 Possível solução: Verifique se está usando a versão mais recente do SDK")
    print("   Tente: pip install --upgrade mercadopago")