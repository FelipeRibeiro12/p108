import math

def mmcn_queue_metrics(arrival_rate, service_rate, num_servers, population_size, waiting_cost, service_cost):
    """
    Modelo M/M/s/N

    Parâmetros:
        arrival_rate (float): λ - taxa de chegada.
        service_rate (float): μ - taxa de serviço.
        num_servers (int): s - número de servidores.
        population_size (int): N - tamanho da população (capacidade do sistema).
        waiting_cost (float): CE - custo de espera por cliente.
        service_cost (float): CA - custo de atendimento por cliente.

    Retorna:
        dict: Métricas da fila M/M/s/N
    """
    rho = (population_size * arrival_rate) / (num_servers * service_rate)

    # Cálculo de P0 (probabilidade do sistema vazio)
    # Primeira soma: n=0 até s-1
    sum1 = 0
    for n in range(min(num_servers, population_size + 1)):
        if population_size >= n:
            factorial_term = math.factorial(
                population_size) / (math.factorial(population_size - n) * math.factorial(n))
            sum1 += factorial_term * ((arrival_rate/service_rate) ** n)

    # Segunda soma: n=s até N
    sum2 = 0
    if population_size >= num_servers:
        for n in range(num_servers, population_size + 1):
            factorial_term = math.factorial(population_size) / (math.factorial(
                population_size - n) * math.factorial(num_servers) * (num_servers ** (n - num_servers)))
            sum2 += factorial_term * ((arrival_rate/service_rate) ** n)

    P0 = 1 / (sum1 + sum2)

    # Probabilidade de bloqueio (sistema cheio)
    def Pn(n):
        if n > population_size or n < 0:
            return 0
        elif n <= num_servers:
            factorial_term = math.factorial(
                population_size) / (math.factorial(population_size - n) * math.factorial(n))
            return factorial_term * ((arrival_rate/service_rate) ** n) * P0
        else:
            factorial_term = math.factorial(population_size) / (math.factorial(
                population_size - n) * math.factorial(num_servers) * (num_servers ** (n - num_servers)))
            return factorial_term * ((arrival_rate/service_rate) ** n) * P0

    probabilities = [Pn(n) for n in range(population_size + 1)]

    # Número médio de clientes no sistema (L)
    L = sum(n * Pn(n) for n in range(1, population_size + 1))

    # Número médio de clientes na fila (Lq)
    L_q = L - (arrival_rate/service_rate) * (population_size - L)

    # Taxa efetiva de chegada (clientes realmente atendidos)
    lambda_eff = arrival_rate * (population_size - L)

    # Tempo médio no sistema (W)
    W = L / lambda_eff if lambda_eff > 0 else 0

    # Tempo médio na fila (Wq)
    W_q = L_q / lambda_eff if lambda_eff > 0 else 0

    # Custo Total (CT)
    CT = waiting_cost * L + service_cost * num_servers

    # Probabilidade de existir n clientes no sistema (Pn) apenas para o n informado
    n = population_size
    if n > population_size:
        Pn_val = 0.0
    else:
        Pn_val = round(probabilities[n], 4)
    return {
        "\nTaxa de Ocupação (ρ)": rho,
        "Probabilidade de Inatividade (P0)": P0,
        "Número Médio no Sistema (L)": L,
        "Taxa de Processamento (lambda_eff)": lambda_eff,
        "Número Médio na Fila (Lq)": L_q,
        "Tempo Médio no Sistema (W)": W,
        "Tempo Médio na Fila (Wq)": W_q,
        "Custo Total (CT)": CT,
        f"Probabilidade de {n} clientes no sistema (Pn)": Pn_val
    }


'''
Esse código calcula métricas de uma fila M/M/s/N, com vários servidores e população limitada (N clientes no total).

Ele recebe a taxa de chegada (λ), taxa de atendimento (μ), número de servidores (s), tamanho da população (N), custo de espera e custo de atendimento.

Retorna:

- Taxa de ocupação (ρ),
- Probabilidade do sistema vazio (P0),
- Taxa efetiva de chegada (clientes que entram de fato),
- Médias de clientes e tempos na fila/sistema (L, Lq, W, Wq),
- Custo total estimado,
- Probabilidades normalizadas de cada estado.

Esse modelo considera que o sistema tem capacidade limitada, então há chance de bloqueio se estiver cheio.
'''
