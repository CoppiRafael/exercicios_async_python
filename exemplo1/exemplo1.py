import asyncio 

#Coroutine  -> Toda vez que definimos uma função assincrona ela é chamada "Corrotina"
async def say_hello(name):
    print(f"{name} is starting...⚡")
    await asyncio.sleep(2) #simulando um IO (talvez uma requisição numa API)
    print(f"{name} says hello ✔️")


async def main():
    # "Toda vez" que eu tiver uma corrotina (async def) eu só irei conseguir chamar esssa corrotina a partir de um "await"
    print("\n -=-=-=-==-=-==- DE MANEIRA ASSÍNCRONA(gather)-=-=-=-==-=-==- \n")
    await asyncio.gather(
        say_hello("Rafael"),
        say_hello("Anjos"),
        say_hello("Serjinho"),
    )
    #0 gather se torna um elemento com dois objetos. Então se eu colocar um await fora dele ele estará rodando sincronamente com o gather porém o gather tem objetos assincronos dentro dele
    print("\n -=-=-=-==-=-==- AGORA DE MANEIRA SÍNCRONA-=-=-=-==-=-==- \n")
    await say_hello("Luisão")
asyncio.run(main()) #estamos aqui informando para o python a maneira que estamos programando, que é assincronamente

