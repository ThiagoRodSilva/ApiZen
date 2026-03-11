from api_zen import ApiZen
import logging

# Opcional: Você pode mudar o nível do log se quiser menos detalhes
# logging.getLogger("ApiZen").setLevel(logging.WARNING)

print("--- Testando ApiZen ---")

# 1. Base URL e Logging Automático
api = ApiZen(base_url="https://api.disneyapi.dev", timeout=5)

# 2. Helper de Autenticação
api.set_token("meu_token_secreto")

print("\nFazendo requisição:")
try:
    data = api.get("character")
    print(f"\nSucesso! Recebemos dados de {len(data['data'])} personagens.")
except Exception as e:
    print(f"\nErro no teste: {e}")
