
import pygame
from pygame.locals import*
import random

screen = pygame.display.set_mode((400, 400))
running = True


picture = pygame.image.load("WechatIMG1.jpeg")
(a, b)= picture.get_rect().size
ratio = min(200/a, 200/b)
picture = pygame.transform.scale(picture, (int(a*ratio), int(b*ratio)))
screen.blit(picture,(50,50))

def exchangecolor(a,b):
	x = a
	y = b
	for k in range (2000):
		pix = screen.get_at((a, b))
		while x == a:
			x = random.randint(a-1,a+1)
		while y == b:
			y = random.randint(b-1, b+1)

		if x > 249:
			x-=1
		if y > 249:
			y-=1
		if x < 51:
			x+=1
		if y < 51:
			y+=1

		pix2 = screen.get_at((x, y))
		screen.set_at((x,y),pix)
		screen.set_at((a,b),pix2)
		a = x
		b = y

for k in range (20):
	for a in range (60, 240, 20):
		m = random.randint(a,a)
		n = random.randint(a,a)
		exchangecolor(m,n)
		exchangecolor(m,250-(n-50))



while running:
	pygame.display.update()
	for event in pygame.event.get():
		if event.type == pygame.QUIT: 
			running = False
	

pygame.quit()
quit()