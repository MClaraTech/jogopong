import pygame
import random

# Inicializar o Pygame e o mixer para sons
pygame.init()
pygame.mixer.init()

# Configurações da tela
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Pong')

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

# Configurações das barras
LARGURA_BARRA, ALTURA_BARRA = 20, 100
x_barra_esquerda = 50
x_barra_direita = LARGURA - 50 - LARGURA_BARRA
velocidade_barra = 10

# Configurações da bola
largura_bola = 20
x_bola = LARGURA // 2
y_bola = ALTURA // 2
velocidade_x_bola = 5 * random.choice((1, -1))
velocidade_y_bola = 5 * random.choice((1, -1))

# Pontuação
pontuacao_esquerda = 0
pontuacao_direita = 0
fonte = pygame.font.SysFont("Arial", 30)

# Flags de controle
jogo_pausado = False

# Carregar sons
som_colisao = pygame.mixer.Sound("hit_sound.wav")
som_ponto = pygame.mixer.Sound("score_sound.wav")

# Função para desenhar as barras
def desenhar_barra(x, y):
    pygame.draw.rect(tela, BRANCO, (x, y, LARGURA_BARRA, ALTURA_BARRA))

# Função para desenhar a bola
def desenhar_bola(x, y):
    pygame.draw.circle(tela, BRANCO, (x, y), largura_bola // 2)

# Função para desenhar o placar
def desenhar_placar():
    texto_placar = f"{pontuacao_esquerda} - {pontuacao_direita}"
    superficie_placar = fonte.render(texto_placar, True, BRANCO)
    tela.blit(superficie_placar, (LARGURA // 2 - superficie_placar.get_width() // 2, 20))

# Função para reiniciar a bola
def reiniciar_bola():
    global x_bola, y_bola, velocidade_x_bola, velocidade_y_bola
    x_bola = LARGURA // 2
    y_bola = ALTURA // 2
    velocidade_x_bola = 5 * random.choice((1, -1))
    velocidade_y_bola = 5 * random.choice((1, -1))

# Função para verificar colisão com as barras
def verificar_colisao():
    global velocidade_x_bola, velocidade_y_bola
    # Colisão com a barra esquerda
    if x_bola - largura_bola // 2 < x_barra_esquerda + LARGURA_BARRA and y_barra_esquerda < y_bola < y_barra_esquerda + ALTURA_BARRA:
        velocidade_x_bola = -velocidade_x_bola
        velocidade_x_bola *= 1.05  # Aumentar a velocidade da bola
        som_colisao.play()  # Tocar som de colisão

    # Colisão com a barra direita
    if x_bola + largura_bola // 2 > x_barra_direita and y_barra_direita < y_bola < y_barra_direita + ALTURA_BARRA:
        velocidade_x_bola = -velocidade_x_bola
        velocidade_x_bola *= 1.05  # Aumentar a velocidade da bola
        som_colisao.play()  # Tocar som de colisão

# Função para tratar eventos de teclado
def tratar_entrada():
    global jogo_pausado, y_barra_esquerda, y_barra_direita

    teclas = pygame.key.get_pressed()

    # Movimento do jogador esquerdo (W e S)
    if teclas[pygame.K_w] and y_barra_esquerda > 0:
        y_barra_esquerda -= velocidade_barra
    if teclas[pygame.K_s] and y_barra_esquerda < ALTURA - ALTURA_BARRA:
        y_barra_esquerda += velocidade_barra

    # Movimento do jogador direito (setas para cima e para baixo)
    if teclas[pygame.K_UP] and y_barra_direita > 0:
        y_barra_direita -= velocidade_barra
    if teclas[pygame.K_DOWN] and y_barra_direita < ALTURA - ALTURA_BARRA:
        y_barra_direita += velocidade_barra

    # Pausar ou retomar o jogo (Espaço)
    if teclas[pygame.K_SPACE]:
        jogo_pausado = not jogo_pausado

# Função para atualizar o jogo
def atualizar_jogo():
    global x_bola, y_bola, velocidade_x_bola, velocidade_y_bola, pontuacao_esquerda, pontuacao_direita

    if not jogo_pausado:
        # Atualizar a posição da bola
        x_bola += velocidade_x_bola
        y_bola += velocidade_y_bola

        # Colisão com as paredes superior e inferior
        if y_bola - largura_bola // 2 < 0 or y_bola + largura_bola // 2 > ALTURA:
            velocidade_y_bola = -velocidade_y_bola

        # Verificar colisão com as barras
        verificar_colisao()

        # Marcar ponto
        if x_bola - largura_bola // 2 < 0:
            pontuacao_direita += 1
            som_ponto.play()  # Tocar som de ponto
            reiniciar_bola()
        elif x_bola + largura_bola // 2 > LARGURA:
            pontuacao_esquerda += 1
            som_ponto.play()  # Tocar som de ponto
            reiniciar_bola()

# Função principal
def principal():
    global y_barra_esquerda, y_barra_direita

    # Posições iniciais das barras
    y_barra_esquerda = ALTURA // 2 - ALTURA_BARRA // 2
    y_barra_direita = ALTURA // 2 - ALTURA_BARRA // 2

    rodando = True
    while rodando:
        tela.fill(PRETO)

        # Lidar com os eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        # Verificar entradas de teclado
        tratar_entrada()

        # Atualizar o jogo
        atualizar_jogo()

        # Desenhar os elementos do jogo
        desenhar_barra(x_barra_esquerda, y_barra_esquerda)
        desenhar_barra(x_barra_direita, y_barra_direita)
        desenhar_bola(x_bola, y_bola)
        desenhar_placar()

        # Atualizar a tela
        pygame.display.flip()

        # Controlar o FPS
        pygame.time.Clock().tick(60)

    pygame.quit()

# Executar o jogo
if __name__ == "__main__":
    principal()
