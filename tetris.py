# # # 
# Tomas Michal
# #

from random import randint
import curses
import datetime
import copy

MaxX, MaxY, Lines, Score, Level, Width, Height, GameOver = 0, 0, 0, 0, 0, 10, 20, False
PlayField = [[0] * Width for x in range(Height)]
Brick, NextBrick, BrickPosition, NextTick = None, None, None, None
Bricks = [
	[[1, 1, 1],
	 [0, 1, 0]],
	[[0, 2, 2],
	 [2, 2, 0]],
	[[3, 3, 0],
	 [0, 3, 3]],
	[[4, 0, 0],
	 [4, 4, 4]],
	[[0, 0, 5],
	 [5, 5, 5]],
	[[6, 6, 6, 6]],
	[[7, 7],
	 [7, 7]]
]

def nextBrick():
    global Brick, NextBrick, BrickPosition
    if NextBrick is None:
        Brick = copy.deepcopy(Bricks[randint(0, len(Bricks) - 1)])
    else:
        Brick = NextBrick
    NextBrick = copy.deepcopy(Bricks[randint(0, len(Bricks) - 1)])
    BrickPosition = [0, 4]

def rotateBrick(brick):
    res = []
    for x in range(0, len(brick[0])):
        a = []
        for y in range(0, len(brick)):
            a.append(brick[len(brick) - y - 1][x])
        res.append(a)
    return res

def getBrickInPlayField(brick, brickPosition):
    res = []
    for row in range(0, len(brick)):
        for column in range(0, len(brick[row])):
            if (brick[row][column] > 0):
                res.append([brickPosition[0] + row, brickPosition[1] + column, brick[row][column]])
    return res

def paintBrick(stdscr, clear):
    brick = getBrickInPlayField(Brick, BrickPosition)    
    for b in brick:
        if clear:
            stdscr.addstr(b[0] + MaxX - Height - 1, b[1] * 2 + 2, ' ' * 2)
        else:
            stdscr.addstr(b[0] + MaxX - Height - 1, b[1] * 2 + 2, ' ' * 2, curses.color_pair(b[2]))

def checkBrick(brick, brickPosition):
    for p in getBrickInPlayField(brick, brickPosition):
        if p[0] == Height or p[1] == Width or p[1] < 0 or PlayField[p[0]][p[1]]:
            return False
    return True

def updateLinesAndScore(stdscr):
    stdscr.addstr(MaxX - Height - 1, Width * 2 + 6, "Score: " + str(Score))
    stdscr.addstr(MaxX - Height + 1, Width * 2 + 6, "Lines: " + str(Lines))
    stdscr.addstr(MaxX - Height + 3, Width * 2 + 6, "Next: ")
    updateNextBrick(stdscr)

def updateNextBrick(stdscr):
    for y in range(0, 2):
        for x in range(0, 4):
            stdscr.addstr(MaxX - Height + 5 + y, Width * 2 + 6 + x * 2, ' ' * 2)
    for y in range(0, len(NextBrick)):
        for x in range(0, len(NextBrick[y])):
            if (NextBrick[y][x] > 0):
                stdscr.addstr(MaxX - Height + 5 + y, Width * 2 + 6 + x * 2, ' ' * 2, curses.color_pair(NextBrick[y][x]))

def moveBrick(stdscr, direction):
    global Brick, NextBrick, BrickPosition, Lines, Score, GameOver
    brick = getBrickInPlayField(Brick, BrickPosition)    
    if direction == curses.KEY_DOWN:
        if not checkBrick(Brick, [BrickPosition[0] + 1, BrickPosition[1]]):
            for pp in brick:
                PlayField[pp[0]][pp[1]] = pp[2]
            nextBrick()
            fullLines = []
            for lineIndex in range(0, len(PlayField)):
                if 0 not in PlayField[lineIndex]:
                    fullLines.append(lineIndex)
            if len(fullLines) > 0:
                for l in fullLines:
                    curses.beep()
                Lines += len(fullLines)
                if (len(fullLines) == 1):
                    Score += Level * 40 + 40
                elif (len(fullLines) == 2): 
                    Score += Level * 100 + 100
                elif (len(fullLines) == 3): 
                    Score += Level * 300 + 300
                elif (len(fullLines) == 4): 
                    Score += Level * 1200 + 1200
                updateLinesAndScore(stdscr)
                for i in fullLines:
                    del PlayField[i]
                    PlayField.insert(0, [0 for x in range(0, Width)])
                for y in range(0, len(PlayField)):
                    for x in range(0, len(PlayField[y])):
                        stdscr.addstr(y + MaxX - Height - 1, x * 2 + 2, ' ' * 2)
                        if (PlayField[y][x] > 0):
                            stdscr.addstr(y + MaxX - Height - 1, x * 2 + 2, ' ' * 2, curses.color_pair(PlayField[y][x]))
            else:
                updateNextBrick(stdscr)
            if not checkBrick(Brick, BrickPosition):
                GameOver = True
            paintBrick(stdscr, False)
            return
    elif direction == curses.KEY_RIGHT:
        if not checkBrick(Brick, [BrickPosition[0], BrickPosition[1] + 1]):
            return
    elif direction == curses.KEY_LEFT:
        if not checkBrick(Brick, [BrickPosition[0], BrickPosition[1] - 1]):
            return
    elif direction == curses.KEY_UP:
        rBrick = rotateBrick(Brick)
        if not checkBrick(rBrick, BrickPosition):
            return
    paintBrick(stdscr, True)
    if direction == curses.KEY_DOWN:
        BrickPosition[0] += 1
    elif direction == curses.KEY_RIGHT:
        BrickPosition[1] += 1
    elif direction == curses.KEY_LEFT:
        BrickPosition[1] -= 1
    elif direction == curses.KEY_UP:
        Brick = rotateBrick(Brick)
    paintBrick(stdscr, False)

def playTetris(stdscr):
    global MaxX, MaxY, NextTick
    MaxX, MaxY = stdscr.getmaxyx()

    stdscr.clear()
    stdscr.refresh()
    stdscr.nodelay(1)
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED)    
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)    
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_BLUE)    
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_YELLOW)    
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_CYAN)    
    curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_MAGENTA)    
    curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_MAGENTA)    
    curses.init_pair(9, curses.COLOR_BLACK, curses.COLOR_WHITE) 

    stdscr.addstr(MaxX - Height +  8, Width * 2 + 6, "Left: left arrow")
    stdscr.addstr(MaxX - Height +  9, Width * 2 + 6, "Right: right arrow")
    stdscr.addstr(MaxX - Height + 10, Width * 2 + 6, "Rotate: up arrow")
    stdscr.addstr(MaxX - Height + 11, Width * 2 + 6, "Drop: down arrow")
    stdscr.addstr(MaxX - Height + 12, Width * 2 + 6, "Exit: q")
    stdscr.addstr(MaxX - Height + 14, Width * 2 + 6, "tomas.michal@gmail.com")

    for x in range(MaxX - Height - 1, MaxX):
        stdscr.addstr(x, 0, ' ' * (Width * 2 + 4), curses.color_pair(9))
        stdscr.addstr(x, 2, ' ' * (Width * 2))
    stdscr.addstr(MaxX - 1, 0, ' ' * (Width * 2 + 4), curses.color_pair(9))
    
    nextBrick()
    NextTick = datetime.datetime.now() + datetime.timedelta(seconds = 1)
    updateLinesAndScore(stdscr)
    paintBrick(stdscr, False)

    key = 0
    while (key != ord('q') and not GameOver):
        key = stdscr.getch()
        if key == curses.KEY_DOWN or key == curses.KEY_RIGHT or key == curses.KEY_LEFT or key == curses.KEY_UP:
            moveBrick(stdscr, key)
        if (datetime.datetime.now() > NextTick):
            moveBrick(stdscr, curses.KEY_DOWN)
            NextTick = datetime.datetime.now() + datetime.timedelta(seconds = 1)
    
def main():
    curses.wrapper(playTetris)
    if GameOver:
        print("Game Over! Your score is " + str(Score))

if __name__ == "__main__":
    main()