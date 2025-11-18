def mm1k_queue_metrics(arrival_rate, service_rate, max_capacity, waiting_cost, service_cost, num_clients):
    """
    Calcular as métricas chave para uma fila M/M/1/K.

    Parâmetros:
        arrival_rate (float): λ, a taxa média de chegada.
        service_rate (float): μ, a taxa média de serviço.
        max_capacity (int): K, a capacidade máxima do sistema.
        waiting_cost (float): Custo de espera por cliente.
        service_cost (float): Custo de serviço por cliente.
        num_clients (int): N, o número de clientes no sistema.

    Retorna:
        dict: Um dicionário contendo as métricas calculadas.
    """
    if service_rate <= 0 or arrival_rate <= 0:
        return {"Erro": "Taxas de chegada e serviço devem ser maiores que zero."}

    rho = arrival_rate / service_rate  # Intensidade de tráfego (ρ)

    # Calcular P0 (constante de normalização)
    if rho == 1:
        P0 = 1 / (max_capacity + 1)
    else:
        P0 = (1 - rho) / (1 - rho**(max_capacity + 1))

    # Calcular Pn para todos os n
    Pn = []
    for n in range(max_capacity + 1):
        Pn.append(P0 * (rho**n))

    # Probabilidade de bloqueio (P_block = Pk)
    P_block = Pn[max_capacity]

    # Taxa efetiva de chegada
    lambda_eff = arrival_rate * (1 - P_block)

    # Número médio de clientes no sistema (L)
    if rho == 1:
        L = max_capacity / 2
    else:
        numerator = rho / (1 - rho)
        correction = ((max_capacity + 1) * (rho**(max_capacity + 1))) / (1 - rho**(max_capacity + 1))
        L = numerator - correction

    # Tempo médio no sistema (W)
    W = L / lambda_eff if lambda_eff > 0 else 0

    # Número médio de clientes na fila (Lq)
    L_q = L - (1 - P0)

    # Tempo médio de espera na fila (Wq)
    W_q = L_q / lambda_eff if lambda_eff > 0 else 0
    
    # Probabilidade de existir n clientes no sistema (Pn) apenas para o n informado
    n = int(num_clients)
    if n > max_capacity:
        Pn_val = 0.0
    else:
        Pn_val = round(P0 * (rho**n), 4)
    # Custo Total (CT) 
    CT = waiting_cost * L + service_cost * 1

    return {
        "\nTaxa de Ocupação (ρ)": rho,
        "Probabilidade de Não Ocupação (P0)": P0,
        "Probabilidade de Bloqueio (P_block)": P_block,
        "Taxa Efetiva de Chegada (λ_eff)": lambda_eff,
        "Número Médio no Sistema (L)": L,
        "Número Médio na Fila (Lq)": L_q,
        "Tempo Médio no Sistema (W)": W,
        "Tempo Médio na Fila (Wq)": W_q,
        "Custo Total (CT)": CT,
        f"Probabilidade de {n} clientes no sistema (Pn)": Pn_val
    }

'''
Esse código calcula métricas de uma fila M/M/1/K, com um servidor, chegadas e atendimentos aleatórios, e capacidade máxima K.

Ele recebe a taxa de chegada (λ), a taxa de atendimento (μ), a capacidade máxima (K), custos de espera e serviço,
e o número de clientes (n) para calcular probabilidades.

Retorna:

- Ocupação do sistema (ρ),
- Probabilidade do sistema vazio (P0),
- Probabilidade de bloqueio (P_block),
- Taxa efetiva de chegada (λ_eff),
- Médias de clientes e tempos na fila/sistema (L, Lq, W, Wq),
- Custo total estimado,
- Probabilidade de existir n clientes no sistema (P_n).

Se as taxas forem inválidas (≤ 0), retorna erro.
'''