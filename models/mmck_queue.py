import math


def mmc_k_queue_metrics(arrival_rate, service_rate, num_servers, max_capacity, waiting_cost, service_cost, num_clients=0):
    """
    Calcula as métricas chave para uma fila M/M/s/K.

    Parâmetros:
        arrival_rate (float): λ, taxa média de chegada.
        service_rate (float): μ, taxa média de serviço.
        num_servers (int): s, número de servidores.
        max_capacity (int): K, capacidade máxima do sistema.
        waiting_cost (float): Custo de espera por cliente.
        service_cost (float): Custo de serviço por cliente.
        num_clients (int): Número de clientes no sistema.

    Retorna:
        dict: Métricas de desempenho do sistema.
    """

    if service_rate <= 0 or arrival_rate <= 0 or num_servers <= 0 or max_capacity <= 0:
        return {"Erro": "Todos os parâmetros devem ser maiores que zero."}

    # Intensidade de tráfego por servidor (ρ)
    rho = arrival_rate / (num_servers * service_rate)

    def factorial(n):
        return math.factorial(n)

    # Cálculo de P0 (probabilidade de sistema vazio)
    def P0_calc():
        sum1 = sum(((arrival_rate / service_rate) ** n) / factorial(n)
                   for n in range(num_servers))
        sum2 = ((arrival_rate / service_rate) ** num_servers / factorial(num_servers)) * ((1 - rho **
                                                                                           (max_capacity - num_servers + 1)) / (1 - rho)) if rho != 1 else (max_capacity - num_servers + 1)
        return 1 / (sum1 + sum2)

    P0 = P0_calc()

    # Probabilidades Pn
    Pn = []
    for num_clients in range(0, max_capacity + 1):
        if num_clients < num_servers:
            Pn_val = ((arrival_rate / service_rate) ** num_clients / factorial(num_clients)) * P0
        else:
            Pn_val = ((arrival_rate / service_rate) ** num_clients /
                      (factorial(num_servers) * num_servers ** (num_clients - num_servers))) * P0
        Pn.append(Pn_val)

    # Probabilidade de bloqueio (P_K)
    P_block = Pn[max_capacity]

    # Taxa efetiva de chegada (λ_eff)
    arrival_rate_eff = arrival_rate * (1 - P_block)

    # Tempo médio de serviço (1/μ)
    service_time = 1 / service_rate

    # Número médio na fila (Lq)
    Lq_numerator = P0 * ((arrival_rate / service_rate) ** num_servers) * rho * (1 - rho ** (max_capacity -
                                                                                            num_servers) * (max_capacity - num_servers + 1 - (max_capacity - num_servers) * rho)) if rho != 1 else 0
    Lq_denominator = factorial(num_servers) * ((1 - rho) ** 2)
    Lq = Lq_numerator / Lq_denominator if rho != 1 else 0

    # Número médio no sistema (L)
    L = sum(n * Pn[n] for n in range(max_capacity + 1))

    # Tempo médio no sistema (W)
    W = L / arrival_rate_eff if arrival_rate_eff != 0 else 0

    # Tempo médio na fila (Wq)
    Wq = Lq / arrival_rate_eff if arrival_rate_eff != 0 else 0

    # Número médio de servidores ocupados
    busy_servers = sum(min(n, num_servers) * Pn[n]
                       for n in range(max_capacity + 1))

    # Custo Total (CT)
    CT = waiting_cost * L + service_cost * num_servers

    return {
        "\nTaxa de Ocupação (ρ)": rho,
        "Probabilidade de 0 clientes (P0)": P0,
        "Probabilidade de Bloqueio (P_K)": P_block,
        "Taxa Efetiva de Chegada (lambda_eff)": arrival_rate_eff,
        "Número Médio na Fila (Lq)": Lq,
        "Tempo Médio na Fila (Wq)": Wq,
        "Número Médio no Sistema (L)": L,
        "Tempo Médio no Sistema (W)": W,
        "Tempo Médio de Serviço (1/μ)": service_time,
        "Número Médio de Servidores Ocupados": busy_servers,
        "Custo Total (CT)": CT,
        "Probabilidade de existir n clientes (Pn)": [round(p, 4) for p in Pn],
    }


'''
Esse código calcula métricas de uma fila M/M/s/K, com vários servidores, capacidade máxima limitada (K),
e chegadas e atendimentos aleatórios.

Ele recebe a taxa de chegada (λ), taxa de atendimento (μ), número de servidores (s), capacidade máxima (K),
custos de espera e serviço, e opcionalmente o número de clientes para calcular probabilidades.

Retorna:

- Taxa de ocupação por servidor (ρ),
- Probabilidade do sistema vazio (P0),
- Probabilidade de bloqueio (P_K),
- Taxa efetiva de chegada (λ_eff),
- Médias de clientes e tempos na fila/sistema (L, Lq, W, Wq),
- Número médio de servidores ocupados,
- Custo total estimado,
- Probabilidade de ter n clientes no sistema (P_n).

Se algum parâmetro for zero ou negativo, retorna erro.
'''