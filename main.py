import pygame
import sys
from models.mm1_queue import mm1_queue_metrics
from models.mmc_queue import mmc_queue_metrics
from models.mm1k_queue import mm1k_queue_metrics
from models.mmck_queue import mmc_k_queue_metrics
from models.mm1n_queue import mm1n_queue_metrics
from models.mmcn_queue import mmcn_queue_metrics
from models.mg1_queue import mg1_queue_metrics
from models.mm1_non_preemptive_priority import mm1_priority_non_preemptive_metrics
from models.mm1_preemptive_priority import mm1_priority_preemptive_metrics
from models.mg1_non_preemptive_priority import mg1_non_preemptive_priority_metrics
from models.mg1_preemptive_priority import mg1_preemptive_priority_metrics

pygame.init()
WIDTH, HEIGHT = 1000, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Teoria das Filas')
font = pygame.font.SysFont(None, 24)

BG = (245, 245, 245)             # White Smoke
PANEL_LEFT = (232, 236, 245)
PANEL_RIGHT = (232, 236, 245)    # Azul perolado
ACCENT = (0, 140, 158)           # Teal moderno
CARD = (30, 115, 216)            # Azul profissional
CARD_HOVER = (74, 174, 250)      # Azul claro interativo


MODELS = [
    "Modelo M/M/1",
    "Modelo M/M/s>1",
    "Modelo M/M/1/K",
    "Modelo M/M/s>1/K",
    "Modelo M/M/1/N",
    "Modelo M/M/s>1/N",
    "Modelo M/G/1",
    "Modelo M/M/1 Prioridade sem Interrupção",
    "Modelo M/M/1 Prioridade com Interrupção",
    "Modelo M/G/1 Prioridade sem Interrupção",
    "Modelo M/G/1 Prioridade com Interrupção"
]

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
        txt = font.render(self.text, True, (255,255,255))
        txt_x = self.rect.x + (self.rect.w - txt.get_width()) // 2
        txt_y = self.rect.y + (self.rect.h - txt.get_height()) // 2
        surface.blit(txt, (txt_x, txt_y))
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
                
class Button(Card):
    def draw(self, surface):
        color = CARD_HOVER if self.hovered else CARD
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, (255,255,255), self.rect, 2, border_radius=10)
        txt = font.render(self.text, True, (255,255,255))
        # Centraliza o texto horizontalmente e verticalmente no botão
        txt_x = self.rect.x + (self.rect.w - txt.get_width()) // 2
        txt_y = self.rect.y + (self.rect.h - txt.get_height()) // 2
        surface.blit(txt, (txt_x, txt_y))

def run_input_screen(title, fields, callback, allow_back=True):
    values = ["" for _ in fields]
    selected = 0
    result = None
    error = None
    calc_card = Card('Calcular', 40, 420, 220, 36, lambda: None)
    back_card = Card('Voltar', 280, 420, 220, 36, lambda: None)
    running = True
    while running:
        screen.fill(BG)
        
        pygame.draw.rect(screen, PANEL_LEFT, (0,0, WIDTH//2, HEIGHT))
        pygame.draw.rect(screen, PANEL_RIGHT, (WIDTH//2, 0, WIDTH//2, HEIGHT))
        
        title_txt = font.render(title, True, CARD)
        screen.blit(title_txt, (WIDTH//4 - title_txt.get_width()//2, 18))
        
        start_y = 70
        for i, (label, typ) in enumerate(fields):
            color = (48, 48, 248) if i == selected else (255,255,255)
            box_rect = pygame.Rect(20, start_y + i*48, WIDTH//2 - 40, 36)
            pygame.draw.rect(screen, (128, 128, 128), box_rect, border_radius=8)
            lbl = font.render(f"{label}: {values[i]}", True, color)
            screen.blit(lbl, (30, start_y + i*48 + 8))
        
        calc_card.draw(screen)
        if allow_back:
            back_card.draw(screen)
        
        pygame.draw.rect(screen, (128, 128, 128), (WIDTH//2+20, 50, WIDTH//2-40, HEIGHT-100), border_radius=12)
        res_title = font.render('Resultados', True, (255, 255, 255))
        screen.blit(res_title, (WIDTH*3//4 - res_title.get_width()//2, 60))
        
        if result:
            y = 100
            for k, v in result.items():
                v_str = f"{v:.6f}" if isinstance(v, float) else str(v)
                txt = font.render(f"{k}: {v_str}", True, (255, 255, 255))
                screen.blit(txt, (WIDTH//2 + 40, y))
                y += 24
        if error:
            txt = font.render(str(error), True, (255, 255,255))
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
                    main_menu()
                    return
        pygame.display.flip()

def run_priority_screen(title, fields, finish_callback, needs_servers=False):
    num_classes_str = ''
    selected = 0
    values_per_class = []
    servers_str = ''
    result = None
    error = None
    calc_card = Card('Calcular', 40, 420, 220, 36, lambda: None)
    back_card = Card('Voltar', 280, 420, 220, 36, lambda: None)
    running = True
    while running:
        screen.fill(BG)
        
        pygame.draw.rect(screen, PANEL_LEFT, (0,0, WIDTH//2, HEIGHT))
        pygame.draw.rect(screen, PANEL_RIGHT, (WIDTH//2, 0, WIDTH//2, HEIGHT))
        
        title_txt = font.render(title, True, CARD)
        screen.blit(title_txt, (WIDTH//4 - title_txt.get_width()//2, 18))
        
        if num_classes_str == '':
            prompt = font.render(f"Quantas classes de prioridade? {num_classes_str}", True, CARD)
            screen.blit(prompt, (40, 100))
        
        elif num_classes_str.isdigit() and int(num_classes_str) > 0:
            n = int(num_classes_str)
            start_y = 70
            if len(values_per_class) < n:
                for _ in range(n - len(values_per_class)):
                    values_per_class.append(["" for _ in fields])
            
            for i in range(n):
                for j, (label, typ) in enumerate(fields):
                    color = (48, 48, 248) if (i == selected // len(fields) and j == selected % len(fields)) else (255, 255, 255)
                    box_rect = pygame.Rect(20, start_y + (i*len(fields)+j)*48, WIDTH//2 - 40, 36)
                    pygame.draw.rect(screen, (128, 128, 128), box_rect, border_radius=8)
                    lbl = font.render(f"Classe {i+1} - {label}: {values_per_class[i][j]}", True, color)
                    screen.blit(lbl, (30, start_y + (i*len(fields)+j)*48 + 8))
            if needs_servers:
                server_txt = font.render(f"Número de servidores (c): {servers_str}", True, (255,255,255))
                screen.blit(server_txt, (40, start_y + n*len(fields)*48 + 20))
            
            calc_card.draw(screen)
            back_card.draw(screen)
        
        pygame.draw.rect(screen, (128, 128, 128), (WIDTH//2+20, 50, WIDTH//2-40, HEIGHT-100), border_radius=12)
        res_title = font.render('Resultados', True, (255, 255, 255))
        screen.blit(res_title, (WIDTH*3//4 - res_title.get_width()//2, 60))
        
        if result:
            y = 100
            
            if isinstance(result, dict):
                for classe, metrics in result.items():
                    screen.blit(font.render(str(classe), True, (255, 255, 255)), (WIDTH//2 + 40, y))
                    y += 22
                    for key, value in metrics.items():
                        v_str = f"{value:.6f}" if isinstance(value, float) else str(value)
                        screen.blit(font.render(f"{key}: {v_str}", True, (255,255,255)), (WIDTH//2 + 60, y))
                        y += 22
                    y += 10
            else:
                
                txt = font.render(str(result), True, (255,255,255))
                screen.blit(txt, (WIDTH//2 + 40, y))
        if error:
            txt = font.render(str(error), True, (255,255,255))
            screen.blit(txt, (WIDTH//2 + 40, 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                
                if num_classes_str == '':
                    if event.key == pygame.K_BACKSPACE:
                        num_classes_str = num_classes_str[:-1]
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_TAB:
                        pass
                    else:
                        if event.unicode.isdigit():
                            num_classes_str += event.unicode
                
                elif num_classes_str.isdigit() and int(num_classes_str) > 0:
                    n = int(num_classes_str)
                    total_fields = n * len(fields)
                    if total_fields > 0:
                        if event.key == pygame.K_DOWN or event.key == pygame.K_TAB:
                            selected = (selected + 1) % total_fields
                        elif event.key == pygame.K_UP:
                            selected = (selected - 1) % total_fields
                        elif event.key == pygame.K_BACKSPACE:
                            i = selected // len(fields)
                            j = selected % len(fields)
                            values_per_class[i][j] = values_per_class[i][j][:-1]
                        elif event.key == pygame.K_RETURN:
                            
                            if all(all(x != '' for x in row) for row in values_per_class[:n]):
                                try:
                                    parsed_fields = []
                                    for r in values_per_class[:n]:
                                        parsed = []
                                        for (lbl, typ), val in zip(fields, r):
                                            try:
                                                if typ == 'float':
                                                    parsed.append(float(val.replace(',', '.')))
                                                elif typ == 'int':
                                                    parsed.append(int(val))
                                                else:
                                                    parsed.append(val)
                                            except Exception as e:
                                                error = f"Erro nos dados: {e}"
                                                break
                                        parsed_fields.append(parsed)
                                    if len(fields) == 1:
                                        arrival_rates = [pf[0] for pf in parsed_fields]
                                        result = finish_callback(arrival_rates)
                                    else:
                                        lists = list(zip(*parsed_fields))
                                        lists = [list(x) for x in lists]
                                        result = finish_callback(*lists)
                                    if isinstance(result, dict) and 'Erro' in result:
                                        error = result['Erro']
                                        result = None
                                    else:
                                        error = None
                                except Exception as e:
                                    error = f"Erro nos dados: {e}"
                        else:
                            i = selected // len(fields)
                            j = selected % len(fields)
                            if event.unicode.isprintable():
                                values_per_class[i][j] += event.unicode
            elif event.type == pygame.MOUSEMOTION:
                calc_card.handle_event(event)
                back_card.handle_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if num_classes_str.isdigit() and int(num_classes_str) > 0:
                    n = int(num_classes_str)
                    if calc_card.rect.collidepoint(event.pos):
                        if n > 0 and all(all(x != '' for x in row) for row in values_per_class[:n]):
                            try:
                                parsed_fields = []
                                for r in values_per_class[:n]:
                                    parsed = []
                                    for (lbl, typ), val in zip(fields, r):
                                        try:
                                            if typ == 'float':
                                                parsed.append(float(val.replace(',', '.')))
                                            elif typ == 'int':
                                                parsed.append(int(val))
                                            else:
                                                parsed.append(val)
                                        except Exception as e:
                                            error = f"Erro nos dados: {e}"
                                            break
                                    parsed_fields.append(parsed)
                                if len(fields) == 1:
                                    arrival_rates = [pf[0] for pf in parsed_fields]
                                    result = finish_callback(arrival_rates)
                                else:
                                    lists = list(zip(*parsed_fields))
                                    lists = [list(x) for x in lists]
                                    result = finish_callback(*lists)
                                if isinstance(result, dict) and 'Erro' in result:
                                    error = result['Erro']
                                    result = None
                                else:
                                    error = None
                            except Exception as e:
                                error = f"Erro nos dados: {e}"
                if back_card.rect.collidepoint(event.pos):
                    main_menu()
                    return
        pygame.display.flip()

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
    run_input_screen('Modelo M/M/s>1', fields, cb)


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
    run_input_screen('Modelo M/M/s>1/K', fields, cb)


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
    run_input_screen('Modelo M/M/s>1/N (População finita)', fields, cb)

def mg1_input_screen():
    fields = [
        ("Taxa de chegada (λ)", 'float'),
        ("Taxa de serviço (μ)", 'float'),
        ("Variância do tempo de serviço (σ²)", 'float'),
    ]
    def cb(lam, mu, sigma2):
        return mg1_queue_metrics(lam, mu, sigma2)
    run_input_screen('Modelo M/G/1', fields, cb)
    
def mm1_priority_non_preemptive_input_screen():
    fields = [
        ("Taxa de chegada (λ)", 'float'),
        ("Taxa de serviço (μ)", 'float'),
        ]
    def cb(arrival_rates, service_rate):
        return mm1_priority_non_preemptive_metrics(arrival_rates, service_rate)
    run_priority_screen("M/M/1 Prioridade sem Interrupção", fields, cb)
    
def mm1_priority_preemptive_input_screen():
    def cb(arrival_rates, mu):
        return mm1_priority_preemptive_metrics(arrival_rates, mu)
    run_priority_screen(
        title="M/M/1 Prioridade com Interrupção",
        fields=[("Taxa de chegada (λ)", 'float')],
        finish_callback=cb,
        needs_servers=False
    )
    
def mg1_non_preemptive_priority_input_screen():
    def cb(arrival_rates, es, var):
        return mg1_non_preemptive_priority_metrics(arrival_rates, es, var)
    run_priority_screen(
        title="M/G/1 Prioridade sem Interrupção",
        fields=[
            ("Taxa de chegada (λ)", 'float'),
            ("Tempo médio de serviço E[S]", 'float'),
            ("Variância do serviço Var[S]", 'float')
        ],
        finish_callback=cb,
        needs_servers=False
    )
    
def mg1_preemptive_priority_input_screen():
    def cb(arrival_rates, es, var):
        return mg1_preemptive_priority_metrics(arrival_rates, es, var)
    run_priority_screen(
        title="M/G/1 Prioridade com Interrupção",
        fields=[
            ("Taxa de chegada (λ)", 'float'),
            ("Tempo médio de serviço E[S]", 'float'),
            ("Variância do serviço Var[S]", 'float')
        ],
        finish_callback=cb,
        needs_servers=False
    )

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
        title = font.render('Selecione o Modelo', True, CARD)
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
        "Modelo M/M/s>1": mmc_input_screen,
        "Modelo M/M/1/K": mm1k_input_screen,
        "Modelo M/M/s>1/K": mmck_input_screen,
        "Modelo M/M/1/N (População finita)": mm1n_input_screen,
        "Modelo M/M/s>1/N (população finita)": mmcn_input_screen,
        "Modelo M/G/1": mg1_input_screen,
        "Modelo M/M/1 Prioridade sem Interrupção": mm1_priority_non_preemptive_input_screen,
        "Modelo M/M/1 Prioridade com Interrupção": mm1_priority_preemptive_input_screen,
        "Modelo M/G/1 Prioridade sem Interrupção": mg1_non_preemptive_priority_input_screen,
        "Modelo M/G/1 Prioridade com Interrupção": mg1_preemptive_priority_input_screen
    }
    
    fn = mapping.get(model_name)
    if fn:
        fn()

if __name__ == '__main__':
    main_menu()