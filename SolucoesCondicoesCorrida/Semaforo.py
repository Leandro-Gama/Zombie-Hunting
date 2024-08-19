import threading
import time

class Semaforo:
    def __init__(self, valor=1):
        self.valor = valor
        self.condicao = threading.Condition()

    def acquire(self, timeout=None):
        with self.condicao:
            start_time = time.time()
            while self.valor <= 0:
                remaining = timeout - (time.time() - start_time)
                if remaining <= 0:
                    return False
                self.condicao.wait(remaining)
            self.valor -= 1
            return True

    def release(self):
        with self.condicao:
            self.valor += 1
            self.condicao.notify()