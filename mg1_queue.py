def mg1_queue_metrics(arrival_rate, service_rate, sigma_squared):
    """
    Calcula as métricas para o modelo de fila M/G/1.

    Parâmetros:
    - arrival_rate (λ): Taxa média de chegada
    - service_rate (μ): Taxa média de serviço
    - sigma_squared (σ²): Variância do tempo de serviço
    """

    # Taxa de utilização (ρ)
    rho = arrival_rate / service_rate

    # Verificação de estabilidade
    if rho >= 1:
        raise ValueError("O sistema é instável (ρ ≥ 1).")

    # Probabilidade de 0 clientes no sistema (P0)
    P0 = 1 - rho

    # Número médio de clientes na fila (Lq)
    Lq = ((arrival_rate**2 * sigma_squared) + rho**2) / (2 * (1 - rho))

    # Tempo médio de espera na fila (Wq)
    Wq = Lq / arrival_rate

    # Tempo médio total no sistema (W)
    W = Wq + (1 / service_rate)

    # Número médio total de clientes no sistema (L)
    L = rho + Lq

    return {
        "\nProbabilidade de Não Esperar (P0)": P0,
        "Taxa de Ocupação (ρ)": rho,
        "Número Médio no Sistema (L)": L,
        "Número Médio na Fila (Lq)": Lq,
        "Tempo Médio no Sistema (W)": W,
        "Tempo Médio na Fila (Wq)": Wq,
    }


'''
Esse código calcula métricas de uma fila M/G/1, onde a chegada é aleatória (M),
o tempo de serviço tem distribuição geral (G), e há um servidor (1).

Ele recebe a taxa de chegada (λ), taxa de atendimento (μ) e a variância do tempo de serviço (σ²).

Retorna:

- Taxa de ocupação (ρ),
- Probabilidade de não esperar (P0),
- Médias de clientes e tempos na fila e no sistema (L, Lq, W, Wq).

Se ρ ≥ 1, o sistema é instável e ele avisa isso.
'''
