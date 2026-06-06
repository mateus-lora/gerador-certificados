let API_URL = "";

const apiConfigUrl = `http://${window.location.hostname}:8000/api/config`;

async function carregarConfiguracao() {
    try {
        const resposta = await fetch(apiConfigUrl);
        const config = await resposta.json();
        API_URL = config.BASE_URL + '/api';
    } catch (error) {
        console.error("Erro ao sincronizar com o .env. Usando fallback local.", error);
        API_URL = 'http://localhost:8000/api';
    }
}

carregarConfiguracao();

async function solicitarCertificado() {
    const nomeInput = document.getElementById('nome');
    const emailInput = document.getElementById('email');
    const statusBox = document.getElementById('status-box');
    const statusTexto = document.getElementById('status-texto');

    const nome = nomeInput.value.trim();
    const email = emailInput.value.trim();

    if (!nome || !email) return alert("Por favor, preencha todos os campos!");

    atualizarUIStatus(statusBox, statusTexto, "#ecf0f1", "#2c3e50", "<strong>Status:</strong> Enviando para a fila...");

    try {
        const resposta = await fetch(`${API_URL}/certificados/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nome_aluno: nome, email_aluno: email })
        });
        
        if (!resposta.ok) throw new Error("Erro no servidor");

        const dados = await resposta.json();
        monitorarProgressoFila(dados.task_id, statusBox, statusTexto, nomeInput, emailInput);
    } catch (error) {
        atualizarUIStatus(statusBox, statusTexto, "#f8d7da", "#721c24", "Erro ao conectar com o servidor. Tente novamente.");
    }
}

function monitorarProgressoFila(taskId, box, texto, campoNome, campoEmail) {
    const intervalo = setInterval(async () => {
        try {
            const resStatus = await fetch(`${API_URL}/status/${taskId}`);
            const dataStatus = await resStatus.json();
            
            texto.innerHTML = `<strong>Status:</strong> ${dataStatus.status}`;

            if (dataStatus.link) {
                clearInterval(intervalo);
                
                const htmlSucesso = "<b>✅ Sucesso! O certificado foi enviado para o seu e-mail.</b>";
                
                atualizarUIStatus(box, texto, "#d4edda", "#155724", htmlSucesso);
                campoNome.value = '';
                campoEmail.value = '';
            }
        } catch (err) {
            clearInterval(intervalo);
            atualizarUIStatus(box, texto, "#f8d7da", "#721c24", "Erro ao checar o status da emissão.");
        }
    }, 1500);
}

function atualizarUIStatus(container, textoElemento, background, corTexto, htmlConteudo) {
    container.style.display = 'block';
    container.style.background = background;
    container.style.color = corTexto;
    textoElemento.innerHTML = htmlConteudo;
}