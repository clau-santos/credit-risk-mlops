import joblib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

class CreditRiskModel:

    def __init__(self, model_path=f"{ROOT}/Model/model_pd.pkl"):
        self.model = joblib.load(model_path)

    def predict(self, features):


        prob = self.model.predict_proba(features)[0, 1]
        regra_limite = features["AMT_INCOME_TOTAL"].iloc[0] * 0.40

        if prob < 0.15:
            faixa = "A - Baixo Risco"
            decisao = "Aprovar"
            limite = regra_limite * 1
            prazo = 48

        elif prob >= 0.15 and prob < 0.30:
            faixa = "B - Baixo Risco"
            decisao = "Aprovar"
            limite = regra_limite * 0.7
            prazo = 36

        elif prob >= 0.30 and prob < 0.60:
            faixa = "C - Médio Risco"
            decisao = "Aprovar"
            limite = regra_limite * 0.4
            prazo = 24

        else:
            faixa = "Alto risco"
            decisao = "Reprovar"
            limite = 0
            prazo = 0

        return {
            "pd": prob,
            "faixa": faixa,
            "decisao": decisao,
            "limite": limite,
            "prazo": prazo,
        }









