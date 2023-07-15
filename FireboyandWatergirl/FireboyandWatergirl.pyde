#imports 
add_library('minim')
import os

#retrieve path to image and sound files/minim player
PATH = os.getcwd()
initial_state = []
print(PATH)
player = Minim(this)

#lever global variable
leverchange = False

#Creature parent class
class Creature: #class defined for the "creatures" of the game e.g. Fireboy and Watergirl
    def __init__(self,x,y,r,g,img,w,h): #x and y correspond to coordinates of creature, r is the radius of the circle encapsulating it, g is the ground level, w is the width and h is the height
        self.x = x
        self.y = y
        self.w=w
        self.h=h
        self.r = r
        self.g = 750
        self.vy = 0
        self.vx = 0
        self.x1 = 0
        self.level = 'incomplete'
        self.x2 = 795
        self.img = loadImage(PATH+"/images/{0}.png".format(img))
        self.a = False
        self.F = 4
        self.slice = 0
        self.dir = 1
        self.tmp = 0
        self.stepped = False
        self.death = player.loadFile(PATH+"/sounds/deathsound.mp3")      
        self.jump = player.loadFile(PATH+"/sounds/jump.mp3")
        self.diamond = player.loadFile(PATH+"/sounds/diamond.mp3")
    
    
    def gravity(self): #this method is responsible for implementing gravity into the game
        self.g = 710

        for p in (g.platforms+g.blocks):
            if self.x+self.r >= p.x and self.x-self.r <= p.x + p.w and self.y+self.r<= p.y: #this is used to change the ground level if creature lies on a platform
                self.g = p.y-5
                p.steppedon = True
                
                if p.photo == "moveable horizontal platform":
                    self.stepped = True
                self.tmp+=1 
                if p.photo == "lever":
                    if p.state == "unpressed":
                        p.state = "pressed"
                    #elif p.state == "pressed":
                     #   p.state = "unpressed"
                     

                break
            else:
                self.g = g.g
                p.steppedon = False
                p.fireboystepped = False
                self.tmp = 0
    
    
                
        if self.y+self.r < self.g:
            self.vy += 0.3
            if self.y+self.r+self.vy > self.g:
                self.vy = self.g - (self.y+self.r)
        else:
            self.vy = 0
            
    def mud_detection(self): #method to detect if creature is standing on a mud platform
        for m in g.muds:
            if m.x <= self.x <= (m.x+m.w):
                if -self.r< m.y - (self.y+self.r+5) <= 0:
                    self.death.rewind()
                    self.death.play()
                    g.state = "death" #by changing the game state, the screen changes to the death screen
    
    def update(self): #where the gravity and mud detection methods are called/checked for
        self.gravity()
        self.mud_detection()
        self.y += self.vy
        
    def display(self):#display the creatures (watergirl, fireboy, block, diamonds)
        noFill()
        stroke(255)
        #circle(self.x,self.y, 2*self.r)
        image(self.img,self.x-self.r+6,self.y-self.r,200,200,0,0,900,900)
        
        
#class for watergirl which is inherited from Creature class
class Watergirl(Creature):
    def __init__(self,x,y,r,g,img,w,h):
        Creature.__init__(self,x,y,r,g,img,w,h)
        self.keyCodes = {'a': False, 'd': False, 'w': False} #keycodes used for watergirl are a(left), w(jump) and d(right)
    
    def block_detection(self): #detect a block in order to move it
        for p in g.platforms:
            if p.photo == "block":
                if ((self.x-p.x)**2 + (self.y-p.y)**2 )**0.5 <= p.r + self.r and self.g-self.y==self.r and p.y<self.y+4:
                    if (self.x-p.x<0 and self.vx>0) or (self.x-p.x>0 and self.vx<0):
                        block = p
                        if self.keyCodes['a']:
                            a = True
                            for platform in g.platforms:
                                if block.x+block.r-20 > p.x and ((p.y-block.y)**2+((p.x+p.w)-block.x)**2)**0.5<1*block.r and p.photo != "block":
                                    a = False
                                    break
                            if block.x-block.r > 120 and a ==True:
                                p.x+=self.vx
                            else:
                                self.vx = 0
                        elif self.keyCodes['d']:
                            a = True
                            for platform in g.platforms:
                                if block.x+block.r-20 > p.x and ((p.y-block.y)**2+(p.x-block.x)**2)**0.5<1*block.r and p.photo != "block":
                                    a = False
                                    break
                            if block.x+block.r < 405 and a == True:
                                p.x+=self.vx
                            else:
                                self.vx = 0
            
            
        
        
    def lever_detection(self): #this method detects if a creature has come in contact with a lever
        for p in g.platforms[::-1]:
            if p.x <= self.x <= (p.x+p.w) and p == g.l1:
                if -self.r < p.y - (self.y+self.r+5) <= 0:
                    p.watergirlpressed = True
            else:
                p.watergirlpressed = False
                
    def button_detection(self): #detects if character is on a button
        for p in g.platforms[::-1]:
            if p.x <= self.x <= (p.x+p.w) and p.photo == "button":
                if -self.r< p.y - (self.y+self.r+5) <= 0:
                    p.watergirlstepped = True
            else:
                p.watergirlstepped = False
        
    def fire_detection(self): #detects if watergirl is touching a fire platform and terminate level if she does
        for f in g.fires:
            if f.x <= self.x <= (f.x+f.w):
                if  -self.r < f.y - (self.y+self.r+5) == 0:
                    self.death.rewind()
                    self.death.play()
                    g.state = "death"
                    
    def gravity(self): #update gravity/ground over platforms and blocks
        self.g = 710

        for p in (g.platforms+g.blocks):
            if self.x+self.r >= p.x and self.x-self.r <= p.x + p.w and self.y+self.r<= p.y:
                self.g = p.y-5
                p.steppedon = True
                if p.photo == "moveable horizontal platform":
                    self.stepped = True
                self.tmp+=1
                break
            else:
                self.g = g.g
                self.tmp = 0
    
    
                
        if self.y+self.r < self.g:
            self.vy += 0.3
            if self.y+self.r+self.vy > self.g:
                self.vy = self.g - (self.y+self.r)
        else:
            self.vy = 0
            
    def checkLevelCompletion(self): #check if watergirl is standing in front of designated door
        if self.y < g.watergirldoor.y +g.watergirldoor.h:
            if g.watergirldoor.x1 <= self.x <= g.watergirl.x2:
                self.level = 'complete'
            
    def update(self): #where detection methods are checked
        self.checkLevelCompletion()
        self.fire_detection()
        self.gravity()
        self.mud_detection()
        
        if self.keyCodes['a']:
            a = True
            for p in g.platforms:
                if self.x+self.r-20 > p.x and ((p.y-self.y)**2+((p.x+p.w)-self.x)**2)**0.5<1*self.r and p.photo != "block":
                    a = False
                    break
            if g.level == "1":
                if 160<self.y<300 and self.x<150:
                    a = False

            if self.x-self.r > self.x1 and a ==True:
                self.vx = -3.5
            else:
                self.vx = 0
                
        elif self.keyCodes['d']:
            a = True
            for p in g.platforms:
                if self.x+self.r-20 > p.x and p.steppedon == False and ((p.y-self.y)**2+(p.x-self.x)**2)**0.5<self.r and p.photo != "block":
                    a = False
                    break
            if g.level == "1" or g.level == "2":
                if 660<self.y<800 and self.x>710:
                    a = False
            if (self.x+self.r < self.x2) and a== True:
                self.vx = 3.5
            else:
                self.vx = 0
        else:
            self.vx = 0
        if self.keyCodes['w'] and self.vy == 0:
            self.jump.rewind()
            self.jump.play()
            self.vy = -7
            
        for p in g.platforms:
                if p.x<self.x<p.x+p.w and self.y>p.y and self.y-p.y <= 120:
                    platformabove = p
                    if (self.y-platformabove.y-platformabove.h-self.r)>=0 and self.keyCodes['w'] == True:
                        self.vy = self.vy
                    elif self.y <= self.y+platformabove.h and self.keyCodes['w'] == True:
                        self.vy = 0
                        self.keyCodes['w'] = False
                
            
        self.block_detection()
                        
        self.x += self.vx
        self.y += self.vy
        
        #how watergirl collects blue diamonds
        for d in g.diamonds:    
             if ((self.x-d.x)**2+(self.y-d.y)**2)**0.5 <= d.r +self.r:
                 if d.c == 'blue':
                     self.diamond.rewind()
                     self.diamond.play()
                     g.diamonds.remove(d)       
                     g.gemscollected +=1
                     

class Fireboy(Creature): #fireboy class inherited from Creature class
    def __init__(self,x,y,r,g,img,w,h):
        Creature.__init__(self,x,y,r,g,img,w,h)
        self.keyHandlers = {LEFT: False, RIGHT: False, UP: False}
        
    def block_detection(self): #detect if fireboy is touching block to move it
        for p in g.platforms:
            if p.photo == "block":
                if ((self.x-p.x)**2 + (self.y-p.y)**2 )**0.5 <= p.r + self.r and self.g-self.y==self.r and p.y<self.y+4:
                    if (self.x-p.x<0 and self.vx>0) or (self.x-p.x>0 and self.vx<0):
                        block = p
                        if self.keyHandlers[LEFT]:
                            a = True
                            for platform in g.platforms:
                                if block.x+block.r-20 > p.x and ((p.y-block.y)**2+((p.x+p.w)-block.x)**2)**0.5<1*block.r and p.photo != "block":
                                    a = False
                                    break
                            if block.x-block.r > 120 and a ==True:
                                p.x+=self.vx
                            else:
                                self.vx = 0
                        elif self.keyHandlers[RIGHT]:
                            a = True
                            for platform in g.platforms:
                                if block.x+block.r-20 > p.x and ((p.y-block.y)**2+(p.x-block.x)**2)**0.5<1*block.r and p.photo != "block":
                                    a = False
                                    break
                            if block.x+block.r < 405 and a == True:
                                p.x+=self.vx
                            else:
                                self.vx = 0
    #method checking if character is on lever
    def lever_detection(self):
        for p in g.platforms[::-1]:
            if   p.x <= self.x <= (p.x+p.w) and p == g.l1:
                if -self.r < p.y - (self.y+self.r+5) <= 0:
                    p.fireboypressed = True
            else:
                p.fireboypressed = False
     #method checking if character on button           
    def button_detection(self):
        for p in g.platforms[::-1]:
            if p.x <= self.x <= (p.x+p.w) and p.photo == "button":
                if  -self.r < p.y - (self.y+self.r+5) <= 0:
                    p.fireboystepped = True
            else:
                p.fireboystepped = False
                
     #method checking ig fireboy is on water platform, terminates level if he is   
    def water_detection(self):
        for w in g.waters:
            if w.x <= self.x <= (w.x+w.w):
                if  -self.r < w.y - (self.y+self.r+5) == 0:
                    self.death.rewind()
                    self.death.play()
                    g.state = "death"
                    
    #method changing ground level if on platform or block
    def gravity(self):
        self.g = 710

        for p in (g.platforms+g.blocks):
            if self.x+self.r >= p.x and self.x-self.r <= p.x + p.w and self.y+self.r<= p.y:
                self.g = p.y-5
                p.steppedon = True
                if p.photo == "moveable horizontal platform":
                    self.stepped = True        
                break
            else:
                self.g = g.g
                p.steppedon = False
                self.tmp = 0
    
    
                
        if self.y+self.r < self.g:
            self.vy += 0.3
            if self.y+self.r+self.vy > self.g:
                self.vy = self.g - (self.y+self.r)
        else:
            self.vy = 0
            
    def checkLevelCompletion(self): #check if fireboy in front of designated door 
        if self.y < g.fireboydoor.y +g.fireboydoor.h:
            if g.fireboydoor.x1 <= self.x <= g.fireboydoor.x2:
                self.level = 'complete'
            
    def update(self): #where the detection methods are checked
        self.water_detection()
        self.gravity()
        self.mud_detection()
        self.checkLevelCompletion()

        if self.keyHandlers[LEFT]:
            a = True
            for p in g.platforms:
                if p.h<= 50:
                    if self.x+self.r-20 > p.x and ((p.y-self.y)**2+((p.x+p.w)-self.x)**2)**0.5<1*self.r and p.photo != "block" and p.h<=50:
                        a = False
                        break
                elif p.h>=50:
                    if self.x+self.r-20 > p.x and ((p.y-self.y)**2+((p.x+p.w)-self.x)**2)**0.5<2*self.r and p.photo != "block" and p.h<=50:
                        a = False
                        break
            if g.level == "1":
                if 160<self.y<300 and self.x<150:
                    a = False

            if self.x-self.r > self.x1 and a ==True:
                self.vx = -3.5
            else:
                self.vx = 0
                
        elif self.keyHandlers[RIGHT]:
            a = True
            for p in g.platforms:
                if self.x+self.r-20 > p.x and p.steppedon == False and ((p.y-self.y)**2+(p.x-self.x)**2)**0.5<self.r and p.photo != "block":
                    a = False
                    break
                
            if g.level == "1" or g.level == "2":
                if 660<self.y<800 and self.x>710:
                    a = False
            if (self.x+self.r < self.x2) and a== True:
                self.vx = 3.5
            else:
                self.vx = 0
        else:
            self.vx = 0
        
        platformabove = 0
        if self.keyHandlers[UP] and self.vy == 0:   
            self.jump.rewind()
            self.jump.play()
            self.vy = -7
        
        for p in g.platforms:
                if p.x<self.x<p.x+p.w and self.y>p.y and self.y-p.y <= 120:
                    platformabove = p
                    if (self.y-platformabove.y-platformabove.h-self.r)>=0 and self.keyHandlers[UP] == True:
                        self.vy = self.vy
                        #self.keyHandlers[UP] = False
                    elif self.y <= self.y+platformabove.h and self.keyHandlers[UP] == True:
                        self.vy = 0
                        self.keyHandlers[UP] = False
                
        self.block_detection()
        
        self.x += self.vx
        self.y += self.vy
        
        # detection between fireboy and the red diamonds
        for d in g.diamonds:    
             if ((self.x-d.x)**2+(self.y-d.y)**2)**0.5 <= d.r +self.r:
                 if d.c == 'red':
                    self.diamond.rewind()
                    self.diamond.play()
                    g.diamonds.remove(d)
                    g.gemscollected +=1
 
# diamond class inherited from Creature        
class Diamond(Creature):
     def __init__(self,x,y,r,g,img,w,h,c):
         Creature.__init__(self, x,y,r,g,img,w,h)
         self.c = c #c is color of the diamond
        
     def update(self):
         return
     
#parent platform class
class Platform:
    def __init__(self,x,y,w,h,photo,type): #x and y coordinates of up-left corner of platform, width/height of platform, the image displayed and the type of platform it is
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.photo = photo
        self.type = type
        self.platform = loadImage(PATH+"/images/{0}.png".format(self.photo))
        self.steppedon = False
    def display(self):
        if self.type == "Horizontal":
            image(self.platform,self.x, self.y,self.w,self.h)
        if self.type == "Vertical":
            image(self.platform,self.x, self.y,self.w,self.h)

#lever class inherited from Platform
class Lever(Platform):
    def __init__(self,x,y,w,h,photo,type, link):
        Platform.__init__(self,x,y,w,h,photo,type)
        self.state = "unpressed"
        self.nomorechange = False
        self.link = link
        self.watergirlpressed = False
        self.fireboypressed = False
    
    #method detecting which lever image is displayed    
    def getPressed(self):
        if self.state == "pressed":
            self.platform = loadImage(PATH+"/images/pressed lever.png")
        elif self.state == "unpressed":
            self.platform = loadImage(PATH+"/images/lever.png")
            
            
    def display(self): #display lever image
        self.getPressed()
        image(self.platform,self.x, self.y,self.w,self.h)

#button class inherited from Platform class
class Button(Platform):
    def __init__(self,x,y,w,h,photo,type, link):
        Platform.__init__(self,x,y,w,h,photo,type)
        self.state = "unpressed"
        self.link = link  
        self.watergirlstepped = False
        self.fireboystepped = False
    
#moving wall class inherited from platform class  
class MoveableWall(Platform):
    def __init__(self,x,y,w,h,photo,type,link):
        Platform.__init__(self,x,y,w,h,photo,type)
        self.link = link
        self.moving = False

#fire platform inherited from platform class        
class Fire(Platform):
    def __init__(self,x,y,w,h,photo,type):
        Platform.__init__(self,x,y,w,h,photo,type)

#water platform inherited from platform class
class Water(Platform):
    def __init__(self,x,y,w,h,photo,type):
        Platform.__init__(self, x,y,w,h,photo,type)

#mud class inherited from platform class        
class Mud(Platform):
    def __init__(self,x,y,w,h,photo,type):
        Platform.__init__(self,x,y,w,h,photo,type)     

#moving block inherited from Creature class
class Block(Creature):
    def __init__(self,x,y,r,g,img,w,h, photo):
        Creature.__init__(self,x,y,r,g,img,w,h)
        self.photo = "block"
        self.touched = False
        self.steppedon = False
    def display(self):
        noFill()
        stroke(255)
        #circle(self.x,self.y, 2*self.r)
        image(self.img,self.x-self.r+5,self.y-self.r+20,self.w,self.h)

#door class for the doors the characters stand in front of to complete the level        
class Door():
    def __init__(self, x, y, w, h, img):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.x1 = self.x + 25 
        self.x2 = (self.x + self.w) 
        self.img = loadImage(PATH+"/images/{0}.png".format(img))
        
    def display(self):
        image(self.img, self.x, self.y, self.w, self.h)
            
#game class where the game is implemented    
class Game:
    def __init__(self, w,h, level):
        self.state = "menu"
        self.w = w
        self.h = h
        self.backdrop = loadImage(PATH+"/images/background.png")
        self.ground = loadImage(PATH+"/images/ground.png")
        self.mainscreen = loadImage(PATH+"/images/mainscreen.png")
        self.keysimage = loadImage(PATH+'/images/keys.png')
        self.blocks = []
        self.watergirl = Watergirl(100,600,26,710,'watergirl',50,50)
        self.fireboy = Fireboy(100,700,26,710,'fireboy',20,20)
        self.platforms = []
        self.muds = []
        self.waters = []
        self.fires = []
        self.diamonds = []
        self.blocks = []
        self.gemscollected = 0
        self.level = level
        self.bgMusic = player.loadFile(PATH+"/sounds/levelmusic.mp3")
        self.bgMusic.rewind()
        self.bgMusic.play()
#append platforms, door position, buttons, lever, block, and diamonds for level one
        if self.level == "1":
            self.butuplevel = 280
            self.butdownlevel = 400
            self.platforms.append(Platform(200,100,800,25,'platform', "Horizontal"))
            self.platforms.append(Platform(0,160,120,140,'platform',"Horizontal"))
            self.b1 = Button(600,265,40,20,'button',"Horizontal","b")
            self.platforms.append(self.b1)
            self.block1 = Block(300,150,30,710,'block',50,50, "block")
            self.platforms.append(self.block1)
            self.platforms.append(Platform(400,230,120,50,'platform',"Horizontal"))
            self.platforms.append(Platform(0,280,670,25,'platform',"Horizontal"))
            self.b2 = (Button(250,385,40,20,'button',"Horizontal","b"))
            self.platforms.append(self.b2)
            self.platforms.append(MoveableWall(640,400,200,40,'moveable horizontal platform', "Horizontal", "b"))
            self.platforms.append(Platform(120,400,550,25,'platform',"Horizontal"))
            self.l1 = Lever(250,500,50,50,'lever',"Horizontal","a")
            self.platforms.append(self.l1)
            self.platforms.append(MoveableWall(-30,400,155,40,'moveable horizontal platform', "Horizontal", "a"))
            self.platforms.append(Platform(0,540,500,25,'platform',"Horizontal"))
            self.platforms.append(Mud(550,540,80,30,'mud','Horizontal'))
            self.platforms.append(Platform(500,570,200,25,'platform',"Horizontal"))
            self.platforms.append(Platform(0,630,200,25,'platform',"Horizontal"))
            self.platforms.append(Platform(740,660,90,110,'platform',"Horizontal"))
            self.platforms.append(Fire(500,720,140,30,'fire','Horizontal'))
            self.platforms.append(Water(240,720,140,30,'water','Horizontal'))
            self.fires.append(Fire(500,720,100,30,'fire','Horizontal'))
            self.waters.append(Water(240,720,100,30,'water','Horizontal'))
            self.muds.append(Mud(550,530,80,30,'mud','Horizontal'))
            self.diamonds.append(Diamond(200,360,15,710,'red',200,200,'red'))
            self.diamonds.append(Diamond(500,360,15,710,'blue',200,200,'blue'))
            self.diamonds.append(Diamond(50,130,15,710,'blue',200,200,'blue'))
            self.diamonds.append(Diamond(300,70,15,710,'blue',200,200,'blue'))
            self.diamonds.append(Diamond(550,70,15,710,'red',200,200,'red'))
            self.diamonds.append(Diamond(570,680,15,710,'red',200,200,'red'))
            self.diamonds.append(Diamond(310,680,15,710,'blue',200,200,'blue'))
            self.fireboydoor = Door(700, 27, 60, 75, 'fireboydoor')
            self.watergirldoor = Door(630, 26, 62, 75, 'watergirldoor')
#append platforms,character beginning position, door position, buttons, lever, block, and diamonds for level two
        if self.level == "2":
            self.butuplevel = 100
            self.butdownlevel = 200
            self.watergirl = Watergirl(20,600,26,710,'watergirl',50,50)
            self.fireboy = Fireboy(100,600,26,710,'fireboy',20,20)
            self.b2 = (Button(560,83,40,20,'button',"Horizontal","b"))
            self.platforms.append(self.b2)
            self.platforms.append(Platform(550,100,800,25,'platform', "Horizontal"))
            #self.platforms.append(Platform(0,160,120,140,'platform',"Horizontal"))
            self.fireboydoor = Door(700, 27, 60, 75, 'fireboydoor')
            self.watergirldoor = Door(630, 26, 62, 75, 'watergirldoor')
            self.block1 = Block(300,150,30,710,'block',50,50, "block")
            #self.platforms.append(self.block1)
            #self.platforms.append(MoveableWall(640,400,200,40,'moveable horizontal platform', "Horizontal", "b"))
            #self.platforms.append(Platform(120,400,550,25,'platform',"Horizontal"))
            self.l1 = Lever(250,500,50,50,'lever',"Horizontal","a")
            #self.platforms.append(self.l1)
            self.b1 = Button(340,185,40,20,'button',"Horizontal","b")
            self.platforms.append(self.b1)
            self.platforms.append(MoveableWall(360,200,200,40,'moveable horizontal platform', "Horizontal", "b"))
            self.platforms.append(Platform(180,200,200,25,'platform', "Horizontal"))
            self.platforms.append(Platform(0,270,50,19,'platform',"Horizontal"))
            self.diamonds.append(Diamond(20,250,15,710,'blue',200,200,'blue'))
            self.platforms.append(Platform(130,350,50,19,'platform',"Horizontal"))
            self.diamonds.append(Diamond(150,330,15,710,'red',200,200,'red'))
            self.platforms.append(Platform(300,420,50,19,'platform',"Horizontal"))
            self.diamonds.append(Diamond(320,400,15,710,'blue',200,200,'blue'))
            self.platforms.append(Platform(450,500,50,19,'platform',"Horizontal"))
            self.diamonds.append(Diamond(470,480,15,710,'red',200,200,'red'))
            self.platforms.append(Platform(450,500,50,19,'platform',"Horizontal"))
            self.platforms.append(Platform(740,660,90,110,'platform',"Horizontal"))
            
            self.platforms.append(Mud(0,560,600,30,'mud','Horizontal'))
            
            self.platforms.append(Platform(600,570,100,19,'platform',"Horizontal"))
            
            self.platforms.append(Water(450,650,200,30,'water','Horizontal'))
            self.diamonds.append(Diamond(540,630,15,710,'blue',200,200,'blue'))
            self.platforms.append(Fire(150,650,200,30,'fire','Horizontal'))
            self.diamonds.append(Diamond(250,630,15,710,'red',200,200,'red'))
            self.diamonds.append(Diamond(250,700,15,710,'blue',200,200,'blue'))
            self.diamonds.append(Diamond(540,700,15,710,'red',200,200,'red'))
            self.platforms.append(Fire(450,720,200,30,'fire','Horizontal'))
            self.platforms.append(Water(150,720,200,30,'water','Horizontal'))
            self.waters.append(Water(450,650,200,30,'water','Horizontal'))
            self.fires.append(Fire(150,650,200,30,'fire','Horizontal'))
            self.fires.append(Fire(450,720,200,30,'fire','Horizontal'))
            self.waters.append(Water(150,720,200,30,'water','Horizontal'))
            self.muds.append((Mud(0,550,600,30,'mud','Horizontal')))
            #self.diamonds.append(Diamond(200,360,15,710,'red',200,200,'red'))
#append platforms, character beginning positions, door position, buttons, lever, block, and diamonds for level three            
        if self.level == '3':
            self.butuplevel = 100
            self.butdownlevel = 200
            self.watergirl = Watergirl(100,50,26,710,'watergirl',50,50)
            self.fireboy = Fireboy(140,50,26,710,'fireboy',20,20)
            self.b2 = (Button(560,83,40,20,'button',"Horizontal","b"))
            self.diamonds.append(Diamond(268, 90, 15, 710, 'blue',200,200,'blue'))
            self.diamonds.append(Diamond(490, 90, 15, 710, 'red',200,200,'red'))
            # self.platforms.append(self.b2)
            self.platforms.append(Platform(640,100,160,25,'platform', "Horizontal"))
            self.platforms.append(Platform(0, 100, 150, 25, 'platform', 'Horizontal'))
            self.platforms.append(Platform(259, 100, 30,25,'platform','Horizontal'))
            self.platforms.append(Platform(480, 100, 30, 25, 'platform','Horizontal'))
            self.block1 = Block(470,200,30,710,'block',50,50, "block")
            self.platforms.append(self.block1)
            self.platforms.append(Mud(290, 100, 190, 25, 'mud', 'Horizontal'))
            self.muds.append(Mud(290, 100, 190, 25, 'mud', 'Horizontal'))
            self.diamonds.append(Diamond(750, 180, 15, 710, 'blue',200,200,'blue'))
            self.platforms.append(Water(725, 184.8, 65, 25, 'water','Horizontal'))
            self.waters.append(Water(725, 184.8, 65, 25, 'water','Horizontal'))
            self.diamonds.append(Diamond(37, 179, 15, 710, 'red',200,200,'red'))
            self.platforms.append(Fire(10, 184.8, 65, 25, 'fire','Horizontal'))
            self.fires.append(Fire(10, 184.8, 65, 25, 'fire','Horizontal'))
            self.diamonds.append(Diamond(203, 175, 15, 710, 'blue',200,200,'blue'))
            self.diamonds.append(Diamond(567, 175, 15, 710, 'red',200,200,'red'))
            self.platforms.append(Platform(190, 185, 40, 25, 'platform','Horizontal'))
            self.platforms.append(Platform(550, 185, 40, 25, 'platform', 'Horizontal'))
            self.diamonds.append(Diamond(117, 265, 15, 710, 'blue',200,200,'blue'))
            self.diamonds.append(Diamond(645, 265, 15, 710, 'red',200,200,'red'))
            self.platforms.append(Platform(100, 275, 40, 25, 'platform','Horizontal'))
            self.platforms.append(Platform(630, 275, 40, 25, 'platform','Horizontal'))
            self.diamonds.append(Diamond(470, 240, 15, 710, 'red',200,200,'red'))
            self.platforms.append(Platform(450, 300, 100, 25, 'platform', 'Horizontal'))
            self.diamonds.append(Diamond(43, 355, 15, 710, 'blue',200,200,'blue'))
            self.diamonds.append(Diamond(733, 355, 15, 710, 'red',200,200,'red'))
            self.platforms.append(Platform(30, 365, 40, 25,'platform','Horizontal'))
            self.platforms.append(Platform(720, 365, 40, 25, 'platform', 'Horizontal'))
            self.diamonds.append(Diamond(113, 445, 15, 710, 'red',200,200,'red'))
            self.diamonds.append(Diamond(643, 445, 15, 710, 'blue',200,200,'blue'))
            self.platforms.append(Platform(100, 455, 40, 25, 'platform', 'Horizontal'))
            self.platforms.append(Platform(630, 455, 40, 25, 'platform','Horizontal'))
            self.diamonds.append(Diamond(204, 535, 15, 710, 'red',200,200,'red'))
            self.diamonds.append(Diamond(563, 535, 15, 710, 'blue',200,200,'blue'))
            self.platforms.append(Platform(190, 545, 40, 25, 'platform', 'Horizontal'))
            self.platforms.append(Platform(550, 545, 40, 25, 'platform', 'Horizontal'))
            self.diamonds.append(Diamond(658, 625, 15, 710, 'red',200,200,'red'))
            self.diamonds.append(Diamond(698, 625, 15, 710, 'red',200,200,'red'))
            self.diamonds.append(Diamond(35, 625, 15, 710, 'blue',200,200,'blue'))
            self.diamonds.append(Diamond(70, 625, 15, 710, 'blue',200,200,'blue'))
            self.diamonds.append(Diamond(375, 570, 15, 710, 'blue',200,200,'blue'))
            self.platforms.append(Fire(260,635, 250, 25, 'fire','Horizontal'))
            self.fires.append(Fire(260,635, 250, 25, 'fire','Horizontal'))
            self.fires.append(Fire(635,635, 100, 25, 'fire','Horizontal'))
            self.platforms.append(Fire(635, 635, 100, 25, 'fire', 'Horizontal'))
            self.platforms.append(Water(10, 635, 100, 25, 'water', 'Horizontal'))
            self.waters.append(Water(10, 635, 100, 25, 'water','Horizontal'))
            self.muds.append(Mud(0, 700, 800, 30, 'mud','Horizontal'))
            self.platforms.append(Mud(0, 705, 800, 40, 'mud','Horizontal'))
            self.fireboydoor = Door(725, 27, 60, 75, 'fireboydoor')
            self.watergirldoor = Door(650, 26, 62, 75, 'watergirldoor')
            # self.block1 = Block(450,300,30,710,'block',50,50, "block")
            # self.platforms.append(self.block1)
            self.l1 = Lever(250,500,50,50,'lever',"Horizontal","a")
            #self.platforms.append(self.l1)
            self.b1 = Button(340,185,40,20,'button',"Horizontal","b")
            
        self.g = 740
        
        #if players complete final level (3), game is resetted to begin with level one
        if self.level == '4':
            self.level == "1"
            
     #method for moving platform if lever or button is interacted with       
    def movePlatform(self):
        link = 0
        change = 0
        but = 0
        
        
        self.fireboy.button_detection()
        self.watergirl.button_detection()
        self.fireboy.lever_detection()
        self.watergirl.lever_detection()
        
        
            
        for p in self.platforms:
            if p==self.b1:
                if p.watergirlstepped or p.fireboystepped:
                    self.b1.state = "pressed"
                elif not(p.watergirlstepped or p.fireboystepped):
                    self.b1.state = "unpressed"
            elif p == self.b2:
                if p.watergirlstepped or p.fireboystepped:
                    self.b2.state = "pressed"
                elif not(p.watergirlstepped or p.fireboystepped):
                    self.b2.state = "unpressed"
                
                    
        for p in self.platforms:
            if p == self.l1:
                if (p.watergirlpressed or p.fireboypressed) and leverchange == False:
                    if self.l1.state == "unpressed":
                         self.l1.state = "pressed"
                    
                    elif self.l1.state == "pressed":
                        self.l1.state = "unpressed"
                    global leverchange
                    leverchange = True
                    #p.watergirlpressed = False
                    #p.fireboypressed = False
                if not p.watergirlpressed and not p.fireboypressed and leverchange == True:
                    leverchange = False
                

        for p in self.platforms:        
            if p.photo == "moveable horizontal platform" and p.link == "a" and self.l1.state == "pressed":
                if p.y<480:
                    p.y+=0.6
                    p.moving = True  
                else:
                    p.moving = False
                
                for i in [self.watergirl, self.fireboy]:
                    if i.stepped and p.moving == True:
                        i.y-= 0.6
                        #i.display()
                    #elif i.stepped ==False:
                       # i.display()
            if p.photo == "moveable horizontal platform" and (self.b1.state == "pressed" or self.b2.state == "pressed") and p.link == "b":
                if  p.y>self.butuplevel:
                    p.y -= 1
                    p.moving = True
                        
                for i in [self.watergirl, self.fireboy]:
                    if i.stepped and p.moving == True:
                        i.y-= 1
                     #   i.display()
                   # else:
                      #  i.display()
        for p in g.platforms:
            if p.photo == "moveable horizontal platform" and  p.link == "b":
                if p.y<self.butdownlevel:
                    p.y+=0.5
                
        for p in g.platforms:
            if p.photo == "moveable horizontal platform" and  p.link == "a" and self.l1.state == "unpressed":
                if p.y>400:
                    p.y-=0.5
            
            
            

 #method displaying screens: menu, level 1, level 2, level 3, retry screen, score screen, settings screen           
    def display(self):
        if self.state == "menu":
            background(0)
            image(self.mainscreen,0,0)
            fill(255,204,0)
            textSize(83)
            text("Fireboy & Watergirl",28,350)
            fill(255,204,0)
            textSize(80)
            text("PLAY", 290, 470)
            fill(255,204,0)
            textSize(50)
            text('Guidelines', 260, 560)
    
            if 283 <= mouseX <= 490 and 400<= mouseY <= 530:
                stroke(0)
                strokeWeight(4)
                noFill()
                rect(283,405,205,73)
            if 255 <= mouseX <= 480 and 500 <= mouseY <= 575:
                stroke(0)
                strokeWeight(4)
                noFill()
                rect(255, 516, 267, 50)
                
        elif self.state == 'settings':
            background(0)
            image(self.backdrop, 0, 0)
            image(self.backdrop, 0, 743)
            image(self.keysimage, 10, 10, 500, 300)
            image(loadImage(PATH+'/images/fire.png'),2, 350, 500, 100)
            fill(255,255,255)
            textSize(30)
            text("Watergirl keys:" ,520,50)
            fill(255,255,255)
            textSize(22)
            text('Press "A" to go left' ,520,80)
            fill(255,255,255)
            textSize(22)
            text('Press "D" to go right ' ,520,110)
            fill(255,255,255)
            textSize(22)
            text('Press "W" to jump' ,520,140)
            fill(255,255,255)
            textSize(30)
            text("Fireboy keys:" ,520,185)
            fill(255,255,255)
            textSize(22)
            text('Press "<-" to go left',520,215)
            fill(255,255,255)
            textSize(22)
            text('Press "->" to go right' ,520,245)
            fill(255,255,255)
            textSize(22)
            text('Press "up arrow " to jump' ,520,275)
            fill(255,255,255)
            textSize(20)
            text('Only Fireboy can walk on fire' ,487,375)
            fill(255,255,255)
            textSize(20)
            text('Watergirl dies if she touches fire' ,485,405)       
            image(loadImage(PATH+'/images/water.png'), 0, 450, 500, 100)
            text('Watergirl dies if she touches fire' ,485,405)
            fill(255,255,255)
            textSize(20)
            text('Only Watergirl can walk on water' ,480,480) 
            fill(255,255,255)
            textSize(20)
            text('Fireboy dies if he touches water' ,480,510)  
            image(loadImage(PATH+'/images/mud.png'), 11, 550, 480, 90)
            fill(255,255,255)
            textSize(20)
            text('Both die if they touch mud' ,500,590)  
            image(loadImage(PATH+'/images/watergirldoor.png'), 10, 650, 120, 150)
            image(loadImage(PATH+'/images/fireboydoor.png'), 150, 650, 120, 150)
            fill(255,255,255)
            textSize(20)
            text('To end level, characters' ,275,675) 
            fill(255,255,255)
            textSize(20)
            text('stand in front of their' ,275,700) 
            fill(255,255,255)
            textSize(20)
            text('marked doors' ,275,725)
            fill(255,255,255)
            textSize(20)
            text('Return to:' ,625,675)
            fill(255,204,0)
            textSize(20)
            text('MENU' ,645,715)
            
            if 640 <= mouseX <= 700 and 700<= mouseY <= 740:
                stroke(0)
                strokeWeight(4)
                noFill()
                rect(635,690,76,35)
                
        elif self.state == "score screen":
            if int(self.level) == 1 or int(self.level) == 2:
                background(0)
                image(self.backdrop, 0, 0)
                image(self.backdrop, 0, 743)
                fill(255,204,0)
                textSize(40)
                text("You betta work! Gems collected: "+str(g.gemscollected), 50, 350)
                fill(255,204,0)
                textSize(30)
                text("NEXT LEVEL", 300, 450)
                if 283 <= mouseX <= 490 and 400<= mouseY <= 530:
                    stroke(0)
                    strokeWeight(4)
                    noFill()
                    rect(283,405,205,73)
                    
                fill(255,204,0)
                textSize(30)
                text(" GO TO MENU", 285, 650)
                if 283 <= mouseX <= 490 and 500<= mouseY <= 700:
                    stroke(0)
                    strokeWeight(4)
                    noFill()
                    rect(283,600,205,73)
            if int(self.level) == 3:
                background(0)
                image(self.backdrop, 0, 0)
                image(self.backdrop, 0, 743)
                fill(255,204,0)
                textSize(40)
                text("You betta work! Gems collected: "+str(g.gemscollected), 50, 350)
                fill(255,204,0)
                textSize(30)
                text(" GO TO MENU", 285, 650)
                if 283 <= mouseX <= 490 and 500<= mouseY <= 700:
                    stroke(0)
                    strokeWeight(4)
                    noFill()
                    rect(283,600,205,73)
                
            
        elif self.state == "death":
            background(0)
            image(self.backdrop, 0, 0)
            image(self.backdrop, 0, 743)
            fill(255,204,0)
            textSize(40)
            text("You Lost! Do Better Girl!", 150, 350)
            fill(255,204,0)
            textSize(30)
            text("RETRY LEVEL", 300, 450)
            if 283 <= mouseX <= 490 and 400<= mouseY <= 530:
                stroke(0)
                strokeWeight(4)
                noFill()
                rect(283,405,205,73)
            
            fill(255,204,0)
            textSize(30)
            text(" GO TO MENU", 285, 650)
            if 283 <= mouseX <= 490 and 500<= mouseY <= 700:
                stroke(0)
                strokeWeight(4)
                noFill()
                rect(283,600,205,73)
            
            
            

        elif self.state == "play":
            background(0)  
            image(self.backdrop, 0, 0)
            image(self.ground,0,330)
    
            
            for p in self.platforms:
                p.display()
                if p.photo == "block":
                    p.update()
            for b in self.blocks:
                b.display()
                b.update()
                
            for d in self.diamonds:
                d.display()
                
            self.fireboydoor.display()
            self.watergirldoor.display()
                
            self.watergirl.display()
            self.watergirl.update()
            self.fireboy.display()
            self.fireboy.update()
            
            self.movePlatform()
            
            if self.fireboy.level == 'complete' and self.watergirl.level == 'complete':
               # g.__init__(800,800, str(int(g.level)+1))
                if int(self.level)<4:
                    self.state = 'score screen'

g = Game(800,800, "1")

def setup():
    background(255,255,255)
    size(800, 800)
    
def draw():
    g.display()
 
#key handlers for fireboy and watergirl
def keyPressed():
    if keyCode == LEFT:
        g.fireboy.keyHandlers[LEFT] = True
    elif keyCode == RIGHT:
        g.fireboy.keyHandlers[RIGHT] = True
    elif keyCode == UP:
        g.fireboy.keyHandlers[UP] = True
    elif key == 'a':
        g.watergirl.keyCodes['a'] = True
    elif key == 'w':
        g.watergirl.keyCodes['w'] = True
    elif key == 'd':
        g.watergirl.keyCodes['d'] = True

def keyReleased():
    if keyCode == LEFT:
        g.fireboy.keyHandlers[LEFT] = False
    elif keyCode == RIGHT:
        g.fireboy.keyHandlers[RIGHT] = False
    elif keyCode == UP:
        g.fireboy.keyHandlers[UP] = False
    elif key == 'a':
        g.watergirl.keyCodes['a'] = False
    elif key == 'w':
        g.watergirl.keyCodes['w'] = False
    elif key == 'd':
        g.watergirl.keyCodes['d'] = False   

#click buttons to navigate menu, retry, next level, settings
def mouseClicked():
    if g.state == "menu":
        if 283 <= mouseX <= 490 and 400<= mouseY <= 530:
            g.state = "play"
        if 255 <= mouseX <= 480 and 500 <= mouseY <= 575:
            g.state = 'settings'
    elif g.state == "settings":
        if 640 <= mouseX <= 700 and 700<= mouseY <= 740:
            g.state = 'menu'
    elif g.state == "score screen":
        if 283 <= mouseX <= 490 and 400<= mouseY <= 530:
            player.stop()
            g.__init__(800,800, str(int(g.level)+1))
            g.state = "play"
        if 283 <= mouseX <= 490 and 531<= mouseY <= 700:
            player.stop()
            g.__init__(800,800,"1")
            g.state = "menu"


    elif g.state == "death":
        if 283 <= mouseX <= 490 and 400<= mouseY <= 530:
            player.stop()
            g.__init__(800,800, g.level)
            g.state = "play"
            
        if 283 <= mouseX <= 490 and 531<= mouseY <= 700:
            player.stop()
            g.__init__(800,800,"1")
            g.state = "menu"
    
                

    
                
                
    
                

    
                
                
