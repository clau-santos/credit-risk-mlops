from pathlib import Path

import joblib
import json
import pandas as pd

from app.de_para import ESTADO_CIVIL, TIPO_RENDA, ESCOLARIDADE

ROOT = Path(__file__).resolve().parents[1]


model = joblib.load(ROOT / "Model" / "model_pd.pkl")

artifact = json.load(open(ROOT / "Model" / "metrics.json"))


FEATURES = artifact["features"]
DEFAULTS = artifact["defaults"]


def _safe_div(a, b):
    if b in (0, None):
        return 0.0
    return a / b


def build_features(
    renda,
    valor_credito,
    valor_bem,
    valor_parcela,
    idade,
    anos_emprego,
    filhos,
    membros_familia,
    sexo,
    possui_carro,
    possui_imovel,
    tipo_renda,
    estado_civil,
    escolaridade,
):
    """
    Constrói exatamente a mesma ABT utilizada no treinamento.
    """

    row = DEFAULTS.copy()

    # ==========================
    # Variáveis numéricas
    # ==========================

    row["AMT_INCOME_TOTAL"] = renda
    row["AMT_CREDIT"] = valor_credito
    row["AMT_GOODS_PRICE"] = valor_bem
    row["AMT_ANNUITY"] = valor_parcela

    row["CNT_CHILDREN"] = filhos
    row["CNT_FAM_MEMBERS"] = membros_familia

    row["AGE_YEARS"] = idade
    row["YEARS_EMPLOYED"] = anos_emprego

    # ==========================
    # Features derivadas
    # ==========================

    row["EMPLOYED_TO_AGE"] = _safe_div(
        anos_emprego,
        idade
    )

    row["CREDIT_INCOME_RATIO"] = _safe_div(
        valor_credito,
        renda
    )

    row["ANNUITY_INCOME_RATIO"] = _safe_div(
        valor_parcela,
        renda
    )

    row["CREDIT_TERM"] = _safe_div(
        valor_credito,
        valor_parcela
    )

    row["CREDIT_GOODS_RATIO"] = _safe_div(
        valor_credito,
        valor_bem
    )

    row["INCOME_PER_PERSON"] = _safe_div(
        renda,
        membros_familia
    )

    # ==========================
    # One-Hot Encoding
    # ==========================

    for col in FEATURES:

        if (
            col.startswith("CODE_GENDER_")
            or col.startswith("FLAG_OWN_CAR_")
            or col.startswith("FLAG_OWN_REALTY_")
            or col.startswith("NAME_INCOME_TYPE_")
            or col.startswith("NAME_FAMILY_STATUS_")
            or col.startswith("NAME_EDUCATION_TYPE_")
        ):
            row[col] = 0

    # Sexo
    gender_col = f"CODE_GENDER_{'F' if sexo == 'Feminino' else 'M'}"

    if gender_col in row:
        row[gender_col] = 1

    # Carro
    car_col = f"FLAG_OWN_CAR_{'Y' if possui_carro else 'N'}"

    if car_col in row:
        row[car_col] = 1

    # Imóvel
    house_col = f"FLAG_OWN_REALTY_{'Y' if possui_imovel else 'N'}"

    if house_col in row:
        row[house_col] = 1

    # Tipo de renda
    tipo_renda = TIPO_RENDA[tipo_renda]
    income_col = f"NAME_INCOME_TYPE_{tipo_renda}"

    if income_col in row:
        row[income_col] = 1

    # Estado civil
    estado_civil = ESTADO_CIVIL[estado_civil]
    family_col = f"NAME_FAMILY_STATUS_{estado_civil}"

    if family_col in row:
        row[family_col] = 1

    # Escolaridade
    escolaridade = ESCOLARIDADE[escolaridade]
    education_col = f"NAME_EDUCATION_TYPE_{escolaridade}"

    if education_col in row:
        row[education_col] = 1


    df = pd.DataFrame([row])
    df = df.reindex(columns=FEATURES)

    return df

