# Gerador Distribuído de Certificados 🎓

Este ecossistema foi projetado para simular um cenário de produção em arquiteturas corporativas e distribuídas. Ele utiliza o modelo de processamento assíncrono baseado em filas para a geração pesada de PDFs e envio de e-mails via SMTP, permitindo que a API responda instantaneamente ao usuário final, mantendo alta disponibilidade.

---

## Integrantes:
* Mateus Lora - 1136218
* Gabriel Hanel - 1135926

## 🛠️ Tecnologias Utilizadas

### Front-End

* HTML5
* CSS3
* JavaScript Avançado (Async/Await e Fetch API)

### Back-End API

* Python
* FastAPI
* Uvicorn

### Task Worker (Consumidor)

* Python
* ReportLab

### Mensageria e Broker

* RabbitMQ

### Cache de Estado

* Redis

### Containerização

* Docker
* Docker Compose

---

## 🏛️ Alinhamento com Princípios SOLID

### SRP (Single Responsibility Principle)

Cada classe e arquivo possui uma única responsabilidade:

* A API gerencia conexões HTTP.
* O `pdf_generator.py` gera os certificados em PDF.
* O `email_service.py` gerencia o envio de e-mails.
* O `CacheService` abstrai a comunicação com o Redis.

### OCP (Open/Closed Principle)

Se o layout do certificado precisar ser alterado, apenas a classe responsável pela geração dos PDFs será modificada, sem impactar o fluxo da API ou do Worker.

### DIP (Dependency Inversion Principle)

Configurações sensíveis, credenciais e parâmetros de infraestrutura são carregados através de variáveis de ambiente centralizadas em `config.py`, evitando dependências rígidas espalhadas pelo sistema.

---

## 🚀 Como Executar o Projeto

### 📋 Pré-requisitos

* Docker instalado
* Docker Compose instalado
* Python 3.10 ou superior

---

### Passo 1: Subir a Infraestrutura

Na raiz do projeto execute:

```bash
docker compose up -d
```

Verifique se os contêineres estão em execução:

```bash
docker ps
```

---

### Passo 2: Instalar as Dependências

```bash
pip install -r requirements.txt
```

---

### Passo 3: Configurar Variáveis de Ambiente

Abra o arquivo `.env` e preencha as credenciais SMTP necessárias para o envio dos certificados.

Exemplo:

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=465
EMAIL_REMETENTE=
SENHA_REMETENTE=
```

---

### Passo 4: Executar a API (Pronta para Acesso em Rede)

Acesse a pasta do servidor e inicie o FastAPI liberando o acesso para outros dispositivos da rede:

```bash
cd servidor
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

A API estará disponível tanto localmente quanto para outros dispositivos conectados à mesma rede Wi-Fi.

Exemplos:

```text
http://localhost:8000
```

```text
http://SEU_IP_LOCAL:8000
```

Documentação automática:

```text
http://localhost:8000/docs
```

```text
http://SEU_IP_LOCAL:8000/docs
```

---

### Passo 5: Iniciar o Worker

Abra um novo terminal, acesse a pasta do servidor e execute o consumidor:

```bash
cd servidor
python worker.py
```

O Worker ficará aguardando mensagens na fila RabbitMQ para:

* Gerar certificados em PDF;
* Armazenar os arquivos gerados;
* Realizar o envio dos certificados por e-mail.

---

### Passo 6: Executar o Cliente Web

Abra um novo terminal na raiz do projeto e inicie o servidor HTTP liberando a porta para a rede:

```bash
python -m http.server 3000 --bind 0.0.0.0 --directory cliente
```

Acesse pelo navegador do computador ou celular conectado à mesma rede Wi-Fi:

```text
http://localhost:3000
```

ou

```text
http://SEU_IP_LOCAL:3000
```

---

## 🔄 Fluxo da Aplicação

```text
Usuário
   │
   ▼
Front-End (HTML/CSS/JS)
   │
   ▼
FastAPI
   │
   ▼
RabbitMQ
   │
   ▼
Worker
   ├── Geração de PDF
   ├── Armazenamento do Arquivo
   └── Envio de E-mail
   │
   ▼
Redis (Status e Cache)
```

---

## 🎯 Objetivos do Projeto

* Demonstrar processamento assíncrono utilizando filas de mensagens.
* Aplicar conceitos de arquitetura distribuída.
* Implementar comunicação entre múltiplos serviços.
* Utilizar cache para controle de estado e monitoramento de tarefas.
* Aplicar princípios SOLID em um sistema real.
* Simular um ambiente corporativo de geração automatizada de certificados.
* Demonstrar desacoplamento entre API e processamento pesado.
* Permitir acesso à aplicação em dispositivos da mesma rede local.

---

## 📚 Conceitos Demonstrados

* APIs REST com FastAPI.
* Processamento assíncrono orientado a eventos.
* Arquitetura Producer/Consumer.
* Filas de mensagens com RabbitMQ.
* Cache distribuído com Redis.
* Geração dinâmica de PDFs com ReportLab.
* Containerização com Docker.
* Comunicação entre microsserviços.
* Configuração via variáveis de ambiente.
* Boas práticas de desenvolvimento utilizando SOLID.
