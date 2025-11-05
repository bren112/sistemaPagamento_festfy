# gerar_ingressos.py - VERSÃO CORRIGIDA
import os
import qrcode
from supabase import create_client
from dotenv import load_dotenv
import uuid
from PIL import Image, ImageDraw

load_dotenv()

# Configurar Supabase
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def gerar_ingresso_com_qr(nome_comprador, email, valor, descricao, status='approved'):
    """Gera um ingresso com QR Code e salva no Supabase"""
    try:
        # Gerar IDs únicos
        id_pagamento = f'pag_{uuid.uuid4().hex[:12]}'
        id_ingresso = f'ing_{uuid.uuid4().hex[:8]}'
        
        # Dados para o QR Code
        dados_qr = f"INGRESSO:{id_ingresso}"
        
        # Criar QR Code primeiro
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(dados_qr)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # Criar ingresso visual
        img = criar_ingresso_visual(nome_comprador, descricao, valor, id_ingresso, qr_img)
        
        # Salvar no Supabase
        venda_data = {
            'id_pagamento': id_pagamento,
            'id_ingresso': id_ingresso,
            'nome_comprador': nome_comprador,
            'email': email,
            'status': status,
            'valor': valor,
            'descricao': descricao
        }
        
        response = supabase.table('vendas').insert(venda_data).execute()
        
        if response.data:
            print(f"✅ Ingresso gerado: {id_ingresso}")
            print(f"📁 Salvo como: ingressos/{id_ingresso}.png")
            return id_ingresso
        else:
            print("❌ Erro ao salvar no banco de dados")
            return None
            
    except Exception as e:
        print(f"❌ Erro ao gerar ingresso: {e}")
        return None

def criar_ingresso_visual(nome, evento, valor, codigo, qr_img):
    """Cria um ingresso visual com QR Code"""
    # Criar imagem do ingresso (600x300 pixels)
    ingresso = Image.new('RGB', (600, 300), color='white')
    draw = ImageDraw.Draw(ingresso)
    
    # Adicionar borda colorida
    draw.rectangle([0, 0, 599, 299], outline='#2563eb', width=4)
    
    # Adicionar área de informações
    draw.rectangle([10, 10, 290, 290], outline='#d1d5db', width=1)
    
    # Informações textuais
    info_text = [
        "EVENTO:",
        evento,
        "",
        "NOME:",
        nome,
        "",
        f"VALOR: R$ {valor:.2f}",
        "",
        f"CÓDIGO: {codigo}",
        "",
        "🎉 APRESENTE ESTE QR CODE",
        "NA ENTRADA DO EVENTO"
    ]
    
    # Adicionar texto
    y_position = 20
    for line in info_text:
        if line.strip():
            draw.text((20, y_position), line, fill='black')
            y_position += 20 if line else 10
    
    # Redimensionar QR Code se necessário e adicionar ao ingresso
    qr_img = qr_img.resize((200, 200))
    ingresso.paste(qr_img, (320, 50))
    
    # Salvar ingresso
    os.makedirs('ingressos', exist_ok=True)
    ingresso.save(f'ingressos/{codigo}.png')
    
    return ingresso

# Gerar alguns ingressos de teste
if __name__ == "__main__":
    print("🎪 GERANDO INGRESSOS DE TESTE...")
    print("=" * 40)
    
    ingressos_teste = [
        {
            'nome_comprador': 'João Silva',
            'email': 'joao@email.com',
            'valor': 99.90,
            'descricao': 'Show da Banda Rock - VIP'
        },
        {
            'nome_comprador': 'Maria Santos',
            'email': 'maria@email.com', 
            'valor': 79.90,
            'descricao': 'Show da Banda Rock - Pista'
        },
        {
            'nome_comprador': 'Pedro Costa',
            'email': 'pedro@email.com',
            'valor': 59.90,
            'descricao': 'Show da Banda Rock - Arquibancada'
        }
    ]
    
    ingressos_gerados = []
    
    for ingresso in ingressos_teste:
        ingresso_id = gerar_ingresso_com_qr(**ingresso)
        if ingresso_id:
            ingressos_gerados.append(ingresso_id)
        print("-" * 40)
    
    print("🎉 Ingressos gerados com sucesso!")
    print(f"📁 Total criados: {len(ingressos_gerados)}")
    print(f"📂 Pasta 'ingressos' criada com os arquivos PNG")
    
    if ingressos_gerados:
        print("\n🔍 Códigos para teste:")
        for codigo in ingressos_gerados:
            print(f"   📝 {codigo}")