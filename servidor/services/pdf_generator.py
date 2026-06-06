import os
from datetime import datetime
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from config import settings

class CertificatePDFGenerator:
    def __init__(self):
        self.page_width, self.page_height = landscape(A4)

    def _obter_data_atual_extenso(self) -> str:
        meses = {1: "janeiro", 2: "fevereiro", 3: "março", 4: "abril", 5: "maio", 6: "junho", 7: "julho", 8: "agosto", 9: "setembro", 10: "outubro", 11: "novembro", 12: "dezembro"}
        hoje = datetime.now()
        return f"{hoje.day} de {meses[hoje.month]} de {hoje.year}"

    def generate(self, nome: str, task_id: str):
        nome_arquivo = f"certificado_{task_id}.pdf"
        
        caminho_local = os.path.join("certificados", nome_arquivo)
        os.makedirs(os.path.dirname(caminho_local), exist_ok=True)
        
        link_pdf = f"{settings.BASE_URL}/certificados/{nome_arquivo}"

        c = canvas.Canvas(caminho_local, pagesize=landscape(A4))

        # Design
        c.setFillColor(HexColor("#F9F9FB"))
        c.rect(0, 0, self.page_width, self.page_height, fill=True, stroke=False)
        c.setStrokeColor(HexColor("#1B2A4A"))
        c.setLineWidth(8)
        c.rect(20, 20, self.page_width - 40, self.page_height - 40, fill=False, stroke=True)
        c.setStrokeColor(HexColor("#C5A059"))
        c.setLineWidth(3.5)
        c.rect(29, 29, self.page_width - 58, self.page_height - 58, fill=False, stroke=True)

        # Textos
        c.setFillColor(HexColor("#1B2A4A"))
        c.setFont("Times-Bold", 42)
        c.drawCentredString(self.page_width / 2, 460, "CERTIFICADO DE PARTICIPAÇÃO")

        c.setFillColor(HexColor("#555555"))
        c.setFont("Times-Italic", 16)
        c.drawCentredString(self.page_width / 2, 420, "Este documento certifica a presença na apresentação do projeto Gerador de Certificado Distribuído.")

        c.setFillColor(HexColor("#C5A059"))
        c.setFont("Times-Bold", 34)
        c.drawCentredString(self.page_width / 2, 340, nome.upper())

        c.setStrokeColor(HexColor("#C5A059"))
        c.setLineWidth(2.5)
        c.line(self.page_width / 2 - 220, 315, self.page_width / 2 + 220, 315)
        
        c.setFillColor(HexColor("#333333"))
        c.setFont("Helvetica", 12)
        c.drawCentredString(self.page_width / 2, 275, "Solução desenvolvida sob uma arquitetura distribuída e processamento assíncrono,")
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(self.page_width / 2, 255, "integrando as tecnologias: API REST (FastAPI), Redis, RabbitMQ e Docker.")

        data_extenso = self._obter_data_atual_extenso()
        c.setFillColor(HexColor("#777777"))
        c.setFont("Times-Italic", 14)
        c.drawCentredString(self.page_width / 2, 190, f"Emitido a {data_extenso}.")

        # Assinaturas
        c.setStrokeColor(HexColor("#C5A059"))
        c.setLineWidth(1.5)
        c.line(150, 100, 350, 100)
        c.setFillColor(HexColor("#1B2A4A"))
        c.setFont("Times-BoldItalic", 16)
        c.drawCentredString(250, 85, "Mateus Lora")
        c.setFont("Helvetica", 10)
        c.setFillColor(HexColor("#777777"))
        c.drawCentredString(250, 70, "Desenvolvedor da Ferramenta")

        c.setStrokeColor(HexColor("#C5A059"))
        c.line(self.page_width - 350, 100, self.page_width - 150, 100)
        c.setFillColor(HexColor("#1B2A4A"))
        c.setFont("Times-BoldItalic", 16)
        c.drawCentredString(self.page_width - 250, 85, "Gabriel Hanel")
        c.setFont("Helvetica", 10)
        c.setFillColor(HexColor("#777777"))
        c.drawCentredString(self.page_width - 250, 70, "Desenvolvedor da Ferramenta")

        c.showPage()
        c.save()
        
        print(f" [PDF] Salvo: {caminho_local}")
        return link_pdf, caminho_local