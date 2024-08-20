import random

class Matriz:
    """
    Classe Matriz para representar o ambiente de jogo em uma grade NxN.

    A matriz é utilizada para posicionar jogadores (bots) e zombies, e contém
    métodos para manipular e atualizar o estado do jogo, incluindo movimento dos bots,
    geração de zombies e verificação de capturas.
    """

    def __init__(self, n):
        """
        Inicializa uma matriz NxN com todos os valores definidos como (0, None).
        
        :param n: Tamanho da matriz (n x n)
        """
        self.n = n
        self.matriz = [[(0, None) for _ in range(n)] for _ in range(n)]

    def colocar_jogadores(self, jogadores):
        """
        Coloca os jogadores na última linha da matriz, das colunas do meio para os cantos.

        :param jogadores: Lista de objetos jogadores com atributo 'id'
        """
        meio = self.n // 2
        colunas_disponiveis = [meio]
        for i in range(1, meio + 1):
            if meio - i >= 0:
                colunas_disponiveis.append(meio - i)
            if meio + i < self.n:
                colunas_disponiveis.append(meio + i)
        for jogador in jogadores:
            if colunas_disponiveis:
                coluna = colunas_disponiveis.pop(0)
                self.matriz[self.n-1][coluna] = (0, jogador.id)

    def gerar_zombies(self, numero_zombies):
        """
        Gera um número especificado de zombies em posições aleatórias na matriz.
        
        :param numero_zombies: Número de zombies a serem gerados
        """
        zombies_criados = 0
        while zombies_criados < numero_zombies:
            linha = random.randint(0, self.n-1)
            coluna = random.randint(0, self.n-1)
            if self.matriz[linha][coluna] == (0, None):
                self.matriz[linha][coluna] = (1, None)
                zombies_criados += 1
        
    def encontrar_zombie_mais_proximo(self, posicao_jogador):
        """
        Encontra o zombie mais próximo da posição do jogador.
        
        :param posicao_jogador: Tupla contendo a posição do jogador (linha, coluna)
        :return: Posição do zombie mais próximo (linha, coluna) ou None se não houver zombies
        """        
        linha_jogador, coluna_jogador = posicao_jogador
        menor_distancia = float('inf')
        posicao_zombie_mais_proximo = None

        for i in range(self.n):
            for j in range(self.n):
                if self.matriz[i][j][0] == 1:
                    distancia = abs(linha_jogador - i) + abs(coluna_jogador - j)
                    if distancia < menor_distancia:
                        menor_distancia = distancia
                        posicao_zombie_mais_proximo = (i, j)

        return posicao_zombie_mais_proximo

    def proximo_movimento_bot(self, bot):
        """
        Determina o próximo movimento do bot para se aproximar do zombie mais próximo.

        :param bot: Objeto bot com atributo 'id'
        :return: Próxima posição do bot (linha, coluna) ou posição atual se não houver movimento        
        """
        posicao_atual = None
        for i in range(self.n):
            for j in range(self.n):
                if self.matriz[i][j][1] == bot.id:
                    posicao_atual = (i, j)
                    break
            if posicao_atual:
                break

        if not posicao_atual:
            print(f"Bot {bot.id} não encontrado na matriz.")
            return None

        posicao_zombie = self.encontrar_zombie_mais_proximo(posicao_atual)

        if not posicao_zombie:
            print(f"Nenhum zombie encontrado.")
            return None

        linha_atual, coluna_atual = posicao_atual
        linha_zombie, coluna_zombie = posicao_zombie

        # Determinar o próximo movimento
        if linha_atual < linha_zombie:
            return (linha_atual + 1, coluna_atual)  # Mover para baixo
        elif linha_atual > linha_zombie:
            return (linha_atual - 1, coluna_atual)  # Mover para cima
        elif coluna_atual < coluna_zombie:
            return (linha_atual, coluna_atual + 1)  # Mover para a direita
        elif coluna_atual > coluna_zombie:
            return (linha_atual, coluna_atual - 1)  # Mover para a esquerda

        return posicao_atual  # O bot já está na posição do zombie (não se move)
    
    def mover_bot(self, bot):
        """
        Move o bot para a próxima posição determinada pelo método 'proximo_movimento_bot',
        tentando aproximar o bot do zombie mais próximo.

        :param bot: Objeto bot com atributo 'id'
        """
        print(f"Bot {bot.id} tentando se mover...")
        posicao_atual = None
        for i in range(self.n):
            for j in range(self.n):
                if self.matriz[i][j] == (0, bot.id):
                    posicao_atual = (i, j)
                    break
            if posicao_atual:
                break

        nova_posicao = self.proximo_movimento_bot(bot)

        if self.matriz[nova_posicao[0]][nova_posicao[1]][1] is None:
            self.matriz[posicao_atual[0]][posicao_atual[1]] = (0, None)
            self.matriz[nova_posicao[0]][nova_posicao[1]] = (self.matriz[nova_posicao[0]][nova_posicao[1]][0], bot.id)
            print(f"Bot {bot.id} moveu-se para {nova_posicao}.")
        else:
            print(f"Bot {bot.id} encontrou uma célula ocupada em {nova_posicao} e não se moveu.")

    def verificar_captura(self, bot):
        """
        Verifica se o bot capturou um zombie na posição atual e atualiza a pontuação do bot.

        :param bot: Objeto bot com atributo 'id'
        """
        posicao_atual = None
        for i in range(self.n):
            for j in range(self.n):
                if self.matriz[i][j][1] == bot.id:
                    posicao_atual = (i, j)
                    break
            if posicao_atual:
                break

        linha_atual, coluna_atual = posicao_atual

        if self.matriz[linha_atual][coluna_atual][0] == 1:
            print(f"Bot {bot.id} capturou um zombie em ({linha_atual}, {coluna_atual}).")
            # Atualiza a célula para indicar que o zombie foi removido, mas o bot ainda está presente
            self.matriz[linha_atual][coluna_atual] = (0, bot.id)
            bot.pontuacao += 1

    def verificar_existencia_zombies(self):
        """
        Verifica se ainda existem zombies na matriz.

        :return: True se houver zombies, False caso contrário
        """
        for i in range(self.n):
            for j in range(self.n):
                if self.matriz[i][j][0] == 1:
                    return True
        return False
