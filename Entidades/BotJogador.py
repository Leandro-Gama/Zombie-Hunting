class Bot:
    def __init__(self, id, velocidade):
        self.id = id 
        self.velocidade = velocidade   # Tempo (em segundos) para se deslocar entre as células
        self.pontuacao = 0
    
    def __repr__(self):
        return f"Bot {self.id}"