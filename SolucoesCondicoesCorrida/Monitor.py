import threading

class Monitor:
    """
    Classe Monitor para sincronização de threads, combinando mutex e condição.
    
    Um monitor permite que apenas uma thread por vez execute código dentro de um bloco sincronizado.
    Ele também fornece métodos para que as threads possam esperar por condições e serem notificadas.
    """

    def __init__(self):
        """
        Inicializa o monitor.

        Define a variável `locked` como False, indicando que o monitor está desbloqueado,
        e cria uma condição de sincronização.
        """
        self.locked = False
        self.condition = threading.Condition()

    def acquire(self):
        """
        Adquire o monitor, bloqueando-o para exclusão mútua.

        Se o monitor já estiver bloqueado, a thread aguardará até que ele seja liberado.
        Quando o monitor é adquirido, a variável `locked` é definida como True.
        """
        with self.condition:
            while self.locked:
                self.condition.wait()  # Aguarda até que o monitor seja liberado
            self.locked = True  # Bloqueia o monitor para uso exclusivo

    def release(self):
        """
        Libera o monitor, permitindo que outras threads o adquiram.

        Define a variável `locked` como False e notifica uma thread
        em espera para que ela possa adquirir o monitor.
        """
        with self.condition:
            self.locked = False  # Libera o monitor
            self.condition.notify()  # Notifica uma thread em espera

    def wait(self, timeout=None):
        """
        Faz a thread liberar o monitor e esperar por uma notificação.

        A thread libera o monitor (permitindo que outra thread o adquira),
        aguarda por uma notificação ou até que o tempo limite expire,
        e depois tenta adquirir o monitor novamente.

        :param timeout: Tempo máximo de espera em segundos (opcional).
        """
        with self.condition:
            self.locked = False  # Libera o monitor antes de esperar
            self.condition.notify()  # Notifica outra thread antes de esperar
            self.condition.wait(timeout)  # Aguarda até ser notificada ou até que o tempo expire
            self.locked = True  # Re-adquire o monitor após a espera

    def notify(self):
        """
        Notifica uma thread em espera para que ela possa prosseguir.

        Este método deve ser chamado quando uma thread deseja acordar outra thread
        que está esperando por uma condição no monitor.
        """
        with self.condition:
            self.condition.notify()  # Notifica uma thread em espera
