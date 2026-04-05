import pygame
import random
import sys

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Хто хоче стати мільйонером")

bg_img = pygame.image.load("WWTBAM_Logo_Ukraine_on_BG_2021.webp")
background = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

pygame.mixer.music.load("Who_Wants_to_Be_a_Millionaire_-_Ask_The_Host_(SkySound.cc).mp3")
pygame.mixer.music.play(-1)
sound_correct = pygame.mixer.Sound("9f3d770d1446e6c.mp3")
sound_wrong = pygame.mixer.Sound("fail-wha-wha-version.mp3")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE_DARK = (0, 25, 70)
BLUE_LIGHT = (0, 120, 255)
RED = (200, 0, 0)
GREEN = (0, 200, 0)

font_question = pygame.font.SysFont("Arial", 24, bold=True)
font_option = pygame.font.SysFont("Arial", 20, bold=True)
font_money = pygame.font.SysFont("Arial", 26, bold=True)
font_restart = pygame.font.SysFont("Arial", 18, bold=True)

questions = [
    {"q": "Столиця Франції?", "options": ["Берлін", "Париж", "Мадрид", "Рим"], "answer": 1},
    {"q": "12 × 12 = ?", "options": ["124", "144", "132", "154"], "answer": 1},
    {"q": "Найбільший океан?", "options": ["Атлантичний", "Індійський", "Тихий", "Північний Льодовитий"], "answer": 2},
    {"q": "Автор 'Гамлета'?", "options": ["Шекспір", "Діккенс", "Гете", "Байрон"], "answer": 0},
    {"q": "Хімічний символ золота?", "options": ["Au", "Ag", "Fe", "O"], "answer": 0},
    {"q": "Скільки кісток у дорослої людини?", "options": ["206", "210", "198", "250"], "answer": 0},
    {"q": "Найшвидша наземна тварина?", "options": ["Лев", "Гепард", "Тигр", "Антилопа"], "answer": 1},
    {"q": "Мова Python названа на честь?", "options": ["Змії", "Вченого", "Комедійного шоу", "Бога"], "answer": 2}
]

money_levels = [1000, 5000, 10000, 50000, 100000, 250000, 500000, 1000000]

current_q = 0
used_5050 = False
running = True
disabled = []
current_money = 0

def reset_game():
    global questions, current_q, used_5050, disabled, current_money
    random.shuffle(questions)
    current_q = 0
    used_5050 = False
    disabled = []
    current_money = 0

reset_game()

def draw_text_centered(text, font, color, surface, rect):
    rendered = font.render(text, True, color)
    text_rect = rendered.get_rect(center=rect.center)
    surface.blit(rendered, text_rect)

def draw_buttons(options, disabled=[]):
    btns = []
    start_y = 180
    for i, option in enumerate(options):
        rect = pygame.Rect(150, start_y + i*50, 500, 40)
        color = BLUE_DARK if i in disabled else BLUE_LIGHT
        pygame.draw.rect(screen, color, rect, border_radius=6)
        pygame.draw.rect(screen, WHITE, rect, 2, border_radius=6)
        draw_text_centered(option, font_option, WHITE, screen, rect)
        btns.append(rect)
    return btns

while running:
    screen.blit(background, (0, 0))

    restart_rect = pygame.Rect(10, 10, 120, 25)
    pygame.draw.rect(screen, BLUE_DARK, restart_rect, border_radius=5)
    pygame.draw.rect(screen, WHITE, restart_rect, 2, border_radius=5)
    draw_text_centered("R - Рестарт", font_restart, WHITE, screen, restart_rect)

    if current_q >= len(questions):
        win_rect = pygame.Rect(50, 150, 700, 60)
        pygame.draw.rect(screen, BLUE_DARK, win_rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, win_rect, 2, border_radius=10)
        draw_text_centered("🎉 ВИ ВИГРАЛИ ПЕРШИЙ МІЛЬЙОН! 🎉", font_money, WHITE, screen, win_rect)
    else:
        q = questions[current_q]

        question_rect = pygame.Rect(50, 80, 700, 50)
        pygame.draw.rect(screen, BLUE_DARK, question_rect, border_radius=8)
        pygame.draw.rect(screen, WHITE, question_rect, 2, border_radius=8)
        draw_text_centered(q["q"], font_question, WHITE, screen, question_rect)

        buttons = draw_buttons(q["options"], disabled)

        btn_5050_rect = pygame.Rect(WIDTH - 140, HEIGHT - 60, 100, 35)
        pygame.draw.rect(screen, RED if used_5050 else GREEN, btn_5050_rect, border_radius=5)
        draw_text_centered("50/50", font_option, WHITE, screen, btn_5050_rect)

        money_text = f"Ваш виграш: {current_money} грн"
        money_rect = pygame.Rect(0, 20, WIDTH, 30)
        draw_text_centered(money_text, font_money, WHITE, screen, money_rect)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()

        if event.type == pygame.MOUSEBUTTONDOWN and current_q < len(questions):
            mx, my = pygame.mouse.get_pos()

            if btn_5050_rect.collidepoint(mx, my) and not used_5050:
                wrong_indexes = [i for i in range(4) if i != q["answer"]]
                disabled = random.sample(wrong_indexes, 2)
                used_5050 = True

            for i, rect in enumerate(buttons):
                if rect.collidepoint(mx, my) and i not in disabled:
                    if i == q["answer"]:
                        sound_correct.play()
                        current_money = money_levels[current_q]
                        current_q += 1
                        used_5050 = False
                        disabled = []
                    else:
                        sound_wrong.play()
                        error_rect = pygame.Rect(50, 150, 700, 50)
                        pygame.draw.rect(screen, BLUE_DARK, error_rect, border_radius=8)
                        pygame.draw.rect(screen, RED, error_rect, 2, border_radius=8)
                        draw_text_centered(f"Неправильно! Ви виграли {current_money} грн", font_option, RED, screen, error_rect)
                        pygame.display.flip()
                        pygame.time.wait(2000)

                        reset_game()  # 🔥 перезапуск гри після програшу

pygame.quit()
sys.exit()