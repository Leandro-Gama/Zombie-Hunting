import random
class Matriz:
    def __init__(self, n):
        self.n = n
        self.matriz = [[(0, None) for _ in range(n)] for _ in range(n)]

    def colocar_jogadores(self, jogadores):
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
        zombies_criados = 0
        while zombies_criados < numero_zombies:
            linha = random.randint(0, self.n-1)
            coluna = random.randint(0, self.n-1)
            if self.matriz[linha][coluna] == (0, None):
                self.matriz[linha][coluna] = (1, None)
                zombies_criados += 1
        
    def encontrar_zombie_mais_proximo(self, posicao_jogador):
        linha_jogador, coluna_jogador = posicao_jogador
        menor_distancia = float('inf')
        posicao_zombie_mais_proximo = None

        for i in range(self.n):
            for j in range(self.n):
                if self.matriz[i][j][0] == 1:  # Se há um zombie na posição (i, j)
                    distancia = abs(linha_jogador - i) + abs(coluna_jogador - j)
                    if distancia < menor_distancia:
                        menor_distancia = distancia
                        posicao_zombie_mais_proximo = (i, j)

        return posicao_zombie_mais_proximo

    def proximo_movimento_bot(self, bot):
        # Encontrar a posição atual do bot
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
            # Atualiza a célula para indicar que o zumbi foi removido, mas o bot ainda está presente
            self.matriz[linha_atual][coluna_atual] = (0, bot.id)
            bot.pontuacao += 1

    def verificar_existencia_zombies(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.matriz[i][j][0] == 1:
                    return True
        return False
