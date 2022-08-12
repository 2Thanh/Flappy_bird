#Hello world 
print("Hello world")
from asyncio.windows_utils import pipe
from tkinter import CENTER
import pygame, random
import os
pygame.mixer.pre_init()
pygame.init()
screen=pygame.display.set_mode((432,668))
run=True
clock= pygame.time.Clock()#khoi tao fps
floor_x=0

bg = pygame.image.load (r'C:\Users\vulon\OneDrive\Tài liệu\python\Pygame\plappy bird\FileGame\background-night.png').convert()
floor= pygame.image.load(r'C:\Users\vulon\OneDrive\Tài liệu\python\Pygame\plappy bird\FileGame\assets\floor.png').convert()
bg = pygame.transform.scale(bg, (432, 668))#resize anh
floor = pygame.transform.scale(floor,(450,100))

gravity=0.25
bird_movement=0
bird_up= pygame.image.load(r'C:\Users\vulon\OneDrive\Tài liệu\python\Pygame\plappy bird\FileGame\assets\yellowbird-upflap.png').convert_alpha()
bird_mid= pygame.image.load(r'C:\Users\vulon\OneDrive\Tài liệu\python\Pygame\plappy bird\FileGame\assets\yellowbird-midflap.png').convert_alpha()
bird_down= pygame.image.load(r'C:\Users\vulon\OneDrive\Tài liệu\python\Pygame\plappy bird\FileGame\assets\yellowbird-downflap.png').convert_alpha()
bird_list=[bird_up,bird_mid,bird_down]
bird_index=0
bird= bird_list[bird_index]
bird_rect=bird.get_rect(center=(100,384))#create a hide regtangle around bird has center of bird coddinate is: 100, 384

#Tao score
game_font=pygame.font.Font(None,40)
score=0
hight_score=0
def score_display():
    global hight_score,score
    score_surface= game_font.render('Score '+str(int(score)),True,(255,255,255))
    high_score_surface= game_font.render('High '+str(int(hight_score)),True,(255,255,255))
    if hight_score<score:
        hight_score=score 
    score_rect=score_surface.get_rect(center=(216,40))
    high_score_rect=high_score_surface.get_rect(center=(350,40))
    screen.blit(high_score_surface,high_score_rect)
    screen.blit(score_surface,score_rect)
#xoay chim khi move
def rotate_bird(bird1):
    new_bird=pygame.transform.rotozoom(bird1,-bird_movement*3,1)
    return new_bird
#doi bird va rect khi doi anh
def bird_animation():
    new_bird= bird_list[bird_index]
    new_bird_rect=new_bird.get_rect(center=(100,bird_rect.centery))
    return new_bird, new_bird_rect
#pipe
pipe_surface=pygame.image.load(r'C:\Users\vulon\OneDrive\Tài liệu\python\Pygame\plappy bird\FileGame\assets\pipe-green.png')
pipe_surface=pygame.transform.scale2x(pipe_surface)


# tao time cho bird flap
birdflap=pygame.USEREVENT +1#event 2
pygame.time.set_timer(birdflap,200)

#endgame
begin_surface=pygame.image.load(r'C:\Users\vulon\OneDrive\Tài liệu\python\Pygame\plappy bird\FileGame\assets\message.png')
begin_surface = pygame.transform.scale2x(begin_surface)#resize anh
begin_surface_rect=begin_surface.get_rect(center=(216,334))

#chen am thanh
flap_sound= pygame.mixer.Sound(r'C:\Users\vulon\OneDrive\Tài liệu\python\Pygame\plappy bird\FileGame\sound\sfx_wing.wav')
hit_sound= pygame.mixer.Sound(r'C:\Users\vulon\OneDrive\Tài liệu\python\Pygame\plappy bird\FileGame\sound\sfx_hit.wav')
point_sound= pygame.mixer.Sound(r'C:\Users\vulon\OneDrive\Tài liệu\python\Pygame\plappy bird\FileGame\sound\sfx_point.wav')

#tao thoi gian ra ong tiep theo
pipe_list=[]
spwanpipe= pygame.USEREVENT
pygame.time.set_timer(spwanpipe,1200)# sau moi 1,2s thi in ra
pipe_height=[400,500,450]
def create_pipe():
    pipe_y=random.choice(pipe_height)
    bottom_pipe=pipe_surface.get_rect(midtop=(416,pipe_y))
    top_pipe=pipe_surface.get_rect(midbottom=(416,pipe_y-190))
    return bottom_pipe,top_pipe

def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -=3  # di chuyen cac cai ong sang phai
    return pipes


def draw_pipe(pipes):
    global score
    for pipe in pipes:
        if pipe.y>399:#neu cai ong duoi chay ra
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe=pygame.transform.flip(pipe_surface,False,True)#neu cai ong tren chay ra
            #thi lat nguoc cai ong o tren
            screen.blit(flip_pipe,pipe) 
        if pipe.centerx==104:
             score+=0.5
             point_sound.play()
#xet va cham
game_active=True
def check_collision(pipes):
    global game_active,score
    for pipe in pipes:
        if bird_rect.colliderect(pipe) or (bird_rect.bottom<=-5 or bird_rect.bottom>=648):
            score=0
            game_active=False
            hit_sound.play()
            
def out(bird_rect):
    global bird_movement,gravity
    if bird_rect.centery<668:
        bird_movement+=gravity
        bird_rect.centery +=bird_movement
        screen.blit(rotated_bird,(bird_rect))
    else:
        screen.blit(begin_surface,begin_surface_rect)
        return True

while run:
    clock.tick(120)#120fps

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active==False and out(bird_rect):
                pipe_list.clear()
                bird_rect.center=(100,384)
                bird_movement=0
                game_active=True
            elif event.key == pygame.K_SPACE and game_active==True :
                flap_sound.play()
                bird_movement=-8
        elif event.type == spwanpipe:
            pipe_list.extend(create_pipe())
        elif event.type == birdflap:
            if bird_index<2:
                bird_index+=1
            else:
                bird_index=0
            #thay doi bird va rect
            bird, bird_rect=  bird_animation()
    #tao nen
    screen.blit(bg,(0,0))
    score_display()
    screen.blit(floor,(floor_x,570))
    
    #tao san
    screen.blit(floor,(floor_x+432,570))#tao ra hai san lien tiep
    floor_x-=3
    if floor_x==-432:
        floor_x=0
    
    if game_active:
        check_collision(pipe_list)
        rotated_bird= rotate_bird(bird) #de xoay chim
        #tao ong
        pipe_list=move_pipe(pipe_list)
        draw_pipe(pipe_list)# phai o duoi day thi moi nhin duo
        bird_movement+=gravity
        bird_rect.centery +=bird_movement
        bird_index+=1
        if bird_index==3:
            bird_index=0
        screen.blit(rotated_bird,(bird_rect))
    else:
        out(bird_rect)
   
    #screen.blit(pipe_surface,(pipe_rect))
    
    pygame.display.update()
pygame.quit()
