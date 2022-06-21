import pygame, sys
from pygame.locals import *
import random, time
import minigame1
import minigame2

Hp = 10  # 체력 ( MAX = 10)
Like = 0  # 애정도
Hungry = 6  # 배고픔 ( 0 ~ 10 )  , 0 이면 죽음
feel = 20  # 초기값 =  50
clean = 7  # 초기값 = 10 // 시간에 따라 감소
days = 1  # 날짜
mn = 1  # 밤 = 0 , 낮 = 1
Time = 0  # 3분할로 나누어 행동 3번 하면 밤낮 바뀜
money = 200  # 시작값 = 200 // 차후에 사용

#전역함수
def display_start_screen():     #게임 시작 화면
    screen.blit(background_intro, (0, 0))  # 배경 그리기- 인트로 사진
    # pygame.draw.circle(screen,play_button,start_button.center,60)       # 동그란 버튼 만들기
    screen.blit(play_button,(30,500))

def display_game_screen():
    global character_x_pos, character_y_pos
    if mn==0:
        screen.blit(background_night, (0, 0))  # 배경 그리기
        screen.blit(character, (character_x_pos, character_y_pos))
    elif mn==1:
        screen.blit(background_day, (0, 0))  # 배경 그리기
        screen.blit(character, (character_x_pos, character_y_pos))

def display_mn():
    global character_x_pos, character_y_pos
    if mn == 0:
        screen.blit(background_night, (0, 0))  # 배경 그리기
    elif mn == 1:
        screen.blit(background_day, (0, 0))  # 배경 그리기

def check_buttons(pos):     #버튼 누르면 시작함
    global start
    if start_button.collidepoint(pos):
        start=True

def check_buttons_act(pos):
    if wash_button.collidepoint(pos):
        dama_wash()
        change_time()
    elif eat_button.collidepoint(pos):
        dama_feed()
        change_time()
    elif sleep_button.collidepoint(pos):
        dama_sleep()
        change_time()
    elif clean_button.collidepoint(pos):
        dama_clean()
        change_time()
    elif playing_button.collidepoint(pos):
        game_choose()
    elif store_button.collidepoint(pos):
        go_store()


def go_store():
    global Hp,Hungry,Like,feel,clean,money
    store_run = True
    while store_run:
        click_pos = None
        screen.blit(background_store, (0, 0))  # 배경 그리기
        pygame.display.update()
        for event in pygame.event.get():  # 어떤 이벤트가 발생하였는가
            if event.type == pygame.QUIT:  # 창이 닫히는 이벤트가 발생하면
                run = False  # 게임 종료
            elif event.type == pygame.MOUSEBUTTONUP:
                click_pos = pygame.mouse.get_pos()
                print(click_pos)
                if (money >= 200):
                    if Likema_button.collidepoint(click_pos):
                        character = pygame.image.load("daram_ma.png")
                        screen.blit(character, (character_x_pos, character_y_pos))
                        pygame.display.update()
                        Like += 5
                        money -= 200
                if (money >= 100):
                    if Hungryma_button.collidepoint(click_pos):
                        character = pygame.image.load("daram_ma.png")
                        screen.blit(character, (character_x_pos, character_y_pos))
                        pygame.display.update()
                        Hungry += 1
                        money -= 100
                    elif Hpma_button.collidepoint(click_pos):
                        character = pygame.image.load("daram_ma.png")
                        screen.blit(character, (character_x_pos, character_y_pos))
                        pygame.display.update()
                        Hp += 1
                        money -= 100
                    elif cleanma_button.collidepoint(click_pos):
                        character = pygame.image.load("daram_ma.png")
                        screen.blit(character, (character_x_pos, character_y_pos))
                        pygame.display.update()
                        clean += 1
                        money -= 100
                    elif feelma_button.collidepoint(click_pos):
                        character = pygame.image.load("daram_ma.png")
                        screen.blit(character, (character_x_pos, character_y_pos))
                        pygame.display.update()
                        feel += 3
                        money -= 100
                if (money >= 1000):
                    if man_button.collidepoint(click_pos):
                        character = pygame.image.load("daram_ma.png")
                        screen.blit(character, (character_x_pos, character_y_pos))
                        pygame.display.update()
                        feel += 10
                        clean=10
                        Hungry=10
                        Hp=10
                        Like=10
                        money -= 1000


                store_run=False
                time.sleep(3)

def game_choose():
    global Hp, Hungry,clean, feel, Like, Time,money
    screen.blit(background_choose,(0,0))
    time.sleep(1)
    minigame_playing=True
    while minigame_playing:
        click_pos=None
        pygame.display.update()
        for event in pygame.event.get():  # 어떤 이벤트가 발생하였는가
            if event.type == pygame.QUIT:  # 창이 닫히는 이벤트가 발생하면
                run = False  # 게임 종료
            elif event.type == pygame.MOUSEBUTTONUP:
                click_pos = pygame.mouse.get_pos()
                print(click_pos)
                if wash_button.collidepoint(click_pos):
                    #bgm.stop()
                    minigame1.mini()
                    #bgm.play()
                elif playing_button.collidepoint(click_pos):
                    #bgm.stop()
                    minigame2.mini()
                    #bgm.play()

                if Hp - 2 >= 0:
                    Hp -= 2
                elif Hp - 2 < 0:
                    Hp = 0

                feel += 2

                if Hungry - 2 >= 0:
                    Hungry -= 2
                elif Hungry - 2 < 0:
                    Hungry = 0

                if clean - 1 >= 0:
                    clean -= 1
                elif clean - 1 < 0:
                    clean = 0
                Like += 4
                Time += 1
                money+=10

                die_daram()

                # display_game_screen()
                # pygame.display.update()
                minigame_playing = False

# 기본적인 기능 구현 함수
def dama_wash(): # 씻기기
    global Hp, feel, Hungry, clean, Time,Like
    global character
    screen.blit(background_bath,(0,0))

    for i in range(1,3):
        character = pygame.image.load("C:/Users/admin/PycharmProjects/openswproject/daram_condition/daram_washing.png")
        screen.blit(character, (200, character_y_pos))
        pygame.display.update()
        time.sleep(1)
        screen.blit(background_bath,(0,0))

        character = pygame.image.load("C:/Users/admin/PycharmProjects/openswproject/daram_condition/washing_daram_left.png")
        screen.blit(character, (200, character_y_pos))
        pygame.display.update()
        time.sleep(1)
        screen.blit(background_bath,(0,0))

    character=pygame.image.load("C:/Users/admin/PycharmProjects/openswproject/daram_clear.png")
    if Hp - 1 >= 0:
        Hp -= 1
    elif Hp - 1 < 0:
        Hp = 0

    feel += 2

    if Hungry - 1 >= 0:
        Hungry -= 1
    elif Hungry - 1 < 0:
        Hungry = 0

    if clean + 2 <= 10:
        clean += 2
    elif clean + 2 > 10:
        clean = 10
    Like += 3
    Time += 1
    daram_update()
    die_daram()


def dama_feed():  # 밥 먹이기
    global Hp, Like, Time, Hungry,Like,character, clean
    screen.blit(background_eat, (0, 0))
    pygame.display.update()
    for i in range (1,4):
        character = pygame.image.load("C:/Users/admin/PycharmProjects/openswproject/daram_condition/다람먹는중%d.png" %i)
        screen.blit(character, (character_x_pos, character_y_pos))
        pygame.display.update()
        time.sleep(1)
        screen.blit(background_eat, (0, 0))
    if Hp + 3 <= 10:
        Hp += 3
    elif Hp + 3 > 10:
        Hp = 10

    if Hungry + 3 <= 10:
        Hungry += 3
    elif Hungry + 3 > 10:
        Hungry = 10

    if clean - 2 >= 0:
        clean -= 2
    elif clean - 2 < 0:
        clean = 0

    Like += 5
    Time += 1
    daram_update()
    die_daram()
    return Hp


def dama_sleep(): # 잠 자기
    global Time, Hp, Hungry, Like,clean,character
    screen.blit(background_sleep, (0, 0))
    for i in range (1,3):
        for a in range(1, 4):
            character = pygame.image.load("C:/Users/admin/PycharmProjects/openswproject/zzz%d_daram.png" % a)
            screen.blit(character, (200, 100))
            pygame.display.update()
            time.sleep(1)
            screen.blit(background_sleep, (0, 0))
    if Hp + 3 <= 10:
        Hp += 3
    elif Hp + 3 > 10:
        Hp = 10

    if Hungry - 3 >= 0:
        Hungry -= 3
    elif Hungry - 3 < 0:
        Hungry = 0

    if clean - 2 >= 0:
        clean -= 2
    elif clean - 2 < 0:
        clean = 0

    Like += 2

    Time = 3
    daram_update()
    die_daram()



def dama_clean():  # 청소하기
    global Hp, clean, Time, Like, character
    screen.blit(background_basic, (0,0))
    pygame.display.update()
    for i in range (1,9):
        character = pygame.image.load("C:/Users/admin/PycharmProjects/openswproject/daram_condition/청소 중%d.png" %i)
        screen.blit(character, (character_x_pos, character_y_pos))
        pygame.display.update()
        time.sleep(0.5)
        screen.blit(background_basic, (0, 0))


    if Hp - 2 >= 0:
        Hp -= 2
    elif Hp - 2 < 0:
        Hp = 0

    if clean + 3 <= 10:
        clean += 3
    elif clean + 3 > 10:
        clean = 10

    Like += 3

    Time += 1
    daram_update()
    die_daram()


def change_time():  # 일정 시간이 지나면 or 행동을 하면 time 변수가 증가 ( 0 ~ 6을 12시간으로 변화 )
    global Time, mn, days, Hp, Like, Hungry, feel, clean, run
    #a = random.randint(-1, 0)
    #b = random.randint(-1, 0)
    #c = random.randint(-1, 0)
    #d = random.randint(-1, 0)
    #e = random.randint(-1, 0)
    #Hp += a
    #Like += b
    #Hungry += c
    #feel += d
    #clean += e

    if (Time == 3) and (mn == 1): # 활동 3번 후 시간이 낮이면
        mn = 0  # 밤으로 바꿈
        Time = 0

    if (Time == 3) and (mn == 0): # 활동 3번 후 시간이 밤이면 or sleep 함수 실행 시
        mn = 1  # 낮으로 바꿈
        days += 1
        Time = 0

    die_daram()

    if Hungry == 0:
        Hp = Hp - 5
    if clean == 0:
        Hp = Hp - 5

def die_daram():
    global Hp, run_1
    if(Hp < 0):
        run_1 = False



def display_txt():
    # 폰트 객체 생성 (폰트,크기)
    game_font = pygame.font.Font(None, 40)
    # 출력할 글자, TRUE, 글자 색상
    txt_Hp = game_font.render(f"HP : {Hp}", True, (0, 0, 0))
    txt_Like = game_font.render(f"Like : {Like}", True, (0, 0, 0))
    txt_Hungry = game_font.render(f"Hungry : {Hungry}", True, (0, 0, 0))
    txt_feel = game_font.render(f"Feel : {feel}", True, (0, 0, 0))
    txt_clean = game_font.render(f"Clean : {clean}", True, (0, 0, 0))
    txt_days = game_font.render(f"Day : {days}", True, (0, 0, 0))
    txt_time = game_font.render(f"Time : {Time}", True, (0, 0, 0))
    txt_money = game_font.render(f"Money : {money}", True, (0, 0, 0))
    # 좌표에 글씨출력
    screen.blit(txt_Hp, (20, 440))
    screen.blit(txt_Like, (20, 470))
    screen.blit(txt_feel, (20, 500))
    screen.blit(txt_Hungry, (20,530))
    screen.blit(txt_clean, (20, 560))
    screen.blit(txt_days, (700, 500))
    screen.blit(txt_time, (700, 530))
    screen.blit(txt_money, (700, 560))

def daram_update():
    global clean, Hungry, Hp, feel, character
    die_daram()
    if 3 <= Hp < 6 and 6 <= clean < 9:  # 1아픔 1깨끗함
        character = pygame.image.load('C:/Users/admin/PycharmProjects/openswproject/daram_condition/1아픔_1깨끗함.png')
        return character
    if 3 <= Hp < 6 and clean >= 9:  # 1아픔 2깨끗함
        character = pygame.image.load('C:/Users/admin/PycharmProjects/openswproject/daram_condition/1아픔_2깨끗함.png')
        return character
    if 3 <= Hp < 6 and 3 <= clean < 6:  # 1아픔 1더러움
        character = pygame.image.load('C:/Users/admin/PycharmProjects/openswproject/daram_condition/1아픔_1더러움.png')
        return character
    if 3 <= Hp < 6 and clean <= 2:  # 1아픔 2더러움
        character = pygame.image.load('C:/Users/admin/PycharmProjects/openswproject/daram_condition/1아픔_1더러움.png')
        return character

    if Hp < 3 and 6 <= clean < 9:  # 2아픔 1깨끗함
        character = pygame.image.load('C:/Users/admin/PycharmProjects/openswproject/daram_condition/2아픔_1깨끗함.png')
        return character
    if Hp < 3 and clean >= 9:  # 2아픔 2깨끗함
        character = pygame.image.load('C:/Users/admin/PycharmProjects/openswproject/daram_condition/2아픔_2깨끗함.png')
        return character
    if Hp < 3 and  3 <= clean < 6:  # 2아픔 1더러움
        character = pygame.image.load('C:/Users/admin/PycharmProjects/openswproject/daram_condition/2아픔_1더러움.png')
        return character
    if Hp < 3 and clean <= 2:  # 2아픔 2더러움
        character = pygame.image.load('C:/Users/admin/PycharmProjects/openswproject/daram_condition/2아픔_2더러움.png')
        return character

    if 3 <= Hungry < 6 and 6 <= clean < 9:  # 1배고픔 1깨끗함
        character = pygame.image.load('C:/Users/admin/PycharmProjects/openswproject/daram_condition/1배고픔_1깨끗함.png')
        return character
    if 3 <= Hungry < 6 and clean >= 9:  # 1배고픔 2깨끗함
        character = pygame.image.load('C:/Users/admin/PycharmProjects/openswproject/daram_condition/1배고픔_2깨끗함.png')
        return character
    if 3 <= Hungry < 6 and 3 <= clean < 6:  # 1배고픔 1더러움
        character = pygame.image.load('C:/Users/admin/PycharmProjects/openswproject/daram_condition/1배고픔_1더러움.png')
        return character
    if 3 <= Hungry < 6 and clean <= 2:  # 1배고픔 2더러움
        character = pygame.image.load('C:/Users/admin/PycharmProjects/openswproject/daram_condition/1배고픔_2더러움.png')
        return character

    if Hungry <= 2 and 6 <= clean < 9:  # 2배고픔 1깨끗함
        character = pygame.image.load('C:/Users/admin/PycharmProjects/openswproject/daram_condition/2배고픔_1깨끗함.png')
        return character
    if Hungry <= 2 and clean >= 9:  # 2배고픔 2깨끗함
        character = pygame.image.load('C:/Users/admin/PycharmProjects/openswproject/daram_condition/2배고픔_2깨끗함.png')
        return character
    if Hungry <= 2 and 3 <= clean < 6:  # 2배고픔 1더러움
        character = pygame.image.load('C:/Users/admin/PycharmProjects/openswproject/daram_condition/2배고픔_1더러움.png')
        return character
    if Hungry <= 2 and clean <= 2:  # 2배고픔 2더러움
        character = pygame.image.load('C:/Users/admin/PycharmProjects/openswproject/daram_condition/2배고픔_2더러움.png')
        return character

    if Hungry >= 6 and Hp >= 6 and clean >= 9: # 기본 상태 2깨끗함
        character = pygame.image.load('C:/Users/admin/PycharmProjects/openswproject/daram_condition/기본상태_2깨끗함.png')
        return character
    if Hungry >= 6 and Hp >= 6 and 6 <= clean < 9:  # 기본 상태 1깨끗함
        character = pygame.image.load('C:/Users/admin/PycharmProjects/openswproject/daram_condition/기본상태_1깨끗함.png')
        return character
    if Hungry >= 6 and Hp >= 6 and 3 <= clean < 6:  # 기본 상태 1더러움
        character = pygame.image.load('C:/Users/admin/PycharmProjects/openswproject/daram_condition/기본상태_1더러움.png')
        return character
    if Hungry >= 6 and Hp >= 6 and clean <= 2:  # 기본 상태 2더러움
        character = pygame.image.load('C:/Users/admin/PycharmProjects/openswproject/daram_condition/기본상태_2더러움.png')
        return character

def daram_update_right():
    global clean, Hungry, Hp, feel, character
    die_daram()
    if 3 <= Hp < 6 and 6 <= clean < 9:  # 1아픔 1깨끗함
        character = pygame.image.load('C:/Users/admin/PycharmProjects/openswproject/daram_condition/1아픔_1깨끗함_반전.png')
        return character
    if 3 <= Hp < 6 and clean >= 9:  # 1아픔 2깨끗함
        character = pygame.image.load('C:/Users/admin/PycharmProjects/openswproject/daram_condition/1아픔_2깨끗함_반전.png')
        return character
    if 3 <= Hp < 6 and 3 <= clean < 6:  # 1아픔 1더러움
        character = pygame.image.load('C:/Users/admin/PycharmProjects/openswproject/daram_condition/1아픔_1더러움_반전.png')
        return character
    if 3 <= Hp < 6 and clean <= 2:  # 1아픔 2더러움
        character = pygame.image.load('C:/Users/admin/PycharmProjects/openswproject/daram_condition/1아픔_1더러움_반전.png')
        return character

    if Hp < 3 and 6 <= clean < 9:  # 2아픔 1깨끗함
        character = pygame.image.load('C:/Users/admin/PycharmProjects/openswproject/daram_condition/2아픔_1깨끗함_반전.png')
        return character
    if Hp < 3 and clean >= 9:  # 2아픔 2깨끗함
        character = pygame.image.load('C:/Users/admin/PycharmProjects/openswproject/daram_condition/2아픔_2깨끗함_반전.png')
        return character
    if Hp < 3 and  3 <= clean < 6:  # 2아픔 1더러움
        character = pygame.image.load('C:/Users/admin/PycharmProjects/openswproject/daram_condition/2아픔_1더러움_반전.png')
        return character
    if Hp < 3 and clean <= 2:  # 2아픔 2더러움
        character = pygame.image.load('C:/Users/admin/PycharmProjects/openswproject/daram_condition/2아픔_2더러움_반전.png')
        return character

    if 3 <= Hungry < 6 and 6 <= clean < 9:  # 1배고픔 1깨끗함
        character = pygame.image.load('C:/Users/admin/PycharmProjects/openswproject/daram_condition/1배고픔_1깨끗함_반전.png')
        return character
    if 3 <= Hungry < 6 and clean >= 9:  # 1배고픔 2깨끗함
        character = pygame.image.load('C:/Users/admin/PycharmProjects/openswproject/daram_condition/1배고픔_2깨끗함_반전.png')
        return character
    if 3 <= Hungry < 6 and 3 <= clean < 6:  # 1배고픔 1더러움
        character = pygame.image.load('C:/Users/admin/PycharmProjects/openswproject/daram_condition/1배고픔_1더러움_반전.png')
        return character
    if 3 <= Hungry < 6 and clean <= 2:  # 1배고픔 2더러움
        character = pygame.image.load('C:/Users/admin/PycharmProjects/openswproject/daram_condition/1배고픔_2더러움_반전.png')
        return character

    if Hungry <= 2 and 6 <= clean < 9:  # 2배고픔 1깨끗함
        character = pygame.image.load('C:/Users/admin/PycharmProjects/openswproject/daram_condition/2배고픔_1깨끗함_반전.png')
        return character
    if Hungry <= 2 and clean >= 9:  # 2배고픔 2깨끗함
        character = pygame.image.load('C:/Users/admin/PycharmProjects/openswproject/daram_condition/2배고픔_2깨끗함_반전.png')
        return character
    if Hungry <= 2 and 3 <= clean < 6:  # 2배고픔 1더러움
        character = pygame.image.load('C:/Users/admin/PycharmProjects/openswproject/daram_condition/2배고픔_1더러움_반전.png')
        return character
    if Hungry <= 2 and clean <= 2:  # 2배고픔 2더러움
        character = pygame.image.load('C:/Users/admin/PycharmProjects/openswproject/daram_condition/2배고픔_2더러움_반전.png')
        return character

    if Hungry >= 6 and Hp >= 6 and clean >= 9: # 기본 상태 2깨끗함
        character = pygame.image.load('C:/Users/admin/PycharmProjects/openswproject/daram_condition/기본상태_2깨끗함_반전.png')
        return character
    if Hungry >= 6 and Hp >= 6 and 6 <= clean < 9:  # 기본 상태 1깨끗함
        character = pygame.image.load('C:/Users/admin/PycharmProjects/openswproject/daram_condition/기본상태_1깨끗함_반전.png')
        return character
    if Hungry >= 6 and Hp >= 6 and 3 <= clean < 6:  # 기본 상태 1더러움
        character = pygame.image.load('C:/Users/admin/PycharmProjects/openswproject/daram_condition/기본상태_1더러움_반전.png')
        return character
    if Hungry >= 6 and Hp >= 6 and clean <= 2:  # 기본 상태 2더러움
        character = pygame.image.load('C:/Users/admin/PycharmProjects/openswproject/daram_condition/기본상태_2더러움_반전.png')
        return character


#초기화
pygame.init()
screen = pygame.display.set_mode((900, 600))

#화면 타이틀 설정
pygame.display.set_caption("다마고치 게임")

#fps
clock=pygame.time.Clock()

#배경이미지 불러오기
background_intro=pygame.image.load("C:/Users/admin/PycharmProjects/openswproject/background_intro.png")
background_day=pygame.image.load("C:/Users/admin/PycharmProjects/openswproject/background_day.png")
background_night=pygame.image.load("C:/Users/admin/PycharmProjects/openswproject/background_night.png")
background_choose=pygame.image.load("C:/Users/admin/PycharmProjects/openswproject/background_choose.png")
background_gameover=pygame.image.load("C:/Users/admin/PycharmProjects/openswproject/background_gameover.png")
play_button=pygame.image.load("C:/Users/admin/PycharmProjects/openswproject/play_button.png")
background_basic=pygame.image.load("C:/Users/admin/PycharmProjects/openswproject/background_basic.png")
background_store=pygame.image.load("C:/Users/admin/PycharmProjects/openswproject/background_store.png")
background_bath=pygame.image.load("C:/Users/admin/PycharmProjects/openswproject/background_bath.png")
background_eat=pygame.image.load("C:/Users/admin/PycharmProjects/openswproject/background_eat.png")
background_sleep=pygame.image.load("C:/Users/admin/PycharmProjects/openswproject/background_sleep.png")

#시작버튼
start_button=pygame.Rect(0,0,120,120)
start_button.center=(120,600-120)

#내부 기능 버튼
wash_button=pygame.Rect(0,0,180,120)
eat_button=pygame.Rect(180,0,180,120)
sleep_button=pygame.Rect(360,0,180,120)
clean_button=pygame.Rect(540,0,180,120)
playing_button=pygame.Rect(720,0,180,120)
store_button=pygame.Rect(360,480,180,120)

Likema_button=pygame.Rect(0,0,180,120)
Hungryma_button=pygame.Rect(180,0,180,120)
cleanma_button=pygame.Rect(360,0,180,120)
feelma_button=pygame.Rect(540,0,180,120)
Hpma_button=pygame.Rect(720,0,180,120)
man_button=pygame.Rect(360,480,180,120)

mini1_button=pygame.Rect(0,0,300,200)
mini2_button=pygame.Rect(720,0,300,200)

#mini1_button=pygame.Rect()
#mini2_button=pygame.Rect()

#색깔
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

#게임 시작 여부
start=False
game=False
run_1=True

#캐릭터 불러오기
character=pygame.image.load("C:/Users/admin/PycharmProjects/openswproject/daram_left.png")
character_size=character.get_rect().size        #이미지 크기 구해옴
character_width=character_size[0]       #캐릭터 가로 크기
character_height=character_size[1]      #캐릭터 세로 크기
character_x_pos=900/2       #가로의 반정도 되는 지점에 위치
character_y_pos=600/3       #세로의 반정도 되는 지점에 위치

#이동할 좌표
to_x=0
to_y=0

#bgm
bgm = pygame.mixer.Sound('bgm_dama.mp3')
bgm.play() # 게임 BGM 재생

change_background=False
#이동 속도
character_speed=0.6

#이벤트 루프
run = True  #게임이 진행중인가
while run:
    dt=clock.tick(10)       #게임 화면의 초당 프레임
    click_pos=None
    for event in pygame.event.get():    #어떤 이벤트가 발생하였는가
        if event.type == pygame.QUIT:       #창이 닫히는 이벤트가 발생하면
            run = False     #게임 종료
        elif event.type==pygame.MOUSEBUTTONUP:
            click_pos=pygame.mouse.get_pos()
            print(click_pos)

        if event.type==pygame.KEYDOWN: #방향 키를 누르면 이동
            if event.key==pygame.K_LEFT:
                character = daram_update()
                to_x-=character_speed
            elif event.key==pygame.K_RIGHT:
                character = daram_update_right()
                to_x+=character_speed

        if event.type==pygame.KEYUP:        #방향 키에서 떼면 이동
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                to_x=0

    character_x_pos+=to_x*dt

    #가로 경계값 처리
    if character_x_pos<0:
        character_x_pos=0
    elif character_x_pos>900-character_width:
        character_x_pos=900-character_width

    #게임 시작 버튼 누르면
    if start:
        display_game_screen()
        screen.blit(character,(character_x_pos,character_y_pos)) #캐릭터 그리기
    else:
        display_start_screen()

    if click_pos and start == False:
        check_buttons(click_pos)

    if click_pos and start == True:
        check_buttons_act(click_pos)

    if game == False and start==True :
        display_txt()

    pygame.display.update()  # 게임 화면을 다시 그리기

    if(run_1==False):
        screen.blit(background_gameover, (0, 0))
        time.sleep(1)
        pygame.display.update()
        time.sleep(5)
        pygame.quit()
        sys.exit()


pygame.quit()
sys.exit()
