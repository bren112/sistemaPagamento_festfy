# supabase_test.py
import os
from supabase import create_client, Client
from dotenv import load_dotenv
import uuid

# Carregar variáveis
load_dotenv()

# Configurar Supabase
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def testar_conexao():
    """Testa a conexão com Supabase"""
    try:
        # Tenta fazer uma consulta simples
        response = supabase.table('vendas').select('*').limit(1).execute()
        print("✅ Conexão com Supabase: OK!")
        return True
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return False

def criar_venda_teste():
    """Cria uma venda de teste"""
    try:
        # Dados de teste
        venda_teste = {
            'id_pagamento': f'pag_test_{uuid.uuid4().hex[:8]}',
            'id_ingresso': f'ing_{uuid.uuid4().hex[:8]}',
            'nome_comprador': 'Cliente Teste',
            'email': 'teste@email.com',
            'status': 'approved',  # Simulando pagamento aprovado
            'valor': 99.90,
            'descricao': 'Ingresso VIP - Show Teste'
        }
        
        # Insere no Supabase
        response = supabase.table('vendas').insert(venda_teste).execute()
        
        if response.data:
            print("✅ Venda teste criada com sucesso!")
            print(f"✅ ID do Ingresso: {venda_teste['id_ingresso']}")
            return venda_teste['id_ingresso']
        else:
            print("❌ Erro ao criar venda teste")
            return None
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None

def validar_ingresso(id_ingresso):
    """Valida se um ingresso é válido"""
    try:
        # Busca o ingresso no banco
        response = supabase.table('vendas')\
            .select('*')\
            .eq('id_ingresso', id_ingresso)\
            .execute()
        
        if not response.data:
            return {"status": "error", "message": "Ingresso não encontrado"}
        
        venda = response.data[0]
        
        # Verifica condições
        if venda['status'] != 'approved':
            return {"status": "error", "message": "Pagamento não aprovado"}
        
        if venda['utilizado']:
            return {"status": "error", "message": "Ingresso já utilizado"}
        
        # Marca como utilizado
        supabase.table('vendas')\
            .update({'utilizado': True})\
            .eq('id_ingresso', id_ingresso)\
            .execute()
        
        return {
            "status": "success", 
            "message": "Ingresso válido!",
            "dados": {
                "nome": venda['nome_comprador'],
                "email": venda['email'],
                "valor": venda['valor'],
                "descricao": venda['descricao']
            }
        }
        
    except Exception as e:
        return {"status": "error", "message": f"Erro na validação: {e}"}

# Executar testes
if __name__ == "__main__":
    print("🧪 Testando integração com Supabase...")
    
    # Teste 1: Conexão
    if testar_conexao():
        # Teste 2: Criar venda
        id_ingresso = criar_venda_teste()
        
        if id_ingresso:
            # Teste 3: Validar ingresso
            print(f"\n🔍 Validando ingresso: {id_ingresso}")
            resultado = validar_ingresso(id_ingresso)
            print(f"Resultado: {resultado}")
            
            # Teste 4: Tentar validar novamente (deve falhar)
            print(f"\n🔍 Tentando validar novamente...")
            resultado2 = validar_ingresso(id_ingresso)
            print(f"Resultado: {resultado2}")