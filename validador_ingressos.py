# validador_ingressos.py
import os
from supabase import create_client
from dotenv import load_dotenv
import qrcode
from PIL import Image

load_dotenv()

# Configurar Supabase
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def validar_ingresso_app(id_ingresso):
    """Versão simplificada para usar no evento"""
    try:
        # Busca o ingresso
        response = supabase.table('vendas')\
            .select('*')\
            .eq('id_ingresso', id_ingresso)\
            .execute()
        
        if not response.data:
            print("❌ INGRESSO NÃO ENCONTRADO")
            return False
        
        venda = response.data[0]
        
        if venda['status'] != 'approved':
            print("❌ PAGAMENTO NÃO APROVADO")
            return False
        
        if venda['utilizado']:
            print("❌ INGRESSO JÁ UTILIZADO")
            return False
        
        # Marcar como utilizado
        supabase.table('vendas')\
            .update({'utilizado': True})\
            .eq('id_ingresso', id_ingresso)\
            .execute()
        
        print("🎫 INGRESSO VÁLIDO!")
        print(f"👤 Nome: {venda['nome_comprador']}")
        print(f"📧 Email: {venda['email']}")
        print(f"💰 Valor: R$ {venda['valor']}")
        print("✅ ACESSO LIBERADO!")
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

# Para usar no evento:
if __name__ == "__main__":
    print("🔍 VALIDADOR DE INGRESSOS")
    print("=" * 30)
    
    while True:
        id_ingresso = input("\nDigite o código do ingresso: ").strip()
        
        if id_ingresso.lower() == 'sair':
            break
            
        validar_ingresso_app(id_ingresso)
        print("-" * 30)