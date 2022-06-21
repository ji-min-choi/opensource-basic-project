
import random, time, pygame, sys, copy
from pygame.locals import *


FPS = 30 # 프레임 수
WINDOWWIDTH = 900  # 윈도우 넓이
WINDOWHEIGHT = 600 # 윈도우 높이

BOARDWIDTH = 8 # 열 수
BOARDHEIGHT = 8 # 줄 수
GEMIMAGESIZE = 64 # 보석 이미지 사이즈



# 색상         R    G    B
PURPLE    = (255,   0, 255)
LIGHTBLUE = (170, 190, 255)
BLUE      = (  0,   0, 255)
RED       = (255, 100, 100)
BLACK     = (  0,   0,   0)
BROWN     = ( 85,  65,   0)
HIGHLIGHTCOLOR = PURPLE # 선택 보석 색상
BGCOLOR = LIGHTBLUE # 배경색
GRIDCOLOR = BLUE # 게임 보드 색상
GAMEOVERCOLOR = RED # 게임 오버 색상
GAMEOVERBGCOLOR = BLACK # 게임 오버 배경색
SCORECOLOR = BROWN # 점수 색상

# 수평, 수직 여백
XMARGIN = int((WINDOWWIDTH - GEMIMAGESIZE * BOARDWIDTH) / 2)
YMARGIN = int((WINDOWHEIGHT - GEMIMAGESIZE * BOARDHEIGHT) / 2)

# 이미지 파일 수
NUMGEMIMAGES = 7

# 보석 이동 속도
MOVERATE = 25
# 점수 차감 속도
DEDUCTSPEED = 0.8

# 방향 변수
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'


EMPTY_SPACE = -1 # 빈 공간 값
ROWABOVEBOARD = 'row above board' # 임의의 문자열

def mini():
    global FPSCLOCK, DISPLAYSURF, GEMIMAGES, BASICFONT, BOARDRECTS

    # 초기 셋업
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('선유 맞추기')
    BASICFONT = pygame.font.Font('freesansbold.ttf', 36)

    # 이미지 로딩
    GEMIMAGES = []
    for i in range(1, NUMGEMIMAGES + 1):
        gemImage = pygame.image.load('C:/Users/admin/PycharmProjects/선유%s.jpg' % i)
        if gemImage.get_size() != (GEMIMAGESIZE, GEMIMAGESIZE):
            gemImage = pygame.transform.smoothscale(gemImage, (GEMIMAGESIZE, GEMIMAGESIZE))
        GEMIMAGES.append(gemImage)

    # 보드 사각형 생성
    BOARDRECTS = []
    for x in range(BOARDWIDTH):
        BOARDRECTS.append([])
        for y in range(BOARDHEIGHT):
            r = pygame.Rect((XMARGIN + (x * GEMIMAGESIZE),
                             YMARGIN + (y * GEMIMAGESIZE),
                             GEMIMAGESIZE,
                             GEMIMAGESIZE))
            BOARDRECTS[x].append(r)

    while True:
        runGame()
        break


def runGame():

    gameBoard = getBlankBoard()
    score = 0
    fillBoardAndAnimate(gameBoard, [], score) # 첫번째 보석 드랍

    # 새 게임 설정
    firstSelectedGem = None
    lastMouseDownX = None
    lastMouseDownY = None
    gameIsOver = False
    gameIsClear = False
    clickContinueTextSurf = None

    while True : # 메인 게임 루프
        clickedSpace = None
        for event in pygame.event.get(): # 이벤트 핸들링 루프
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP and event.key == K_BACKSPACE:
                return # 백스페이스를 누르면 게임 초기화

            elif event.type == MOUSEBUTTONUP:
                if gameIsOver:
                    return # 게임 오버시 마우스 클릭
                if gameIsClear:
                    return # 게임 클리어 시 마우스 클릭

                if event.pos == (lastMouseDownX, lastMouseDownY):
                    # 마우스 클릭시
                    clickedSpace = checkForGemClick(event.pos) # 보석 클릭 확인
                else:
                    # 마우스 드래그
                    firstSelectedGem = checkForGemClick((lastMouseDownX, lastMouseDownY))
                    clickedSpace = checkForGemClick(event.pos)
                    if not firstSelectedGem or not clickedSpace:
                        # 정당한 드래그가 아닐시 무시
                        firstSelectedGem = None
                        clickedSpace = None
            elif event.type == MOUSEBUTTONDOWN:
                # 마우스 클릭 과 드래그 시작
                lastMouseDownX, lastMouseDownY = event.pos

        if clickedSpace and not firstSelectedGem:
            # 첫번째 클릭인 경우
            firstSelectedGem = clickedSpace
        elif clickedSpace and firstSelectedGem:
            # 두개의 보석이 클릭된 경우 서로 바꾸기
            firstSwappingGem, secondSwappingGem = getSwappingGems(gameBoard, firstSelectedGem, clickedSpace)
            if firstSwappingGem == None and secondSwappingGem == None:
                # 인접한 보석이 아닌 경우
                firstSelectedGem = None # 첫번째 보석 해제
                continue

            # 바꾸기 애니메이션
            boardCopy = getBoardCopyMinusGems(gameBoard, (firstSwappingGem, secondSwappingGem))
            animateMovingGems(boardCopy, [firstSwappingGem, secondSwappingGem], [], score)

            # 보드 데이터 에서 바꾸기
            gameBoard[firstSwappingGem['x']][firstSwappingGem['y']] = secondSwappingGem['imageNum']
            gameBoard[secondSwappingGem['x']][secondSwappingGem['y']] = firstSwappingGem['imageNum']


            # 올바른 바꾸기 인지 체크
            matchedGems = findMatchingGems(gameBoard)
            if matchedGems == []:
                # 올바른 바꾸기가 아닌 경우 되돌림
                #GAMESOUNDS['bad swap'].play() # 매칭 불가 사운드 재생
                animateMovingGems(boardCopy, [firstSwappingGem, secondSwappingGem], [], score)
                gameBoard[firstSwappingGem['x']][firstSwappingGem['y']] = firstSwappingGem['imageNum']
                gameBoard[secondSwappingGem['x']][secondSwappingGem['y']] = secondSwappingGem['imageNum']
            else:
                # 올바른 바꾸기 인 경우
                scoreAdd = 0
                while matchedGems != []:
                    # 퍼즐이 완성된 보석을 없애고 한줄 내림


                    points = []
                    for gemSet in matchedGems:
                        scoreAdd += (10 + (len(gemSet) - 3) * 10)
                        for gem in gemSet:
                            gameBoard[gem[0]][gem[1]] = EMPTY_SPACE
                        points.append({'points': scoreAdd,
                                       'x': gem[0] * GEMIMAGESIZE + XMARGIN,
                                       'y': gem[1] * GEMIMAGESIZE + YMARGIN})
                       # random.choice(GAMESOUNDS['match']).play() # 매칭 사운드 재생

                    score += scoreAdd  # 점수 더하기

                    # 새로운 보석 채우기
                    fillBoardAndAnimate(gameBoard, points, score)

                    # 완성된 퍼즐 체크
                    matchedGems = findMatchingGems(gameBoard)
            firstSelectedGem = None

            if not canMakeMove(gameBoard):
                gameIsOver = True

            if score > 20:
                gameIsClear = True



        # 보드 그리기
        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(gameBoard)
        if firstSelectedGem != None:
            highlightSpace(firstSelectedGem['x'], firstSelectedGem['y'])

        if gameIsOver:
            # 게임 오버
            if clickContinueTextSurf == None:
                clickContinueTextSurf = BASICFONT.render('Final Score: %s (Click to continue)' % (score), 1, GAMEOVERCOLOR, GAMEOVERBGCOLOR)
                clickContinueTextRect = clickContinueTextSurf.get_rect()
                clickContinueTextRect.center = int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2)
            DISPLAYSURF.blit(clickContinueTextSurf, clickContinueTextRect)

        if gameIsClear:
            # 게임 클리어
            drawBoard(getBlankBoard())
            if clickContinueTextSurf == None:
                clickContinueTextSurf = BASICFONT.render('GAME CLEAR !!' ,GAMEOVERBGCOLOR, GAMEOVERBGCOLOR)
                clickContinueTextRect = clickContinueTextSurf.get_rect()
                clickContinueTextRect.center = int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2)
            DISPLAYSURF.blit(clickContinueTextSurf, clickContinueTextRect)


        elif score >= 0:
            drawScore(score)


        pygame.display.update()
        FPSCLOCK.tick(FPS)




def getBlankBoard():
    # 빈 보드 반환
    board = []
    for x in range(BOARDWIDTH):
        board.append([EMPTY_SPACE] * BOARDHEIGHT)
    return board


def drawBoard(board):
    # 보드 그리기
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            pygame.draw.rect(DISPLAYSURF, GRIDCOLOR, BOARDRECTS[x][y], 1)
            gemToDraw = board[x][y]
            if gemToDraw != EMPTY_SPACE:
                DISPLAYSURF.blit(GEMIMAGES[gemToDraw], BOARDRECTS[x][y])

def fillBoardAndAnimate(board, points, score):
    # 첫번째 보석 그리고 이동
    dropSlots = getDropSlots(board)
    while dropSlots != [[]] * BOARDWIDTH:
        # 떨어뜨릴 보석이 있는 경우
        movingGems = getDroppingGems(board)
        for x in range(len(dropSlots)):
            if len(dropSlots[x]) != 0:
                # 가장 아랫쪽 보석 하강
                movingGems.append({'imageNum': dropSlots[x][0], 'x': x, 'y': ROWABOVEBOARD, 'direction': DOWN})

        boardCopy = getBoardCopyMinusGems(board, movingGems)
        animateMovingGems(boardCopy, movingGems, points, score)
        moveGems(board, movingGems)

        # 이전 마지막 보석 제거
        for x in range(len(dropSlots)):
            if len(dropSlots[x]) == 0:
                continue
            board[x][0] = dropSlots[x][0]
            del dropSlots[x][0]

def getDropSlots(board):
    # 보석이 떨어질 슬롯 반환
    boardCopy = copy.deepcopy(board)
    pullDownAllGems(boardCopy)

    dropSlots = []
    for i in range(BOARDWIDTH):
        dropSlots.append([])

    # 텅빈 공간 카운트
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT -1, -1, -1): # 바닥부터 위로 올라가기
            if boardCopy[x][y] == EMPTY_SPACE:
                possibleGems = list(range(len(GEMIMAGES)))
                for offsetX, offsetY in ((0, -1), (1, 0), (0, 1), (-1, 0)):
                    # 보석 겹침 제거
                    neighborGem = getGemAt(boardCopy, x + offsetX, y + offsetY)
                    if neighborGem != None and neighborGem in possibleGems:
                        possibleGems.remove(neighborGem)

                newGem = random.choice(possibleGems)
                boardCopy[x][y] = newGem
                dropSlots[x].append(newGem)
    return dropSlots

def getGemAt(board, x, y):
    # 보석 위치 반환
    if x < 0 or y < 0 or x >= BOARDWIDTH or y >= BOARDHEIGHT:
        return None
    else:
        return board[x][y]

def getDroppingGems(board):
    # 아랫쪽 공간이 비어있는 모든 보석 탐색
    boardCopy = copy.deepcopy(board)
    droppingGems = []
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT - 2, -1, -1):
            if boardCopy[x][y + 1] == EMPTY_SPACE and boardCopy[x][y] != EMPTY_SPACE:
                # 비어있지 않으면 드랍
                droppingGems.append( {'imageNum': boardCopy[x][y], 'x': x, 'y': y, 'direction': DOWN} )
                boardCopy[x][y] = EMPTY_SPACE
    return droppingGems


def getBoardCopyMinusGems(board, gems):
    # 보드 데이터 구조 반환

    boardCopy = copy.deepcopy(board)

    # 보석 제거
    for gem in gems:
        if gem['y'] != ROWABOVEBOARD:
            boardCopy[gem['x']][gem['y']] = EMPTY_SPACE
    return boardCopy

def animateMovingGems(board, gems, pointsText, score):
    # 움직이는 보석 애니메이션
    progress = 0 # 0이 시작, 100이 마지막
    while progress < 100: # 애니메이션 루프
        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(board)
        for gem in gems: # 각각의 보석 그리기
            drawMovingGem(gem, progress)

        for pointText in pointsText:
            pointsSurf = BASICFONT.render(str(pointText['points']), 1, SCORECOLOR)
            pointsRect = pointsSurf.get_rect()
            pointsRect.center = (pointText['x'], pointText['y'])
            DISPLAYSURF.blit(pointsSurf, pointsRect)

        pygame.display.update()
        FPSCLOCK.tick(FPS)
        progress += MOVERATE # 애니메이션 시간 추가

def moveGems(board, movingGems):
    # 보석 이동 딕셔너리
    for gem in movingGems:
        if gem['y'] != ROWABOVEBOARD:
            board[gem['x']][gem['y']] = EMPTY_SPACE
            movex = 0
            movey = 0
            if gem['direction'] == LEFT:
                movex = -1
            elif gem['direction'] == RIGHT:
                movex = 1
            elif gem['direction'] == DOWN:
                movey = 1
            elif gem['direction'] == UP:
                movey = -1
            board[gem['x'] + movex][gem['y'] + movey] = gem['imageNum']
        else:
            # 새로운 보석 준비
            board[gem['x']][0] = gem['imageNum'] # 첫 줄로 이동



def drawMovingGem(gem, progress):
    # 움직이는 보석 그리기
    movex = 0
    movey = 0
    progress *= 0.01

    if gem['direction'] == UP:
        movey = -int(progress * GEMIMAGESIZE)
    elif gem['direction'] == DOWN:
        movey = int(progress * GEMIMAGESIZE)
    elif gem['direction'] == RIGHT:
        movex = int(progress * GEMIMAGESIZE)
    elif gem['direction'] == LEFT:
        movex = -int(progress * GEMIMAGESIZE)

    basex = gem['x']
    basey = gem['y']
    if basey == ROWABOVEBOARD:
        basey = -1

    pixelx = XMARGIN + (basex * GEMIMAGESIZE)
    pixely = YMARGIN + (basey * GEMIMAGESIZE)
    r = pygame.Rect( (pixelx + movex, pixely + movey, GEMIMAGESIZE, GEMIMAGESIZE) )
    DISPLAYSURF.blit(GEMIMAGES[gem['imageNum']], r)


def pullDownAllGems(board):
    # 보석 바닥까지 하강
    for x in range(BOARDWIDTH):
        gemsInColumn = []
        for y in range(BOARDHEIGHT):
            if board[x][y] != EMPTY_SPACE:
                gemsInColumn.append(board[x][y])
        board[x] = ([EMPTY_SPACE] * (BOARDHEIGHT - len(gemsInColumn))) + gemsInColumn

def highlightSpace(x, y):
    # 클릭한 슬롯 하일라이트
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, BOARDRECTS[x][y], 4)

def checkForGemClick(pos):
    # 보드에 클릭이 일어났는지 체크
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if BOARDRECTS[x][y].collidepoint(pos[0], pos[1]):
                return {'x': x, 'y': y}
    return None # 보드 외의 곳이 클릭된 경우 무시

def getSwappingGems(board, firstXY, secondXY):
    # 인접한 보석이 타당한 방향으로 클릭된 경우 바꾸기
    firstGem = {'imageNum': board[firstXY['x']][firstXY['y']],
                'x': firstXY['x'],
                'y': firstXY['y']}
    secondGem = {'imageNum': board[secondXY['x']][secondXY['y']],
                 'x': secondXY['x'],
                 'y': secondXY['y']}
    highlightedGem = None
    if firstGem['x'] == secondGem['x'] + 1 and firstGem['y'] == secondGem['y']:
        firstGem['direction'] = LEFT
        secondGem['direction'] = RIGHT
    elif firstGem['x'] == secondGem['x'] - 1 and firstGem['y'] == secondGem['y']:
        firstGem['direction'] = RIGHT
        secondGem['direction'] = LEFT
    elif firstGem['y'] == secondGem['y'] + 1 and firstGem['x'] == secondGem['x']:
        firstGem['direction'] = UP
        secondGem['direction'] = DOWN
    elif firstGem['y'] == secondGem['y'] - 1 and firstGem['x'] == secondGem['x']:
        firstGem['direction'] = DOWN
        secondGem['direction'] = UP
    else:
        # 인접한 보석이 아니어서 바꿀 수 없는 경우
        return None, None
    return firstGem, secondGem

def findMatchingGems(board):
    gemsToRemove = [] # 제거해야할 보석 리스트
    boardCopy = copy.deepcopy(board)

    # 제거해야할 보석 체크
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            # 수평 퍼즐 완성 체크
            if getGemAt(boardCopy, x, y) == getGemAt(boardCopy, x + 1, y) == getGemAt(boardCopy, x + 2, y) and getGemAt \
                    (boardCopy, x, y) != EMPTY_SPACE:
                targetGem = boardCopy[x][y]
                offset = 0
                removeSet = []
                while getGemAt(boardCopy, x + offset, y) == targetGem:
                    # 3개이상 완성 체크
                    removeSet.append((x + offset, y))
                    boardCopy[x + offset][y] = EMPTY_SPACE
                    offset += 1
                gemsToRemove.append(removeSet)

            # 수직 퍼즐 완성 체크
            if getGemAt(boardCopy, x, y) == getGemAt(boardCopy, x, y + 1) == getGemAt(boardCopy, x, y + 2) and getGemAt \
                    (boardCopy, x, y) != EMPTY_SPACE:
                targetGem = boardCopy[x][y]
                offset = 0
                removeSet = []
                while getGemAt(boardCopy, x, y + offset) == targetGem:
                    # 3개이상 완성 체크
                    removeSet.append((x, y + offset))
                    boardCopy[x][y + offset] = EMPTY_SPACE
                    offset += 1
                gemsToRemove.append(removeSet)

    return gemsToRemove


def canMakeMove(board):
    # 보드에 매칭이 가능한 보석이 있는지 체크
    # 한번의 바꿈으로 이동이 가능한 경우
    oneOffPatterns = (((0 ,1), (1 ,0), (2 ,0)),
                      ((0 ,1), (1 ,1), (2 ,0)),
                      ((0 ,0), (1 ,1), (2 ,0)),
                      ((0 ,1), (1 ,0), (2 ,1)),
                      ((0 ,0), (1 ,0), (2 ,1)),
                      ((0 ,0), (1 ,1), (2 ,1)),
                      ((0 ,0), (0 ,2), (0 ,3)),
                      ((0 ,0), (0 ,1), (0 ,3)))


    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            for pat in oneOffPatterns:
                # 다음 이동에 매칭이 가능한 경우
                if (getGemAt(board, x+ pat[0][0], y + pat[0][1]) == \
                    getGemAt(board, x + pat[1][0], y + pat[1][1]) == \
                    getGemAt(board, x + pat[2][0], y + pat[2][1]) != None) or \
                        (getGemAt(board, x + pat[0][1], y + pat[0][0]) == \
                         getGemAt(board, x + pat[1][1], y + pat[1][0]) == \
                         getGemAt(board, x + pat[2][1], y + pat[2][0]) != None):
                    return True
    return False


def drawScore(score):
    scoreImg = BASICFONT.render(str(score), 1, SCORECOLOR)
    scoreRect = scoreImg.get_rect()
    scoreRect.bottomleft = (10, WINDOWHEIGHT - 6)
    DISPLAYSURF.blit(scoreImg, scoreRect)


if __name__ == '__main__':
    mini()