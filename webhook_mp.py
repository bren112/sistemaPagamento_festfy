# webhook_mp.py
from flask import Flask, request, jsonify
import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

@app.route('/webhook/mercadopago', methods=['POST'])
def webhook_mercadopago():
    try:
        data = request.json
        
        # Verificar se é uma notificação de pagamento
        if data.get('type') == 'payment':
            payment_id = data.get('data', {}).get('id')
            
            # Aqui você buscaria os detalhes do pagamento na API do MP
            # e atualizaria o status no Supabase
            
            print(f"📦 Webhook recebido - Payment ID: {payment_id}")
            
            # Exemplo de atualização:
            # supabase.table('vendas')\
            #     .update({'status': 'approved'})\
            #     .eq('id_pagamento', payment_id)\
            #     .execute()
            
        return jsonify({"status": "success"}), 200
        
    except Exception as e:
        print(f"❌ Erro no webhook: {e}")
        return jsonify({"status": "error"}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)