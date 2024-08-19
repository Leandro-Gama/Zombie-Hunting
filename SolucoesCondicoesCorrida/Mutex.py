import threading

class Mutex:
    def __init__(self):
        self.locked = False
        self.condicao = threading.Condition()

    def acquire(self):
        with self.condicao:
            while self.locked:
                self.condicao.wait()
            self.locked = True

    def release(self):
        with self.condicao:
            self.locked = False
            self.condicao.notify_all()