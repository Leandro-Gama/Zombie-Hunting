import threading

class Monitor:
    def __init__(self):
        self.locked = False
        self.condition = threading.Condition()

    def acquire(self):
        with self.condition:
            while self.locked:
                self.condition.wait()
            self.locked = True

    def release(self):
        with self.condition:
            self.locked = False
            self.condition.notify()

    def wait(self, timeout=None):
        with self.condition:
            self.locked = False
            self.condition.notify()
            self.condition.wait(timeout)
            self.locked = True

    def notify(self):
        with self.condition:
            self.condition.notify()
