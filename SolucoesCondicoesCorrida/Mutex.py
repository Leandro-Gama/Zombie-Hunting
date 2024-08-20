import threading

class Mutex:
    """
    Classe Mutex para exclusão mútua, garantindo que apenas uma thread
    por vez tenha acesso a um recurso compartilhado.

    Esta implementação simples de um mutex (Mutual Exclusion) utiliza
    uma variável de bloqueio (locked) para controlar o acesso ao recurso.
    """

    def __init__(self):
        """
        Inicializa o mutex.

        Define a variável `locked` como False, indicando que o recurso
        está disponível, e cria uma condição de sincronização.
        """
        self.locked = False
        self.condicao = threading.Condition()

    def acquire(self):
        """
        Tenta adquirir o mutex para garantir exclusão mútua.

        Se o mutex já estiver bloqueado, a thread aguardará até que ele seja liberado.
        Quando o mutex é adquirido, a variável `locked` é definida como True.
        """
        with self.condicao:
            while self.locked:
                self.condicao.wait()  # Aguarda até que o mutex seja liberado
            self.locked = True  # Bloqueia o mutex para uso exclusivo

    def release(self):
        """
        Libera o mutex, permitindo que outras threads adquiram o bloqueio.

        Define a variável `locked` como False e notifica todas as threads
        em espera para que elas possam tentar adquirir o mutex.
        """
        with self.condicao:
            self.locked = False  # Libera o mutex
            self.condicao.notify_all()  # Notifica todas as threads em espera
