import pika
import json
import sys
from config import settings
from database import CacheService
from services.pdf_generator import CertificatePDFGenerator
from services.email_service import EmailNotificationService

class QueueWorker:
    def __init__(self):
        self.cache = CacheService()
        self.pdf_engine = CertificatePDFGenerator()
        self.email_engine = EmailNotificationService()
        self.queue_name = settings.RABBITMQ_QUEUE

    def start(self):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST))
            channel = connection.channel()
            channel.queue_declare(queue=self.queue_name)
            
            print(' [*] Worker ativo. Aguardando mensagens na fila. Para sair pressione CTRL+C')
            channel.basic_consume(queue=self.queue_name, on_message_callback=self._process_message, auto_ack=True)
            channel.start_consuming()
        except KeyboardInterrupt:
            print('\n [!] Encerrando execução do Worker.')
            sys.exit(0)

    def _process_message(self, ch, method, properties, body):
        dados = json.loads(body)
        task_id = dados['task_id']
        nome = dados['nome_aluno']
        email = dados['email_aluno']
        
        print(f"\n [x] Processando ID: {task_id} ({nome})")
        
        self.cache.set_status(task_id, "Gerando PDF...")
        link_pdf, caminho_local = self.pdf_engine.generate(nome, task_id)
        
        self.cache.set_status(task_id, "Enviando e-mail...")
        self.email_engine.enviar_com_anexo(email, nome, caminho_local)
        
        self.cache.set_status(task_id, link_pdf)
        print(f" [v] Task {task_id} concluída!")

if __name__ == "__main__":
    worker = QueueWorker()
    worker.start()