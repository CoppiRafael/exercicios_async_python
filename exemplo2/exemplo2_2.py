import asyncio
import httpx
import time

async def buscar_pokemon(client, poke_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{poke_id}"
    
    # O httpx facilita a leitura: await client.get() já inicia o processo
    response = await client.get(url)
    
    # Verificamos se a requisição teve sucesso (Status 200)
    if response.status_code == 200:
        dados = response.json()
        nome = dados['name'].capitalize()
        print(f"[ID {poke_id}] Capturado : {nome}")
        return nome
    else:
        print(f"[ID {poke_id}] Erro: {response.status_code}")
        return None

async def main():
    ids = [1, 4, 7, 25, 150, 149, 52] # Aumentamos a lista para testar a performance
    
    start_time = time.perf_counter()

    # Usamos o ASYNC Client para manter as conexões abertas (Keep-Alive)
    async with httpx.AsyncClient() as client:
        # Criamos a lista de tarefas (Comprehension)
        tarefas = [buscar_pokemon(client, pid) for pid in ids]
        
        # O maestro (gather) executa a sinfonia
        resultados = await asyncio.gather(*tarefas)
        
    end_time = time.perf_counter()
    
    # Filtramos possíveis erros (Nones) e exibimos
    sucessos = [r for r in resultados if r]
    print(f"\nTotal capturado: {len(sucessos)} pokémons.")
    print(f"Tempo total: {end_time - start_time:.2f}s")

if __name__ == "__main__":
    asyncio.run(main())