import pygame
import random
import sys

# --- Ініціалізація Pygame ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Перший мільйон")

# --- Кольори ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
GRAY = (100, 100, 100)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)

# --- Шрифти ---
font_question = pygame.font.SysFont("Arial", 28)
font_option = pygame.font.SysFont("Arial", 24)
font_money = pygame.font.SysFont("Arial", 30)

# --- Питання та варіанти ---
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

random.shuffle(questions)

current_q = 0
used_5050 = False
running = True
disabled = []

def draw_text(text, font, color, surface, x, y):
    render = font.render(text, True, color)
    surface.blit(render, (x, y))

def draw_buttons(options, disabled=[]):
    btns = []
    for i, option in enumerate(options):
        color = GRAY if i in disabled else BLUE
        rect = pygame.Rect(150, 200 + i*60, 500, 50)
        pygame.draw.rect(screen, color, rect)
        draw_text(option, font_option, WHITE, screen, rect.x + 10, rect.y + 10)
        btns.append(rect)
    return btns

while running:
    screen.fill(BLACK)

    if current_q >= len(questions):
        draw_text("🎉 ВИ ВИГРАЛИ ПЕРШИЙ МІЛЬЙОН! 🎉", font_money, GOLD, screen, 100, 250)
        pygame.display.flip()
        pygame.time.wait(5000)
        break

    q = questions[current_q]
    draw_text(f"Питання на {money_levels[current_q]} грн", font_money, GOLD, screen, 250, 20)
    draw_text(q["q"], font_question, WHITE, screen, 50, 100)

    buttons = draw_buttons(q["options"], disabled)

    # --- Кнопка 50/50 ---
    btn_5050_rect = pygame.Rect(350, 500, 100, 40)
    pygame.draw.rect(screen, RED if used_5050 else GREEN, btn_5050_rect)
    draw_text("50/50", font_option, WHITE, screen, btn_5050_rect.x+10, btn_5050_rect.y+5)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            # Натиск на 50/50
            if btn_5050_rect.collidepoint(mx, my) and not used_5050:
                wrong_indexes = [i for i in range(4) if i != q["answer"]]
                disabled = random.sample(wrong_indexes, 2)
                used_5050 = True
            # Натиск на варіант відповіді
            for i, rect in enumerate(buttons):
                if rect.collidepoint(mx, my) and i not in disabled:
                    if i == q["answer"]:
                        current_q += 1
                        used_5050 = False
                        disabled = []
                    else:
                        screen.fill(BLACK)
                        draw_text(f"Неправильно! Ви виграли {money_levels[current_q-1] if current_q>0 else 0} грн", font_money, RED, screen, 100, 250)
                        pygame.display.flip()
                        pygame.time.wait(4000)
                        running = False

pygame.quit()
sys.exit()