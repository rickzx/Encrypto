import random, sys, string, os
from tinydb import TinyDB, Query
import pygame_textinput

try:
    import numpy as N
    import pygame
    from pgu import text, gui as pgui

except ImportError:
    raise (ImportError, "NumPy and Surfarray are required.")

## Basic Parameters ##

class Config(object):
	display_width = 800
	display_height = 600

	white = (255,255,255)
	black = (0,0,0)
	grey = (214, 215, 216)
	darkGrey = (127, 129, 130)
	red = (255,0,0)
	blue = (0, 134, 179)

	mode = 0
	enterKey = None
	shuffleList = None
	isPassed = False


	button = (133, 224, 224)

	buttonT = (0, 40, 100)

	userdb = TinyDB('userdb.json')
	keydb = TinyDB('keydb.json')

	username = None
	userinfo = None

	uploadImg = None

	fps = 30
	
	mousePos = 0
	button_down = False
	isDialog = False
	dialogComplete = False
	warning = False
	showError = False
	isChange = False

## Welcome Screen ##

def text_objects(text, font):
    textSurface = font.render(text, True, Config.white)
    return textSurface, textSurface.get_rect()

def text_objects1(text, font):
    textSurface = font.render(text, True, Config.black)
    return textSurface, textSurface.get_rect()

def text_objects2(text, font):
    textSurface = font.render(text, True, Config.buttonT)
    return textSurface, textSurface.get_rect()

def welcome():
	gameDisplay = pygame.display.set_mode((Config.display_width, Config.display_height))
	clock = pygame.time.Clock()
	welcomeImg = pygame.image.load('back1.jpg')
	welcomeImg = pygame.transform.smoothscale(welcomeImg, (800,600))

	logoImg = pygame.image.load('logo.png')
	logoImg = pygame.transform.scale(logoImg, (600,500))
	

	textinput1 = pygame_textinput.TextInput(font_size = 28, text_color = Config.white)
	textinput2 = pygame_textinput.TextInput(font_size = 28, text_color = Config.white)

	def drawWelcome(x, y):
		gameDisplay.blit(welcomeImg,(x,y))

	def drawButton(a, b, c, d, text):
		pygame.draw.rect(gameDisplay, Config.blue, (a,b,c,d))
		smallText1 = pygame.font.SysFont("comicsansms", 25)
		textSurf1, textRect1 = text_objects(text, smallText1)
		textRect1.center = (a + c/2, b + d/2)		
		gameDisplay.blit(textSurf1, textRect1)


	intro = True

	while intro:
		gameDisplay.fill(Config.white)

		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()

		drawWelcome(0,0)
		gameDisplay.blit(logoImg, (120,-100))

		smallText1 = pygame.font.SysFont("comicsansms", 25)

		if Config.mousePos == 0 or (250<mouse[0]<650 and 300 < mouse[1] < 328 and click[0] == 1):
			events0 = pygame.event.get()	    
			textinput1.update(events0)
			
			Config.mousePos = 0

			for event in events0:
				if event.type == pygame.QUIT:
					pygame.quit()
					intro = False
					sys.exit()

		if Config.mousePos == 1 or (250<mouse[0]<650 and 350 < mouse[1] < 378 and click[0] == 1): 
			events1 = pygame.event.get()	    
			textinput2.update(events1)
			
			Config.mousePos = 1

			for event in events1:
				if event.type == pygame.QUIT:
					pygame.quit()
					intro = False
					sys.exit()	

			
		eventsAll = pygame.event.get()
		for event in eventsAll:
			if event.type == pygame.QUIT:
				pygame.quit()
				intro = False
				sys.exit()	

		pygame.draw.rect(gameDisplay, Config.white, (400-250,300,500,30), 2)
		pygame.draw.rect(gameDisplay, Config.white, (400-250,350,500,30), 2)

		gameDisplay.blit(textinput1.get_surface(),(400-148,305))
		gameDisplay.blit(textinput2.get_surface(),(400-148,355))


		textSurf1, textRect1 = text_objects("Username:", smallText1)
		textRect1.center = (400-200,315)		
		gameDisplay.blit(textSurf1, textRect1)

		textSurf2, textRect2 = text_objects("Password:", smallText1)
		textRect2.center = (400-200,365)
		gameDisplay.blit(textSurf2, textRect2)

		drawButton(200, 430, 150, 60, "Log In")
		drawButton(450, 430, 150, 60, "Sign Up")


		if (450 < mouse[0] < 600 and 430 < mouse[1] < 490) and click[0] == 1 and (not Config.button_down):
			username = textinput1.get_text()
			password = textinput2.get_text()
			Config.userdb.insert({'Name':str(username), 'Pass':str(password)})
			Config.button_down = True
			Config.isDialog = True

		if Config.isDialog == True:
			dialog = pygame.image.load("signin.png")
			dialog = pygame.transform.smoothscale(dialog, (800,160))
			gameDisplay.blit(dialog, (5,230))

		if (705 < mouse[0] < 720 and 245 < mouse[1] < 260 and click[0] == 1):
			Config.isDialog = False

		if 200 < mouse[0] < 350 and 430 < mouse[1] < 490 and click[0] == 1:
			username = textinput1.get_text()
			password = textinput2.get_text()
			SearchUser = Query()
			if password == Config.userdb.search(SearchUser.Name == username)[0]['Pass']:
				Config.username = username
				Config.userinfo = TinyDB(username + '.json')
				intro = False
				choose()
		
		if click[0] == 0:
			Config.button_down = False

		pygame.display.update()
		clock.tick(30)

def choose():
	Config.warning = False
	Config.isChange = False
	gameDisplay = pygame.display.set_mode((Config.display_width, Config.display_height))
	clock = pygame.time.Clock()
	welcomeImg = pygame.image.load('back1.jpg')
	welcomeImg = pygame.transform.smoothscale(welcomeImg, (800,600))

	logoImg = pygame.image.load('logo.png')
	logoImg = pygame.transform.scale(logoImg, (600,500))

	returnImg = pygame.image.load('return.png')
	returnImg = pygame.transform.scale(returnImg, (60,60))

	def drawWelcome(x, y):
		gameDisplay.blit(welcomeImg,(x,y))

	intro = True

	while intro:
		gameDisplay.fill(Config.white)

		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()

		drawWelcome(0,0)
		gameDisplay.blit(logoImg, (120,-100))

			
		eventsAll = pygame.event.get()
		for event in eventsAll:
			if event.type == pygame.QUIT:
				pygame.quit()
				intro = False
				sys.exit()

		button = pygame.image.load("button.png")
		button = pygame.transform.smoothscale(button, (230, 80))
		gameDisplay.blit(button, (290,220))
		gameDisplay.blit(button, (290,330))
		gameDisplay.blit(button, (290,440))

		gameDisplay.blit(returnImg,(50,20))

		pygame.font.init()
		smallText = pygame.font.SysFont('arial', 50)
		textSurf1, textRect1 = text_objects2("Encrypt", smallText)
		textRect1.center = (405,260)		
		gameDisplay.blit(textSurf1, textRect1)

		textSurf2, textRect2 = text_objects2("Decrypt", smallText)
		textRect2.center = (405,370)		
		gameDisplay.blit(textSurf2, textRect2)

		textSurf3, textRect3 = text_objects2("History", smallText)
		textRect3.center = (405,480)		
		gameDisplay.blit(textSurf3, textRect3)

		if 300 < mouse[0] < 510 and 230 < mouse[1] < 290 and click[0] == 1:
			intro = False
			encrypt()

		if 300 < mouse[0] < 510 and 340 < mouse[1] < 400 and click[0] == 1:
			intro = False
			decrypt()

		if 300 < mouse[0] < 510 and 450 < mouse[1] < 510 and click[0] == 1:
			intro = False
			history()

		if 60 < mouse[0] < 100 and 25 < mouse[1] < 70 and click[0] == 1:
			intro = False
			welcome()


		pygame.display.update()
		clock.tick(30)


def id_generator(size=20, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

class Image(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self,self.groups)

		self.toHash = []

		self.image = self.loadImg()
		#self.image = self.reshuf()
		self.rect = (Config.display_width/2 - 200, Config.display_height/2 - 230, 400, 400)
		self.mask = pygame.mask.from_surface(self.image)
		


	def swap(self, ndarr, r1, c1, r2, c2):
		temp = ndarr[r1][c1]
		ndarr[r1][c1] = ndarr[r2][c2]
		ndarr[r2][c2] = temp
		return ndarr

	def loadImg(self):
		picSur = pygame.Surface((400, 400))
		picture = pygame.image.load("instruction.jpeg")
		picture = pygame.transform.smoothscale(picture, (400,400))
		picSur.blit(picture, (0, 0))
		
		return picSur

	def loadUserImg(self):
		picSur = pygame.Surface((400, 400))
		picture = pygame.image.load(Config.uploadImg)
		picture = pygame.transform.smoothscale(picture, (400,400))
		picSur.blit(picture, (0, 0))
		
		return picSur


	def loadWarning(self):
		picSur = pygame.Surface((400, 400))
		picture = pygame.image.load("warning.png")
		picture = pygame.transform.smoothscale(picture, (400,400))
		picSur.blit(picture, (0, 0))
		
		return picSur


	def shuf(self):
		
		picSur = pygame.Surface((400, 400))
		picture = pygame.image.load(Config.uploadImg)
		picture = pygame.transform.smoothscale(picture, (400,400))
		picSur.blit(picture, (0, 0))

		surfArray = pygame.surfarray.pixels2d(picSur)
		(length, width) = (len(surfArray), len(surfArray[0]))


		indexList = []
		for i in range(len(surfArray)):
			for j in range(len(surfArray[0])):
				indexList.append((i,j))

		
		indexList1 = random.sample(indexList,len(indexList) // 2)
		indexList2 = list(set(indexList) - set(indexList1))

		for x in range(len(indexList1)):
			(r1, c1) = indexList1[x]
			(r2, c2) = indexList2[x]
			self.swap(surfArray, r1, c1, r2, c2)
			self.toHash.append([r1, c1, r2, c2])


		uniqueKey = id_generator()
		Config.keydb.insert({'key':uniqueKey, 'list':self.toHash})
		Config.userinfo.insert({'picName': Config.uploadImg.split('/')[-1], 'key':uniqueKey})


		direc = os.listdir("Output")

		find = True
		acc = 0
		name = None

		while find:
			name = "key" + str(acc) + ".txt"
			if name not in direc:
				find = False
			else:
				acc += 1 

		pygame.image.save(self.image, 'Output/' + name)

		f = open('Output/' + name,'w')
		f.write(uniqueKey)
		f.close()

		return picSur

	def reshuf(self, reList):
		picSur = pygame.Surface((400, 400))
		picture = pygame.image.load(Config.uploadImg)
		picture = pygame.transform.smoothscale(picture, (400,400))
		picSur.blit(picture, (0, 0))

		surfArray = pygame.surfarray.pixels2d(picSur)
		(length, width) = (len(surfArray), len(surfArray[0]))

		for i in range(len(reList)):
			[r1,c1,r2,c2] = reList[len(reList) - i - 1]
			self.swap(surfArray, r1, c1, r2, c2)

		return picSur


	def update(self, seconds):
		if Config.uploadImg != None and (not Config.isChange):			
			userImg = pygame.image.load(Config.uploadImg)
			userImg = pygame.transform.smoothscale(userImg,(400,400))
			self.image = userImg

		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()


		if 378 < mouse[0] < 418 and 8 < mouse[1] < 46 and (click[0] == 1) and (not Config.button_down) and (Config.uploadImg != None):
			if Config.mode == 0:
				self.image = self.shuf()

				direc = os.listdir("Output")

				find = True
				acc = 0
				name = None

				while find:
					name = "output" + str(acc) + ".jpeg"
					if name not in direc:
						find = False
					else:
						acc += 1 

				pygame.image.save(self.image, 'Output/' + name)

				Config.button_down = True
				Config.isChange = True
				Config.isDialog = True

			if Config.mode == 1:
				Config.dialogComplete = True
				Config.button_down = True
				Config.isChange = True


		if click[0] == 0:			
			Config.button_down = False
		else:
			print(mouse[0],mouse[1])

		if Config.mode == 1:
			if Config.isPassed:
				self.image = self.reshuf(Config.shuffleList)
			elif Config.isChange == True and Config.isPassed == False:
				self.image = self.loadUserImg()

			keys = pygame.key.get_pressed()
			if keys[pygame.K_LSHIFT] and keys[pygame.K_LCTRL] and Config.warning == False:
				Config.warning = True

			if 	Config.warning == True:
				self.image = self.loadWarning()

			

## fileBrowser ##


def encrypt():
	Config.uploadImg = None
	Config.mode = 0
	screen = pygame.display.set_mode((Config.display_width,Config.display_height))
	background = pygame.Surface((screen.get_size()))
	background.fill(Config.black)

	welcomeImg = pygame.image.load('back1.jpg')
	welcomeImg = pygame.transform.smoothscale(welcomeImg, (800,600))

	logoImg = pygame.image.load('logo.png')
	logoImg = pygame.transform.scale(logoImg, (600,500))

	returnImg = pygame.image.load('return.png')
	returnImg = pygame.transform.scale(returnImg, (60,60))

	def drawWelcome(x, y):
		screen.blit(welcomeImg,(x,y))

	def drawCheck(x, y):
		check = pygame.image.load("check.png")
		check = pygame.transform.smoothscale(check, (60,60))
		screen.blit(check, (x,y))

	def open_file_browser(arg):
		d = pgui.FileDialog()
		d.connect(pgui.CHANGE, handle_file_browser_closed, d)
		d.open()

	def handle_file_browser_closed(dlg):
		if dlg.value: 
			input_file.value = dlg.value
			Config.uploadImg = input_file.value
			Config.isChange = False

	
	crashed = False
	FPS = Config.fps
	clock = pygame.time.Clock()

	imageGroup = pygame.sprite.Group()
	allGroups = pygame.sprite.LayeredUpdates()

	Image.groups = imageGroup, allGroups
	Image._layer = 1

	image = Image()
	
	global lines

	#Initialize Everything
	pygame.init()
	pygame.font.init()
	font = pygame.font.SysFont("default",10)
	fontBig = pygame.font.SysFont("default",10)
	fontSub = pygame.font.SysFont("default",10)

	gscreen = pygame.display.set_mode((800,600))
	pygame.display.set_caption('GUI Test - PGU')

	# create GUI object
	gui = pgui.App()
	textArea = pygame.Rect(370, 20, 250, 320)

	# layout using document
	lo = pgui.Container(width=350, height=350)

	td_style = {'padding_right': 10}
	
	t = pgui.Table()
	t.tr()
	t.td( pgui.Label('File Name:') , style=td_style )
	input_file = pgui.Input()
	t.td( input_file, style=td_style )
	b = pgui.Button("Browse...")
	t.td( b, style=td_style )
	b.connect(pgui.CLICK, open_file_browser, None)


	lo.add(t, 20, 420)

	gui.init(lo)

	while not crashed:
		milliseconds = clock.tick(Config.fps)  # milliseconds passed since last frame
		seconds = milliseconds / 1000.0


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				crashed = True
				pygame.quit()
				crashed = True
				sys.exit()

			gui.event(event)


		drawWelcome(0, 0)
		screen.blit(returnImg, (50, 20))

		if Config.uploadImg != None:
			drawCheck(370,0)

		allGroups.clear(screen, background)
		allGroups.update(seconds)
		allGroups.draw(screen)

		gui.paint(gscreen)

		if Config.isDialog == True:
			dialog = pygame.image.load("dialog.png")
			dialog = pygame.transform.smoothscale(dialog, (800,160))
			screen.blit(dialog, (5,230))

		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()

		if 675 < mouse[0] < 690 and 240 < mouse[1] < 260 and click[0] == 1:
			Config.isDialog = False

		if 60 < mouse[0] < 100 and 25 < mouse[1] < 70 and click[0] == 1:
			intro = False
			choose()

		pygame.display.update()


	pygame.quit()

def decrypt():
	Config.uploadImg = None
	Config.mode = 1
	screen = pygame.display.set_mode((Config.display_width,Config.display_height))
	background = pygame.Surface((screen.get_size()))
	background.fill(Config.black)

	welcomeImg = pygame.image.load('back1.jpg')
	welcomeImg = pygame.transform.smoothscale(welcomeImg, (800,600))

	logoImg = pygame.image.load('logo.png')
	logoImg = pygame.transform.scale(logoImg, (600,500))

	returnImg = pygame.image.load('return.png')
	returnImg = pygame.transform.scale(returnImg, (60,60))

	def drawWelcome(x, y):
		screen.blit(welcomeImg,(x,y))

	def drawCheck(x, y):
		check = pygame.image.load("check.png")
		check = pygame.transform.smoothscale(check, (60,60))
		screen.blit(check, (x,y))

	def open_file_browser(arg):
		d = pgui.FileDialog()
		d.connect(pgui.CHANGE, handle_file_browser_closed, d)
		d.open()

	def handle_file_browser_closed(dlg):
		if dlg.value: 
			input_file.value = dlg.value
			Config.enterKey = None
			Config.isPassed = False
			Config.uploadImg = input_file.value

	
	crashed = False
	FPS = Config.fps
	clock = pygame.time.Clock()

	imageGroup = pygame.sprite.Group()
	allGroups = pygame.sprite.LayeredUpdates()

	Image.groups = imageGroup, allGroups
	Image._layer = 1

	image = Image()
	
	global lines

	#Initialize Everything
	pygame.init()
	pygame.font.init()
	font = pygame.font.SysFont("default",10)
	fontBig = pygame.font.SysFont("default",10)
	fontSub = pygame.font.SysFont("default",10)

	gscreen = pygame.display.set_mode((800,600))
	pygame.display.set_caption('GUI Test - PGU')

	# create GUI object
	gui = pgui.App()
	textArea = pygame.Rect(370, 20, 250, 320)

	# layout using document
	lo = pgui.Container(width=350, height=350)

	td_style = {'padding_right': 10}
	
	t = pgui.Table()
	t.tr()
	t.td( pgui.Label('File Name:') , style=td_style )
	input_file = pgui.Input()
	t.td( input_file, style=td_style )
	b = pgui.Button("Browse...")
	t.td( b, style=td_style )
	b.connect(pgui.CLICK, open_file_browser, None)


	lo.add(t, 20, 420)

	gui.init(lo)

	textinput1 = pygame_textinput.TextInput(font_size = 28, text_color = Config.black)

	while not crashed:
		milliseconds = clock.tick(Config.fps)  # milliseconds passed since last frame
		seconds = milliseconds / 1000.0
		events = pygame.event.get()
		textinput1.update(events)

		for event in events:
			if event.type == pygame.QUIT:
				crashed = True
				pygame.quit()
				crashed = True
				sys.exit()

		gui.event(event)

		drawWelcome(0, 0)

		if Config.uploadImg != None:
			drawCheck(370,0)

		screen.blit(returnImg, (50, 20))

		allGroups.clear(screen, background)
		allGroups.update(seconds)
		allGroups.draw(screen)

		gui.paint(gscreen)

		if Config.isDialog == True:
			dialog = pygame.image.load("dialog.png")
			dialog = pygame.transform.smoothscale(dialog, (800,160))
			screen.blit(dialog, (5,230))

		pygame.draw.rect(screen, Config.grey, (295,540,310,25))
		pygame.draw.rect(screen, Config.darkGrey, (295,540,310,25), 1)

		smallText = pygame.font.SysFont('arial', 25)
		textSurf1, textRect1 = text_objects1("Enter your key:", smallText)
		textRect1.center = (230,550)		
		screen.blit(textSurf1, textRect1)

		
		screen.blit(textinput1.get_surface(),(300,544))

		if Config.dialogComplete == True:
			Config.enterKey = textinput1.get_text()

			if Config.enterKey != None:
				User = Query()
				result = Config.keydb.search(User.key == Config.enterKey)

				if len(result) > 0:
					Config.shuffleList = result[0]['list']
					Config.isPassed = True
				else:
					Config.showError = True
					Config.isPassed = False
				Config.dialogComplete = False

		if Config.showError == True:
			err = pygame.image.load("error.png")
			err = pygame.transform.smoothscale(err, (600, 120))
			screen.blit(err, (100, 230))

			if 630 < mouse[0] < 645 and 255 < mouse[1] < 270 and click[0] == 1:
				Config.showError = False

		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()

		if click[0] == 1:
			print(mouse[0], mouse[1])


			


		if 675 < mouse[0] < 690 and 240 < mouse[1] < 260 and click[0] == 1:
			Config.isDialog = False

		if 60 < mouse[0] < 100 and 25 < mouse[1] < 70 and click[0] == 1:
			intro = False
			Config.isPassed = False
			choose()

		pygame.display.update()


	pygame.quit()

def history():
	gameDisplay = pygame.display.set_mode((Config.display_width, Config.display_height))
	clock = pygame.time.Clock()
	welcomeImg = pygame.image.load('back1.jpg')
	welcomeImg = pygame.transform.smoothscale(welcomeImg, (800,600))

	rect = pygame.Surface((700,500),pygame.SRCALPHA)
	rect.fill((148,148,148,200))
	
	

	textinput1 = pygame_textinput.TextInput(font_size = 28, text_color = Config.white)
	textinput2 = pygame_textinput.TextInput(font_size = 28, text_color = Config.white)

	returnImg = pygame.image.load('return.png')
	returnImg = pygame.transform.scale(returnImg, (40,40))

	def drawWelcome(x, y):
		gameDisplay.blit(welcomeImg,(x,y))


	intro = True

	while intro:
		gameDisplay.fill(Config.white)

		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()

		drawWelcome(0,0)
		gameDisplay.blit(rect,(56,70))

		for y in range (135, 510, 60):
			pygame.draw.line(gameDisplay, Config.white, (56, y), (56+700, y))

		pygame.draw.line(gameDisplay, Config.white, (210, 70), (210, 570))
		pygame.draw.line(gameDisplay, Config.white, (650, 70), (650, 570))

		smallText = pygame.font.SysFont('arial', 25)

		connect = Config.userinfo.all()

		closeImg = pygame.image.load("close.png")
		closeImg = pygame.transform.smoothscale(closeImg, (30,30))


		(sx, sy) = (130,105)
		for entry in connect:
			entryText = entry['picName']
			entryKey = entry['key']

			textSurf1, textRect1 = text_objects1(entryText, smallText)
			textRect1.center = (sx, sy)	
			gameDisplay.blit(textSurf1, textRect1)

			textSurf2, textRect2 = text_objects1(entryKey, smallText)
			textRect2.center = (sx + 250, sy)	
			gameDisplay.blit(textSurf2, textRect2)

			gameDisplay.blit(closeImg, (sx + 560, sy - 18))

			if sx + 560 < mouse[0] < sx + 560 + 30 and sy - 18 < mouse[1] < sy - 18 + 30 and click[0] == 1 and (Config.button_down == False):
				User = Query()
				Config.userinfo.remove((User.picName == entryText) & (User.key == entryKey))
				Config.keydb.remove(User.key == entryKey)
				Config.button_down = True

			

			(sx, sy) = (sx, sy + 60)

		gameDisplay.blit(returnImg, (50, 10))

		if click[0] == 0:			
				Config.button_down = False
			
		eventsAll = pygame.event.get()
		for event in eventsAll:
			if event.type == pygame.QUIT:
				pygame.quit()
				intro = False
				sys.exit()

		if 50 < mouse[0] < 90 and 10 < mouse[1] < 50 and click[0] == 1:
			intro = False
			choose()

		pygame.display.update()
		clock.tick(30)


def main():
	pygame.init()
	#encrypt()
	welcome()
	#choose()
	#decrypt()
	#history()


if __name__ == '__main__':
    main()