# ApiZen 🚀

Uma biblioteca Python moderna, leve e resiliente para simplificar a interação com APIs REST. Esqueça a configuração manual de retentativas, timeouts e headers de autenticação toda vez que for iniciar um novo projeto.

---

## ✨ Principais Recursos

- **Resiliência Integrada**: Retentativas automáticas (retries) para erros comuns de servidor (500, 502, 503, 504) e rate limit (429).
- **Logging Automático**: Feedback em tempo real no terminal sobre URLs chamadas, métodos, status de resposta e tempo de execução.
- **Sessões Persistentes**: Utiliza `requests.Session()` internamente para melhor performance.
- **Autenticação Simplificada**: Configure tokens Bearer ou outros esquemas com um único comando.
- **Tratamento de Erros**: Lança exceções automaticamente (`raise_for_status()`) para respostas de erro.

---

## 📦 Instalação

### Instalação em modo desenvolvimento/local
Para testar a biblioteca localmente no seu ambiente virtual:

```bash
# Ative seu venv primeiro
.\.venv\Scripts\Activate.ps1

# Instale em modo editável
pip install -e .
```

---

## 🚀 Como Usar

### 1. Uso Básico (Rápido)
Para uma chamada única e rápida sem configurações:

```python
from api_zen import request_api

data = request_api("https://api.github.com")
print(data)
```

### 2. Uso Profissional (ApiZen)
Recomendado para projetos que interagem com uma API específica:

```python
from api_zen import ApiZen

# Configura o cliente uma única vez
api = ApiZen(
    base_url="https://api.exemplo.com", # URL base para todos os endpoints
    timeout=10,                        # Tempo limite de espera (segundos)
    max_retries=3                      # Número de tentativas em caso de erro
)

# Configura autenticação Bearer
api.set_token("seu_token_aqui")

# Faz a chamada e recebe o JSON já convertido
usuarios = api.get("usuarios") 
```

### 3. Métodos Suportados
A classe `ApiZen` suporta os principais verbos HTTP:

```python
api.get("endpoint", params={"id": 1})
api.post("endpoint", json={"nome": "Thiago"})
api.put("endpoint", json={"status": "ativo"})
api.delete("endpoint")
```

---

## 🛠️ Estrutura do Projeto

```text
api-zen/
├── pyproject.toml      # Configurações de build e dependências
├── README.md           # Esta documentação
├── src/
│   └── api_zen/        # Corrigido: underscore para importação
│       ├── __init__.py  # Exportação da API pública
│       └── core.py      # Lógica robusta com ApiZen
└── tests/
    └── verify_install.py # Script de teste rápido
```

---

## 📖 Dependências

- `requests`: A base sólida para comunicações HTTP.
- `urllib3`: Gerenciamento avançado de retentativas.

---

## 🤝 Contribuindo

Sinta-se à vontade para sugerir melhorias ou abrir issues! Esta biblioteca foi criada para ser o ponto de partida ideal para qualquer integração de API em Python.

---

## 📄 Licença

Este projeto está sob a licença [MIT](LICENSE).
