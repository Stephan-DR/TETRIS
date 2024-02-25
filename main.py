import pygame_menu
from pygame_menu.examples import create_example_window
from typing import Tuple, Any
import pygame
from copy import deepcopy
from random import choice
import time

diff = "('Easy', 1) (1)"


def draw(screen):
    sh_open = pygame.font.SysFont('arial', 36)
    sh_text = sh_open.render('Welcome  to  the  game  TETRIS', True, (255, 255, 255))
    screen.blit(sh_text, (200, 300))

def main():
    surface = create_example_window('Example - Simple', (800, 750))
    k = None
    recording = None
    score = None



    def set_difficulty(selected: Tuple, value: Any) -> None:
        global diff
        diff = str(f'Set difficulty to {selected[0]} ({value})'[17:])
        return diff



    def start_the_game() -> None:
        global k, recording, score
        vcl = True
        print(diff)
        if 'Easy' in diff:
            W = 10
            H = 20
            RAZ = 37

            pygame.init()
            game_sc = pygame.display.set_mode([800, 750])
            clock = pygame.time.Clock()

            record = open('RECORDS_NOT_USE.txt')
            for i in record:
                recording = i.split(';')
            record.close()
            k = recording[0]

            win = pygame.mixer.Sound("win.ogg")
            kill = pygame.mixer.Sound('kill.ogg')
            pygame.mixer.music.load("music.mp3")
            pygame.mixer.music.play(-1)

            grid = [pygame.Rect(i * RAZ, j * RAZ, RAZ, RAZ) for i in range(W) for j in range(H)]

            figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
                           [(0, -1), (-1, -1), (-1, 0), (0, 0)],
                           [(-1, 0), (-1, 1), (0, 0), (0, -1)],
                           [(0, 0), (-1, 0), (0, 1), (-1, -1)],
                           [(0, 0), (0, -1), (0, 1), (-1, -1)],
                           [(0, 0), (0, -1), (0, 1), (1, -1)],
                           [(0, 0), (0, -1), (0, 1), (-1, 0)]]

            figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
            figure_rect = pygame.Rect(0, 0, RAZ - 2, RAZ - 2)
            field = [[0 for i in range(10)] for j in range(20)]

            anim_count, anim_speed, anim_limit = 0, 60, 1000
            figure = deepcopy(choice(figures))
            color = (139, 234, 0)
            game_over_back = (0, 0, 0)

            a = pygame.font.SysFont('bold', 50)
            b = pygame.font.Font('ARCADECLASSIC.TTF', 39)
            c = pygame.font.Font('ARCADECLASSIC.TTF', 70)
            book_record = b.render(str(k), True, color)
            text_record = b.render('Record', True, color)
            text_score = b.render('Score', True, color)
            text_sl = c.render('EASY', True, color)
            score = 0

            def check_borders():
                if figure[i].x < 0 or figure[i].x > W - 1:
                    return False
                elif figure[i].y > H - 1 or field[figure[i].y][figure[i].x]:
                    return False
                return True

            while True:
                dx, rotate = 0, False
                game_sc.fill(pygame.Color('black'))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            dx = -1
                        elif event.key == pygame.K_RIGHT:
                            dx = 1
                        elif event.key == pygame.K_k:
                            rotate = True

                for i in range(4):
                    figure[i].x += dx
                    if not check_borders():
                        figure = deepcopy(figure_old)
                        break

                anim_count += anim_speed

                if anim_count > anim_limit:
                    anim_count = 0
                    for i in range(4):
                        figure[i].y += 1
                        if not check_borders():
                            for i in range(4):
                                field[figure_old[i].y][figure_old[i].x] = pygame.Color(color)
                            figure = deepcopy(choice(figures))
                            break

                center = figure[0]
                figure_old = deepcopy(figure)
                if rotate:
                    for i in range(4):
                        x = figure[i].y - center.y
                        y = figure[i].x - center.x
                        figure[i].x = center.x - x
                        figure[i].y = center.y + y
                        if not check_borders():
                            for i in range(4):
                                figure = deepcopy(figure_old)
                                break
                    win.play()

                line = H - 1
                for row in range(H - 1, -1, -1):
                    count = 0
                    for i in range(W):
                        if field[row][i]:
                            count += 1
                        field[line][i] = field[row][i]
                    if count < W:
                        line -= 1
                    else:
                        score += 100
                        kill.play()

                [pygame.draw.rect(game_sc, (40, 40, 40), i, 1) for i in grid]

                for i in range(4):
                    figure_rect.x = figure[i].x * RAZ
                    figure_rect.y = figure[i].y * RAZ
                    pygame.draw.rect(game_sc, pygame.Color(color), figure_rect)

                    for y, raw in enumerate(field):
                        for x, col in enumerate(raw):
                            if col:
                                figure_rect.x, figure_rect.y = x * RAZ, y * RAZ
                                pygame.draw.rect(game_sc, col, figure_rect)

                game_sc.blit(text_record, (400, 10))
                game_sc.blit(text_score, (400, 60))
                score_chet = b.render(str(score), True, (color))
                game_sc.blit(score_chet, (530, 60))
                game_sc.blit(text_sl, (400, 150))
                game_sc.blit(book_record, (530, 10))

                for i in range(W):
                    if field[0][i]:
                        end_screen()

                def end_screen():
                    global k, recording
                    game_sc.fill(pygame.Color('black'))
                    win.stop()
                    kill.stop()
                    pygame.mixer.music.pause()
                    game_over_shr = pygame.font.Font('ARCADECLASSIC.TTF', 100)
                    text_game_over = game_over_shr.render('GAME OVER', True, color)
                    game_sc.blit(text_game_over, (170, 300))
                    text_score = b.render('Score', True, color)
                    game_sc.blit(text_score, (170, 400))
                    game_sc.blit(score_chet, (300, 400))
                    game_sc.blit(text_record, (170, 450))
                    if int(score) > int(k):
                        recording[0] = str(score)
                        recording = ';'.join(recording)
                        with open('RECORDS_NOT_USE.txt', 'w') as f:
                            f.write(recording)
                    record = open('RECORDS_NOT_USE.txt')
                    for i in record:
                        recording = i.split(';')
                    record.close()
                    k = recording[0]
                    book_record = b.render(str(k), True, color)
                    game_sc.blit(book_record, (300, 450))
                    pygame.display.flip()
                    clock.tick(60)
                    time.sleep(4)
                    main()

                pygame.display.flip()
                clock.tick(60)
        elif 'Normal' in diff:
            W = 10
            H = 20
            RAZ = 37

            pygame.init()
            game_sc = pygame.display.set_mode([800, 750])
            clock = pygame.time.Clock()

            record = open('RECORDS_NOT_USE.txt')
            for i in record:
                recording = i.split(';')
            record.close()
            k = recording[1]

            win = pygame.mixer.Sound("win.ogg")
            kill = pygame.mixer.Sound('kill.ogg')
            pygame.mixer.music.load("music.mp3")
            pygame.mixer.music.play(-1)

            grid = [pygame.Rect(i * RAZ, j * RAZ, RAZ, RAZ) for i in range(W) for j in range(H)]

            figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
                           [(0, -1), (-1, -1), (-1, 0), (0, 0)],
                           [(-1, 0), (-1, 1), (0, 0), (0, -1)],
                           [(0, 0), (-1, 0), (0, 1), (-1, -1)],
                           [(0, 0), (0, -1), (0, 1), (-1, -1)],
                           [(0, 0), (0, -1), (0, 1), (1, -1)],
                           [(0, 0), (0, -1), (0, 1), (-1, 0)]]

            figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
            figure_rect = pygame.Rect(0, 0, RAZ - 2, RAZ - 2)
            field = [[0 for i in range(10)] for j in range(20)]

            anim_count, anim_speed, anim_limit = 0, 60, 500
            figure = deepcopy(choice(figures))
            color = (235, 227, 0)
            game_over_back = (0, 0, 0)

            a = pygame.font.SysFont('bold', 50)
            b = pygame.font.Font('ARCADECLASSIC.TTF', 39)
            c = pygame.font.Font('ARCADECLASSIC.TTF', 70)
            book_record = b.render(str(k), True, color)
            text_record = b.render('Record', True, color)
            text_score = b.render('Score', True, color)
            text_sl = c.render('NORMAL', True, color)
            score = 0

            def check_borders():
                if figure[i].x < 0 or figure[i].x > W - 1:
                    return False
                elif figure[i].y > H - 1 or field[figure[i].y][figure[i].x]:
                    return False
                return True

            while True:
                dx, rotate = 0, False
                game_sc.fill(pygame.Color('black'))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            dx = -1
                        elif event.key == pygame.K_RIGHT:
                            dx = 1
                        elif event.key == pygame.K_k:
                            rotate = True

                for i in range(4):
                    figure[i].x += dx
                    if not check_borders():
                        figure = deepcopy(figure_old)
                        break

                anim_count += anim_speed

                if anim_count > anim_limit:
                    anim_count = 0
                    for i in range(4):
                        figure[i].y += 1
                        if not check_borders():
                            for i in range(4):
                                field[figure_old[i].y][figure_old[i].x] = pygame.Color(color)
                            figure = deepcopy(choice(figures))
                            break

                center = figure[0]
                figure_old = deepcopy(figure)
                if rotate:
                    for i in range(4):
                        x = figure[i].y - center.y
                        y = figure[i].x - center.x
                        figure[i].x = center.x - x
                        figure[i].y = center.y + y
                        if not check_borders():
                            for i in range(4):
                                figure = deepcopy(figure_old)
                                break
                    win.play()

                line = H - 1
                for row in range(H - 1, -1, -1):
                    count = 0
                    for i in range(W):
                        if field[row][i]:
                            count += 1
                        field[line][i] = field[row][i]
                    if count < W:
                        line -= 1
                    else:
                        score += 100
                        kill.play()

                [pygame.draw.rect(game_sc, (40, 40, 40), i, 1) for i in grid]

                for i in range(4):
                    figure_rect.x = figure[i].x * RAZ
                    figure_rect.y = figure[i].y * RAZ
                    pygame.draw.rect(game_sc, pygame.Color(color), figure_rect)

                    for y, raw in enumerate(field):
                        for x, col in enumerate(raw):
                            if col:
                                figure_rect.x, figure_rect.y = x * RAZ, y * RAZ
                                pygame.draw.rect(game_sc, col, figure_rect)

                game_sc.blit(text_record, (400, 10))
                game_sc.blit(text_score, (400, 60))
                score_chet = b.render(str(score), True, (color))
                game_sc.blit(score_chet, (530, 60))
                game_sc.blit(text_sl, (400, 150))
                game_sc.blit(book_record, (530, 10))

                for i in range(W):
                    if field[0][i]:
                        end_screen()

                def end_screen():
                    global k, recording
                    game_sc.fill(pygame.Color('black'))
                    win.stop()
                    kill.stop()
                    pygame.mixer.music.pause()
                    game_over_shr = pygame.font.Font('ARCADECLASSIC.TTF', 100)
                    text_game_over = game_over_shr.render('GAME OVER', True, color)
                    game_sc.blit(text_game_over, (170, 300))
                    text_score = b.render('Score', True, color)
                    game_sc.blit(text_score, (170, 400))
                    game_sc.blit(score_chet, (300, 400))
                    game_sc.blit(text_record, (170, 450))
                    if int(score) > int(k):
                        recording[1] = str(score)
                        recording = ';'.join(recording)
                        with open('RECORDS_NOT_USE.txt', 'w') as f:
                            f.write(recording)
                    record = open('RECORDS_NOT_USE.txt')
                    for i in record:
                        recording = i.split(';')
                    record.close()
                    k = recording[1]
                    book_record = b.render(str(k), True, color)
                    game_sc.blit(book_record, (300, 450))
                    pygame.display.flip()
                    clock.tick(60)
                    time.sleep(4)
                    main()

                pygame.display.flip()
                clock.tick(60)
        elif 'Hard' in diff:
            W = 10
            H = 20
            RAZ = 37

            pygame.init()
            game_sc = pygame.display.set_mode([800, 750])
            clock = pygame.time.Clock()

            record = open('RECORDS_NOT_USE.txt')
            for i in record:
                recording = i.split(';')
            record.close()
            k = recording[2]

            win = pygame.mixer.Sound("win.ogg")
            kill = pygame.mixer.Sound('kill.ogg')
            pygame.mixer.music.load("music.mp3")
            pygame.mixer.music.play(-1)

            grid = [pygame.Rect(i * RAZ, j * RAZ, RAZ, RAZ) for i in range(W) for j in range(H)]

            figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
                           [(0, -1), (-1, -1), (-1, 0), (0, 0)],
                           [(-1, 0), (-1, 1), (0, 0), (0, -1)],
                           [(0, 0), (-1, 0), (0, 1), (-1, -1)],
                           [(0, 0), (0, -1), (0, 1), (-1, -1)],
                           [(0, 0), (0, -1), (0, 1), (1, -1)],
                           [(0, 0), (0, -1), (0, 1), (-1, 0)]]

            figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
            figure_rect = pygame.Rect(0, 0, RAZ - 2, RAZ - 2)
            field = [[0 for i in range(10)] for j in range(20)]

            anim_count, anim_speed, anim_limit = 0, 60, 250
            figure = deepcopy(choice(figures))
            color = (255, 66, 66)
            game_over_back = (0, 0, 0)

            a = pygame.font.SysFont('bold', 50)
            b = pygame.font.Font('ARCADECLASSIC.TTF', 39)
            c = pygame.font.Font('ARCADECLASSIC.TTF', 70)
            book_record = b.render(str(k), True, color)
            text_record = b.render('Record', True, color)
            text_score = b.render('Score', True, color)
            text_sl = c.render('HARD', True, color)
            score = 0

            def check_borders():
                if figure[i].x < 0 or figure[i].x > W - 1:
                    return False
                elif figure[i].y > H - 1 or field[figure[i].y][figure[i].x]:
                    return False
                return True

            while True:
                dx, rotate = 0, False
                game_sc.fill(pygame.Color('black'))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            dx = -1
                        elif event.key == pygame.K_RIGHT:
                            dx = 1
                        elif event.key == pygame.K_k:
                            rotate = True

                for i in range(4):
                    figure[i].x += dx
                    if not check_borders():
                        figure = deepcopy(figure_old)
                        break

                anim_count += anim_speed

                if anim_count > anim_limit:
                    anim_count = 0
                    for i in range(4):
                        figure[i].y += 1
                        if not check_borders():
                            for i in range(4):
                                field[figure_old[i].y][figure_old[i].x] = pygame.Color(color)
                            figure = deepcopy(choice(figures))
                            break

                center = figure[0]
                figure_old = deepcopy(figure)
                if rotate:
                    for i in range(4):
                        x = figure[i].y - center.y
                        y = figure[i].x - center.x
                        figure[i].x = center.x - x
                        figure[i].y = center.y + y
                        if not check_borders():
                            for i in range(4):
                                figure = deepcopy(figure_old)
                                break
                    win.play()

                line = H - 1
                for row in range(H - 1, -1, -1):
                    count = 0
                    for i in range(W):
                        if field[row][i]:
                            count += 1
                        field[line][i] = field[row][i]
                    if count < W:
                        line -= 1
                    else:
                        score += 100
                        kill.play()

                [pygame.draw.rect(game_sc, (40, 40, 40), i, 1) for i in grid]

                for i in range(4):
                    figure_rect.x = figure[i].x * RAZ
                    figure_rect.y = figure[i].y * RAZ
                    pygame.draw.rect(game_sc, pygame.Color(color), figure_rect)

                    for y, raw in enumerate(field):
                        for x, col in enumerate(raw):
                            if col:
                                figure_rect.x, figure_rect.y = x * RAZ, y * RAZ
                                pygame.draw.rect(game_sc, col, figure_rect)

                game_sc.blit(text_record, (400, 10))
                game_sc.blit(text_score, (400, 60))
                score_chet = b.render(str(score), True, (color))
                game_sc.blit(score_chet, (530, 60))
                game_sc.blit(text_sl, (400, 150))
                game_sc.blit(book_record, (530, 10))

                for i in range(W):
                    if field[0][i]:
                        end_screen()

                def end_screen():
                    global k, recording
                    game_sc.fill(pygame.Color('black'))
                    win.stop()
                    kill.stop()
                    pygame.mixer.music.pause()
                    game_over_shr = pygame.font.Font('ARCADECLASSIC.TTF', 100)
                    text_game_over = game_over_shr.render('GAME OVER', True, color)
                    game_sc.blit(text_game_over, (170, 300))
                    text_score = b.render('Score', True, color)
                    game_sc.blit(text_score, (170, 400))
                    game_sc.blit(score_chet, (300, 400))
                    game_sc.blit(text_record, (170, 450))
                    if int(score) > int(k):
                        recording[2] = str(score)
                        recording = ';'.join(recording)
                        with open('RECORDS_NOT_USE.txt', 'w') as f:
                            f.write(recording)
                    record = open('RECORDS_NOT_USE.txt')
                    for i in record:
                        recording = i.split(';')
                    record.close()
                    k = recording[2]
                    book_record = b.render(str(k), True, color)
                    game_sc.blit(book_record, (300, 450))
                    pygame.display.flip()
                    clock.tick(60)
                    time.sleep(4)
                    main()

                pygame.display.flip()
                clock.tick(60)



    menu = pygame_menu.Menu(
        height=750,
        theme=pygame_menu.themes.THEME_DARK,
        title='TETRIS',
        width=800
    )

    menu.add.selector('Сложность: ', [('Easy', 1), ('Normal', 2), ('Hard', 3)], onchange=set_difficulty)
    menu.add.button('Play', start_the_game)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    if __name__ == '__main__':
        menu.mainloop(surface)

if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 750
    screen = pygame.display.set_mode(size)
    draw(screen)
    pygame.display.flip()
    time.sleep(3)
    main()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()
