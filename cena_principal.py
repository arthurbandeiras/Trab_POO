import sys
import pygame as pg
from config_jogo import ConfigJogo
from persona import Lista1
from persona import Lista2
from personagem_bat import *
from cronometro import Cronometro
import math
from ataque_distancia import Ataque_distancia
from spritesheet import Spritesheet
from tiles import *

class CenaPrincipal:
    def __init__(self, tela, indice1, indice2):
        self.tela = tela
        self.encerra = False
        self.cronometro = Cronometro()
        self.cd = Cronometro()
        '''self.estado = EstadoJogo()'''
        self.font = pg.font.SysFont(None, 48)
        self.spritesheet = Spritesheet('owlishmedia_pixel_tiles.png')
        self.map = Tilemap('1mapa.csv', self.spritesheet)
        
        py = ConfigJogo.ALTURA_TELA // 2 - ConfigJogo.ALTURA_P // 2
        px_esq = ConfigJogo.POS_X1
        px_dir = ConfigJogo.POS_X2

        self.indice1 = indice1
        self.indice2 = indice2
        
        self.player1 = Lista1[indice1]
        self.player2 = Lista2[indice2]
        
        self.vida_total1 = self.player1.vida    #gambiarra provisória permanente
        self.vida_total2 = self.player2.vida

        self.player1.posicao = (px_esq, py)     #self.player1 = Personagem_batalha(posicao=(px_esq, py))
        self.player2.posicao = (px_dir, py)     #self.player2 = Personagem_batalha(posicao=(px_dir, py))

        self.x_mouse = 0
        self.y_mouse = 0
        self.gambiarra = 0

        self.ataque_dist1 = False
        self.ataque_dist2 = False

        if self.player1.nome == 'Toninha Maga':
            distancia1 = Ataque_distancia(self.player1)
            self.player1.classe2 = distancia1
        
        if self.player2.nome == 'Soldado Atirador':
           distancia2 = Ataque_distancia(self.player2)
           self.player2.classe2 = distancia2 



    def tratamento_eventos(self):

        for event in pg.event.get():
            if (event.type == pg.QUIT):
                sys.exit()
            
            if (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                ConfigJogo.TELA -= 2
                self.player1.vida = Lista1[self.indice1].vida
                self.player2.vida = Lista2[self.indice2].vida                
                self.resetar()
                self.encerra = True

            if pg.key.get_pressed()[pg.K_a]:
                self.player1.mover_para_esquerda()
            elif pg.key.get_pressed()[pg.K_d]:
                self.player1.mover_para_direita()
            else:
                self.player1.parar_x()
            
            if pg.key.get_pressed()[pg.K_j]:
                self.player2.mover_para_esquerda()
            elif pg.key.get_pressed()[pg.K_l]:
                self.player2.mover_para_direita()
            else:
                self.player2.parar_x()
            
            
            if pg.key.get_pressed()[pg.K_w]:
                self.player1.mover_para_cima()
            elif pg.key.get_pressed()[pg.K_s]:
                self.player1.mover_para_baixo()
            else:
                self.player1.parar_y()
            
            if pg.key.get_pressed()[pg.K_i]:
                self.player2.mover_para_cima()
            elif pg.key.get_pressed()[pg.K_k]:
                self.player2.mover_para_baixo()
            else:
                self.player2.parar_y()

            '''if pg.key.get_pressed()[pg.K_q]:
                self.player1.classe.ataque_normal(self.tela,self.player1,self.player2)
            

            if pg.key.get_pressed()[pg.K_u]:
                self.player2.classe.ataque_normal(self.tela,self.player2,self.player1)'''


            '''if (event.type == pg.MOUSEBUTTONDOWN) or (pg.mouse.get_pressed()[0]):
                mouse_position = pg.mouse.get_pos()
                self.gambiarra = 1
                self.x_mouse = mouse_position[0]
                self.y_mouse= mouse_position[1]'''


    def vencedor(self):
        if self.player1.vida > self.player2.vida:
            return "Toninhas"
        elif self.player2.vida > self.player1.vida:
            return "Soldados"
        else:
            return "Empate"
    
    def reseta_vida1(self):
        return self.vida_total1

    def reseta_vida2(self):
        return self.vida_total2

    def resetar(self):
        self.player1.direcao = 0
        self.player2.direcao = 1
        self.cronometro.reset()
        self.player1.vida = self.reseta_vida1()
        self.player2.vida = self.reseta_vida2()
        self.player1.velocidade = self.player1.velocidade_nominal
        self.player2.velocidade = self.player2.velocidade_nominal
        self.player1.sprite_atual = self.player1.sprite_inicial
        self.player2.sprite_atual = self.player2.sprite_inicial

    def atualiza_estado(self):
        self.player1.atualizar_posicao()
        self.player2.atualizar_posicao()

    def desenha_vidas(self, tela, vida1, vida2):
        img = self.font.render(f'{math.ceil(vida1):.0f} x {math.ceil(vida2):.0f}',
                                True, ConfigJogo.COR_ESTADO)
        px = ConfigJogo.LARGURA_TELA_PRINCIPAL // 2 - img.get_size()[0] // 2
        py = ConfigJogo.ALTURA_PLACAR
        tela.blit(img, (px, py))
    
    def desenha_tempo(self, tela):
        tempo = ConfigJogo.DURACAO_PARTIDA - self.cronometro.tempo_passado()
        img = self.font.render(f'{tempo:.0f}',
                                True, ConfigJogo.COR_ESTADO)
        px = ConfigJogo.LARGURA_TELA_PRINCIPAL // 2 - img.get_size()[0] // 2
        py = ConfigJogo.ALTURA_TEMPO
        tela.blit(img, (px, py))

    def desenha(self):
        self.map.draw_map(self.tela)

        if self.gambiarra == 1:
            pg.draw.circle(self.tela,
                        (255, 0, 0), 
                        (self.x_mouse, self.y_mouse),
                        10)

        self.desenha_vidas(self.tela, self.player1.vida, self.player2.vida)
        self.desenha_tempo(self.tela)
        self.player2.desenha(self.tela)
        self.player1.desenha(self.tela)
        
        pg.display.flip()


        if pg.key.get_pressed()[pg.K_q]:
            self.player1.classe1.ataque_normal(self.tela,self.player1,self.player2)
        
            
        if pg.key.get_pressed()[pg.K_u]:
            self.player2.classe1.ataque_normal(self.tela,self.player2,self.player1)

        
        if pg.key.get_pressed()[pg.K_e]:
            if self.player1.nome != 'Toninha Maga':
                self.player1.classe2.ataque_especial(self.tela,self.player1, self.player2)
            else:
                '''distancia1 = Ataque_distancia(self.player1)
                self.player1.classe2 = distancia1'''
                self.player1.classe2.acontece = True
                self.player1.classe2.ataque_normal(self.tela, self.player2)
                
        elif not pg.key.get_pressed()[pg.K_e]:
            self.player1.classe2.acontece = False

        
        if pg.key.get_pressed()[pg.K_o]:
            if self.player2.nome != 'Soldado Atirador':
                self.player2.classe2.ataque_especial(self.tela,self.player2, self.player1)
            else:
                '''distancia2 = Ataque_distancia(self.player2)
                self.player2.classe2 = distancia2'''
                self.player2.classe2.ataque_normal(self.tela, self.player1)

        if (pg.mouse.get_pressed()[0]):
            if self.ataque_dist1 == 1:
                self.player1.classe2.ataque_especial(self.tela,self.player1, self.player2)
                self.ataque_dist1 = 0
                
            elif self.ataque_dist2 == 1:
                self.player2.classe2.ataque_especial(self.tela,self.player2, self.player1)
                self.ataque_dist2 = 0

        if not pg.key.get_pressed()[pg.K_q] and not pg.key.get_pressed()[pg.K_e]:
            if self.player1.direcao == 0:
                self.player1.sprite_atual = self.player1.sprite_direita

            elif self.player1.direcao == 1:
                self.player1.sprite_atual = self.player1.sprite_esquerda
            
        if not pg.key.get_pressed()[pg.K_u] and not pg.key.get_pressed()[pg.K_o]:
            if self.player2.direcao == 0:
                self.player2.sprite_atual = self.player2.sprite_direita

            elif self.player2.direcao == 1:
                self.player2.sprite_atual = self.player2.sprite_esquerda


    def jogo_terminou(self):
        if (self.player1.vida <= 0) or \
            (self.player2.vida <= 0) or \
                (self.cronometro.tempo_passado() > float(ConfigJogo.DURACAO_PARTIDA)):
            self.encerra = True
            return self.encerra

    def rodar(self):
        while not self.encerra:
            self.desenha()
            self.tratamento_eventos()
            self.atualiza_estado()
            self.jogo_terminou()