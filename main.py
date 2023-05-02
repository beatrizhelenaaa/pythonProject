import pygame
from pygame.locals import *
from sys import exit
import os

diretorio_principal = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio_principal, 'sprites')
pygame.init()

#criar janela
largura = 640
altura = 480
y = 400
velocidade_jogo = 10

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Marcelinho Delivery')


#sprites usadas
sprite_sheet = pygame.image.load(os.path.join(diretorio_imagens, 'persona_1.png')).convert_alpha()
GUARDINHA = pygame.image.load(os.path.join(diretorio_imagens, 'guardinha.png')).convert_alpha()
CACHORRO = pygame.image.load(os.path.join(diretorio_imagens, 'dog.png')).convert_alpha()
CAFE = pygame.image.load(os.path.join(diretorio_imagens, 'coffee.png')).convert_alpha()
PIZZA = pygame.image.load(os.path.join(diretorio_imagens, 'pizza.png')).convert_alpha()
COXINHA = pygame.image.load(os.path.join(diretorio_imagens, 'coxinha.png')).convert_alpha()


def reiniciar():
  global pontos, velocidade_jogo, colidiu, escolha_obstaculo
  pontos = 0
  velocidade_jogo = 10
  colidiu = False
  estagiario.rect.y = altura - 64 - 96 // 2
  estagiario.pulo = False
  guardinha.rect.x = largura
  cafe.rect.x = largura

##PLAYER CLASS
class Estagiario(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.imagens_estagiario = []
    for i in range(3):
      img = sprite_sheet.subsurface((16, (i * 16) + 1), (16, 16))
      img = pygame.transform.scale(img, (16 * 3, 16 * 3))
      self.imagens_estagiario.append(img)
    self.index_lista = 0
    self.image = self.imagens_estagiario[self.index_lista]
    self.rect = self.image.get_rect()
    self.pos_y = altura - 64 - 96//2
    self.rect.topleft = (100, self.pos_y)
    self.pulo = False

  def pular(self):
    self.pulo = True
  def update(self):
    if self.pulo == True:
      if self.rect.y <= self.pos_y - 150:
        self.pulo = False
      self.rect.y -= 15
    else:
      if self.rect.y >= self.pos_y:
        self.rect.y = self.pos_y
      else:
        self.rect.y += 15

    if self.index_lista > 2:
      self.index_lista = 0
    self.index_lista += 0.25
    self.image = self.imagens_estagiario[int(self.index_lista)]
  def colisao(self, sprite: pygame.sprite.Sprite):
    return self.rect.colliderect(sprite.rect)


##OBSTACULOS CLASS - FAZER DEPOIS
class Obstaculos():
  def __init__(self, type):
    self.type = type
    self.rect = self.image[self.type].get_rect()
    self.rect.x = largura

  def update(self):
    self.rect.x -= game_speed
    if self.rect.x < -self.rect.width:
      obstaculos.pop()


#GUARDINHA CLASS
class Guardinha(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.imagens_guardinha = []
    for i in range(3):
      img = GUARDINHA.subsurface((16*3, (i * 16)+1), (16, 16))
      img = pygame.transform.scale(img, (16 * 3, 16 * 3))
      self.imagens_guardinha.append(img)
    self.index_lista = 0
    self.image = self.imagens_guardinha[self.index_lista]
    self.rect = self.image.get_rect()
    self.pos_y = altura - 64 - 96 // 2 + 25
    self.rect.center = (largura, self.pos_y)
  def update(self):
    #index da sprite
    if self.index_lista > 2:
      self.index_lista = 0
    self.index_lista += 0.25
    self.image = self.imagens_guardinha[int(self.index_lista)]

    if self.rect.topright[0] < 0:
      self.rect.x = largura
    self.rect.x -= velocidade_jogo


#CACHORRO CLASS - FAZER DEPOIS
class Dog(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.imagens_dog = []
    for i in range(6):
      img = CACHORRO.subsurface((16*i, 16), (48, 32))
      img = pygame.transform.scale(img, (32 * 3, 32 * 3))
      self.imagens_dog.append(img)
    self.index_lista = 0
    self.image = self.imagens_dog[self.index_lista]
    self.rect = self.image.get_rect()
    self.rect.center = (largura, y)
  def update(self):
    #index da sprite
    if self.index_lista > 2:
      self.index_lista = 0
    self.index_lista += 0.25
    self.image = self.imagens_dog[int(self.index_lista)]

#COFFEE CLASS
class Cafe(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.image = CAFE
    self.image = pygame.transform.scale(self.image, (32,32))
    self.rect = self.image.get_rect()
    self.mask = pygame.mask.from_surface(self.image)
    self.rect.center = (largura, altura - 64 - 96 // 2 + 25)
    self.rect.x = largura
  def update(self):
    if self.rect.topright[0] < 0:
      self.rect.x = largura
    self.rect.x -= velocidade_jogo


colecao_sprites = pygame.sprite.Group()
estagiario = Estagiario()
colecao_sprites.add(estagiario)

guardinha = Guardinha()
colecao_sprites.add(guardinha)

cafe = Cafe()
colecao_sprites.add(cafe)

run = True
relogio = pygame.time.Clock()
game_speed = 20
points = 0
obstacles = []
death_count = 0

while run:
  relogio.tick(30)
  tela.fill((255,255,255))
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      exit()
    if event.type == KEYDOWN:
      if event.key == K_SPACE:
        estagiario.pular()
      if event.key == K_r and estagiario.colisao(guardinha):
        reiniciar()

  if estagiario.colisao(cafe):
    cafe.remove()

  if estagiario.colisao(guardinha):
    print('GAME OVER')

  guardinha.update()
  estagiario.update()
  colecao_sprites.draw(tela)
  colecao_sprites.update()
  pygame.display.flip()