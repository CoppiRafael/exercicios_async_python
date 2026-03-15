import asyncio
import httpx

#para fazermos multiplas requisições assincronas precisamos da library httpx
#num formato um pouco melhor

#coroutine
async def fetch_get(client: any, pokemon_name: str):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
    response = await client.get(url) # I/O -> para fazer um GET usamos client.get
    # -> toda vez que vou esperar uma resposta eu uso AWAIT
    data = response.json()

    name = data.get("name")
    hability = data.get("moves")[0]["move"]

    print(f"⚡ - name: {name} | move: {hability}⚡")
    print("-=-="*25)


async def main():
    async with httpx.AsyncClient() as client: #httpx.AsyncClient() Estou dizendo que quero um cleinte assíncrono para fazer http's assíncronos 
        await fetch_get(client, "ditto")
        await asyncio.gather(
            fetch_get(client, "charizard"),
            fetch_get(client, "mew"),
        )
        print("Acabei!✔️")

asyncio.run(main())