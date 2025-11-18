import math


def mm1_queue_metrics(arrival_rate, service_rate, waiting_time_w, waiting_time_wq, num_clients):
    """
    Calcular as métricas chave para uma fila M/M/1.

    Parâmetros:
        arrival_rate (float): λ, a taxa média de chegada.
        service_rate (float): μ, a taxa média de serviço.
        waiting_time_w (float): Tempo t1 para cálculo de P(W > t).
        waiting_time_wq (float): Tempo t2 para cálculo de P(Wq > t).

    Retorna:
        dict: Um dicionário contendo as métricas calculadas.
    """
    
    if service_rate <= arrival_rate:
        return {"Erro": "O sistema é instável (λ >= μ)."}

    # Intensidade de tráfego (ρ)
    # ρ = λ / μ
    rho = arrival_rate / service_rate

    # Número médio de clientes no sistema (L)
    # L = ρ / (1 - ρ)
    L = rho / (1 - rho)

    # Número médio de clientes na fila (Lq)
    # Lq = ρ^2 / (1 - ρ)
    L_q = (rho ** 2) / (1 - rho)

    # Tempo médio que um cliente passa no sistema (W)
    # W = 1 / (μ - λ)
    W = 1 / (service_rate - arrival_rate)

    # Tempo médio de espera na fila (Wq)
    # Wq = ρ / (μ - λ)
    W_q = rho / (service_rate - arrival_rate)

    # Probabilidade de que um cliente não precise esperar (P0)
    # P_0 = 1 - ρ
    P_0 = 1 - rho

    # Probabilidade do sistema estar ocioso (P(n=0)) = P_0
    P_0_final = P_0

    # Probabilidade do sistema estar ocupado (P(n > 0)) = 1 - P_0
    P_occupied = 1 - P_0_final

    # t >= 0
    if waiting_time_w < 0 or waiting_time_wq < 0:
        return {"Erro": "Os tempos de espera devem ser maiores ou iguais a zero."}
    
    
    # Probabilidade de W > t (P(W > t))
    P_W_greater_t = math.exp(-service_rate * (1 - rho) * waiting_time_w)

    # Probabilidade de W_q > t (P(W_q > t))
    P_Wq_greater_t = rho * math.exp(-service_rate * (1 - rho) * waiting_time_wq)
    
    # Garantir que num_clients é inteiro
    try:
        num_clients_int = int(num_clients)
    except Exception:
        return {"Erro": "O número de clientes deve ser um inteiro."}
    if num_clients_int < 1:
        return {"Erro": "O número de clientes deve ser maior ou igual a 1."}
    # Calcular apenas para o cliente n (num_clients_int)
    pn_queue = 1 - rho**(num_clients_int + 1)
    pn_system = (rho**num_clients_int) * (1-rho)

    results = {
        "Probabilidade de Não Esperar (P0)": P_0,
        "Taxa de Ocupação (ρ)": rho,
        "Número Médio no Sistema (L)": L,
        "Número Médio na Fila (Lq)": L_q,
        "Tempo Médio no Sistema (W)": W,
        "Tempo Médio na Fila (Wq)": W_q,
        "Probabilidade de o Sistema Ocioso (P(n=0))": P_0_final,
        "Probabilidade de o Sistema Ocupado (P(n>0))": P_occupied,
        "Probabilidade de W > t": P_W_greater_t,
        "Probabilidade de Wq > t": P_Wq_greater_t,
        f"Probabilidade de {num_clients_int} clientes na fila": pn_queue,
        f"Probabilidade de {num_clients_int} clientes no sistema": pn_system
    }

    return results

'''
Esse código calcula métricas de uma fila M/M/1, com um servidor e chegadas e atendimentos aleatórios.

Ele recebe a taxa de chegada (λ), a taxa de atendimento (μ) e dois tempos para cálculo de probabilidades.

Retorna:

- Ocupação do sistema (ρ),
- Médias de clientes e tempos na fila/sistema (L, Lq, W, Wq),
- Probabilidades de esperar ou não na fila/sistema

Se λ ≥ μ, o sistema é instável e ele avisa isso.

Wq = λ/μ(μ-λ)
Lq = λ * Wq
bskr = -b +- sqrt(b**2 - 4ac)/2a
'''