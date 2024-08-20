class Bot:
    """
    Classe Bot representando um jogador controlado por IA no jogo.

    O bot tem um identificador único e uma velocidade que determina a
    rapidez com que ele se move pelo tabuleiro. A pontuação é usada para
    acompanhar o desempenho do bot durante o jogo.
    """

    def __init__(self, id, velocidade):
        """
        Inicializa um novo bot.

        :param id: Identificador único para o bot.
        :param velocidade: Velocidade de movimento do bot, usada para simular atrasos.
        """
        self.id = id 
        self.velocidade = velocidade  # Valor usado para simular atraso no movimento do bot
        self.pontuacao = 0  # Pontuação acumulada pelo bot durante o jogo
    