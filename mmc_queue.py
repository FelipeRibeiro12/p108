import math


def mmc_queue_metrics(arrival_rate, service_rate, num_servers, waiting_time_w, waiting_time_wq, num_clients):
    """
    Calcular as métricas chave para uma fila M/M/c.

    Parâmetros:
        arrival_rate (float): λ, a taxa média de chegada.
        service_rate (float): μ, a taxa média de serviço.
        num_servers (int): c, o número de servidores.
        waiting_time_w (float): Tempo t1 para cálculo de P(W > t).
        waiting_time_wq (float): Tempo t2 para cálculo de P(Wq > t).
        num_clients (int): N, o número de clientes no sistema.

    Retorna:
        dict: Um dicionário contendo as métricas calculadas.
    """
    if service_rate * num_servers <= arrival_rate:
        return {"Erro": "O sistema é instável (λ >= c * μ)."}

    # Intensidade de tráfego por servidor (ρ)
    # ρ = λ / (c * μ)
    rho = arrival_rate / (num_servers * service_rate)

    # Probabilidade de não haver clientes no sistema (P0)
    sum_terms = sum((arrival_rate / service_rate) ** n /
                    math.factorial(n) for n in range(num_servers))
    last_term = ((arrival_rate / service_rate) ** num_servers /
                 math.factorial(num_servers)) * (1 / (1 - rho))
    P0 = 1 / (sum_terms + last_term)

    # Probabilidade de formação de fila (P_queue)
    P_queue = (P0 * ((arrival_rate / service_rate) ** num_servers) /
               math.factorial(num_servers)) * (1 / (1 - rho))

    # Número médio na fila (Lq)
    L_q = P_queue * rho / (1 - rho)

    # Número médio no sistema (L)
    L = L_q + arrival_rate / service_rate

    # Tempo médio de espera na fila (Wq)
    W_q = L_q / arrival_rate

    # Tempo médio no sistema (W)
    W = W_q + 1 / service_rate

    # t >= 0
    if waiting_time_w < 0 or waiting_time_wq < 0:
        return {"Erro": "Os tempos de espera devem ser maiores ou iguais a zero."}

    # Probabilidade de W > t (P(W > t))
    exp_term_w = math.exp(-service_rate * waiting_time_w)
    bracket_numerator = 1 - math.exp(-service_rate * waiting_time_w * (num_servers - 1 - (arrival_rate / service_rate)))
    bracket_denominator = num_servers - 1 - (arrival_rate / service_rate)

    if bracket_denominator == 0:
        P_W_greater_t = exp_term_w
    else:
        P_W_greater_t = exp_term_w * (1 + (P0 * ((arrival_rate / service_rate) ** num_servers) /
                                        (math.factorial(num_servers) * (1 - rho))) *
                                    (bracket_numerator / bracket_denominator))


    # Calcular P(Wq = 0) = soma das probabilidades de 0 até s-1 clientes
    P_Wq_equals_0 = sum(((arrival_rate/service_rate) ** n /
                        math.factorial(n)) * P0 for n in range(num_servers))

    # Probabilidade de Wq > t (P(Wq > t))
    P_Wq_greater_t = (1 - P_Wq_equals_0) * math.exp(-service_rate *
                                                    (num_servers - rho * num_servers) * waiting_time_wq)

    # Probabilidade de ter n clientes no sistema (P_n) para o n informado
    n = int(num_clients)
    if n < num_servers:
        P_n = (math.pow(arrival_rate / service_rate, n) /
               math.factorial(n)) * P0
    else:
        P_n = (math.pow(arrival_rate / service_rate, n) /
               (math.factorial(num_servers) * math.pow(num_servers, n - num_servers))) * P0

    return {
        "\nTaxa de Ocupação (ρ)": rho,
        "Probabilidade de Fila (P_queue)": P_queue,
        "Probabilidade do sistema estar vazio (P0)": P0,
        "Número Médio na Fila (Lq)": L_q,
        "Número Médio no Sistema (L)": L,
        "Tempo Médio na Fila (Wq)": W_q,
        "Tempo Médio no Sistema (W)": W,
        "Probabilidade de W > t": P_W_greater_t,
        "Probabilidade de Wq > t": P_Wq_greater_t,
        f"Probabilidade de {n} clientes no sistema (P_n)": P_n
    }


'''
Esse código calcula métricas de uma fila M/M/s, com vários servidores e chegadas e atendimentos aleatórios.

Ele recebe a taxa de chegada (λ), a taxa de atendimento (μ), o número de servidores (s), dois tempos para cálculo de probabilidades
e o número de clientes (n) para calcular a probabilidade de ter n clientes no sistema.

Retorna:

- Ocupação do sistema por servidor (ρ),
- Probabilidade de formação de fila (P_queue),
- Médias de clientes e tempos na fila/sistema (L, Lq, W, Wq),
- Probabilidades de esperar ou não,
- Probabilidade de ter n clientes no sistema (P_n).

Se λ ≥ s * μ, o sistema é instável e ele avisa isso.
'''
