import asyncio
import sys
import os

# Adiciona o diretório src ao path para os testes
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from api_zen import ApiZen, AsyncApiZen, request_api, ApiZenHttpError

def test_sync():
    print("--- Testando Sync ---")
    api = ApiZen(base_url="https://jsonplaceholder.typicode.com")
    
    # Teste GET
    post = api.get("/posts/1")
    print(f"GET /posts/1: {post['title']}")
    
    # Teste POST
    new_post = api.post("/posts", json={"title": "Zen Title", "body": "Zen Body", "userId": 1})
    print(f"POST /posts: ID {new_post.get('id')}")

    # Teste Error Handling
    try:
        api.get("/invalid-endpoint")
    except ApiZenHttpError as e:
        print(f"Expected Error: {e.status_code}")

async def test_async():
    print("\n--- Testando Async ---")
    api = AsyncApiZen(base_url="https://jsonplaceholder.typicode.com")
    
    # Teste GET Async
    post = await api.get("/posts/2")
    print(f"Async GET /posts/2: {post['title']}")
    
    # Teste Concorrente
    tasks = [api.get(f"/posts/{i}") for i in range(3, 6)]
    results = await asyncio.gather(*tasks)
    print(f"Async Mixed Results: {[r['id'] for r in results]}")

def test_util():
    print("\n--- Testando Utilitário ---")
    data = request_api("https://jsonplaceholder.typicode.com/todos/1")
    print(f"Quick Request: {data['title']}")

if __name__ == "__main__":
    try:
        test_sync()
        test_util()
        asyncio.run(test_async())
        print("\n✅ Todos os testes básicos passaram!")
    except Exception as e:
        print(f"\n❌ Erro durante os testes: {e}")
