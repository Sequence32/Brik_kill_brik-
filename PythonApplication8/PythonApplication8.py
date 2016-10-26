import pygame
from pygame import *
import sys, random, math, fractions
pygame.init()

D_Width = 800
D_Height = 600
h_Height = int(D_Height / 2)
h_Width = int(D_Width / 2)
p_Offset_x = 0
p_Offset_y = 0

Total_Display = pygame.display.set_mode((D_Width, D_Height))
pygame.display.set_caption('Fire Death. die die die')

Menu_Display = pygame.display.set_mode((D_Width, D_Height))
meun_caption = pygame.display.set_caption('Menu!')

clock = pygame.time.Clock()
level_List =['L1.txt', "l2.TXT", "L3.TXT", "L4.txt"]

class Flying_Blocks(pygame.sprite.Sprite):
    def __init__(self, width, height):

        super().__init__()

        self.image = pygame.image.load('fire.png').convert_alpha()
        self.rect = self.image.get_rect()
        
    def update(self):
        self.rect.x += -3
        if self.rect.x <= 0 :
            pygame.sprite.Sprite.kill(self)

class Blocks(pygame.sprite.Sprite):
    def __init__(self, width, height, Direction):

        super().__init__()

        self.image = pygame.image.load("bullet.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.change_y = 0
        self.change_x = 0
        self.Direction = Direction

    def shell_movement(self, cursor_pos_x, cursor_pos_y, player_pos_x, player_pos_y, offsetx, offsety):
    
        shell_vec_x = cursor_pos_x - player_pos_x - offsetx
        shell_vec_y = cursor_pos_y - player_pos_y - offsety
        vec_length = math.sqrt(shell_vec_x ** 2 + shell_vec_y ** 2)
        shell_vec_y = (shell_vec_y / vec_length) * 5
        shell_vec_x = (shell_vec_x / vec_length) * 5
        self.change_y += shell_vec_y  
        self.change_x += shell_vec_x
       
    def update(self):

        self.rect.y += self.change_y

        if self.Direction == "Right":
            self.rect.x += 5
        elif self.Direction == "Left":
            self.rect.x -= 5

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):

        self.Animation_Count = 0
        self.Animation_List = {"Moving_Right": ["mega1_converted.png","mega2_converted.png","mega3_converted.png","mega4_converted.png","mega5_converted.png","mega6_converted.png","mega7_converted.png","mega8_converted.png","mega8_converted.png"],
                               "Moving_Left": ["Mega_R1.png", "Mega_R2.png", "Mega_R3.png", "Mega_R4.png", "Mega_R5.png", "Mega_R6.png", "Mega_R7.png", "Mega_R8.png", "Mega_R8.png" ],
                               "Standing": ["Mega1_converted.png"],
                               "Jumping":["M_Jump1.png", "M_jump2.png", "M_Jump3.png", "M_jump4.png", "m_Jump5.png", "M_jump6.png", "m_jump7.png", "M_jump8.png"]
                               }
        
        pygame.sprite.Sprite.__init__(self)
        all_Sprite_List.add(self)
        player_list.add(self)
        self.On_Ground = False
        self.image = pygame.image.load(self.Animation_List["Moving_Right"][self.Animation_Count]).convert_alpha()
        self.rect = Rect(x, y, 16, 16)
        self.isStanding = True
        self.direction = "Right"
        self.fallspeed = 10

    def jump(self):

        if self.On_Ground == True:
            self.isStanding = False        
            self.move(0, -45)
            self.On_Ground = False
               
    def move(self, px, py):

        if px != 0:

            self.move_on_axis(px, 0)
            if px > 0:
                self.direction = "Right"
                self.image = pygame.image.load(self.Animation_List["Moving_Right"][self.Animation_Count]).convert_alpha()
                if self.Animation_Count == len(self.Animation_List["Moving_Right"]) or self.Animation_Count >= 8:
                    self.Animation_Count = 0
                else:
                    self.Animation_Count += 1
            if px < 0:

                self.direction = "Left"
                self.image = pygame.image.load(self.Animation_List["Moving_Left"][self.Animation_Count]).convert_alpha()
                if self.Animation_Count == len(self.Animation_List["Moving_Left"]) or self.Animation_Count >= 8:
                    self.Animation_Count = 0
                else:
                    self.Animation_Count += 1

        if py != 0:
            self.move_on_axis(0, py)
               
    def move_on_axis(self, px, py):
        self.rect.x += px
        self.rect.y += py
        self.On_Ground = False

        for wall in walls:
            if pygame.sprite.collide_rect(self, wall):   
                if px > 0:
                     self.rect.right = wall.rect.left
                if px < 0:
                    self.rect.left = wall.rect.right
                if py > 0:
                    self.rect.bottom = wall.rect.top
                    self.On_Ground = True
                    self.py = 0
                if py < 0:
                    self.rect.top = wall.rect.bottom

    def update(self):
        
        if self.isStanding == True:
            if self.direction == "Left":
                self.image = pygame.image.load(self.Animation_List["Moving_Left"][0]).convert_alpha()
            if self.direction == "Right":
                self.image = pygame.image.load(self.Animation_List["Moving_Right"][0]).convert_alpha()
            if self.On_Ground == False:
                isStanding = False
            isStanding = False

        if self.On_Ground == False:
            fall = self.fallspeed
            fall+=5
            self.move_on_axis(0, fall)
            if self.direction == "Left":
                self.move_on_axis(0, fall)
                self.image = pygame.image.load(self.Animation_List["Jumping"][6]).convert_alpha()
            if self.direction == "Right":
                self.move_on_axis(0, fall)
                self.image = pygame.image.load(self.Animation_List["Jumping"][6]).convert_alpha()

        else:
            self.fallspeed=0

    def Reset(self,px, py):
        self.rect.x = px
        self.rect.y = py
        self.On_Ground = False      

class Wall(pygame.sprite.Sprite):
    def __init__(self, wx, image):
        super().__init__()
        all_Sprite_List.add(self)
        walls.add(self)
        self.image = pygame.Surface((32,32))
        self.rect = Rect(wx[0], wx[1], 32, 32)
class orgin(Wall):
    def __init__(self):

        self.rect = Rect(wx[0], wx[1],1,1)


class Item(pygame.sprite.Sprite):
    def __init__(self, ix, image):
        super().__init__()
        all_Sprite_List.add(self)
        ItemList.add(self)
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = Rect(ix[0], ix[1], 16, 16)

class Monster(pygame.sprite.Sprite):
    def __init__(self, mx, image):
        super().__init__()
        all_Sprite_List.add(self)
        Monster_List.add(self)
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = Rect(mx[0], mx[1], 16, 16)
        self.on_Ground = False
        self.wallOverRideL = False
        self.wallOverRideR = False
    def move_on_axis(self, mx, my):
        self.on_Ground = False
        self.rect.x += mx
        self.rect.y += my

        for wall in walls:
            if pygame.sprite.collide_rect(self, wall):   
                if mx > 0:
                    self.rect.right = wall.rect.left
                    self.wallOverRideR = False
                    self.wallOverRideL = True
                if mx < 0:
                    self.rect.left = wall.rect.right
                    self.wallOverRideL = False
                    self.wallOverRideR = True
                if my > 0:
                    self.on_Ground = True
                    self.rect.bottom = wall.rect.top
                if my < 0:
                    self.rect.top = wall.rect.bottom

    def move(self, Targetx, Targety):
        if self.wallOverRideL == True:
            self.move_on_axis(-1,0)
        elif self.wallOverRideR == True:
            self.move_on_axis(1, 0)            
        elif self.rect.x < Targetx.rect.x:
            self.move_on_axis(1, 0)
        elif self.rect.x > Targetx.rect.x:
            self.move_on_axis(-1, 0)
        if self.on_Ground == False:
            self.move_on_axis(0, 3)


class Exit(object):
    def __init__(self, wx):
       exits.append(self)
       self.rect = Rect(wx[0], wx[1], 16, 16)
       self.image = pygame.Surface((32,32))

class GameMenu():
    def __init__(self, screen, items, bg_color=(0,0,0), font = None, font_size = 30, font_color = (255,255,255)):

        self.screen = Menu_Display
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height
        
        self.bg_color = bg_color
        self.clock = pygame.time.Clock()

        self.items = items
        self.font = pygame.font.SysFont(font, font_size)
        self.font_color = font_color
        
        self.items = []

        for index, item in enumerate(items):
            label = self.font.render(item, 1, font_color)
 
            width = label.get_rect().width
            height = label.get_rect().height

            posx = (self.scr_width / 2) - (width / 2)
            text_height = len(items) * height
            posy = (self.scr_height / 2) - (text_height / 2) + (index * height)
            
            self.items.append([item, label, (width, height), (posx, posy)])

    def run(self):
        MenuLoop = True
        while MenuLoop:

            self.clock.tick(60)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    MenuLoop = False

            key = pygame.key.get_pressed()
            if key[pygame.K_ESCAPE]:
                pygame.display.set_caption('Fire Death. die die die')
                Main()							
            # Redraw the background
            self.screen.fill(self.bg_color)
 
            for name, label, (width, height), (posx, posy) in self.items:
                self.screen.blit(label, (posx, posy))

            pygame.display.flip()
    def runNext(self):
         iLevel_Count += 1
         MenuLoop = True
         while MenuLoop:
            
            BuildLevel(level_List[iLevel_Count])
            Main()		
            self.clock.tick(60)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    MenuLoop = False

            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                pygame.display.set_caption('Fire Death. die die die')
            # Redraw the background
 
            for name, label, (width, height), (posx, posy) in self.items:
                self.screen.blit(label, (posx, posy))

            pygame.display.flip()
#Thanks StackOverFlow!
class Camera(object):
    def __init__(self, function, Width, Hight):
        self.function = function
        self.state = Rect(0, 0, Width, Hight)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.function(self.state, target.rect)

def C_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+h_Width, -t+h_Height, w, h

    l = min(0, l)                          
    l = max(-(camera.width-D_Width), l)  
    t = max(-(camera.height-D_Height), t) 
    t = min(0, t)                           
    return Rect(l, t, w, h)


#setting up are sprite list with the sprite group
bulletList = pygame.sprite.Group()
all_Sprite_List = pygame.sprite.Group()
shell_List = pygame.sprite.Group()
player_list = pygame.sprite.GroupSingle()
walls = pygame.sprite.Group()
ItemList = pygame.sprite.Group()
Monster_List = pygame.sprite.Group()
#makes the first 10 bullets
for b in range(10):
    bullet = Flying_Blocks(16, 16)
    bullet.rect.x = random.randrange(700,800)
    bullet.rect.y = random.randrange(1, 260)

#adding bullets to sprite and bullet list
    bulletList.add(bullet)
    all_Sprite_List.add(bullet)

exits = []

def BuildLevel(file):
    total_level_height = 0
    total_level_width = 0
    lLength = 0
    lHeight = 0
    row1 = 0
    monster = []
    Level = open(file)
    x = y = 0
    for row in Level:
        row1 += 1
        total_level_height +=32
        for col in row:
            if col == "m":
                monster.append((x,y))
            if col  == "p":
                lHeight = x
                lLength = y
            if col == "w":
                if row1 == 1 and col == "w":
                    total_level_width += 32
                Wall((x, y),"tileq.png")
            elif col == "q":
                Wall((x,y), "re1.png")
            elif col == "d":
                Item((x, y),"Diamond.png")
            if col == "E":
                exit = Exit((x, y))
            x += 32
        y += 32
        x = 0

    camera = Camera(C_camera, total_level_width, total_level_height)
    
    return {"cam": camera,"LevWidth": total_level_width, "levHeight": total_level_height, "PH": lHeight, "PL": lLength, "mon": monster}

def Main():
    resetPlayer = False
    itemdict = BuildLevel(level_List[0])
    monster1 = itemdict["mon"]
    total_level_width = itemdict["LevWidth"]
    total_level_height = itemdict["levHeight"]
    camera = itemdict["cam"]
    player = Player(itemdict["PH"],itemdict["PL"])
    print(total_level_width)
    iLevel_count = 0
    Reset_Shell_Timer = 0
    Spawn_Timer = 0
    Reset = True
    running = True
    pDirection = "Right"
    animation_timer = 0
    
    for monster in monster1:
        Monster(monster, "slime1.png")


    while running == True:
        
        if resetPlayer == True:
            player.Reset(itemdict["PH"],itemdict["PL"])
            resetPlayer = False
    
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN and e.type == pygame.K_ESCAPE:
                running = False    

        Get_Time = clock.tick(60)
        Reset_Shell_Timer += Get_Time
        Spawn_Timer += Get_Time
        animation_timer += Get_Time


# Reset bullets at end of map
       # for bullet in bulletList:
           # if bullet.rect.x <= 0:
           #     bullet.rect.x = random.randrange(600, 700)
            #if player.rect.colliderect(bullet.rect):
               # pygame.sprite.spritecollide(bullet, player_list, True)  
              #  Menu_Display = pygame.display.set_mode((D_Width,D_Height))
              #  Lose_Menu = ("You lose!", "")
             #   gm = GameMenu(Menu_Display, Lose_Menu)
             #   gm.run()
         
# Adds new bullets firing at the end of the map    
        bulletList.update()
        if Spawn_Timer == 1200 and len(bulletList) < 150:
            #Spawn_Timer = 0
            #for b in range(5):
                bullet = Flying_Blocks(16, 16)
                bullet.rect.x = random.randrange(total_level_width, total_level_width + 100)
                bullet.rect.y = random.randrange(1, total_level_height)
                bulletList.add(bullet)
                all_Sprite_List.add(bullet)
        
    #Spaces bullets so you can't spam shoot 
        if Reset_Shell_Timer >= 150:
            Reset_Shell_Timer = 0
            Reset = True
    #Kills bullets hit by shells shot
        for shell in shell_List:
            Block_kill = pygame.sprite.spritecollide(shell, bulletList, True)

        x1, y1 = pygame.mouse.get_pos()
        p_OffsetX = -x1 + h_Width
        p_Offsety = -y1 + h_Height
        
        print(x1, "  ", y1)
     #Moves the player left, right, up and down
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] or key[pygame.K_w] and player.On_Ground == True:
            player.jump()
        if key[pygame.K_DOWN] or key[pygame.K_s]:
            player.move(0, 2)                   
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            animation_timer = 0
            pDirection = "Right"
            player.move(2, 0)
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            animation_timer = 0
            pDirection = "Left"
            player.move(-2, 0)
        if key[pygame.K_SPACE]  and Reset == True:
             shell = Blocks(5, 5, pDirection)
             shell.shell_movement( x1, y1, player.rect.x ,  player.rect.y, p_OffsetX, p_Offsety)
             shell.rect.x = player.rect.x
             shell.rect.y = player.rect.y
             shell_List.add(shell)
             all_Sprite_List.add(shell)
             Reset = False
        if player.On_Ground == False:
            player.move(0, 1)
        if animation_timer >= 100:
            player.update()
            if player.On_Ground == False:
                pass
            else:
                player.isStanding = True

        for mon in Monster_List:
            mon.move(player, player)

#Call menu class when i is pressed!
        if key[pygame.K_i]:
   
            # Making menu screen
            Menu_Display = pygame.display.set_mode((width, height))
            menu_items = ('Weapons', 'Armor', 'Stats')
            pygame.display.set_caption('Game Menu')
            gm = GameMenu(Menu_Display, menu_items)
            gm.run()

    #Removes tje shells that make it off the map
        for shell in shell_List:
            if shell.rect.x > total_level_width or shell.rect.x < 0 or shell.rect.y > total_level_height or shell.rect.y < 0:
                shell_List.remove(shell)
                all_Sprite_List.remove(shell)
         
        shell_List.update()
    
        Total_Display.fill((255,255,255))
    #draws exit
        for exit in exits:
            Total_Display.blit(exit.image, camera.apply(exit)) 
      #Next Level loop
            if pygame.sprite.collide_rect(player, exit):	
                iLevel_count += 1 
                for wall in walls:
                    pygame.sprite.Sprite.kill(wall)
                for bullet in bulletList:
                    pygame.sprite.Sprite.kill(bullet)
                for item in ItemList:
                    pygame.sprite.Sprite.kill(item)
                for shell in shell_List:
                    pygame.sprite.Sprite.kill(shell)
                resetPlayer = True 
                player.Reset(0,0)

                itemdict = BuildLevel(level_List[iLevel_count])

    #draws all_sprit_list to the display, This is why we add sprites to there own list and all_sprites_list
        
        for e in all_Sprite_List:
            Total_Display.blit(e.image, camera.apply(e))

        camera.update(player)
    #Flips dat page bro!
        pygame.display.flip()
Main()