# 🧘 ApiZen

[![PyPI version](https://img.shields.io/pypi/v/api-zen.svg)](https://pypi.org/project/api-zen/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**ApiZen** é uma biblioteca Python moderna, leve e resiliente projetada para tornar a interação com APIs REST o mais simples possível. Inspirada na filosofia Zen, ela elimina o "boilerplate" e foca na clareza e robustez.

---

## ✨ Funcionalidades

- 🚀 **Sync & Async**: Suporte nativo para requisições síncronas (`requests`) e assíncronas (`httpx`).
- 🛡️ **Exceções Customizadas**: Hierarquia de erros clara para facilitar o tratamento de falhas.
- 🔄 **Resiliência Integrada**: Retentativas automáticas inteligentes (Exponential Backoff) com `tenacity`.
- 🔑 **Auth Facilitado**: Helpers para tokens dinâmicos.
- 📝 **Logging Transparente**: Acompanhe o que acontece em cada requisição.
- ⚡ **Zero Config**: Comece com uma linha de código, mas configure tudo se precisar.

---

## 📦 Instalação

```bash
pip install api-zen
```

---

## 🛠️ Como Usar

### 1. Requisição Rápida (Estilo Zen)
Para algo rápido, você nem precisa instanciar uma classe:

```python
from api_zen import request_api

data = request_api("https://jsonplaceholder.typicode.com/posts/1")
print(data['title'])
```

### 2. Uso Síncrono (Recomendado para Scripts)

```python
from api_zen import ApiZen

# Configure uma base URL e headers padrão
api = ApiZen(base_url="https://api.exemplo.com", timeout=5)
api.set_token("seu-token-aqui")

# GET
users = api.get("/users", params={"active": "true"})

# POST
new_user = api.post("/users", json={"name": "Thiago", "role": "Dev"})

# Outros métodos: put(), patch(), delete(), head(), options()
```

### 3. Uso Assíncrono (Para Performance Máxima)

```python
import asyncio
from api_zen import AsyncApiZen

async def main():
    api = AsyncApiZen(base_url="https://jsonplaceholder.typicode.com")
    
    # Executa várias requisições concorrentemente
    tasks = [api.get(f"/posts/{i}") for i in range(1, 5)]
    results = await asyncio.gather(*tasks)
    
    for post in results:
        print(post['title'])

asyncio.run(main())
```

---

## 🚨 Tratamento de Erros

A ApiZen fornece exceções específicas para que seu código seja mais previsível:

```python
from api_zen import ApiZen, ApiZenHttpError, ApiZenError

api = ApiZen()

try:
    data = api.get("https://api.exemplo.com/recurso-inexistente")
except ApiZenHttpError as e:
    print(f"Erro HTTP {e.status_code}: {e.response_data}")
except ApiZenError as e:
    print(f"Erro de conexão ou timeout: {e}")
```

---

## ⚙️ Configuração de Resiliência

Por padrão, a ApiZen tenta realizar até **3 tentativas** com um intervalo exponencial se encontrar erros de rede ou timeouts. Você pode customizar isso na inicialização:

```python
api = ApiZen(max_retries=5, timeout=15)
```

---

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir Issues ou Pull Requests no repositório oficial.

---

## 📄 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.
