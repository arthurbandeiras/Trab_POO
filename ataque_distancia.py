import pygame as pg
from config_jogo import *

#TODO: acertar o init, colocar dentro do loop
#e acertar o insta kill


class Ataque_distancia:
    def __init__(self, jogador):
        self.projetil_x = jogador.posicao[0]
        self.projetil_y = jogador.posicao[1]
        self.X_INICIAL = jogador.posicao[0]
        self.Y_INICIAL = jogador.posicao[1]
        self.jogador = jogador
        self.cor = ConfigJogo.COR_ESTADO
        self.raio = 5
        self.direcao = jogador.direcao
        self.acontece = False
    
    def reseta_projetil(self):
        self.projetil_x = self.jogador.posicao[0] + 42
        self.projetil_y = self.jogador.posicao[1] + 42

    def ataque_normal(self, tela, inimigo):
        if self.acontece == True:    
            if self.direcao == 0:
                novo_x = self.projetil_x + ConfigJogo.VELOCIDADE_P
            elif self.direcao == 1:
                novo_x = self.projetil_x - ConfigJogo.VELOCIDADE_P

            
            if ((novo_x > 0) and (novo_x < ConfigJogo.LARGURA_TELA_PRINCIPAL)):
                self.projetil_x = novo_x
            else:
                self.reseta_projetil()
        elif self.acontece == False:
            self.reseta_projetil()
    

        if ((self.projetil_x > inimigo.posicao[0]) and (self.projetil_x <= inimigo.posicao[0] + 82)) and \
            ((self.projetil_y > inimigo.posicao[1]) and (self.projetil_y <= inimigo.posicao[1] + 82)):
            inimigo.vida -= ConfigJogo.DANO_PROJETIL

        pg.draw.circle(tela, 
                    self.cor,
                    (self.projetil_x, self.projetil_y), 
                    self.raio)
            
        pg.display.flip()


        
