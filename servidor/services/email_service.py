import smtplib
from email.message import EmailMessage
from config import settings

class EmailNotificationService:
    def __init__(self):
        self.remetente = settings.EMAIL_REMETENTE
        self.senha = settings.SENHA_REMETENTE
        self.host = settings.SMTP_HOST
        self.port = settings.SMTP_PORT

    def enviar_com_anexo(self, destinatario: str, nome: str, caminho_pdf: str) -> bool:
        msg = EmailMessage()
        msg['Subject'] = '🎓 Obrigado pela presença! - Seu Certificado Chegou'
        msg['From'] = self.remetente
        msg['To'] = destinatario
        
        conteudo_html = f"""
        <html>
          <body style="font-family: 'Segoe UI', Arial, sans-serif; background-color: #f0f2f5; padding: 20px; color: #333; margin: 0;">
            <div style="background-color: #ffffff; max-width: 600px; margin: 0 auto; padding: 30px; border-radius: 12px; border-top: 6px solid #2c3e50; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
              <h2 style="color: #2c3e50; text-align: center; margin-top: 0;">🎓 Obrigado pela sua presença!</h2>
              <p style="font-size: 16px;">Olá, <strong>{nome}</strong>!</p>
              <p style="font-size: 16px; line-height: 1.6; color: #555;">
                Ficamos felizes com a sua participação na apresentação do nosso projeto prático <strong>Gerador de Certificados Distribuído</strong>.
              </p>
              <p style="font-size: 16px; line-height: 1.6; color: #555;">
                Como forma de agradecimento, o seu certificado oficial foi processado e segue em anexo!
              </p>
              <hr style="border: none; border-top: 1px solid #eaeaea; margin: 25px 0;">
              <p style="font-size: 14px; color: #7f8c8d; text-align: center; margin-bottom: 0;">
                Atenciosamente,<br>
                <strong style="color: #2c3e50;">Equipe do Projeto</strong><br>
                Disciplina de Computação Distribuída - Atitus Educação
              </p>
            </div>
          </body>
        </html>
        """
        msg.add_alternative(conteudo_html, subtype='html')

        try:
            with open(caminho_pdf, 'rb') as f:
                dados_pdf = f.read()
                nome_arquivo = f'Certificado_{nome.replace(" ", "_")}.pdf'
                msg.add_attachment(dados_pdf, maintype='application', subtype='pdf', filename=nome_arquivo)

            with smtplib.SMTP_SSL(self.host, self.port) as smtp:
                smtp.login(self.remetente, self.senha)
                smtp.send_message(msg)
            print(f" [E-mail] Enviado para {destinatario}")
            return True
        except Exception as e:
            print(f" [Erro de SMTP] Falha: {e}")
            return False