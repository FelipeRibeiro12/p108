import pygame
import sys
from main import (
    mm1_queue_metrics, mmc_queue_metrics, mm1k_queue_metrics, mmc_k_queue_metrics,
    mm1n_queue_metrics, mmcn_queue_metrics, mg1_queue_metrics,
    mm1_priority_non_preemptive_metrics, mm1_priority_preemptive_metrics,
    mg1_non_preemptive_priority_metrics, mg1_preemptive_priority_metrics,
    mmc_priority_non_preemptive_metrics, mmc_priority_preemptive_metrics
)

pygame.init()
WIDTH, HEIGHT = 1000, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Teoria das Filas - Interface Gráfica')
font = pygame.font.SysFont(None, 24)
font_small = pygame.font.SysFont(None, 18)

# Theme colors (kept consistent)
BG = (32, 34, 44)
PANEL_LEFT = (44, 48, 60)
PANEL_RIGHT = (38, 40, 50)
ACCENT = (0, 200, 180)
CARD = (0, 120, 200)
CARD_HOVER = (0, 180, 255)

MODELS = [
    "Modelo M/M/1",
    "Modelo M/M/c",
    "Modelo M/M/1/K",
    "Modelo M/M/c/K",
    "Modelo M/M/1/N (População finita)",
    "Modelo M/M/c/N (população finita)",
    "Modelo M/G/1",
    "Modelo M/M/1 Prioridade Nao Preemptiva",
    "Modelo M/M/1 Prioridade Preemptiva",
    "Modelo M/G/1 Prioridade Nao Preemptiva",
    "Modelo M/G/1 Prioridade Preemptiva",
    "Modelo M/M/c Prioridade Nao Preemptiva",
    "Modelo M/M/c Prioridade Preemptiva"
]

# Reusable UI components
class Card:
    def __init__(self, text, x, y, w, h, callback):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.callback = callback
        self.hovered = False
    def draw(self, surface):
        color = CARD_HOVER if self.hovered else CARD
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, (255,255,255), self.rect, 2, border_radius=10)
        txt = font_small.render(self.text, True, (255,255,255))
        surface.blit(txt, (self.rect.x+12, self.rect.y + self.rect.h//2 - txt.get_height()//2))
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()

# Simple button like Card but using main font for bigger text
class Button(Card):
    def draw(self, surface):
        color = CARD_HOVER if self.hovered else CARD
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, (255,255,255), self.rect, 2, border_radius=10)
        txt = font.render(self.text, True, (255,255,255))
        surface.blit(txt, (self.rect.x+12, self.rect.y + self.rect.h//2 - txt.get_height()//2))

# Generic input screen runner
# fields: list of tuples (label, type) where type in {'float','int','str'}
# callback: function that receives list of parsed values and returns dict metric or raises

def run_input_screen(title, fields, callback, allow_back=True):
    # values are strings while editing
    values = ["" for _ in fields]
    selected = 0
    result = None
    error = None
    calc_card = Card('Calcular', 40, 420, 220, 36, lambda: None)
    back_card = Card('Voltar', 280, 420, 220, 36, lambda: None)
    running = True
    while running:
        screen.fill(BG)
        # Panels
        pygame.draw.rect(screen, PANEL_LEFT, (0,0, WIDTH//2, HEIGHT))
        pygame.draw.rect(screen, PANEL_RIGHT, (WIDTH//2, 0, WIDTH//2, HEIGHT))
        # Title
        title_txt = font.render(title, True, ACCENT)
        screen.blit(title_txt, (WIDTH//4 - title_txt.get_width()//2, 18))
        # Render inputs
        start_y = 70
        for i, (label, typ) in enumerate(fields):
            color = (255,255,0) if i == selected else (220,220,220)
            box_rect = pygame.Rect(20, start_y + i*48, WIDTH//2 - 40, 36)
            pygame.draw.rect(screen, (60,70,90), box_rect, border_radius=8)
            lbl = font_small.render(f"{label} ({typ}): {values[i]}", True, color)
            screen.blit(lbl, (30, start_y + i*48 + 8))
        # Buttons
        calc_card.draw(screen)
        if allow_back:
            back_card.draw(screen)
        # Results area
        pygame.draw.rect(screen, (60,70,90), (WIDTH//2+20, 50, WIDTH//2-40, HEIGHT-100), border_radius=12)
        res_title = font.render('Resultados', True, ACCENT)
        screen.blit(res_title, (WIDTH*3//4 - res_title.get_width()//2, 60))
        # show result or error
        if result:
            y = 100
            for k, v in result.items():
                v_str = f"{v:.6f}" if isinstance(v, float) else str(v)
                txt = font_small.render(f"{k}: {v_str}", True, (0,255,0))
                screen.blit(txt, (WIDTH//2 + 40, y))
                y += 24
        if error:
            txt = font_small.render(str(error), True, (255,80,80))
            screen.blit(txt, (WIDTH//2 + 40, 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(fields)
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % len(fields)
                elif event.key == pygame.K_TAB:
                    selected = (selected + 1) % len(fields)
                elif event.key == pygame.K_BACKSPACE:
                    values[selected] = values[selected][:-1]
                elif event.key == pygame.K_RETURN:
                    # attempt calculate
                    try:
                        parsed = []
                        for (label, typ), val in zip(fields, values):
                            if typ == 'float':
                                parsed.append(float(val.replace(',', '.')))
                            elif typ == 'int':
                                parsed.append(int(val))
                            else:
                                parsed.append(val)
                        result = callback(*parsed)
                        if isinstance(result, dict) and 'Erro' in result:
                            error = result['Erro']
                            result = None
                        else:
                            error = None
                    except Exception as e:
                        error = f"Erro nos dados: {e}"
                        result = None
                else:
                    if event.unicode.isprintable():
                        values[selected] += event.unicode
            elif event.type == pygame.MOUSEMOTION:
                calc_card.handle_event(event)
                back_card.handle_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if calc_card.rect.collidepoint(event.pos):
                    try:
                        parsed = []
                        for (label, typ), val in zip(fields, values):
                            if typ == 'float':
                                parsed.append(float(val.replace(',', '.')))
                            elif typ == 'int':
                                parsed.append(int(val))
                            else:
                                parsed.append(val)
                        result = callback(*parsed)
                        if isinstance(result, dict) and 'Erro' in result:
                            error = result['Erro']
                            result = None
                        else:
                            error = None
                    except Exception as e:
                        error = f"Erro nos dados: {e}"
                        result = None
                if allow_back and back_card.rect.collidepoint(event.pos):
                    return
        pygame.display.flip()

# Helper for priority models (asks number of classes then collects arrays)
def run_priority_screen(title, per_class_fields, finish_callback, needs_servers=False):
    # per_class_fields: list of tuples (label, type) that will be asked for each class
    num_classes_str = ''
    step = 0
    values_per_class = []
    servers_str = ''
    result = None
    error = None
    running = True
    back_card = Card('Voltar', 40, 500, 200, 36, lambda: None)
    while running:
        screen.fill(BG)
        pygame.draw.rect(screen, PANEL_LEFT, (0,0, WIDTH//2, HEIGHT))
        pygame.draw.rect(screen, PANEL_RIGHT, (WIDTH//2, 0, WIDTH//2, HEIGHT))
        title_txt = font.render(title, True, ACCENT)
        screen.blit(title_txt, (WIDTH//4 - title_txt.get_width()//2, 18))
        back_card.draw(screen)
        if step == 0:
            prompt = font.render(f"Quantas classes de prioridade? {num_classes_str}", True, (255,255,0))
            screen.blit(prompt, (40, 100))
        elif 1 <= step <= (int(num_classes_str) if num_classes_str.isdigit() else 0):
            idx = step - 1
            screen.blit(font.render(f"Classe {step}", True, (255,255,255)), (40, 90))
            start_y = 130
            # ensure lists exist
            while len(values_per_class) < int(num_classes_str):
                values_per_class.append(["" for _ in per_class_fields])
            for j, (lbl, typ) in enumerate(per_class_fields):
                txt = font_small.render(f"{lbl}: {values_per_class[idx][j]}", True, (255,255,255))
                screen.blit(txt, (40, start_y + j*36))
            if needs_servers:
                server_txt = font_small.render(f"Número de servidores (c): {servers_str}", True, (255,255,0))
                screen.blit(server_txt, (40, start_y + len(per_class_fields)*36 + 20))
        elif step == (int(num_classes_str) if num_classes_str.isdigit() else 0) + 1:
            screen.blit(font.render("Revisão - pressione Enter para calcular", True, (200,200,200)), (40, 100))
            if result:
                y = 150
                for k, v in result.items():
                    screen.blit(font_small.render(f"{k}: {v}", True, (0,255,0)), (40, y))
                    y += 22
            if error:
                screen.blit(font_small.render(str(error), True, (255,0,0)), (40, 150))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if step == 0:
                    if event.key == pygame.K_BACKSPACE:
                        num_classes_str = num_classes_str[:-1]
                    elif event.key == pygame.K_RETURN:
                        if num_classes_str.isdigit() and int(num_classes_str) > 0:
                            step = 1
                        else:
                            error = 'Digite um número válido de classes.'
                    else:
                        if event.unicode.isprintable():
                            num_classes_str += event.unicode
                elif 1 <= step <= int(num_classes_str):
                    idx = step - 1
                    # handle typing into fields sequentially
                    # find first empty or last field
                    row = values_per_class[idx]
                    # determine which field the user is filling: first that is incomplete
                    field_idx = 0
                    for k, v in enumerate(row):
                        # allow overwriting
                        field_idx = k
                        if v == '':
                            break
                    if event.key == pygame.K_BACKSPACE:
                        row[field_idx] = row[field_idx][:-1]
                    elif event.key == pygame.K_RETURN:
                        # move to next class
                        # if current row not empty for all fields, advance
                        if all(x != '' for x in row):
                            step += 1
                        else:
                            error = 'Preencha todos os campos da classe antes de avançar.'
                    else:
                        if event.unicode.isprintable():
                            row[field_idx] += event.unicode
                elif step == int(num_classes_str) + 1:
                    if event.key == pygame.K_RETURN:
                        # try to parse and compute
                        try:
                            n = int(num_classes_str)
                            arrs = []
                            parsed_fields = []
                            for r in values_per_class[:n]:
                                parsed = []
                                for (lbl, typ), val in zip(per_class_fields, r):
                                    if typ == 'float':
                                        parsed.append(float(val.replace(',', '.')))
                                    elif typ == 'int':
                                        parsed.append(int(val))
                                    else:
                                        parsed.append(val)
                                parsed_fields.append(parsed)
                            # transform parsed_fields into separate lists for callback convenience
                            # e.g. arrival_rates, service_times, service_vars
                            # If per_class_fields == [('Taxa de chegada (λ)','float')...] etc
                            # Build argument lists in order
                            # For common cases: arrival_rates only OR arrival_rates+service_times+vars
                            if len(per_class_fields) == 1:
                                arrival_rates = [pf[0] for pf in parsed_fields]
                                if needs_servers:
                                    raise NotImplementedError('Para este fluxo use a tela customizada')
                                result = finish_callback(arrival_rates)
                            else:
                                # multiple values per class -> unzip
                                lists = list(zip(*parsed_fields))
                                # convert tuples to lists
                                lists = [list(x) for x in lists]
                                if needs_servers:
                                    # last element expected to be servers provided separately
                                    # not supported in this simplified flow
                                    pass
                                result = finish_callback(*lists)
                            if isinstance(result, dict) and 'Erro' in result:
                                error = result['Erro']
                                result = None
                            else:
                                error = None
                        except Exception as e:
                            error = f"Erro nos dados: {e}"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_card.rect.collidepoint(event.pos):
                    return
        pygame.display.flip()

# Specific screens implemented using generic helpers

def mm1_input_screen():
    fields = [
        ("Taxa de chegada (λ)", 'float'),
        ("Taxa de serviço (μ)", 'float'),
        ("Tempo t1 para P(W > t)", 'float'),
        ("Tempo t2 para P(Wq > t)", 'float'),
        ("Número de clientes (N)", 'int'),
    ]
    def cb(lam, mu, t1, t2, n):
        return mm1_queue_metrics(lam, mu, t1, t2, n)
    run_input_screen('Modelo M/M/1', fields, cb)


def mmc_input_screen():
    fields = [
        ("Taxa de chegada (λ)", 'float'),
        ("Taxa de serviço (μ)", 'float'),
        ("Número de servidores (c)", 'int'),
        ("Tempo t1 para P(W > t)", 'float'),
        ("Tempo t2 para P(Wq > t)", 'float'),
        ("Número de clientes (N)", 'int'),
    ]
    def cb(lam, mu, c, t1, t2, n):
        return mmc_queue_metrics(lam, mu, c, t1, t2, n)
    run_input_screen('Modelo M/M/c', fields, cb)


def mm1k_input_screen():
    fields = [
        ("Taxa de chegada (λ)", 'float'),
        ("Taxa de serviço (μ)", 'float'),
        ("Capacidade máxima (K)", 'int'),
        ("Custo de espera (CE)", 'float'),
        ("Custo de atendimento (CA)", 'float'),
        ("Número de clientes (N)", 'int'),
    ]
    def cb(lam, mu, K, CE, CA, N):
        return mm1k_queue_metrics(lam, mu, K, CE, CA, N)
    run_input_screen('Modelo M/M/1/K', fields, cb)


def mmck_input_screen():
    fields = [
        ("Taxa de chegada (λ)", 'float'),
        ("Taxa de serviço (μ)", 'float'),
        ("Número de servidores (c)", 'int'),
        ("Capacidade máxima (K)", 'int'),
        ("Custo de espera (CE)", 'float'),
        ("Custo de atendimento (CA)", 'float'),
        ("Número de clientes (N)", 'int'),
    ]
    def cb(lam, mu, c, K, CE, CA, N):
        return mmc_k_queue_metrics(lam, mu, c, K, CE, CA, N)
    run_input_screen('Modelo M/M/c/K', fields, cb)


def mm1n_input_screen():
    fields = [
        ("Taxa de chegada (λ)", 'float'),
        ("Taxa de serviço (μ)", 'float'),
        ("Tamanho da população (N)", 'int'),
        ("Custo de espera (CE)", 'float'),
        ("Custo de atendimento (CA)", 'float'),
    ]
    def cb(lam, mu, N, CE, CA):
        return mm1n_queue_metrics(lam, mu, N, CE, CA)
    run_input_screen('Modelo M/M/1/N (População finita)', fields, cb)


def mmcn_input_screen():
    fields = [
        ("Taxa de chegada (λ)", 'float'),
        ("Taxa de serviço (μ)", 'float'),
        ("Número de servidores (s)", 'int'),
        ("Tamanho da população (N)", 'int'),
        ("Custo de espera (CE)", 'float'),
        ("Custo de atendimento (CA)", 'float'),
    ]
    def cb(lam, mu, s, N, CE, CA):
        return mmcn_queue_metrics(lam, mu, s, N, CE, CA)
    run_input_screen('Modelo M/M/c/N (População finita)', fields, cb)


def mg1_input_screen():
    fields = [
        ("Taxa de chegada (λ)", 'float'),
        ("Taxa de serviço (μ)", 'float'),
        ("Variância do tempo de serviço (σ²)", 'float'),
    ]
    def cb(lam, mu, sigma2):
        return mg1_queue_metrics(lam, mu, sigma2)
    run_input_screen('Modelo M/G/1', fields, cb)

# Priority screens: ask number of classes then per-class inputs

def mm1_priority_non_preemptive_input_screen():
    num_classes = ""
    arrival_rates = []
    mu_str = ""
    step = 0
    error = None
    result = None
    show_result = False

    back_card = Card('Voltar', 40, 500, 200, 36, lambda: None)

    while True:
        screen.fill(BG)
        pygame.draw.rect(screen, PANEL_LEFT, (0, 0, WIDTH // 2, HEIGHT))
        pygame.draw.rect(screen, PANEL_RIGHT, (WIDTH // 2, 0, WIDTH // 2, HEIGHT))
        screen.blit(font.render('M/M/1 Prioridade Não-Preemptiva', True, ACCENT),
                    (WIDTH//4 - 220, 20))

        back_card.draw(screen)

        # BOTÃO VOLTAR (funciona sempre)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_card.is_clicked(event.pos):
                    return

            # SE MOSTRANDO RESULTADO, NÃO ACEITA INPUT
            if show_result:
                continue

            if event.type == pygame.KEYDOWN:

                # STEP 0 — número de classes
                if step == 0:
                    if event.key == pygame.K_BACKSPACE:
                        num_classes = num_classes[:-1]
                    elif event.key == pygame.K_RETURN:
                        if num_classes.isdigit() and int(num_classes) > 0:
                            n = int(num_classes)
                            arrival_rates = [""] * n
                            step = 1
                        else:
                            error = "Digite um número válido de classes."
                    else:
                        if event.unicode.isdigit():
                            num_classes += event.unicode

                # STEP 1..N — lambdas
                elif 1 <= step <= int(num_classes):
                    idx = step - 1
                    if event.key == pygame.K_BACKSPACE:
                        arrival_rates[idx] = arrival_rates[idx][:-1]
                    elif event.key == pygame.K_RETURN:
                        if arrival_rates[idx] != "":
                            step += 1
                    else:
                        if event.unicode.isprintable():
                            arrival_rates[idx] += event.unicode

                # STEP N+1 — μ
                elif step == int(num_classes) + 1:
                    if event.key == pygame.K_BACKSPACE:
                        mu_str = mu_str[:-1]
                    elif event.key == pygame.K_RETURN:
                        try:
                            arr = [float(v.replace(",", ".")) for v in arrival_rates]
                            mu = float(mu_str.replace(",", "."))

                            result = mm1_priority_non_preemptive_metrics(arr, mu)

                            if isinstance(result, dict) and "Erro" in result:
                                error = result["Erro"]
                                result = None
                            else:
                                error = None
                                show_result = True

                        except Exception as e:
                            error = f"Erro: {e}"
                            result = None
                    else:
                        if event.unicode.isprintable():
                            mu_str += event.unicode

        # ----------- DESENHO DA INTERFACE -----------

        if not show_result:
            if step == 0:
                screen.blit(font_small.render(
                    f"Quantas classes? {num_classes}", True, (255,255,0)), (40,100))

            elif 1 <= step <= (int(num_classes) if num_classes.isdigit() else 0):
                idx = step - 1
                screen.blit(font_small.render(
                    f"Classe {step} λ: {arrival_rates[idx]}", True, (255,255,255)), (40,100))

            elif step == int(num_classes) + 1:
                screen.blit(font_small.render(
                    f"μ: {mu_str}", True, (255,255,0)), (40,100))

        else:
            if isinstance(result, dict):
                y = 150
                for classe, metrics in result.items():

                    screen.blit(font_small.render(
                        str(classe), True, (255,255,0)), (WIDTH//2 + 40, y))
                    y += 22

                    for key, value in metrics.items():
                        screen.blit(font_small.render(
                            f"{key}: {value}", True, (0,255,0)),
                            (WIDTH//2 + 60, y))
                        y += 22
                    y += 10

        if error:
            screen.blit(font_small.render(
                str(error), True, (255,0,0)), (WIDTH//2 + 40, 140))

        pygame.display.flip()

# For brevity and parity we'll implement priority screens similarly to mm1_priority_non_preemptive_input_screen
# but calling appropriate functions. Implementations are analogous and keep unified layout.

def mm1_priority_preemptive_input_screen():
    num_classes = ""
    arrival_rates = []
    mu_str = ""
    step = 0
    error = None
    result = None
    show_result = False

    back_card = Card('Voltar', 40, 500, 200, 36, lambda: None)

    while True:
        screen.fill(BG)
        pygame.draw.rect(screen, PANEL_LEFT, (0, 0, WIDTH // 2, HEIGHT))
        pygame.draw.rect(screen, PANEL_RIGHT, (WIDTH // 2, 0, WIDTH // 2, HEIGHT))
        screen.blit(font.render('M/M/1 Prioridade Preemptiva', True, ACCENT),
                    (WIDTH//4 - 220, 20))

        back_card.draw(screen)

        # BOTÃO VOLTAR (funciona em qualquer momento)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_card.is_clicked(event.pos):
                    return

            # Se estiver mostrando o resultado, ignora entrada
            if show_result:
                continue

            # TECLADO
            if event.type == pygame.KEYDOWN:

                # STEP 0 — número de classes
                if step == 0:
                    if event.key == pygame.K_BACKSPACE:
                        num_classes = num_classes[:-1]
                    elif event.key == pygame.K_RETURN:
                        if num_classes.isdigit() and int(num_classes) > 0:
                            n = int(num_classes)
                            arrival_rates = [""] * n
                            step = 1
                            error = None
                        else:
                            error = "Digite um número válido de classes."
                    else:
                        if event.unicode.isdigit():
                            num_classes += event.unicode

                # STEP 1..N — lambdas
                elif 1 <= step <= int(num_classes):
                    idx = step - 1
                    if event.key == pygame.K_BACKSPACE:
                        arrival_rates[idx] = arrival_rates[idx][:-1]
                    elif event.key == pygame.K_RETURN:
                        if arrival_rates[idx] != "":
                            step += 1
                    else:
                        if event.unicode.isprintable():
                            arrival_rates[idx] += event.unicode

                # STEP N+1 — μ
                elif step == int(num_classes) + 1:
                    if event.key == pygame.K_BACKSPACE:
                        mu_str = mu_str[:-1]
                    elif event.key == pygame.K_RETURN:
                        try:
                            arr = [float(v.replace(",", ".")) for v in arrival_rates]
                            mu = float(mu_str.replace(",", "."))

                            result = mm1_priority_preemptive_metrics(arr, mu)

                            if isinstance(result, dict) and "Erro" in result:
                                error = result["Erro"]
                                result = None
                            else:
                                error = None
                                show_result = True

                        except Exception as e:
                            error = f"Erro: {e}"
                            result = None
                    else:
                        if event.unicode.isprintable():
                            mu_str += event.unicode

        # ------------ DESENHO DA TELA --------------

        if not show_result:

            if step == 0:
                screen.blit(font_small.render(
                    f"Quantas classes? {num_classes}",
                    True, (255,255,0)
                ), (40,100))

            elif 1 <= step <= (int(num_classes) if num_classes.isdigit() else 0):
                idx = step - 1
                screen.blit(font_small.render(
                    f"Classe {step} λ: {arrival_rates[idx]}",
                    True, (255,255,255)
                ), (40,100))

            elif step == int(num_classes) + 1:
                screen.blit(font_small.render(
                    f"μ: {mu_str}",
                    True, (255,255,0)
                ), (40,100))

        else:
            # MOSTRAR RESULTADOS FORMATADOS
            if isinstance(result, dict):
                y = 150
                for classe, metrics in result.items():

                    screen.blit(font_small.render(
                        str(classe), True, (255,255,0)
                    ), (WIDTH//2 + 40, y))
                    y += 22

                    for key, value in metrics.items():
                        screen.blit(font_small.render(
                            f"{key}: {value}", True, (0,255,0)
                        ), (WIDTH//2 + 60, y))
                        y += 22

                    y += 10

        # ERRO
        if error:
            screen.blit(font_small.render(
                str(error), True, (255, 0, 0)
            ), (WIDTH//2 + 40, 140))

        pygame.display.flip()


def mg1_non_preemptive_priority_input_screen():
    num_classes = ""
    arrival_rates = []
    service_times = []
    variances = []

    step = 0
    error = None
    result = None
    show_result = False

    back_card = Card("Voltar", 40, 500, 200, 36, lambda: None)

    while True:
        screen.fill(BG)
        pygame.draw.rect(screen, PANEL_LEFT, (0, 0, WIDTH//2, HEIGHT))
        pygame.draw.rect(screen, PANEL_RIGHT, (WIDTH//2, 0, WIDTH//2, HEIGHT))
        screen.blit(font.render("M/G/1 Prioridade Não-Preemptiva (SPT)", True, ACCENT),
                    (WIDTH//4 - 260, 20))

        back_card.draw(screen)

        # ===============================
        #          EVENTOS
        # ===============================
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            # VOLTAR — funciona sempre
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_card.is_clicked(event.pos):
                    return

            # Após calcular, não aceita novos inputs
            if show_result:
                continue

            # ===============================
            #     INPUT DE TECLAS
            # ===============================
            if event.type == pygame.KEYDOWN:

                # ---- STEP 0: número de classes ----
                if step == 0:

                    if event.key == pygame.K_BACKSPACE:
                        num_classes = num_classes[:-1]

                    elif event.key == pygame.K_RETURN:
                        if num_classes.isdigit() and int(num_classes) > 0:
                            n = int(num_classes)
                            arrival_rates = [""] * n
                            service_times = [""] * n
                            variances = [""] * n
                            step = 1
                            error = None
                        else:
                            error = "Digite um número válido de classes."

                    else:
                        if event.unicode.isdigit():
                            num_classes += event.unicode

                # ---- STEPS 1..N: λ ----
                elif 1 <= step <= int(num_classes):
                    idx = step - 1

                    if event.key == pygame.K_BACKSPACE:
                        arrival_rates[idx] = arrival_rates[idx][:-1]

                    elif event.key == pygame.K_RETURN:
                        if arrival_rates[idx] != "":
                            step += 1

                    else:
                        if event.unicode.isprintable():
                            arrival_rates[idx] += event.unicode

                # ---- STEPS N+1..2N: E[S] por classe ----
                elif int(num_classes) < step <= 2 * int(num_classes):
                    idx = step - 1 - int(num_classes)

                    if event.key == pygame.K_BACKSPACE:
                        service_times[idx] = service_times[idx][:-1]

                    elif event.key == pygame.K_RETURN:
                        if service_times[idx] != "":
                            step += 1

                    else:
                        if event.unicode.isprintable():
                            service_times[idx] += event.unicode

                # ---- STEPS 2N+1..3N: Var[S] por classe ----
                elif 2 * int(num_classes) < step <= 3 * int(num_classes):
                    idx = step - 1 - 2 * int(num_classes)

                    if event.key == pygame.K_BACKSPACE:
                        variances[idx] = variances[idx][:-1]

                    elif event.key == pygame.K_RETURN:

                        # Último campo? vamos calcular
                        if idx == int(num_classes) - 1:

                            try:
                                arr = [float(v.replace(",", ".")) for v in arrival_rates]
                                es = [float(v.replace(",", ".")) for v in service_times]
                                var = [float(v.replace(",", ".")) for v in variances]

                                result = mg1_non_preemptive_priority_metrics(arr, es, var)

                                if isinstance(result, dict) and "Erro" in result:
                                    error = result["Erro"]
                                    result = None
                                else:
                                    error = None
                                    show_result = True

                            except Exception as e:
                                error = f"Erro: {e}"
                                result = None

                        else:
                            if variances[idx] != "":
                                step += 1

                    else:
                        if event.unicode.isprintable():
                            variances[idx] += event.unicode

        # ===============================
        #      DESENHO DA TELA
        # ===============================

        # ----- INPUT MODE -----
        if not show_result:

            if step == 0:
                screen.blit(font_small.render(
                    f"Quantas classes? {num_classes}", True, (255,255,0)), (40,100))

            elif 1 <= step <= int(num_classes):
                idx = step - 1
                screen.blit(font_small.render(
                    f"Classe {step} λ: {arrival_rates[idx]}",
                    True, (255,255,255)), (40, 100))

            elif int(num_classes) < step <= 2 * int(num_classes):
                idx = step - 1 - int(num_classes)
                screen.blit(font_small.render(
                    f"Classe {idx+1} E[S]: {service_times[idx]}",
                    True, (255,255,0)), (40, 100))

            elif 2 * int(num_classes) < step <= 3 * int(num_classes):
                idx = step - 1 - 2 * int(num_classes)
                screen.blit(font_small.render(
                    f"Classe {idx+1} Var[S]: {variances[idx]}",
                    True, (255,255,0)), (40, 100))

        # ----- RESULT MODE -----
        else:
            if isinstance(result, dict):
                y = 150

                for classe, metrics in result.items():

                    screen.blit(font_small.render(
                        str(classe), True, (255,255,0)
                    ), (WIDTH//2 + 40, y))
                    y += 22

                    for key, value in metrics.items():
                        screen.blit(font_small.render(
                            f"{key}: {value}",
                            True, (0,255,0)
                        ), (WIDTH//2 + 60, y))
                        y += 22

                    y += 12

        # ----- ERRO -----
        if error:
            screen.blit(font_small.render(
                str(error), True, (255,0,0)
            ), (WIDTH//2 + 40, 140))

        pygame.display.flip()


def mg1_preemptive_priority_input_screen():
    num_classes = ""
    arrival_rates = []
    service_times = []
    variances = []

    step = 0
    error = None
    result = None
    show_result = False

    back_card = Card("Voltar", 40, 500, 200, 36, lambda: None)

    while True:
        screen.fill(BG)
        pygame.draw.rect(screen, PANEL_LEFT, (0, 0, WIDTH//2, HEIGHT))
        pygame.draw.rect(screen, PANEL_RIGHT, (WIDTH//2, 0, WIDTH//2, HEIGHT))

        screen.blit(
            font.render("M/G/1 Prioridade Preemptiva (SPT)", True, ACCENT),
            (WIDTH//4 - 240, 20)
        )

        back_card.draw(screen)

        # ===================================
        #           EVENTOS
        # ===================================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            # Botão Voltar — funciona sempre
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_card.is_clicked(event.pos):
                    return

            # Após calcular o resultado, ignora inputs
            if show_result:
                continue

            # ===================================
            #           INPUT VIA TECLADO
            # ===================================
            if event.type == pygame.KEYDOWN:

                # STEP 0: número de classes
                if step == 0:
                    if event.key == pygame.K_BACKSPACE:
                        num_classes = num_classes[:-1]

                    elif event.key == pygame.K_RETURN:
                        if num_classes.isdigit() and int(num_classes) > 0:
                            n = int(num_classes)
                            arrival_rates = [""] * n
                            service_times = [""] * n
                            variances = [""] * n
                            step = 1
                            error = None
                        else:
                            error = "Digite um número válido de classes."
                    else:
                        if event.unicode.isdigit():
                            num_classes += event.unicode

                # STEP 1..N: λ
                elif 1 <= step <= int(num_classes):
                    idx = step - 1

                    if event.key == pygame.K_BACKSPACE:
                        arrival_rates[idx] = arrival_rates[idx][:-1]

                    elif event.key == pygame.K_RETURN:
                        if arrival_rates[idx] != "":
                            step += 1

                    else:
                        if event.unicode.isprintable():
                            arrival_rates[idx] += event.unicode

                # STEP N+1..2N: E[S] por classe
                elif int(num_classes) < step <= 2 * int(num_classes):
                    idx = step - 1 - int(num_classes)

                    if event.key == pygame.K_BACKSPACE:
                        service_times[idx] = service_times[idx][:-1]

                    elif event.key == pygame.K_RETURN:
                        if service_times[idx] != "":
                            step += 1

                    else:
                        if event.unicode.isprintable():
                            service_times[idx] += event.unicode

                # STEP 2N+1..3N: Var[S]
                elif 2 * int(num_classes) < step <= 3 * int(num_classes):
                    idx = step - 1 - 2 * int(num_classes)

                    if event.key == pygame.K_BACKSPACE:
                        variances[idx] = variances[idx][:-1]

                    elif event.key == pygame.K_RETURN:

                        # Se este é o último input → calcular
                        if idx == int(num_classes) - 1:
                            try:
                                arr = [float(v.replace(",", ".")) for v in arrival_rates]
                                es = [float(v.replace(",", ".")) for v in service_times]
                                var = [float(v.replace(",", ".")) for v in variances]

                                result = mg1_preemptive_priority_metrics(arr, es, var)

                                if isinstance(result, dict) and "Erro" in result:
                                    error = result["Erro"]
                                    result = None
                                else:
                                    error = None
                                    show_result = True

                            except Exception as e:
                                error = f"Erro: {e}"
                                result = None
                        else:
                            if variances[idx] != "":
                                step += 1

                    else:
                        if event.unicode.isprintable():
                            variances[idx] += event.unicode

        # ===================================
        #            DESENHO DA TELA
        # ===================================

        # -------- INPUT MODE --------
        if not show_result:

            if step == 0:
                screen.blit(font_small.render(
                    f"Quantas classes? {num_classes}", True, (255,255,0)
                ), (40,100))

            elif 1 <= step <= int(num_classes):
                idx = step - 1
                screen.blit(font_small.render(
                    f"Classe {step} λ: {arrival_rates[idx]}",
                    True, (255,255,255)
                ), (40,100))

            elif int(num_classes) < step <= 2 * int(num_classes):
                idx = step - 1 - int(num_classes)
                screen.blit(font_small.render(
                    f"Classe {idx+1} E[S]: {service_times[idx]}",
                    True, (255,255,0)
                ), (40,100))

            elif 2 * int(num_classes) < step <= 3 * int(num_classes):
                idx = step - 1 - 2 * int(num_classes)
                screen.blit(font_small.render(
                    f"Classe {idx+1} Var[S]: {variances[idx]}",
                    True, (255,255,0)
                ), (40,100))

        # -------- RESULT MODE --------
        else:
            if isinstance(result, dict):
                y = 150

                for classe, metrics in result.items():

                    screen.blit(font_small.render(
                        classe, True, (255,255,0)
                    ), (WIDTH//2 + 40, y))
                    y += 22

                    for key, value in metrics.items():
                        screen.blit(font_small.render(
                            f"{key}: {value}", True, (0,255,0)
                        ), (WIDTH//2 + 60, y))
                        y += 22

                    y += 12

        # -------- ERRO --------
        if error:
            screen.blit(font_small.render(
                str(error), True, (255,0,0)
            ), (WIDTH//2 + 40, 140))

        pygame.display.flip()


def mmc_priority_non_preemptive_input_screen():
    num_classes = ""
    arrival_rates = []
    mu_str = ""
    c_str = ""
    step = 0
    error = None
    result = None
    show_result = False

    back_card = Card("Voltar", 40, 500, 200, 36, lambda: None)

    while True:
        screen.fill(BG)

        pygame.draw.rect(screen, PANEL_LEFT, (0, 0, WIDTH//2, HEIGHT))
        pygame.draw.rect(screen, PANEL_RIGHT, (WIDTH//2, 0, WIDTH//2, HEIGHT))

        screen.blit(font.render("M/M/c Prioridade Não-Preemptiva", True, ACCENT),
                    (WIDTH//4 - 240, 20))

        back_card.draw(screen)

        # ===========================
        #      EVENTOS
        # ===========================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            # Botão voltar — funciona sempre
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_card.is_clicked(event.pos):
                    return

            # Se estamos no modo resultado → ignora input
            if show_result:
                continue

            # ---------------------------
            #   INPUT VIA TECLADO
            # ---------------------------
            if event.type == pygame.KEYDOWN:

                # STEP 0 — número de classes
                if step == 0:
                    if event.key == pygame.K_BACKSPACE:
                        num_classes = num_classes[:-1]
                    elif event.key == pygame.K_RETURN:
                        if num_classes.isdigit() and int(num_classes) > 0:
                            n = int(num_classes)
                            arrival_rates = [""] * n
                            step = 1
                            error = None
                        else:
                            error = "Digite um número válido de classes."
                    else:
                        if event.unicode.isdigit():
                            num_classes += event.unicode

                # STEP 1..N — arrival rates
                elif 1 <= step <= int(num_classes):
                    idx = step - 1
                    if event.key == pygame.K_BACKSPACE:
                        arrival_rates[idx] = arrival_rates[idx][:-1]
                    elif event.key == pygame.K_RETURN:
                        if arrival_rates[idx] != "":
                            step += 1
                    else:
                        if event.unicode.isprintable():
                            arrival_rates[idx] += event.unicode

                # STEP N+1 — μ
                elif step == int(num_classes) + 1:
                    if event.key == pygame.K_BACKSPACE:
                        mu_str = mu_str[:-1]
                    elif event.key == pygame.K_RETURN:
                        if mu_str != "":
                            step += 1
                        else:
                            error = "Digite μ."
                    else:
                        if event.unicode.isprintable():
                            mu_str += event.unicode

                # STEP N+2 — c
                elif step == int(num_classes) + 2:
                    if event.key == pygame.K_BACKSPACE:
                        c_str = c_str[:-1]
                    elif event.key == pygame.K_RETURN:

                        try:
                            arr = [float(v.replace(",", ".")) for v in arrival_rates]
                            mu = float(mu_str.replace(",", "."))
                            c = int(c_str)

                            result = mmc_priority_non_preemptive_metrics(arr, mu, c)

                            if isinstance(result, dict) and "Erro" in result:
                                error = result["Erro"]
                                result = None
                            else:
                                error = None
                                show_result = True

                        except Exception as e:
                            error = f"Erro: {e}"
                            result = None

                    else:
                        if event.unicode.isprintable():
                            c_str += event.unicode

        # ===========================
        #      DESENHO DA TELA
        # ===========================

        # INPUT MODE
        if not show_result:

            if step == 0:
                screen.blit(font_small.render(
                    f"Quantas classes? {num_classes}",
                    True, (255,255,0)), (40, 100)
                )

            elif 1 <= step <= (int(num_classes) if num_classes.isdigit() else 0):
                idx = step - 1
                screen.blit(font_small.render(
                    f"Classe {step} λ: {arrival_rates[idx]}",
                    True, (255,255,255)), (40, 100)
                )

            elif step == int(num_classes) + 1:
                screen.blit(font_small.render(
                    f"μ: {mu_str}",
                    True, (255,255,0)), (40, 100)
                )

            elif step == int(num_classes) + 2:
                screen.blit(font_small.render(
                    f"c: {c_str}",
                    True, (255,255,0)), (40, 100)
                )

        # RESULT MODE
        else:
            if isinstance(result, dict):
                y = 150

                for classe, metrics in result.items():

                    screen.blit(font_small.render(
                        str(classe),
                        True, (255,255,0)
                    ), (WIDTH//2 + 40, y))
                    y += 22

                    for key, value in metrics.items():
                        screen.blit(font_small.render(
                            f"{key}: {value}",
                            True, (0,255,0)
                        ), (WIDTH//2 + 60, y))
                        y += 22

                    y += 12

        # ERRO
        if error:
            screen.blit(font_small.render(
                str(error), True, (255,0,0)
            ), (WIDTH//2 + 40, 140))

        pygame.display.flip()


def mmc_priority_preemptive_input_screen():
    num_classes = ""
    arrival_rates = []
    mu_str = ""
    c_str = ""
    step = 0
    error = None
    result = None
    show_result = False

    back_card = Card("Voltar", 40, 500, 200, 36, lambda: None)

    while True:
        screen.fill(BG)

        pygame.draw.rect(screen, PANEL_LEFT, (0, 0, WIDTH//2, HEIGHT))
        pygame.draw.rect(screen, PANEL_RIGHT, (WIDTH//2, 0, WIDTH//2, HEIGHT))

        screen.blit(font.render("M/M/c Prioridade Preemptiva", True, ACCENT),
                    (WIDTH//4 - 200, 20))

        back_card.draw(screen)

        # ===========================
        #      EVENTOS
        # ===========================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            # Botão VOLTAR — funciona sempre
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_card.is_clicked(event.pos):
                    return

            # Se em modo RESULTADO, ignora input
            if show_result:
                continue

            # ===========================
            #     INPUT VIA TECLADO
            # ===========================
            if event.type == pygame.KEYDOWN:

                # ============= STEP 0 — número de classes
                if step == 0:
                    if event.key == pygame.K_BACKSPACE:
                        num_classes = num_classes[:-1]

                    elif event.key == pygame.K_RETURN:
                        if num_classes.isdigit() and int(num_classes) > 0:
                            n = int(num_classes)
                            arrival_rates = [""] * n
                            step = 1
                            error = None
                        else:
                            error = "Digite um número válido de classes."

                    else:
                        if event.unicode.isdigit():
                            num_classes += event.unicode

                # ============= STEP 1..N — λ de cada classe
                elif 1 <= step <= int(num_classes):
                    idx = step - 1

                    if event.key == pygame.K_BACKSPACE:
                        arrival_rates[idx] = arrival_rates[idx][:-1]

                    elif event.key == pygame.K_RETURN:
                        if arrival_rates[idx] != "":
                            step += 1

                    else:
                        if event.unicode.isprintable():
                            arrival_rates[idx] += event.unicode

                # ============= STEP N+1 — μ
                elif step == int(num_classes) + 1:

                    if event.key == pygame.K_BACKSPACE:
                        mu_str = mu_str[:-1]

                    elif event.key == pygame.K_RETURN:
                        if mu_str != "":
                            step += 1
                        else:
                            error = "Digite μ."

                    else:
                        if event.unicode.isprintable():
                            mu_str += event.unicode

                # ============= STEP N+2 — c (último input)
                elif step == int(num_classes) + 2:

                    if event.key == pygame.K_BACKSPACE:
                        c_str = c_str[:-1]

                    elif event.key == pygame.K_RETURN:

                        try:
                            arr = [float(v.replace(",", ".")) for v in arrival_rates]
                            mu = float(mu_str.replace(",", "."))
                            c = int(c_str)

                            result = mmc_priority_preemptive_metrics(arr, mu, c)

                            if isinstance(result, dict) and "Erro" in result:
                                error = result["Erro"]
                                result = None
                            else:
                                error = None
                                show_result = True  # <<< agora entra no modo resultados

                        except Exception as e:
                            error = f"Erro: {e}"
                            result = None

                    else:
                        if event.unicode.isprintable():
                            c_str += event.unicode

        # ===========================
        #      DESENHO DA TELA
        # ===========================

        # ---------- INPUT MODE ----------
        if not show_result:

            if step == 0:
                screen.blit(font_small.render(
                    f"Quantas classes? {num_classes}",
                    True, (255,255,0)
                ), (40,100))

            elif 1 <= step <= (int(num_classes) if num_classes.isdigit() else 0):
                idx = step - 1

                screen.blit(font_small.render(
                    f"Classe {step} λ: {arrival_rates[idx]}",
                    True, (255,255,255)
                ), (40,100))

            elif step == int(num_classes) + 1:
                screen.blit(font_small.render(
                    f"μ: {mu_str}",
                    True, (255,255,0)
                ), (40,100))

            elif step == int(num_classes) + 2:
                screen.blit(font_small.render(
                    f"c: {c_str}",
                    True, (255,255,0)
                ), (40,100))

        # ---------- RESULT MODE ----------
        else:
            if isinstance(result, dict):
                y = 150

                for classe, metrics in result.items():

                    screen.blit(font_small.render(
                        str(classe), True, (255,255,0)
                    ), (WIDTH//2 + 40, y))
                    y += 22

                    for key, value in metrics.items():
                        screen.blit(font_small.render(
                            f"{key}: {value}", True, (0,255,0)
                        ), (WIDTH//2 + 60, y))
                        y += 22

                    y += 12

        # ----------- ERROS -----------
        if error:
            screen.blit(font_small.render(
                str(error), True, (255,0,0)
            ), (WIDTH//2 + 40, 140))

        pygame.display.flip()


# Main menu

def main_menu():
    cards = []
    margin_x = 24
    margin_y = 18
    card_w = 440
    card_h = 44
    cols = 2
    for i, model in enumerate(MODELS):
        row = i // cols
        col = i % cols
        x = margin_x + col * (card_w + margin_x)
        y = 60 + row * (card_h + margin_y)
        card = Card(model, x, y, card_w, card_h, lambda m=model: select_model(m))
        cards.append(card)
    running = True
    
    while running:
        screen.fill(BG)
        title = font.render('Selecione o Modelo', True, ACCENT)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 18))
        for card in cards:
            card.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            for card in cards:
                card.handle_event(event)
        pygame.display.flip()

def select_model(model_name):
    mapping = {
        "Modelo M/M/1": mm1_input_screen,
        "Modelo M/M/c": mmc_input_screen,
        "Modelo M/M/1/K": mm1k_input_screen,
        "Modelo M/M/c/K": mmck_input_screen,
        "Modelo M/M/1/N (População finita)": mm1n_input_screen,
        "Modelo M/M/c/N (população finita)": mmcn_input_screen,
        "Modelo M/G/1": mg1_input_screen,
        "Modelo M/M/1 Prioridade Nao Preemptiva": mm1_priority_non_preemptive_input_screen,
        "Modelo M/M/1 Prioridade Preemptiva": mm1_priority_preemptive_input_screen,
        "Modelo M/G/1 Prioridade Nao Preemptiva": mg1_non_preemptive_priority_input_screen,
        "Modelo M/G/1 Prioridade Preemptiva": mg1_preemptive_priority_input_screen,
        "Modelo M/M/c Prioridade Nao Preemptiva": mmc_priority_non_preemptive_input_screen,
        "Modelo M/M/c Prioridade Preemptiva": mmc_priority_preemptive_input_screen,
    }
    fn = mapping.get(model_name)
    if fn:
        fn()

if __name__ == '__main__':
    main_menu()