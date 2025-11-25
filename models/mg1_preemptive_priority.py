from decimal import Decimal, getcontext

def mg1_preemptive_priority_metrics(arrival_rates, service_times, service_variances):
    """
    Calcula métricas para uma fila M/G/1 com prioridade preemptiva.

    Parâmetros:
    - arrival_rates: lista de taxas de chegada (λ) para cada classe de prioridade (ordem crescente de prioridade)
    - service_times: lista de tempos médios de serviço (E[S]) para cada classe
    - service_variances: lista de variâncias dos tempos de serviço (Var[S]) para cada classe

    Retorna:
    - dicionário com métricas por classe: Classe 1, Classe 2, ...
    """
    getcontext().prec = 10

    n = len(arrival_rates)
    if not (len(service_times) == len(service_variances) == n):
        return {"Erro": "Listas de entrada devem ter o mesmo comprimento."}

    # Conversão para Decimal
    arrival_rates = [Decimal(str(l)) for l in arrival_rates]
    service_times = [Decimal(str(s)) for s in service_times]
    service_variances = [Decimal(str(v)) for v in service_variances]

    # Utilizações individuais e total
    utilizacoes = [arrival_rates[i] * service_times[i] for i in range(n)]
    rho_total = sum(utilizacoes)

    if rho_total >= 1:
        return {"Erro": "Sistema instável: soma das utilizações ≥ 1."}

    # E[S²] = Var[S] + (E[S])²
    ES2 = [service_variances[i] + service_times[i] ** 2 for i in range(n)]

    results = {}
    for i in range(n):
        λi = arrival_rates[i]
        ES_i = service_times[i]
        ES2_i = ES2[i]

        # Soma das utilizações de classes de prioridade ≥ i
        rho_ge_i = sum(utilizacoes[j] for j in range(i, n))

        # Numerador e denominador da fórmula de Wq para preemptiva
        numerator = sum(arrival_rates[j] * ES2[j] for j in range(i, n))
        denominator = 2 * (1 - rho_ge_i)

        Wq = numerator / denominator
        W = Wq + ES_i
        L = λi * W
        Lq = L - λi * ES_i  # ou Lq = λi * Wq

        results[f"Classe {i + 1}"] = {
            "Taxa de Chegada (λ)": round(λi, 2),
            "Tempo Médio de Serviço (E[S])": round(ES_i, 2),
            "Variância do Serviço (Var[S])": round(service_variances[i], 2),
            "Taxa de Ocupação (ρ)": round(utilizacoes[i], 2),
            "Tempo Médio na Fila (Wq)": round(Wq, 2),
            "Tempo Médio no Sistema (W)": round(W, 2),
            "Número Médio no Sistema (L)": round(L, 2),
            "Número Médio na Fila (Lq)": round(Lq, 2)
        }

    return results

"""

Modelo MG1 com interrupção:

Esse código calcula métricas para  fila M/G/1 com várias classes de prioridade, onde uma classe mais prioritária pode interromper o atendimento de uma menos prioritária.

Ele recebe:
- As taxas de chegada (λ),
- Os tempos médios de serviço (E[S]),
- As variâncias dos tempos de serviço (Var[S]),
para cada classe, em ordem de prioridade.

Retorna, por classe:

- Médias de clientes e tempos na fila e no sistema (L, Lq, W, Wq),
- Utilização do servidor (ρ),
- Dados básicos da classe (λ, E[S], Var[S]).

Se a soma das utilizações for ≥ 1, o código indica que o sistema é instável.

"""