from decimal import Decimal, getcontext
def mm1_priority_preemptive_metrics(arrival_rates, service_rate):
    """
    arrival_rates: lista com λ de cada classe de prioridade [λ1, λ2, ..., λn]
    service_rate: taxa de serviço μ
    s: número de canais (servidores)

    Retorna dict com métricas por classe.
    """
    
    getcontext().prec = 10  

    service_rate = Decimal(service_rate)
    arrival_rates = [Decimal(lam) for lam in arrival_rates]

    rho_total = sum(lam / service_rate for lam in arrival_rates)
    if rho_total >= 1:
        return {"Erro": "Sistema instável: soma das taxas de chegada excede ou iguala capacidade do servidor."}

    results = {}
    
    for i, lam_i in enumerate(arrival_rates):
        sum_lam_i = sum(arrival_rates[j] for j in range(i + 1))
        sum_lam_i_minus_1 = sum(arrival_rates[j] for j in range(i)) if i > 0 else Decimal('0')
        
        
        W = (Decimal('1') / service_rate) / \
            (Decimal('1') - (sum_lam_i_minus_1 / service_rate)) / \
            (Decimal('1') - (sum_lam_i / service_rate))

        Wq = W - (Decimal('1') / service_rate)
        L = sum_lam_i * W
        Lq = L - (sum_lam_i / service_rate)

        results[f"Classe {i + 1}"] = {
            "Taxa de Chegada (λ)": round(lam_i,5),
            "Taxa de Ocupação (ρ)": round(rho_total,5),
            "Tempo Médio no Sistema (W)": round(W, 5),
            "Tempo Médio na Fila (Wq)": round(Wq, 5),
            "Número Médio no Sistema (L)": round(L, 5),
            "Número Médio na Fila (Lq)": round(Lq, 5)
            
        }

    return results

'''
Modelo M/M/1 com interrupção

Esse código calcula métricas de uma fila M/M/1 com diferentes classes de prioridade,
onde classes mais prioritárias podem interromper o atendimento das menos prioritárias (preempção).

Ele recebe:
- A taxa de serviço (μ),
- As taxas de chegada (λ) de cada classe, em ordem de prioridade (da mais alta para a mais baixa).

Retorna, para cada classe:

- Taxa de chegada (λ),
- Ocupação total do sistema (ρ),
- Médias de clientes e tempos na fila e no sistema (L, Lq, W, Wq).

Se a soma das chegadas for maior ou igual à capacidade de atendimento (λ_total ≥ μ), o código informa que o sistema é instável.

'''