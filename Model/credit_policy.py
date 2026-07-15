# -*- coding: utf-8 -*-
"""
credit_policy.py — Camada de politica do Sistema de Limite de Credito.
Traduz a Probabilidade de Default (PD) + a renda do cliente em:
  faixa de risco, limite recomendado (R$) e prazo recomendado (meses).

A LOGICA (Capacidade x Risco):
  1. Capacidade: prestacao maxima = dti_cap * renda mensal.
  2. Limite base = valor presente dessa prestacao no prazo, a uma taxa assumida.
  3. Ajuste por risco: limite = limite base * multiplicador da faixa do PD.
  4. Prazo: definido pela faixa de risco (menor risco -> prazo maior).

Nao depende de scikit-learn — pode ser importado pela API/Streamlit e pelo notebook.
"""
from pathlib import Path
import yaml

_CFG = None

def load_policy_cfg(cfg_path=None):
    """Carrega a secao 'policy' do config.yaml (cacheada)."""
    global _CFG
    if _CFG is None:
        p = Path(cfg_path) if cfg_path else Path(__file__).resolve().parent / "config.yaml"
        with open(p, "r", encoding="utf-8") as f:
            _CFG = yaml.safe_load(f)["policy"]
    return _CFG


def faixa_risco(pd_value, bands):
    """Retorna [nome, pd_max, prazo, multiplicador] da 1a faixa cujo pd_max > PD."""
    for band in bands:
        if pd_value < band[1]:
            return band
    return bands[-1]


def recomendar(pd_value, renda, cfg=None):
    """
    Recomendacao para um cliente.
      pd_value : probabilidade de default (0..1)
      renda    : AMT_INCOME_TOTAL (anual, se income_is_annual=True)
    Retorna dict com faixa, decisao, limite_recomendado e prazo_meses.
    """
    cfg = cfg or load_policy_cfg()
    renda_mensal = renda / 12.0 if cfg.get("income_is_annual", True) else float(renda)
    presta_max = cfg["dti_cap"] * renda_mensal

    nome, pd_max, prazo, mult = faixa_risco(pd_value, cfg["bands"])

    if prazo == 0 or mult == 0:
        return {"faixa": nome, "decisao": "Recusar",
                "limite_recomendado": 0.0, "prazo_meses": 0,
                "pd": round(float(pd_value), 4)}

    r = cfg["monthly_rate"]
    # valor presente de uma serie de 'prazo' prestacoes (price)
    fator = (1 - (1 + r) ** (-prazo)) / r
    limite = presta_max * fator * mult

    return {"faixa": nome, "decisao": "Aprovar",
            "limite_recomendado": round(float(limite), 2),
            "prazo_meses": int(prazo),
            "prestacao_maxima": round(float(presta_max), 2),
            "pd": round(float(pd_value), 4)}


if __name__ == "__main__":
    # Exemplos de demonstracao (renda anual)
    cfg = load_policy_cfg()
    exemplos = [("Cliente A", 0.04, 120000), ("Cliente B", 0.48, 72000),
                ("Cliente C", 0.18, 60000), ("Cliente D", 0.70, 90000)]
    for nome, pd_v, renda in exemplos:
        rec = recomendar(pd_v, renda, cfg)
        print(f"{nome}: PD={pd_v:.0%} renda=R${renda:,.0f}/ano -> "
              f"faixa {rec['faixa']} | {rec['decisao']} | "
              f"limite R${rec['limite_recomendado']:,.0f} | {rec['prazo_meses']}m")
