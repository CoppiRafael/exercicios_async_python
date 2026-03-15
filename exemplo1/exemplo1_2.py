import asyncio
import time

async def baixar_arquivo(nome, segundos):
    print(f"-> Iniciando download de: {nome} (levará {segundos}s)")
    # O segredo está aqui: não usamos time.sleep(), pois ele trava o programa inteiro.
    # Usamos o sleep do asyncio para "ceder" o controle de volta ao loop.
    await asyncio.sleep(segundos) 
    print(f"<- Download de {nome} finalizado!")

async def main():
    start_time = time.perf_counter()
    
    # Criamos as tarefas para que o loop saiba que elas devem rodar
    print("Preparando downloads...")
    await asyncio.gather(
        baixar_arquivo("Banco de Dados", 3),
        baixar_arquivo("Imagens de Satélite", 2)
    )
    
    end_time = time.perf_counter()
    print(f"\nTempo total de execução: {end_time - start_time:.2f} segundos.")

if __name__ == "__main__":
    asyncio.run(main())