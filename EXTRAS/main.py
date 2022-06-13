import pygame,sys
from pygame.locals import *
import time
import math

def chk_status():
    global status
    if moving_right:
        status="Runf"
    elif moving_left:
        status="Runb"
    elif moving_up:
        status="Jump"
    elif moving_down:
        status="Crouch"
    else:
        status="Idle"
        
def distance(p1,p2):
    d=math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)
    return d

def frame(i):
    global frames
    x=0
    y=450
    while x<=700:
        screen.blit(platform,[x,y])
        x+=32
    load=frames[i]
    for j in load ["platforms"]:
        x,y=j[0],j[1]
        for p in range(0,3):
            screen.blit(thin_plat,[x,y])
            x+=16
    for j in frames[i]["coin"]:
        screen.blit(coin,j)
    pygame.display.flip()  
    mainclock.tick(100)

def shoot():
    bullet_cord=[player_loc[0]+33,player_loc[1]+17]
    screen.blit(flash,bullet_cord)
    screen.blit(stream,bullet_cord)
    screen.blit(bullet_img,bullet_cord)
    bullet.append(bullet_cord)

    
pygame.font.init()
score=0
font = pygame.font.SysFont('Comic Sans MS', 30)
mainclock=pygame.time.Clock()
pygame.init()
WID=700
HEI=600
bullet=[]
screen=pygame.display.set_mode((WID,HEI),0,32)
pygame.display.set_caption("Platformer")
status="Idle"
player=[]
t_f=0
t_up=16
status_l={"Crouch":3,"Runf":6,"Idle":5,"Death":8,"Jump":2,"Runb":6}
platform=pygame.image.load("EXTRAS/Platform.png")
flash=pygame.image.load("EXTRAS/MuzzleFlash.png")
stream=pygame.image.load("EXTRAS/BulletStream.png")
bullet_img=pygame.image.load("EXTRAS/SpongeBullet.png")
thin_plat=pygame.image.load("EXTRAS/Platform_Thin.png")
coin=pygame.image.load("EXTRAS/coin.png")
status="Idle"
frame_no=0
moving_left=False
moving_right=False
moving_up=False
moving_down=False
on_platform=False
player_loc=[300,400]
t_c1=0
f=0
jump_flag=0
HEI=450
bg = pygame.transform.scale(pygame.image.load("skyline-b.png"),(WID,HEI))
vel=[0,0]
g=10
screen.blit(bg, (0,0))
curr_plat=0
frames=[{"platforms":[(267, 328),(534, 379)],"enemies":[],"coin":[(280,312)]}]
fr=0
while True:
    bg = pygame.transform.scale(pygame.image.load("skyline-b.png"),(WID,HEI))
    player=[]
    screen.blit(bg, (0,0))
    for i in range(0,status_l[status]):
        player.append(pygame.image.load("images\{}\Gunner_Black_{}_{}.png".format(status,status,i+1)))
    if fr>len(player)-1:
        fr=0
    screen.blit(player[fr],player_loc)
        
    fr+=1
    t_c=time.perf_counter()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == K_RIGHT:
                vel[0]=+4
                moving_right=True
                status="Runf"
            elif event.key == K_LEFT:
                vel[0]=-4
                moving_left=True
                status="Runb"
            elif event.key==K_DOWN:
                moving_down=True
                status="Crouch"   
            elif event.key==K_SPACE and jump_flag==0:
                under_plat=False
                moving_up=True
                jump_flag=1
                for i in frames[frame_no]["platforms"]:
                    if player_loc[0]>i[0]-25 and player_loc[0]<i[0]+25 and player_loc[1]-50<i[1] and not player_loc[1]<=i[1]:
                        player_loc[1]=i[1]+25
                        under_plat=True
                        print("under plat" )
                        
                if not under_plat:
                    player_loc[1]=player_loc[1]-40
                status="Jump"
                        
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                t_f=0
                vel[0]=0
                moving_right=False
                chk_status()
            elif event.key == K_LEFT:
                t_f=0
                vel[0]=0
                moving_left=False
                chk_status()
            elif event.key==K_DOWN:
                moving_down=False
                chk_status()
            elif event.key==K_SPACE:
                jump_flag=0
                moving_up=False
                chk_status()
                
        if event.type== MOUSEBUTTONDOWN:
            shoot()
            print(pygame.mouse.get_pos())
            
    player_loc[0]=player_loc[0]+vel[0]
    #if t_up<=10:
        #player_loc[1]=player_loc[1]-vel[1]*t_up
    if player_loc[1]<400 and not moving_up and not on_platform:
        player_loc[1]=player_loc[1]+10
    else:
        player_loc[1]==400;
    if player_loc[0]>650:
        player_loc[0]=10
        frame_no+=1
        frame(frame_no)
    if player_loc[0]<=0:
        if frame!=0:
            player_loc[0]=650
            frame_no-=1
        else:
            player_loc[0]=0
            
    remove=[]
    for i in range(len(bullet)):
        bullet[i]=[bullet[i][0]+9,bullet[i][1]]
        screen.blit(bullet_img,bullet[i])
        
        if bullet[i][0]>=650:
            remove.append(i)              
    for i in remove:
        bullet.pop(i)
    
    for i in frames[frame_no]["platforms"]:
        if player_loc[0]>i[0]-25 and player_loc[0]<i[0]+25 and player_loc[1]<i[1]and player_loc[1]>i[1]-35:
            player_loc[1]=i[1]-35
            curr_plat=(i[0],player_loc[1])
            on_platform=True
    try:
        if not (player_loc[0]>curr_plat[0]-25 and player_loc[0]<curr_plat[0]+25 and player_loc[1]<curr_plat[1] and player_loc[1]>curr_plat[1]-10):
            on_platform=False
    except Exception as e:
        pass
    d=[]
    for i in frames[frame_no]["coin"]:
        if distance(i,player_loc)<=18:
            score+=1
        else:
            d.append(i)
    del frames[frame_no]["coin"]
    frames[frame_no]["coin"]=d
    text_score =font.render('SCORE :'+str(score), False, (250, 100, 100))
    screen.blit(text_score,(0,0))
    frame(frame_no) 
    pygame.display.flip()
    mainclock.tick(10)
