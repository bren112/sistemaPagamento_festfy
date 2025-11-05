# validador_evento.py
import os
import cv2
from supabase import create_client
from dotenv import load_dotenv
import threading
import time

load_dotenv()

# Configurar Supabase
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

class ValidadorIngressos:
    def __init__(self):
        self.ingressos_validados = []
        
    def validar_ingresso(self, id_ingresso):
        """Valida um ingresso pelo código"""
        try:
            # Buscar no banco de dados
            response = supabase.table('vendas')\
                .select('*')\
                .eq('id_ingresso', id_ingresso)\
                .execute()
            
            if not response.data:
                self._mostrar_resultado("❌ INGRESSO NÃO ENCONTRADO", False)
                return False
            
            venda = response.data[0]
            
            if venda['status'] != 'approved':
                self._mostrar_resultado("❌ PAGAMENTO NÃO APROVADO", False)
                return False
            
            if venda['utilizado']:
                self._mostrar_resultado("❌ INGRESSO JÁ UTILIZADO", False)
                return False
            
            # Marcar como utilizado
            supabase.table('vendas')\
                .update({'utilizado': True})\
                .eq('id_ingresso', id_ingresso)\
                .execute()
            
            # Adicionar à lista de validados
            self.ingressos_validados.append({
                'id': id_ingresso,
                'nome': venda['nome_comprador'],
                'timestamp': time.strftime('%H:%M:%S')
            })
            
            self._mostrar_resultado("🎫 INGRESSO VÁLIDO - ACESSO LIBERADO!", True, venda)
            return True
            
        except Exception as e:
            self._mostrar_resultado(f"❌ ERRO: {e}", False)
            return False
    
    def _mostrar_resultado(self, mensagem, sucesso, venda=None):
        """Mostra o resultado da validação de forma visual"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("🎪 SISTEMA DE VALIDAÇÃO - EVENTO")
        print("=" * 50)
        
        if sucesso and venda:
            print("✅ " + "=" * 48)
            print("✅ " + mensagem.center(48))
            print("✅ " + "=" * 48)
            print(f"✅ 👤 Nome: {venda['nome_comprador']}")
            print(f"✅ 📧 Email: {venda['email']}") 
            print(f"✅ 💰 Valor: R$ {venda['valor']:.2f}")
            print(f"✅ 🎫 Código: {venda['id_ingresso']}")
            print(f"✅ ⏰ Horário: {time.strftime('%H:%M:%S')}")
            print("✅ " + "=" * 48)
        else:
            print("❌ " + "=" * 48)
            print("❌ " + mensagem.center(48))
            print("❌ " + "=" * 48)
        
        self._mostrar_estatisticas()
    
    def _mostrar_estatisticas(self):
        """Mostra estatísticas em tempo real"""
        print(f"\n📊 ESTATÍSTICAS DO EVENTO:")
        print(f"   ✅ Ingressos validados: {len(self.ingressos_validados)}")
        print(f"   ⏰ Primeira validação: {self.ingressos_validados[0]['timestamp'] if self.ingressos_validados else 'N/A'}")
        print(f"   🔄 Última validação: {self.ingressos_validados[-1]['timestamp'] if self.ingressos_validados else 'N/A'}")
        
        if len(self.ingressos_validados) > 0:
            print(f"\n📋 ÚLTIMOS 5 INGRESSOS:")
            for ingresso in self.ingressos_validados[-5:]:
                print(f"   👤 {ingresso['nome']} - {ingresso['timestamp']}")
    
    def modo_manual(self):
        """Modo de validação manual (digitar código)"""
        print("🎪 MODO VALIDAÇÃO MANUAL")
        print("=" * 50)
        print("💡 Digite o código do ingresso (ou 'sair' para encerrar)")
        
        while True:
            codigo = input("\n🔍 Código do ingresso: ").strip()
            
            if codigo.lower() in ['sair', 'exit', 'quit']:
                break
                
            if codigo:
                self.validar_ingresso(codigo)
    
    def modo_qr_code(self):
        """Modo de validação por QR Code (usando webcam)"""
        try:
            cap = cv2.VideoCapture(0)
            detector = cv2.QRCodeDetector()
            
            print("🎪 MODO VALIDAÇÃO POR QR CODE")
            print("=" * 50)
            print("📷 Aponte a câmera para o QR Code...")
            print("💡 Pressione 'q' para sair")
            
            while True:
                _, img = cap.read()
                data, bbox, _ = detector.detectAndDecode(img)
                
                if data and data.startswith('INGRESSO:'):
                    codigo = data.replace('INGRESSO:', '').strip()
                    self.validar_ingresso(codigo)
                    time.sleep(2)  # Evitar múltiplas leituras
                
                cv2.imshow("Validador QR Code - Pressione 'q' para sair", img)
                
                if cv2.waitKey(1) == ord('q'):
                    break
            
            cap.release()
            cv2.destroyAllWindows()
            
        except Exception as e:
            print(f"❌ Erro na câmera: {e}")
            print("🎪 Voltando para modo manual...")
            self.modo_manual()

# Interface principal
def main():
    validador = ValidadorIngressos()
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("🎪 SISTEMA DE VALIDAÇÃO DE INGRESSOS")
        print("=" * 50)
        print("1️⃣  Modo Manual (Digitar código)")
        print("2️⃣  Modo QR Code (Usar câmera)")
        print("3️⃣  Estatísticas")
        print("4️⃣  Sair")
        
        opcao = input("\n🔢 Escolha uma opção: ").strip()
        
        if opcao == '1':
            validador.modo_manual()
        elif opcao == '2':
            validador.modo_qr_code()
        elif opcao == '3':
            print(f"\n📊 ESTATÍSTICAS COMPLETAS:")
            print(f"   ✅ Total validado: {len(validador.ingressos_validados)}")
            input("\n📝 Pressione Enter para continuar...")
        elif opcao == '4':
            print("👋 Encerrando sistema...")
            break
        else:
            print("❌ Opção inválida!")
            time.sleep(1)

if __name__ == "__main__":
    main()