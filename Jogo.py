import random
import time
from concurrent.futures import ThreadPoolExecutor
from Entidades.Matriz import Matriz
from Entidades.BotJogador import Bot
import SolucoesCondicoesCorrida.Semaforo as Semaforo
import SolucoesCondicoesCorrida.Mutex as Mutex
import SolucoesCondicoesCorrida.Monitor as Monitor
import SolucoesCondicoesCorrida.Barreira as Barreira

def main():
    # Inicializa a matriz do jogo
    tamanho_matriz = 8
    numero_bots = 5
    numero_zombies = 12

    matriz = Matriz(tamanho_matriz)
    bots = [Bot(chr(65 + i), random.uniform(0.1, 0.5)) for i in range(numero_bots)]
    
    matriz.colocar_jogadores(bots)    
    matriz.gerar_zombies(numero_zombies)
    
    print("Matriz inicial:")
    for linha in matriz.matriz:
        print(linha)

    # Solicita ao usuário para definir a condição de corrida
    condicao_corrida = input("\nEscolha a condição de corrida (semaforo, mutex, monitor, barreira): ").strip().lower()

    # Inicializa a condição de corrida e a função de thread correspondente
    if condicao_corrida == 'semaforo':
        semaforo = Semaforo.Semaforo(numero_bots)
        thread_function = lambda matriz, bot: thread_function_semaforo(matriz, bot, semaforo)
    elif condicao_corrida == 'mutex':
        mutex = Mutex.Mutex()
        thread_function = lambda matriz, bot: thread_function_mutex(matriz, bot, mutex)
    elif condicao_corrida == 'monitor':
        monitor = Monitor.Monitor()
        thread_function = lambda matriz, bot: thread_function_monitor(matriz, bot, monitor)
    elif condicao_corrida == 'barreira':
        barreira = Barreira.Barreira(numero_bots)
        thread_function = lambda matriz, bot: thread_function_barreira(matriz, bot, barreira)
    else:
        raise ValueError("Condição de corrida inválida")

    # Cria e executa threads para mover os bots
    with ThreadPoolExecutor(max_workers=numero_bots) as executor:
        for bot in bots:
            executor.submit(thread_function, matriz, bot)

    # Espera as threads terminarem
    executor.shutdown(wait=True)

    # Exibe resultados e encerra o jogo
    print("\nMatriz final:")
    for linha in matriz.matriz:
        print(linha)

    print("\nPontuação final:")
    for bot in bots:
        print(f"Bot {bot.id}: {bot.pontuacao}")
    
    print("\nFim do jogo!")


# Funções das threads para mover os bots:

def thread_function_semaforo(matriz, bot, semaforo):
    while matriz.verificar_existencia_zombies():
        print(f"\t[Thread do Bot {bot.id} tentando adquirir o semáforo...]")
        
        if semaforo.acquire(timeout=1):
            try:
                print(f"\t[Thread do Bot {bot.id} conseguiu adquirir o semáforo.]")
                matriz.mover_bot(bot)
                matriz.verificar_captura(bot)
            finally:
                semaforo.release()
                print(f"\t[Thread do Bot {bot.id} acaba de liberar o semáforo.]")
        
        time.sleep(bot.velocidade)  # Simula o tempo de movimento

    print(f"\t[Thread do Bot {bot.id} terminou porque não há mais zumbis.]")


def thread_function_monitor(matriz, bot, monitor):
    while matriz.verificar_existencia_zombies():
        print(f"\t[Thread do Bot {bot.id} tentando adquirir o monitor...]")
        
        monitor.acquire()
        try:
            print(f"\t[Thread do Bot {bot.id} conseguiu adquirir o monitor.]")
            matriz.mover_bot(bot)
            matriz.verificar_captura(bot)
        finally:
            monitor.release()
            print(f"\t[Thread do Bot {bot.id} acaba de liberar o monitor.]")
        
        time.sleep(bot.velocidade)  # Simula o tempo de movimento

    print(f"\t[Thread do Bot {bot.id} terminou porque não há mais zumbis.]")


def thread_function_barreira(matriz, bot, barreira):
    while matriz.verificar_existencia_zombies():
        print(f"\t[Thread do Bot {bot.id} esperando na barreira...]")
        
        barreira.wait()  # Espera na barreira até que todas as threads cheguem aqui
        print(f"\t[Thread do Bot {bot.id} passou pela barreira.]")
        
        matriz.mover_bot(bot)
        matriz.verificar_captura(bot)
        
        time.sleep(bot.velocidade)  # Simula o tempo de movimento

    print(f"\t[Thread do Bot {bot.id} terminou porque não há mais zumbis.]")

def thread_function_mutex(matriz, bot, mutex):
    while matriz.verificar_existencia_zombies():
        print(f"\t[Thread do Bot {bot.id} tentando adquirir o mutex...]")
        
        mutex.acquire()
        try:
            print(f"\t[Thread do Bot {bot.id} conseguiu adquirir o mutex.]")
            matriz.mover_bot(bot)
            matriz.verificar_captura(bot)
        finally:
            print(f"\t[Thread do Bot {bot.id} liberou o mutex.]")
            mutex.release()
        
        time.sleep(bot.velocidade)  # Simula o tempo de movimento

    print(f"\t[Thread do Bot {bot.id} terminou porque não há mais zumbis.]")


if __name__ == "__main__":
    main()