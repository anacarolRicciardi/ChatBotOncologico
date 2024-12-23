from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import atividade_fisica
import dicas_nutricao
import apoio_emocional

app = Flask(__name__)

# Função para exibir o menu principal
def menu_principal():
    return (
        "👋 Seja bem-vindo(a) ao nosso suporte para pacientes oncológicos!\n\n"
        "Por favor, escolha uma das opções abaixo:\n\n"
        "1️⃣ Recomendações de Atividade Física\n"
        "2️⃣ Dicas de Nutrição e Bem-estar\n"
        "3️⃣ Apoio Emocional\n"
        "4️⃣ Falar com uma Atendente\n"
        "5️⃣ Sair do chat\n\n"
        "Digite '#' para voltar ao menu principal a qualquer momento."
    )

# Rota para receber mensagens do WhatsApp via webhook do Twilio
@app.route('/whatsapp', methods=['POST'])
def whatsapp():
    incoming_msg = request.values.get('Body', '').strip().lower()
    from_number = request.values.get('From')
    resp = MessagingResponse()
    resposta = ''

    # Se for a primeira interação ou qualquer cumprimento comum, exibe as boas-vindas e o menu inicial
    if incoming_msg in ["oi", "olá", "ola", "bom dia", "boa tarde", "boa noite", "menu", ""]:
        resposta = menu_principal()

    # Opção 1 - Recomendações de Atividade Física
    elif incoming_msg == '1':
        try:
            resposta = atividade_fisica.recomendacoes_exercicios() + "\n\nDigite '#' para voltar ao menu principal."
        except Exception as e:
            resposta = "Houve um erro ao carregar as recomendações de atividade física. Tente novamente mais tarde."
            print(f"Erro: {e}")

    # Opção 2 - Dicas de Nutrição e Bem-estar
    elif incoming_msg == '2':
        try:
            resposta = dicas_nutricao.dicas_nutricao_bemestar() + "\n\nDigite '#' para voltar ao menu principal."
        except Exception as e:
            resposta = "Houve um erro ao carregar as dicas de nutrição e bem-estar. Tente novamente mais tarde."
            print(f"Erro: {e}")

    # Opção 3 - Apoio Emocional
    elif incoming_msg == '3':
        try:
            resposta = apoio_emocional.apoio() + "\n\nDigite '#' para voltar ao menu principal."
        except Exception as e:
            resposta = "Houve um erro ao carregar as mensagens de apoio emocional. Tente novamente mais tarde."
            print(f"Erro: {e}")

    # Opção 4 - Falar com uma Atendente
    elif incoming_msg == '4':
        resposta = "Aguarde em breve você será atendido."

    # Opção 5 - Sair do chat
    elif incoming_msg == '5' or incoming_msg == 'sair':
        resposta = "Obrigado por estar aqui! Volte sempre!"

    # Qualquer outra resposta: digite uma opção válida
    else:
        resposta = "❌ Digite uma opção válida."

    # Adicionar a resposta ao objeto MessagingResponse do Twilio
    msg = resp.message(resposta)
    return str(resp), 200


if __name__ == '__main__':
    app.run(debug=True)
