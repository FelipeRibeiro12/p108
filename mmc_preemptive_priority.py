from decimal import Decimal, getcontext
from math import factorial

def mmc_priority_preemptive_metrics(arrival_rates, service_rate, s):
    """
    arrival_rates: lista com λ de cada classe de prioridade [λ1, λ2, ..., λn]
    service_rate: taxa de serviço μ
    s: número de servidores

    Retorna dict com métricas por classe.
    """
    getcontext().prec = 15

    service_rate = Decimal(service_rate)
    arrival_rates = [Decimal(lam) for lam in arrival_rates]
    s = int(s)

    lambda_total = sum(arrival_rates)
    rho_total = lambda_total / (service_rate * s)
    
    if rho_total >= 1:
        return {"Erro": "Sistema instável: soma das taxas de chegada excede ou iguala capacidade do servidor."}

    def erlang_c(lambd, mu, s):
        a = lambd / mu
        sum_terms = sum((a**k / Decimal(factorial(k))) for k in range(s))
        last_term = (a**s / Decimal(factorial(s))) * (s * mu) / (s * mu - lambd)
        
        return last_term / (sum_terms + last_term)

    results = {}
    for i, lam_i in enumerate(arrival_rates):
        sum_lam_i = sum(arrival_rates[j] for j in range(i + 1))

        rho = lam_i / (service_rate * s)

        Pw = erlang_c(sum_lam_i, service_rate, s)
        
        Wq = Pw / (s * service_rate - sum_lam_i)
        W = Wq + Decimal('1') / service_rate

        Lq = lam_i * Wq
        L = lam_i * W

        results[f"Classe {i + 1}"] = {
            "Taxa de Chegada (λ)": round(lam_i, 5),
            "Taxa de Ocupação da Classe (ρ)": round(rho, 5),
            "Número Médio no Sistema (L)": round(L, 5),
            "Número Médio na Fila (Lq)": round(Lq, 5),
            "Tempo Médio no Sistema (W)": round(W, 5),
            "Tempo Médio na Fila (Wq)": round(Wq, 5),
        }

    return results

"""
Modelo MMC com interrupção:

Esse código calcula métricas para filas com múltiplos servidores (c) e várias classes de prioridade, onde classes com mais prioridade interrompem o atendimento de classes inferiores.

Ele recebe:
- Taxas de chegada (λ) por classe,
- Taxa de serviço (μ),
- Número de servidores (c).

Para cada classe, retorna:
- Médias de clientes e tempos na fila e no sistema (L, Lq, W, Wq),
- Taxa de ocupação (ρ) da classe.

Se a soma das chegadas for maior ou igual à capacidade do sistema (λ_total ≥ c * μ), ele indica que o sistema é instável.
"""