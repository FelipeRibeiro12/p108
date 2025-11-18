def mm1n_queue_metrics(arrival_rate, service_rate, population_size, waiting_cost, service_cost):
    '''
    Modelo M/M/1 com população finita
    
    Parâmetros:
        arrival_rate (float): λ - taxa de chegada.
        service_rate (float): μ - taxa de serviço.
        population_size (int): N - tamanho da população (capacidade do sistema).
        waiting_cost (float): CE - custo de espera por cliente.
        service_cost (float): CA - custo de atendimento por cliente.
        
    Retorna:
        dict: Métricas da fila M/M/1/N
    '''
    
    if service_rate <= arrival_rate:
        return {"Erro": "O sistema é instável (λ >= μ)."}

    # Inicializa as probabilidades de estado
    probabilities = [1.0]  # P0 começa em 1.0 e será ajustado mais tarde
    normalization_constant = 1.0

    # Calcula as probabilidades de estado
    for n in range(1, population_size + 1):
        p_n = probabilities[n - 1] * (arrival_rate * (population_size - (n - 1))) / service_rate
        probabilities.append(p_n)
        normalization_constant += p_n

    # Normaliza as probabilidades
    probabilities = [p / normalization_constant for p in probabilities]

    # Número médio de clientes no sistema (L)
    L = sum(n * probabilities[n] for n in range(population_size + 1))
    
    # Número médio de clientes na fila (Lq)
    Lq = L - (1 - probabilities[0])
    
    # Taxa de processamento (T)
    lambda_eff = arrival_rate * (population_size - L)
    
    # Tempo médio no sistema (W) 
    W = L / lambda_eff
    
    # Tempo médio na fila (Wq)
    Wq = Lq / lambda_eff
    
    # Custo Total (CT) 
    CT = waiting_cost * L + service_cost * 1 

    # Probabilidade de existir n clientes no sistema (Pn) apenas para o n informado
    n = population_size
    if n > population_size:
        Pn_val = 0.0
    else:
        Pn_val = round(probabilities[n], 4)
    return {
        "\nNúmero Médio no Sistema (L)": L,
        "Número Médio na Fila (Lq)": Lq,
        "Taxa de Processamento (T)": lambda_eff,
        "Tempo Médio no Sistema (W)": W,
        "Tempo Médio na Fila (Wq)": Wq,
        "Probabilidade de Inatividade (P0)": probabilities[0],
        "Custo Total (CT)": CT,
        f"Probabilidade de {n} clientes no sistema (Pn)": Pn_val
    }

'''
Esse código calcula métricas de uma fila M/M/1 com população limitada (N clientes no total).

Ele recebe a taxa de chegada (λ), a taxa de atendimento (μ), o tamanho da população (N), custo de espera por cliente e custo de atendimento.

Retorna:

- Médias de clientes e tempos na fila/sistema (L, Lq, W, Wq),
- Taxa efetiva de processamento (λ_eff),
- Probabilidade do sistema estar vazio (P0),
- Custo total estimado,
- Probabilidades normalizadas de cada estado.

Se λ ≥ μ, o sistema é instável e avisa isso.

'''