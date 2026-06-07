import uuid
import os
import hashlib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from database import CacheService
from queue_manager import QueuePublisher
from config import settings

app = FastAPI(title="Gerador de Certificados - API Distribuída")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("certificados", exist_ok=True)
app.mount("/certificados", StaticFiles(directory="certificados"), name="certificados")

cache = CacheService()
publisher = QueuePublisher()

class CertificadoReq(BaseModel):
    nome_aluno: str
    email_aluno: str

@app.get("/api/config")
def obter_configuracoes():
    """Expõe o IP do .env dinamicamente para o Front-End"""
    return {"BASE_URL": settings.BASE_URL}

@app.post("/api/certificados/")
def criar_certificado(dados: CertificadoReq):
    # o hashlib junta o nome e email do aluno para criar uma chave (hash) para evitar duplicidade de certificados
    chave = f"dedup:{hashlib.md5(f'{dados.nome_aluno}{dados.email_aluno}'.encode()).hexdigest()}"
    task_id_existente = cache._client.get(chave)

    if task_id_existente:
        return {"task_id": task_id_existente, "mensagem": "Certificado já existe."}

    task_id = str(uuid.uuid4())
    # o setex do Redis define a chave com um tempo de expiração (24 horas) para evitar que o cache cresça indefinidamente
    cache._client.set(chave, task_id, 86400)
    cache.set_status(task_id, "Processando na fila...")
    publisher.publish_task({
    "task_id": task_id,
    "nome_aluno": dados.nome_aluno,
    "email_aluno": dados.email_aluno
})
    return {"task_id": task_id, "mensagem": "Solicitação em processamento."}

@app.get("/api/status/{task_id}")
def verificar_status(task_id: str):
    status = cache.get_status(task_id)
    if not status:
        return {"status": "Não encontrado", "link": None}
    if status.startswith("http"):
        return {"status": "Concluído", "link": status}
    return {"status": status, "link": None}