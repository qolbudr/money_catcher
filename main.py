import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
import time
import random

pygame.init()

#DISPLAY
display_width = 300
display_height = 600
window = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Money Catcher")

#IMAGES
wallet_img = pygame.image.load('wallet.png')
wallet_img = pygame.transform.scale(wallet_img, (100, 90))
bg = pygame.image.load('background.png')
btnPlay = pygame.image.load('play_btn.png')
btnPlay = pygame.transform.scale(btnPlay, (140, 50))
btnExit = pygame.image.load('exit_btn.png')
btnExit = pygame.transform.scale(btnExit, (140, 50))
btnReplay = pygame.image.load('replay_btn.png')
btnReplay = pygame.transform.scale(btnReplay, (140, 50))

title = pygame.image.load('title.png')
jelly_img = pygame.image.load('jelly.png')
jelly_img = pygame.transform.scale(jelly_img, (50, 77))

over = pygame.image.load('over.png')

clock = pygame.time.Clock()

class Wallet(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.vel = 5
		self.hitbox = (self.x, self.y + 20, 150, 80)
	
	def draw(self, window):
		window.blit(wallet_img, (self.x, self.y))
		self.hitbox = (self.x, self.y + 20, 150, 80)

class Money(object):
	def __init__(self, x, y, f_type):
		self.x = x
		self.y = y
		self.f_type = f_type
		self.hitbox = (self.x, self.y, 80, 36)

	def draw(self, window):
		if self.f_type == 0:
			money = pygame.image.load('money.png')
			self.vel = 5
		window.blit(money, (self.x, self.y))
		self.hitbox = (self.x, self.y, 80, 36)

class Jelly(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.vel = 5
		self.hitbox = (self.x, self.y, 50, 77)

	def draw(self, window):
		window.blit(jelly_img, (self.x, self.y))
		self.hitbox = (self.x, self.y, 50, 77)

def game_intro():
  intro = True
  while intro:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()
    window.blit(bg, (0,0))
    window.blit(title, (display_width/2 - 80, 100))
    button("Start", 85, 400, 75, 50, "play")
    button("Quit", 85, 460, 75, 50, "quit")
    pygame.display.update()
    clock.tick(15)

def button(msg, x, y, width, height, action = None):
  mouse = pygame.mouse.get_pos()
  click = pygame.mouse.get_pressed()
  if(msg == "Start"):
  	window.blit(btnPlay, (x, y))
  elif(msg == "Quit"):
  	window.blit(btnExit, (x, y))
  elif(msg == "Restart"):
  	window.blit(btnReplay, (x, y))

  if (x+width > mouse[0] > x and y+height > mouse[1] > y):
  	if (click[0] == 1 and action != None):
	  	if(action == "play"):
	  		main()
	  	elif(action == "restart"):
	  		main()
	  	elif(action == "quit"):
	  		pygame.quit()
	  		quit()

def text_objects(text, font):
	textSurface = font.render(text, True, (255, 255, 255))
	return textSurface, textSurface.get_rect()

def message_to_screen(msg, x, y, size):
	regText = pygame.font.Font("krabby_patty.ttf", size)
	textSurf, textRect = text_objects(msg, regText)
	textRect.center = (x, y)
	window.blit(textSurf, textRect)

def main():
	score = 0
	money = []
	jelly = []
	money_add_counter = 0
	jelly_add_counter = 0
	add_money_rate = 30
	add_jelly_rate = 70
	lives = 3
	wallet = Wallet(display_width * 0.3, display_height - 100)
	play = True
	while play:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				play = False
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT] and wallet.x > wallet.vel - 5:
			wallet.x -= wallet.vel
		elif keys[pygame.K_RIGHT] and wallet.x < 300 - 100 - wallet.vel:
			wallet.x += wallet.vel
		window.blit(bg, (0,0))
		money_add_counter += 1
		jelly_add_counter += 1
		wallet.draw(window)

		if money_add_counter == add_money_rate:
			money_add_counter = 0
			f_startx = random.randrange(36, display_width - 80)
			f_starty = 0
			f_type = 0
			new_money = Money(f_startx, f_starty, f_type)
			money.append(new_money)
		if jelly_add_counter == add_jelly_rate:
			jelly_add_counter = 0
			b_startx = random.randrange(50, display_width - 77)
			b_starty = 0
			new_jelly = Jelly(b_startx, b_starty)
			jelly.append(new_jelly)
		
		for item in money:
			item.draw(window)
			item.y += item.vel

		for item in money[:]:
			if (item.hitbox[0] >= wallet.hitbox[0] - 50) and (item.hitbox[0] <= wallet.hitbox[0] + 50):
				if wallet.hitbox[1] - 10 <= item.hitbox[1] <= wallet.hitbox[1]:
					money.remove(item)
					score += 1
					if item.f_type == 0:
						score += 0

		for item in jelly:
			item.draw(window)
			item.y += item.vel

		for item in jelly[:]:
			if (item.hitbox[0] >= wallet.hitbox[0] - 50) and (item.hitbox[0] <= wallet.hitbox[0] + 50):
				if wallet.hitbox[1] - 10 <= item.hitbox[1] <= wallet.hitbox[1]:
					jelly.remove(item)
					lives -= 1
					print(lives)
					if(lives <= 0):
						play = False

		message_to_screen("Skor : "+str(score), 50, 30, 20)
		message_to_screen("Nyawa : "+str(lives), display_width - 60, 30, 20)
		pygame.display.update()
		clock.tick(60)
	show_score(score)

def show_score(score):
	show = True
	while(show):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		window.blit(over, (0,0))
		message_to_screen("Skor Anda :", 150, 250, 40)
		message_to_screen(str(score), 150, 300, 40)
		button("Restart", 85, 400, 75, 50, "restart")
		button("Quit", 85, 460, 75, 50, "quit")
		pygame.display.update()


game_intro()
# main()
# show_score(0)