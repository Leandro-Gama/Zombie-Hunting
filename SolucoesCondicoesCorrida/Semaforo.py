import threading
import time

class Semaforo:
    """
    Classe Semaforo para controle de acesso a recursos compartilhados entre threads.
    
    Este semáforo permite que um número limitado de threads acessem um recurso 
    ao mesmo tempo. Ele é inicializado com um valor que representa o número de recursos
    disponíveis. Threads chamam `acquire` para tentar acessar o recurso e `release`
    para liberar o recurso quando terminarem.
    """

    def __init__(self, valor=1):
        """
        Inicializa o semáforo com um valor inicial.

        :param valor: Número de permissões disponíveis (default é 1).
        """
        self.valor = valor
        self.condicao = threading.Condition()

    def acquire(self, timeout=None):
        """
        Tenta adquirir uma permissão para acessar o recurso.
        
        Se o valor do semáforo for maior que zero, diminui o valor e permite o acesso.
        Caso contrário, a thread espera até que o recurso esteja disponível.
        
        :param timeout: Tempo máximo de espera em segundos (opcional).
        :return: True se a permissão foi adquirida, False se o tempo de espera expirou.
        """
        with self.condicao:
            start_time = time.time()  # Marca o início do tempo de espera
            while self.valor <= 0:
                remaining = timeout - (time.time() - start_time)  # Calcula o tempo restante
                if remaining <= 0:  # Se o tempo expirou, retorna False
                    return False
                self.condicao.wait(remaining)  # Espera até que o recurso esteja disponível ou o tempo expire
            self.valor -= 1  # Reduz o valor do semáforo, indicando que um recurso foi adquirido
            return True

    def release(self):
        """
        Libera uma permissão, aumentando o valor do semáforo.
        
        Notifica uma das threads esperando para que ela possa tentar adquirir o recurso.
        """
        with self.condicao:
            self.valor += 1  # Aumenta o valor do semáforo, indicando que um recurso foi liberado
            self.condicao.notify()  # Notifica uma thread em espera
