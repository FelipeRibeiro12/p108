from decimal import Decimal, getcontext
from math import factorial

def mmc_priority_non_preemptive_metrics(arrival_rates, service_rate, servers):
    """
    arrival_rates: lista com λ de cada classe de prioridade [λ1, λ2, ..., λn]
    service_rate: taxa de serviço μ
    servers: número de servidores s
    
    Retorna dict com métricas por classe com base na fórmula correta de W_i.
    """
    getcontext().prec = 30 
    arrival_rates = [Decimal(str(lam)) for lam in arrival_rates]
    mu = Decimal(str(service_rate))
    s = int(servers)

    lambda_total = sum(arrival_rates)
    r = lambda_total / mu

    if lambda_total >= s * mu:
        return {"Erro": "Sistema instável: λ_total ≥ s * μ"}
    
    s_fact = Decimal(factorial(s))
    
    # Cálculo da soma de r^j / j! de j=0 até s-1
    sum_rj_by_jfact = sum([(r ** j) / Decimal(factorial(j)) for j in range(s)])
    r_pow_s = r ** s

    results = {}

    for i in range(len(arrival_rates)):
        lambda_i = arrival_rates[i]

        # Somatórios acumulados
        soma_ate_i_minus_1 = sum(arrival_rates[:i]) if i > 0 else Decimal(0)
        soma_ate_i = sum(arrival_rates[:i+1])

        termo1 = (s_fact * (s * mu - lambda_total) / r_pow_s) * sum_rj_by_jfact + s * mu
        termo2 = (Decimal(1) - soma_ate_i_minus_1 / (s * mu))
        termo3 = (Decimal(1) - soma_ate_i / (s * mu))

        try:
            Wq_i = Decimal(1) / (termo1 * termo2 * termo3)
        except ZeroDivisionError:
            return {"Erro": f"Divisão por zero na classe {i+1}. Verifique os parâmetros."}

        Wi = Wq_i + (Decimal(1) / mu)
        Lq_i = lambda_i * Wq_i
        L_i = lambda_i * Wi

        results[f"Classe {i+1}"] = {
            "Taxa de Chegada (λ)": float(lambda_i),
            "Tempo Médio no Sistema (W)": float(Wi),
            "Tempo Médio na Fila (Wq)": float(Wq_i),
            "Número Médio na Fila (Lq)": float(Lq_i),
            "Número Médio no Sistema (L)": float(L_i)
        }

    return results

"""
Modelo MMC sem interrupção:

Esse código calcula métricas para filas com múltiplos servidores (c) e múltiplas classes de prioridade, onde as classes com mais prioridade são atendidas antes, mas não interrompem quem já está sendo atendido.

Ele recebe:
- Taxas de chegada (λ) por classe,
- Taxa de serviço (μ),
- Número de servidores (c).

Retorna, por classe:

- Médias de clientes e tempos na fila e no sistema (L, Lq, W, Wq),
- Taxa de chegada da classe (λ).

Se a soma das chegadas for maior ou igual à capacidade do sistema (λ_total ≥ c * μ), o código avisa que o sistema é instável.

"""