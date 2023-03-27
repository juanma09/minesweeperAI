import pygame
import sys
import time

from minesweeper import Minesweeper, MinesweeperAI, Sentence, get_islands

HEIGHT = 20
WIDTH = 20
MINES = 50
# Colors
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
DARK_GRAY = (130, 130, 130)
WHITE = (255, 255, 255)
RED = (255,0,0)

MINE_COLORS = {1:(0,0,255),
               2:(0,128,0),
               3:(255,0,0),
               4:(128,0,128),
               5:(128,0,0),
               6:(0,128,128),
               7:(0,0,0),
               8:(128,128,128),}

all_zeros = []
to_add = []

# Create game
pygame.init()
scScale = 300
size = width, height = 3 * scScale, 2 * scScale
screen = pygame.display.set_mode(size)

# Fonts
OPEN_SANS = pygame.font.get_default_font()
smallFont = pygame.font.Font(OPEN_SANS, 20)
mediumFont = pygame.font.Font(OPEN_SANS, 28)
largeFont = pygame.font.Font(OPEN_SANS, 40)

# Compute board size
BOARD_PADDING = 20
board_width = ((2 / 3) * width) - (BOARD_PADDING * 2)
board_height = height - (BOARD_PADDING * 2)
cell_size = int(min(board_width / WIDTH, board_height / HEIGHT))
board_origin = (BOARD_PADDING, BOARD_PADDING)

# Add images
flag1 = pygame.image.load("flag.png")
mine1 = pygame.image.load("mine.png")



# Keep track of revealed cells, flagged cells, and if a mine was hit
revealed = set()
flags = set()
lost = False

# Show instructions initially
instructions = True
mineLost = (-1,-1)
with_ai = False

difficulty = 2 #1: easy, 2: medium 3: hard

while True:

    # Check if game quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(BLACK)

    # Show game instructions
    if instructions:

        # Title
        title = largeFont.render("Play Minesweeper", True, WHITE)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Rules
        rules = [
            "Click a cell to reveal it.",
            "Right-click a cell to mark it as a mine.",
            "Mark all mines successfully to win!"
        ]
        for i, rule in enumerate(rules):
            line = smallFont.render(rule, True, WHITE)
            lineRect = line.get_rect()
            lineRect.center = ((width / 2), 150 + 30 * i)
            screen.blit(line, lineRect)

        #Difficulty buttons
        buttonEasy = pygame.Rect((width / 4) , (4 / 8) * height, width / 6 - 10, 40)
        buttonText = mediumFont.render("Easy", True, BLACK)
        buttonTextRect = buttonText.get_rect()
        buttonTextRect.center = buttonEasy.center
        if difficulty == 1:
            pygame.draw.rect(screen, GRAY, buttonEasy)
        else:
            pygame.draw.rect(screen, WHITE, buttonEasy)
        screen.blit(buttonText, buttonTextRect)

        buttonMedium = pygame.Rect((width / 4)+ (width/6) + 5, (4 / 8) * height, width / 6 - 10, 40)
        buttonText = mediumFont.render("Medium", True, BLACK)
        buttonTextRect = buttonText.get_rect()
        buttonTextRect.center = buttonMedium.center
        if difficulty == 2:
            pygame.draw.rect(screen, GRAY, buttonMedium)
        else:
            pygame.draw.rect(screen, WHITE, buttonMedium)
        screen.blit(buttonText, buttonTextRect)

        buttonHard = pygame.Rect((width / 4)+ 2*(width/6) + 10, (4 / 8) * height, width / 6 - 10, 40)
        buttonText = mediumFont.render("Hard", True, BLACK)
        buttonTextRect = buttonText.get_rect()
        buttonTextRect.center = buttonHard.center
        if difficulty == 3:
            pygame.draw.rect(screen, GRAY, buttonHard)
        else:
            pygame.draw.rect(screen, WHITE, buttonHard)

        screen.blit(buttonText, buttonTextRect)


        # Play game with AI button
        buttonRectAI = pygame.Rect((width / 4), (5 / 8) * height, width / 2, 50)
        buttonTextAI = mediumFont.render("Play Game with AI", True, BLACK)
        buttonTextRectAI = buttonTextAI.get_rect()
        buttonTextRectAI.center = buttonRectAI.center
        pygame.draw.rect(screen, WHITE, buttonRectAI)
        screen.blit(buttonTextAI, buttonTextRectAI)

        # Play game with no AI button
        buttonRect = pygame.Rect((width / 4), (6 / 8) * height, width / 2, 50)
        buttonText = mediumFont.render("Play Game", True, BLACK)
        buttonTextRect = buttonText.get_rect()
        buttonTextRect.center = buttonRect.center
        pygame.draw.rect(screen, WHITE, buttonRect)
        screen.blit(buttonText, buttonTextRect)

        # Check if play button clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if buttonEasy.collidepoint(mouse):
                difficulty = 1
                WIDTH = 10
                HEIGHT = 10
                MINES = 15
                time.sleep(0.1)
            elif buttonMedium.collidepoint(mouse):
                difficulty = 2
                WIDTH = 15
                HEIGHT = 15
                MINES = 20
                time.sleep(0.1)
            elif buttonHard.collidepoint(mouse):
                difficulty = 3
                WIDTH = 20
                HEIGHT = 20
                MINES = 40
                time.sleep(0.1)
 

            if buttonRectAI.collidepoint(mouse):
                game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
                ai = MinesweeperAI(height=HEIGHT, width=WIDTH)
                instructions = False
                with_ai = True
                time.sleep(0.3)
            elif buttonRect.collidepoint(mouse):
                game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
                instructions = False
                with_ai = False
                time.sleep(0.3)
            
            cell_size = int(min(board_width / WIDTH, board_height / HEIGHT))
            flag = pygame.transform.scale(flag1, (cell_size, cell_size))
            mine = pygame.transform.scale(mine1, (cell_size, cell_size))

        pygame.display.flip()
        continue
    elif with_ai:

        # Draw board
        cells = []
        for i in range(HEIGHT):
            row = []
            for j in range(WIDTH):

                # Draw rectangle for cell
                rect = pygame.Rect(
                    board_origin[0] + j * cell_size,
                    board_origin[1] + i * cell_size,
                    cell_size, cell_size
                )
                pygame.draw.rect(screen, GRAY, rect)
                pygame.draw.rect(screen, WHITE, rect, 3)

                # Add a mine, flag, or number if needed
                if (i,j) == mineLost and lost:
                    pygame.draw.rect(screen, RED, rect)
                    screen.blit(mine, rect)
                elif game.is_mine((i,j)) and lost:
                    screen.blit(mine, rect)
                elif (i, j) in flags:
                    screen.blit(flag, rect)
                elif (i, j) in revealed:
                    nearby = game.nearby_mines((i, j))
                    if nearby:
                        neighbors = mediumFont.render(
                            str(nearby),
                            True, MINE_COLORS[nearby]
                        )
                        neighborsTextRect = neighbors.get_rect()
                        neighborsTextRect.center = rect.center
                        screen.blit(neighbors, neighborsTextRect)
                    else:
                        pygame.draw.rect(screen, DARK_GRAY, rect)
                        pygame.draw.rect(screen, WHITE, rect, 3)

                row.append(rect)
            cells.append(row)

        # Back Button
        backButton = pygame.Rect(
            (4/5) * width, (5 / 6) * height,
            (width / 5) - BOARD_PADDING * 2, 50
        )
        buttonText = mediumFont.render("Back", True, BLACK)
        buttonRect = buttonText.get_rect()
        buttonRect.center = backButton.center
        pygame.draw.rect(screen, WHITE, backButton)
        screen.blit(buttonText, buttonRect)

        # AI Move button
        aiButton = pygame.Rect(
            (2 / 3) * width + BOARD_PADDING, (1 / 3) * height - 50,
            (width / 3) - BOARD_PADDING * 2, 50
        )
        buttonText = mediumFont.render("AI Move", True, BLACK)
        buttonRect = buttonText.get_rect()
        buttonRect.center = aiButton.center
        pygame.draw.rect(screen, WHITE, aiButton)
        screen.blit(buttonText, buttonRect)

        # Reset button
        resetButton = pygame.Rect(
            (2 / 3) * width + BOARD_PADDING, (1 / 3) * height + 20,
            (width / 3) - BOARD_PADDING * 2, 50
        )
        buttonText = mediumFont.render("Reset", True, BLACK)
        buttonRect = buttonText.get_rect()
        buttonRect.center = resetButton.center
        pygame.draw.rect(screen, WHITE, resetButton)
        screen.blit(buttonText, buttonRect)

        # Display text
        text = "Lost" if lost else "Won" if game.mines == flags else ""
        text = mediumFont.render(text, True, WHITE)
        textRect = text.get_rect()
        textRect.center = ((5 / 6) * width, (2 / 3) * height)
        screen.blit(text, textRect)

        text = str(len(flags)) + "/" + str(MINES)
        text = mediumFont.render(text, True, WHITE)
        textRect = text.get_rect()
        textRect.center = ((11 / 12) * width, (1 / 12) * height)
        screen.blit(text, textRect)

        move = None

        left, _, right = pygame.mouse.get_pressed()

        # Check for a right-click to toggle flagging
        if right == 1 and not lost:
            mouse = pygame.mouse.get_pos()
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    if cells[i][j].collidepoint(mouse) and (i, j) not in revealed:
                        if (i, j) in flags:
                            flags.remove((i, j))
                        else:
                            flags.add((i, j))
                        time.sleep(0.2)

        elif left == 1:
            mouse = pygame.mouse.get_pos()

            # If AI button clicked, make an AI move
            if aiButton.collidepoint(mouse) and not lost:
                # add_knowledges(to_add)
                move = ai.make_safe_move()
                if move is None:
                    move = ai.make_random_move()
                    if move is None:
                        flags = ai.mines.copy()
                        print("No moves left to make.")
                    else:
                        print("No known safe moves, AI making random move.")
                else:
                    print("AI making safe move.")
                time.sleep(0.2)

            # Reset game state
            elif resetButton.collidepoint(mouse):
                game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
                ai = MinesweeperAI(height=HEIGHT, width=WIDTH)
                revealed = set()
                flags = set()
                lost = False
                continue

            elif backButton.collidepoint(mouse):
                game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
                ai = MinesweeperAI(height=HEIGHT, width=WIDTH)
                revealed = set()
                flags = set()
                lost = False
                instructions = True
                with_ai = False
                print("resetting")
                continue

            # User-made move
            elif not lost:
                for i in range(HEIGHT):
                    for j in range(WIDTH):
                        if (cells[i][j].collidepoint(mouse)
                                and (i, j) not in flags
                                and (i, j) not in revealed):
                            move = (i, j)



        # Make move and update AI knowledge
        if move:
            text = mediumFont.render("Processing...", True, WHITE)
            textRect = text.get_rect()
            textRect.center = ((5 / 6) * width, (2 / 3) * height)
            screen.blit(text, textRect)
            pygame.display.flip()
            if game.is_mine(move):
                lost = True
                mineLost = move
            else:
                nearby = game.nearby_mines(move)
                if nearby == 0:
                    zeros = get_islands(game, [f'{move[0]},{move[1]}'],{f'{move[0]},{move[1]}'})
                    # game.print()
                    # print(zeros)
                    revealed.add(move)
                    to_add.append((move, nearby))
                    ai.add_knowledge(move, nearby)
                    for zero in zeros:
                        var = zero.split(",")
                        move = int(var[0]), int(var[1])
                        revealed.add(move)
                        nearby = game.nearby_mines(move)
                        ai.add_knowledge(move, nearby)
                        if move in flags:
                            flags.remove(move)
                        # print(zeros)
                    
                    
                else:
                    revealed.add(move)
                    # add_knowledges(to_add)
                    ai.add_knowledge(move, nearby)
        pygame.display.flip()
    else:
        # Draw board
        cells = []
        for i in range(HEIGHT):
            row = []
            for j in range(WIDTH):

                # Draw rectangle for cell
                rect = pygame.Rect(
                    board_origin[0] + j * cell_size,
                    board_origin[1] + i * cell_size,
                    cell_size, cell_size
                )
                pygame.draw.rect(screen, GRAY, rect)
                pygame.draw.rect(screen, WHITE, rect, 3)

                # Add a mine, flag, or number if needed
                if (i,j) == mineLost and lost:
                    pygame.draw.rect(screen, RED, rect)
                    screen.blit(mine, rect)
                elif game.is_mine((i,j)) and lost:
                    screen.blit(mine, rect)
                elif (i, j) in flags:
                    screen.blit(flag, rect)
                elif (i, j) in revealed:
                    nearby = game.nearby_mines((i, j))
                    if nearby:
                        neighbors = mediumFont.render(
                            str(nearby),
                            True, MINE_COLORS[nearby]
                        )
                        neighborsTextRect = neighbors.get_rect()
                        neighborsTextRect.center = rect.center
                        screen.blit(neighbors, neighborsTextRect)
                    else:
                        pygame.draw.rect(screen, DARK_GRAY, rect)
                        pygame.draw.rect(screen, WHITE, rect, 3)

                row.append(rect)
            cells.append(row)
        
        #Back Button
        backButton = pygame.Rect(
            (4/5) * width, (5 / 6) * height,
            (width / 5) - BOARD_PADDING * 2, 50
        )
        buttonText = mediumFont.render("Back", True, BLACK)
        buttonRect = buttonText.get_rect()
        buttonRect.center = backButton.center
        pygame.draw.rect(screen, WHITE, backButton)
        screen.blit(buttonText, buttonRect)
        # Reset button
        resetButton = pygame.Rect(
            (2 / 3) * width + BOARD_PADDING, (1 / 3) * height + 20,
            (width / 3) - BOARD_PADDING * 2, 50
        )
        buttonText = mediumFont.render("Reset", True, BLACK)
        buttonRect = buttonText.get_rect()
        buttonRect.center = resetButton.center
        pygame.draw.rect(screen, WHITE, resetButton)
        screen.blit(buttonText, buttonRect)

        # Display text
        text = "Lost" if lost else "Won" if game.mines == flags else ""
        text = mediumFont.render(text, True, WHITE)
        textRect = text.get_rect()
        textRect.center = ((5 / 6) * width, (2 / 3) * height)
        screen.blit(text, textRect)

        text = str(len(flags)) + "/" + str(MINES)
        text = mediumFont.render(text, True, WHITE)
        textRect = text.get_rect()
        textRect.center = ((11 / 12) * width, (1 / 12) * height)
        screen.blit(text, textRect)

        move = None

        left, _, right = pygame.mouse.get_pressed()

        # Check for a right-click to toggle flagging
        if right == 1 and not lost:
            mouse = pygame.mouse.get_pos()
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    if cells[i][j].collidepoint(mouse) and (i, j) not in revealed:
                        if (i, j) in flags:
                            flags.remove((i, j))
                        else:
                            flags.add((i, j))
                        time.sleep(0.2)

        elif left == 1:
            mouse = pygame.mouse.get_pos()        
            # Reset game state
            if resetButton.collidepoint(mouse):
                game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
                ai = MinesweeperAI(height=HEIGHT, width=WIDTH)
                revealed = set()
                flags = set()
                lost = False
                continue
            
            #Back Button pressed
            elif backButton.collidepoint(mouse):
                game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
                ai = MinesweeperAI(height=HEIGHT, width=WIDTH)
                revealed = set()
                flags = set()
                lost = False
                instructions = True
                with_ai = False
                print("resetting")
                continue
            
            # User-made move
            elif not lost:
                for i in range(HEIGHT):
                    for j in range(WIDTH):
                        if (cells[i][j].collidepoint(mouse)
                                and (i, j) not in flags
                                and (i, j) not in revealed):
                            move = (i, j)

        # Make move and update AI knowledge
        if move:
            if game.is_mine(move):
                lost = True
                mineLost = move
            else:
                nearby = game.nearby_mines(move)
                if nearby == 0:
                    zeros = get_islands(game, [f'{move[0]},{move[1]}'],{f'{move[0]},{move[1]}'})
                    revealed.add(move)
                    for zero in zeros:
                        var = zero.split(",")
                        move = int(var[0]), int(var[1])
                        revealed.add(move)
                        if move in flags:
                            flags.remove(move)
                        # print(zeros)  
                else:
                    revealed.add(move)
                    # add_knowledges(to_add)

        pygame.display.flip()