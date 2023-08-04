import os
import pygame
from pygame import mixer
import random
# Inicialização do Pygame
pygame.init()

# posição inicial da nave
x = 500
y = 660

#cores
DOURADO = (255, 215, 0)
CIANO = (0, 255, 255)  
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

#importaçao das imagens
caminho_atual = os.path.abspath(os.path.dirname(__file__))
nave_ret = os.path.join(caminho_atual, 'nave.png')
fundo_ret = os.path.join(caminho_atual, 'fundo.jpeg')
fonte_ret = os.path.join(caminho_atual, 'Guardians.ttf')
musica_ret = os.path.join(caminho_atual, 'guardiões.mp3')
alien_ret = os.path.join(caminho_atual, 'leviathan.png')
lista_palavras = os.path.join(caminho_atual, 'lista.txt')
nave_img = pygame.image.load(nave_ret)
img_fundo = pygame.image.load(fundo_ret)
alien = pygame.image.load(alien_ret)
fonte = pygame.font.Font(fonte_ret, 32)
fonte_p = pygame.font.Font(fonte_ret, 16)
fonte_g = pygame.font.Font(fonte_ret, 64)
musica = pygame.mixer.music.load(musica_ret)
alien_red = pygame.transform.scale(alien, (150, 40))
nave_red = pygame.transform.scale(nave_img, (100, 40))

tempo_restante = 9900
ultima_atualizacao_tempo = pygame.time.get_ticks()

#velocidades
vel = [5, 3, 2]
vel_nave = 3
vel_tiro = 15
vel_letra = 2
vel_alien = random.choices(vel, k=4)

#posição de spawn dos aliens
rectx_1 = 200
rectx_2 = 400
rectx_3 = 600
recty = 260

pontuacao = 0

#musica de fundo
mixer.music.play(-1)

#janela
largura_janela = 1000
altura_janela = 700
janela = pygame.display.set_mode((largura_janela, altura_janela))
pygame.display.set_caption('Word Zapper')

#tiros
tiro_img = pygame.Surface((5, 30))#formato
tiro_img.fill(CIANO)#cor
tiro_largura = tiro_img.get_width()
tiro_altura = tiro_img.get_height()
tiros = []#lista vazia para armazenar os tiros

# Definição das letras
letras = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']#lista das letras (minuscula pois na fonte que eu importei as maiusculas tavam zoadas)
letras_pos_x = [largura_janela + i * 100 for i in range(27)]#posiçao das letras na horizontal( i e variavel de 0 a 26)
letras_pos_y = [altura_janela // 4 for _ in range(27)]#posiçao das letras na vertical

def sortear_nova_palavra():
    global palavra_sorteada, letras_acertadas
    palavra_sorteada = random.choice(palavras)
    letras_acertadas = ['?' for _ in set(palavras)]

# Definição das palavras
with open(lista_palavras,encoding="utf-8 ") as arquivo:
    todas_palavras = arquivo.readlines()

palavras = [linhas.rstrip() for linhas in todas_palavras]#importar lista
palavra_sorteada = random.choice(palavras)#sorteio das palavras
letras_acertadas = ['?' for _ in set(palavra_sorteada)]#trocar a lacuna pela letra acertada
palavra_revelada = False

# Tempo para substituir a palavra por lacunas
tempo_substituicao = 1000#tempo que a palavra sorteada vai ficar na tela antes de ser substituida por lacunas
tempo_inicio_substituicao = None

# Função para desenhar a tela
def desenhar_tela():

    #fundo
    janela.blit(img_fundo, (0, 0))

    #nave
    nave = janela.blit(nave_red, (x, y))

    #alien
    alien1 = janela.blit(alien_red, (rectx_1, recty))
    alien2 = janela.blit(alien_red, (rectx_2, recty + 100))
    alien3 = janela.blit(alien_red, (rectx_3, recty + 200))

    texto_tempo_restante = fonte.render(f"{tempo_restante // 100}", True, BRANCO)
    janela.blit(texto_tempo_restante, (largura_janela // 2 - texto_tempo_restante.get_width() // 2, 10))

    #tiros
    for tiro in tiros:
        pygame.draw.rect(janela, CIANO, (tiro[0], tiro[1], tiro_largura, tiro_altura))

    # Desenha as letras
    for i in range(len(letras)):
        letra = letras[i]
        posicao_x = letras_pos_x[i]
        posicao_y = letras_pos_y[i]
        texto = fonte.render(letra, True, DOURADO)
        janela.blit(texto, (posicao_x, posicao_y))

    # Desenha a palavra sorteada ou as lacunas
    if palavra_revelada:
        palavra_renderizada = fonte.render('?'.join(letras_acertadas), True, DOURADO)#lacunas//ALT
        janela.blit(palavra_renderizada, (20, altura_janela // 6))#posiçao das lacunas
    else:
        palavra_renderizada = fonte.render(palavra_sorteada, True, DOURADO)#letras acertadas
        janela.blit(palavra_renderizada, (20, altura_janela // 6))#posiçao das letras acertadas e da palavra-objetivo
    pygame.display.update()

#definição das telas que vão ser chamadas posteriormente
def tela_lose():
    global janela_aberta
    exibir_tela_lose = True
    while exibir_tela_lose:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    # Reiniciar o jogo
                    reiniciar_jogo()
                    
                    exibir_tela_lose = False
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                # Obter as coordenadas do clique do mouse
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Verificar se o botão 'Sim' foi clicado
                if 300 <= mouse_x <= 300 + texto_sim.get_width() and 500 <= mouse_y <= 500 + texto_sim.get_height():
                    # Reiniciar o jogo
                    reiniciar_jogo()
                    janela_aberta = True
                    exibir_tela_lose = False
                # Verificar se o botão 'Não' foi clicado
                elif 600 <= mouse_x <= 600 + texto_nao.get_width() and 500 <= mouse_y <= 500 + texto_nao.get_height():
                    pygame.quit()
                    quit()
        # preencher o fundo com a cor preta
        janela.fill((0, 0, 0))
        # posicionar o texto na janela
        janela.blit(texto_game_over_l, (230, 200))
        janela.blit(texto_jogar_novamente, (140, 360))
        janela.blit(texto_sim, (300, 500))
        janela.blit(texto_nao, (600, 500))
        pygame.display.update()

def reiniciar_jogo():
    global x, y, pontuacao, tempo_restante, palavra_sorteada, letras_acertadas, palavra_revelada, inicio_jogo, tempo_inicio_substituicao, janela_aberta
    
    #abrir a tela 
    janela_aberta = True

    # Redefinir posição inicial da nave
    x = 500
    y = 660

    # Redefinir pontuação e tempo restante
    pontuacao = 0
    tempo_restante = 9900

    # Sortear nova palavra e atualizar as lacunas
    sortear_nova_palavra()
    palavra_revelada = False

    # Reiniciar o jogo
    inicio_jogo = False
    tempo_inicio_substituicao = 1000

exibir_tela_lose = False
exibir_menu = 'menu'
exibir_menu = False
exibir_instrucoes = 'instruções'
exibir_instrucoes = False
# Renderizar texto
texto_game_over_l =fonte_g.render("GAME OVER", True, (BRANCO))
texto_jogar_novamente = fonte.render("Deseja jogar novamente?", True, (BRANCO))
texto_sim = fonte.render("Sim", True, (BRANCO))
texto_nao = fonte.render("Não", True, (BRANCO))
texto_titulo = fonte_g.render("WORDZAPPER", True, (BRANCO))
texto_jogar = fonte.render("JOGAR", True, (BRANCO))
texto_instrucoes = fonte.render("INSTRUÇÕES", True, (BRANCO))
texto_sair = fonte.render("SAIR", True, (BRANCO))
texto_instrucoes1 = fonte_p.render("        O objetivo do jogo e acertar as letras", True, (BRANCO))
texto_instrucoes2 = fonte_p.render("  para completar a palavra apresentada inicialmente", True, (BRANCO))
texto_instrucoes5 = fonte_p.render("cuidado com os aliens, eles farao voce perder tempo!", True, (BRANCO))
texto_instrucoes3 = fonte_p.render("Use as teclas de seta para mover a nave.", True, (BRANCO))
texto_instrucoes4 = fonte.render("          Boa sorte!", True, (BRANCO))
texto_voltar = fonte.render('voltar', True, (BRANCO))
# Loop do menu inicial
exibir_menu = True
while exibir_menu:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            #coordenadas do clique do mouse
            mouse_x, mouse_y = pygame.mouse.get_pos()
            #qual opção foi selecionada
            if 410 <= mouse_x <= 410 + texto_jogar.get_width() and 330 <= mouse_y <= 330 + texto_jogar.get_height():
                exibir_menu = False
            elif 335 <= mouse_x <= 335 + texto_instrucoes.get_width() and 400 <= mouse_y <= 400 + texto_instrucoes.get_height():
                exibir_instrucoes = True
                while exibir_instrucoes:
                    for evento in pygame.event.get():
                        if evento.type == pygame.QUIT:
                            pygame.quit()
                            quit()
                        elif evento.type == pygame.KEYDOWN:
                            if evento.key == pygame.K_ESCAPE:
                                pygame.quit()
                                quit()
                        elif evento.type == pygame.MOUSEBUTTONDOWN:
                            mouse_x, mouse_y = pygame.mouse.get_pos()
                        elif 0 <= mouse_x <= 0 + texto_jogar.get_width() and 0 <= mouse_y <= 0 + texto_jogar.get_height():
                            exibir_instrucoes = False
                    janela.fill((0, 0, 0))#fundo preto
                    janela.blit(texto_instrucoes1, (20, 200))
                    janela.blit(texto_instrucoes2, (100, 250))
                    janela.blit(texto_instrucoes3, (200, 300))
                    janela.blit(texto_instrucoes5, (130, 350))
                    janela.blit(texto_instrucoes4, (50, 400))
                    janela.blit(texto_voltar, (0, 0))
                    pygame.display.update()
            elif 430 <= mouse_x <= 430 + texto_sair.get_width() and 470 <= mouse_y <= 470 + texto_sair.get_height():
                pygame.quit()
                quit()
    janela.fill((0, 0, 0))
    # Exibir os textos do menu inicial
    janela.blit(texto_titulo, (280, 200))
    janela.blit(texto_jogar, (410, 330))
    janela.blit(texto_instrucoes, (335, 400))
    janela.blit(texto_sair, (430, 470))
    pygame.display.update()

# Loop principal
janela_aberta = True
clock = pygame.time.Clock()
ultimo_disparo = 0
inicio_jogo = False
tempo_inicial = pygame.time.get_ticks()
while janela_aberta:
    clock.tick(60)#fps do jogo


    # Verifica se o usuario fechou a janela
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            janela_aberta = False

#atualizar o tempo restante
    tempo_atual = pygame.time.get_ticks()
    if tempo_atual - ultima_atualizacao_tempo >= 1000:
        tempo_restante -= 1
        ultimo_atualizacao_tempo = tempo_atual

    # Início do jogo após a revelação da palavra
    tempo_atual = pygame.time.get_ticks()
    if not inicio_jogo and tempo_atual - tempo_inicial >= tempo_substituicao:
        inicio_jogo = True
        tempo_inicio_substituicao = tempo_atual
    tecla = pygame.key.get_pressed()  # comandos do jogo
    if tecla[pygame.K_UP]:
        y -= vel_nave
    if tecla[pygame.K_DOWN]:
        y += vel_nave
    if tecla[pygame.K_LEFT]:
        x -= vel_nave
    if tecla[pygame.K_RIGHT]:
        x += vel_nave

#definindo as direções dos aliens
    if rectx_1 < -20 :
        rectx_1 = 1000
        vel_alien = random.choices(vel, k=4)
    if rectx_2 > 1000 :
        rectx_2 = -20
        vel_alien = random.choices(vel, k=4)
    if rectx_3 > 1000 :
        rectx_3 = -20
        vel_alien = random.choices(vel, k=4)
    
    nave = janela.blit(nave_red, (x, y))

    alien1 = janela.blit(alien_red, (rectx_1, recty))
    if alien1.colliderect(nave):
        tempo_restante -= 50
    rectx_1 -= vel_alien[0]

    alien2 = janela.blit(alien_red, (rectx_2, recty + 100))
    if alien2.colliderect(nave):
        tempo_restante -= 50
    rectx_2 += vel_alien[1]

    alien3 = janela.blit(alien_red, (rectx_3, recty + 200))
    if alien3.colliderect(nave):
        tempo_restante -= 50
    rectx_3 += vel_alien[2]

    # Movimentação das letras
    for i in range(len(letras)):
        letras_pos_x[i] -= vel_letra#movimentaçao das letras
        if letras_pos_x[i] + fonte.get_height() < 350:#borda delimitada a esquerda
            letras_pos_x[i] = largura_janela + 1980 #reposiciona a letra na posiçao inicial, formando um loop

    # Criação dos tiros
    if inicio_jogo and tecla[pygame.K_SPACE] and pygame.time.get_ticks() - ultimo_disparo >= 500:#se o jogo começou e foi apertado o espaço e se ja se passaram 500ms do ultimo disparo
        tiros.append([x + nave_img.get_width() // 2 - tiro_largura // 2, y])#alinhamento do tiro(saindo da nave)
        ultimo_disparo = pygame.time.get_ticks()#atualiza o valor do ultimo disparo pra controlar o cooldown dos tiros

    # Atualiza os tiros
    tiros = [[tiro[0], tiro[1] - vel_tiro] for tiro in tiros if tiro[1] > -10]

    # Verificação de colisão entre tiros e letras
    for tiro in tiros:
        for i in range(len(letras)):
            if letras_pos_x[i] <= tiro[0] <= letras_pos_x[i] + fonte.size(letras[i])[0] and letras_pos_y[i] <= tiro[1] <= letras_pos_y[i] + fonte.size(letras[i])[1]:
                if letras[i] in palavra_sorteada:
                    indices = [j for j, letra in enumerate(palavra_sorteada) if letra == letras[i]]
                    for index in indices:
                        if letras_acertadas[index] == '?': 
                            letras_acertadas[index] = letras[i]
                            break
                    if '?' not in letras_acertadas:
                        palavra_revelada = True
                tiros.remove(tiro)
                break

#exibir a tela de game over quando o tempo chegar a zero
    if tempo_restante <= 0:
        janela_aberta = False
        tela_lose()
        
        #função para sortear uma nova palavra quando acertar todas as letras
    if '?' not in letras_acertadas:
        palavra_revelada = True
        pontuacao += 1
        sortear_nova_palavra()
        print(palavra_sorteada)
        palavra_revelada = False
        tempo_inicio_substituicao = pygame.time.get_ticks()

    # Substituição da palavra por lacunas após 4 segundos
    if inicio_jogo and not palavra_revelada:
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - tempo_inicio_substituicao >= tempo_substituicao:
            palavra_revelada = True
    
    desenhar_tela()
pygame.quit()