import threading

class Barreira:
    def __init__(self, n):
        self.n = n
        self.count = 0
        self.condicao = threading.Condition()

    def wait(self):
        with self.condicao:
            self.count += 1
            if self.count == self.n:
                self.count = 0
                self.condicao.notify_all()
            else:
                self.condicao.wait()