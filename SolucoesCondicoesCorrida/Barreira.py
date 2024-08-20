import threading

class Barreira:
    """
    Classe Barreira para sincronização de threads em pontos específicos.

    Uma barreira é um ponto de sincronização onde várias threads devem esperar
    até que todas tenham alcançado o ponto, antes de prosseguir. Ela é útil em
    situações onde é necessário que todas as threads cheguem a um determinado estado
    antes de continuar a execução.
    """

    def __init__(self, n):
        """
        Inicializa a barreira.

        :param n: Número de threads que devem alcançar a barreira antes de prosseguir.
        """
        self.n = n
        self.count = 0
        self.condicao = threading.Condition()

    def wait(self):
        """
        Faz a thread esperar na barreira até que todas as threads tenham chegado.

        Quando o número de threads que chamaram `wait` for igual a `n`, todas
        as threads são liberadas para continuar a execução. Se uma thread chegar
        antes disso, ela aguardará até que as outras também cheguem.
        """
        with self.condicao:
            self.count += 1  # Incrementa o contador de threads que chegaram à barreira
            if self.count == self.n:
                self.count = 0  # Reseta o contador para reutilização da barreira
                self.condicao.notify_all()  # Libera todas as threads em espera
            else:
                self.condicao.wait()  # Aguarda até que todas as threads cheguem à barreira
