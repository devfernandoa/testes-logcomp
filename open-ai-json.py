import json

import requests

url = "https://apim-dataopenai-prod-eastus-001.azure-api.net/professor/davidf5/openai/deployments/gpt-4.1-Correcao-Prova/chat/completions?api-version=2025-03-01-preview"

payload = json.dumps(
    {
        "messages": [
            {
                "role": "system",
                "content": """
Você é um avaliador acadêmico rigoroso. Dê uma nota de 0 a 100 para a resposta do aluno. 

Avalie: (1) precisão conceitual, (2) completude, (3) clareza.

Critérios esperados na resposta:
- Correção parcial: {P} C {Q} garante Q apenas se o programa termina
- Correção total = correção parcial + prova de terminação
- Triplas de Hoare não garantem terminação
- Exemplo: loops infinitos ou falta de função variante

Dê uma nota de 0 a 100.

Responda apenas em JSON no formato: {\"grade\": number, \"feedback\": \"texto curto\"}.
""",
            },
            {
                "role": "user",
                "content": """A lógica de Hoare é considerada parcial porque ela só garante que se o programa terminar então o resultado será correto. Ela não garante que o programa sempre termina, por exemplo em loops infinitos.""",
            },
        ],
        "max_completion_tokens": 300,
        "frequency_penalty": 0,
        "presence_penalty": 0,
    }
)

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "api-key": "41603b9fb0d044ed96522e6968bd2c3f",
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)