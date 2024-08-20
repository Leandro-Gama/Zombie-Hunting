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
    """
    Função principal que inicializa a matriz, bots, zombies e gerencia o jogo com condições de corrida.
    """
    # Define o tamanho da matriz e o número de bots e zombies
    tamanho_matriz = 8
    numero_bots = 5
    numero_zombies = 12

    # Inicializa a matriz do jogo e os bots
    matriz = Matriz(tamanho_matriz)
    bots = [Bot(chr(65 + i), random.uniform(0.1, 0.5)) for i in range(numero_bots)]
    
    # Posiciona os bots na matriz e gera os zombies
    matriz.colocar_jogadores(bots)    
    matriz.gerar_zombies(numero_zombies)
    
    print("Matriz inicial:")
    for linha in matriz.matriz:
        print(linha)

    # Solicita ao usuário para escolher a condição de corrida
    condicao_corrida = input("\nEscolha a condição de corrida (semaforo, mutex, monitor, barreira): ").strip().lower()

    # Inicializa a condição de corrida e associa a função de thread correspondente
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

    # Cria e executa threads para mover os bots de acordo com a condição de corrida selecionada
    with ThreadPoolExecutor(max_workers=numero_bots) as executor:
        for bot in bots:
            executor.submit(thread_function, matriz, bot)

    # Aguarda o término de todas as threads
    executor.shutdown(wait=True)

    # Exibe os resultados finais do jogo
    print("\nMatriz final:")
    for linha in matriz.matriz:
        print(linha)

    print("\nPontuação final:")
    for bot in bots:
        print(f"Bot {bot.id}: {bot.pontuacao}")
    
    print("\nFim do jogo!")


# Funções das threads para mover os bots:

def thread_function_semaforo(matriz, bot, semaforo):
    """
    Função da thread que usa um semáforo para controlar o acesso ao recurso compartilhado (a matriz).
    
    - Cada bot tenta adquirir o semáforo antes de se mover na matriz.
    - Se o semáforo for adquirido, o bot realiza seu movimento e verifica se capturou um zombie.
    - O semáforo é liberado após o movimento, permitindo que outros bots possam tentar adquiri-lo.
    - A função continua até que não existam mais zombies na matriz.
    """
    while matriz.verificar_existencia_zombies():
        print(f"\t[Thread do Bot {bot.id} tentando adquirir o semáforo...]")
        
        # Tenta adquirir o semáforo com um timeout
        if semaforo.acquire(timeout=1):
            try:
                print(f"\t[Thread do Bot {bot.id} conseguiu adquirir o semáforo.]")
                matriz.mover_bot(bot)
                matriz.verificar_captura(bot)
            finally:
                # Libera o semáforo para que outros bots possam utilizá-lo
                semaforo.release()
                print(f"\t[Thread do Bot {bot.id} acaba de liberar o semáforo.]")
        
        time.sleep(bot.velocidade)  # Simula o tempo de movimento

    print(f"\t[Thread do Bot {bot.id} terminou porque não há mais zumbis.]")


def thread_function_monitor(matriz, bot, monitor):
    """
    Função da thread que usa um monitor para controlar o acesso ao recurso compartilhado.
    
    - Cada bot tenta adquirir o monitor antes de se mover na matriz.
    - O monitor garante que apenas uma thread (bot) execute a seção crítica (movimento e verificação de captura) por vez.
    - O monitor é liberado após o movimento, permitindo que outros bots possam adquiri-lo.
    - A função continua até que não existam mais zombies na matriz.
    """
    while matriz.verificar_existencia_zombies():
        print(f"\t[Thread do Bot {bot.id} tentando adquirir o monitor...]")
        
        # Tenta adquirir o monitor (seção crítica)
        monitor.acquire()
        try:
            print(f"\t[Thread do Bot {bot.id} conseguiu adquirir o monitor.]")
            matriz.mover_bot(bot)
            matriz.verificar_captura(bot)
        finally:
            # Libera o monitor para outros bots
            monitor.release()
            print(f"\t[Thread do Bot {bot.id} acaba de liberar o monitor.]")
        
        time.sleep(bot.velocidade)  # Simula o tempo de movimento

    print(f"\t[Thread do Bot {bot.id} terminou porque não há mais zumbis.]")


def thread_function_barreira(matriz, bot, barreira):
    """
    Função da thread que usa uma barreira para sincronizar a execução dos bots.
    
    - Cada bot espera na barreira até que todos os bots estejam prontos para o próximo movimento.
    - A barreira sincroniza as threads, permitindo que elas avancem juntas para a próxima fase do jogo.
    - Após passar pela barreira, o bot se move e verifica se capturou um zombie.
    - A função continua até que não existam mais zombies na matriz.
    """
    mutex = Mutex.Mutex()
    while matriz.verificar_existencia_zombies():
        print(f"\t[Thread do Bot {bot.id} esperando na barreira...]")
        
        # Espera na barreira até que todas as threads (bots) cheguem a este ponto
        barreira.wait()
        print(f"\t[Thread do Bot {bot.id} passou pela barreira.]")
        
        mutex.acquire()
        try:
            matriz.mover_bot(bot)
            matriz.verificar_captura(bot)
        finally:
            mutex.release()
        
        time.sleep(bot.velocidade)  # Simula o tempo de movimento

    print(f"\t[Thread do Bot {bot.id} terminou porque não há mais zumbis.]")


def thread_function_mutex(matriz, bot, mutex):
    """
    Função da thread que usa um mutex para garantir exclusão mútua ao acessar a matriz.
    
    - Cada bot tenta adquirir o mutex antes de acessar a matriz.
    - O mutex garante que apenas um bot possa realizar seu movimento por vez.
    - Após mover o bot e verificar se ele capturou um zombie, o mutex é liberado.
    - A função continua até que não existam mais zombies na matriz.
    """
    while matriz.verificar_existencia_zombies():
        print(f"\t[Thread do Bot {bot.id} tentando adquirir o mutex...]")
        
        # Tenta adquirir o mutex (exclusão mútua)
        mutex.acquire()
        try:
            print(f"\t[Thread do Bot {bot.id} conseguiu adquirir o mutex.]")
            matriz.mover_bot(bot)
            matriz.verificar_captura(bot)
        finally:
            # Libera o mutex para que outros bots possam utilizá-lo
            print(f"\t[Thread do Bot {bot.id} liberou o mutex.]")
            mutex.release()
        
        time.sleep(bot.velocidade)  # Simula o tempo de movimento

    print(f"\t[Thread do Bot {bot.id} terminou porque não há mais zumbis.]")


if __name__ == "__main__":
    main()