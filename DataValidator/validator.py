import pandas as pd
from pydantic import BaseModel, RootModel
from pydantic import ValidationError


class RawData(BaseModel):
    SK_ID_CURR: int
    TARGET: int
    NAME_CONTRACT_TYPE: str
    CODE_GENDER: str
    AMT_ANNUITY: float| None
    AMT_CREDIT: float| None
    AMT_GOODS_PRICE: float| None
    AMT_INCOME_TOTAL: float| None
    AMT_REQ_CREDIT_BUREAU_DAY: float| None
    AMT_REQ_CREDIT_BUREAU_HOUR: float| None
    AMT_REQ_CREDIT_BUREAU_MON: float| None
    AMT_REQ_CREDIT_BUREAU_QRT: float| None
    AMT_REQ_CREDIT_BUREAU_WEEK: float| None
    AMT_REQ_CREDIT_BUREAU_YEAR: float| None
    APARTMENTS_AVG: float| None
    APARTMENTS_MEDI: float| None
    APARTMENTS_MODE: float| None
    BASEMENTAREA_AVG: float| None
    BASEMENTAREA_MEDI: float| None
    BASEMENTAREA_MODE: float| None
    CNT_CHILDREN: int | None
    CNT_FAM_MEMBERS: float| None
    COMMONAREA_AVG: float| None
    COMMONAREA_MEDI: float| None
    COMMONAREA_MODE: float| None
    DAYS_BIRTH: int
    DAYS_EMPLOYED: int
    DAYS_ID_PUBLISH: int
    DAYS_LAST_PHONE_CHANGE: float| None
    DAYS_REGISTRATION: float
    DEF_30_CNT_SOCIAL_CIRCLE: float| None
    DEF_60_CNT_SOCIAL_CIRCLE: float| None
    ELEVATORS_AVG: float| None
    ELEVATORS_MEDI: float| None
    ELEVATORS_MODE: float| None
    EMERGENCYSTATE_MODE: str | None
    ENTRANCES_AVG: float| None
    ENTRANCES_MEDI: float| None
    ENTRANCES_MODE: float| None
    EXT_SOURCE_1: float| None
    EXT_SOURCE_2: float| None
    EXT_SOURCE_3: float | None
    FLAG_CONT_MOBILE: int
    FLAG_DOCUMENT_10: int | None
    FLAG_DOCUMENT_11: int | None
    FLAG_DOCUMENT_12: int | None
    FLAG_DOCUMENT_13: int | None
    FLAG_DOCUMENT_14: int | None
    FLAG_DOCUMENT_15: int | None
    FLAG_DOCUMENT_16: int | None
    FLAG_DOCUMENT_17: int | None
    FLAG_DOCUMENT_18: int | None
    FLAG_DOCUMENT_19: int | None
    FLAG_DOCUMENT_2: int | None
    FLAG_DOCUMENT_20: int | None
    FLAG_DOCUMENT_21: int | None
    FLAG_DOCUMENT_3: int | None
    FLAG_DOCUMENT_4: int | None
    FLAG_DOCUMENT_5: int | None
    FLAG_DOCUMENT_6: int | None
    FLAG_DOCUMENT_7: int | None
    FLAG_DOCUMENT_8: int | None
    FLAG_DOCUMENT_9: int | None
    FLAG_EMAIL: int
    FLAG_EMP_PHONE: int
    FLAG_MOBIL: int
    FLAG_PHONE: int
    FLAG_WORK_PHONE: int
    FLOORSMAX_AVG: float| None
    FLOORSMAX_MEDI: float| None
    FLOORSMAX_MODE: float| None
    FLOORSMIN_AVG: float| None
    FLOORSMIN_MEDI: float| None
    FLOORSMIN_MODE: float| None
    FONDKAPREMONT_MODE: str | None
    HOUR_APPR_PROCESS_START: int
    HOUSETYPE_MODE: str | None
    LANDAREA_AVG: float| None
    LANDAREA_MEDI: float| None
    LANDAREA_MODE: float| None
    LIVE_CITY_NOT_WORK_CITY: int
    LIVE_REGION_NOT_WORK_REGION: int
    LIVINGAPARTMENTS_AVG: float| None
    LIVINGAPARTMENTS_MEDI: float| None
    LIVINGAPARTMENTS_MODE: float| None
    LIVINGAREA_AVG: float| None
    LIVINGAREA_MEDI: float| None
    LIVINGAREA_MODE: float| None
    NAME_EDUCATION_TYPE: str
    NAME_FAMILY_STATUS: str
    NAME_HOUSING_TYPE: str
    NAME_INCOME_TYPE: str
    NAME_TYPE_SUITE: str | None
    NONLIVINGAPARTMENTS_AVG: float| None
    NONLIVINGAPARTMENTS_MEDI: float| None
    NONLIVINGAPARTMENTS_MODE: float| None
    NONLIVINGAREA_AVG: float| None
    NONLIVINGAREA_MEDI: float| None
    NONLIVINGAREA_MODE: float| None
    OBS_30_CNT_SOCIAL_CIRCLE: float| None
    OBS_60_CNT_SOCIAL_CIRCLE: float| None
    OCCUPATION_TYPE: str| None
    ORGANIZATION_TYPE: str | None
    OWN_CAR_AGE: float | None
    REGION_POPULATION_RELATIVE: float | None
    REGION_RATING_CLIENT: int | None
    REGION_RATING_CLIENT_W_CITY: int | None
    REG_CITY_NOT_LIVE_CITY: int | None
    REG_CITY_NOT_WORK_CITY: int | None
    REG_REGION_NOT_LIVE_REGION: int | None
    REG_REGION_NOT_WORK_REGION: int | None
    TOTALAREA_MODE: float| None
    WALLSMATERIAL_MODE: str | None
    WEEKDAY_APPR_PROCESS_START: str | None
    YEARS_BEGINEXPLUATATION_AVG: float| None
    YEARS_BEGINEXPLUATATION_MEDI: float| None
    YEARS_BEGINEXPLUATATION_MODE: float| None
    YEARS_BUILD_AVG: float| None
    YEARS_BUILD_MEDI: float| None
    YEARS_BUILD_MODE: float| None

class RawDataList(RootModel[list[RawData]]):
    pass

class CleanData(BaseModel):
    SK_ID_CURR: int
    TARGET: int
    NAME_CONTRACT_TYPE: str
    CODE_GENDER: str |  None
    AMT_ANNUITY: float | None
    AMT_CREDIT: float | None
    AMT_GOODS_PRICE: float | None
    AMT_INCOME_TOTAL: float | None
    AMT_REQ_CREDIT_BUREAU_DAY: float | None
    AMT_REQ_CREDIT_BUREAU_HOUR: float | None
    AMT_REQ_CREDIT_BUREAU_MON: float | None
    AMT_REQ_CREDIT_BUREAU_QRT: float | None
    AMT_REQ_CREDIT_BUREAU_WEEK: float | None
    AMT_REQ_CREDIT_BUREAU_YEAR: float | None
    APARTMENTS_AVG: float | None
    APARTMENTS_MEDI: float | None
    APARTMENTS_MODE: float | None
    BASEMENTAREA_AVG: float | None
    BASEMENTAREA_MEDI: float | None
    BASEMENTAREA_MODE: float | None
    CNT_CHILDREN: int | None
    CNT_FAM_MEMBERS: float | None
    COMMONAREA_AVG: float | None
    COMMONAREA_MEDI: float | None
    COMMONAREA_MODE: float | None
    DAYS_BIRTH: int
    DAYS_EMPLOYED: int | None
    DAYS_ID_PUBLISH: int
    DAYS_LAST_PHONE_CHANGE: float | None
    DAYS_REGISTRATION: float
    DEF_30_CNT_SOCIAL_CIRCLE: float | None
    DEF_60_CNT_SOCIAL_CIRCLE: float | None
    ELEVATORS_AVG: float | None
    ELEVATORS_MEDI: float | None
    ELEVATORS_MODE: float | None
    EMERGENCYSTATE_MODE: str | None
    ENTRANCES_AVG: float | None
    ENTRANCES_MEDI: float | None
    ENTRANCES_MODE: float | None
    EXT_SOURCE_1: float | None
    EXT_SOURCE_2: float | None
    EXT_SOURCE_3: float | None
    FLAG_CONT_MOBILE: int
    FLAG_DOCUMENT_10: int | None
    FLAG_DOCUMENT_11: int | None
    FLAG_DOCUMENT_12: int | None
    FLAG_DOCUMENT_13: int | None
    FLAG_DOCUMENT_14: int | None
    FLAG_DOCUMENT_15: int | None
    FLAG_DOCUMENT_16: int | None
    FLAG_DOCUMENT_17: int | None
    FLAG_DOCUMENT_18: int | None
    FLAG_DOCUMENT_19: int | None
    FLAG_DOCUMENT_2: int | None
    FLAG_DOCUMENT_20: int | None
    FLAG_DOCUMENT_21: int | None
    FLAG_DOCUMENT_3: int | None
    FLAG_DOCUMENT_4: int | None
    FLAG_DOCUMENT_5: int | None
    FLAG_DOCUMENT_6: int | None
    FLAG_DOCUMENT_7: int | None
    FLAG_DOCUMENT_8: int | None
    FLAG_DOCUMENT_9: int | None
    FLAG_EMAIL: int
    FLAG_EMP_PHONE: int
    FLAG_MOBIL: int
    FLAG_PHONE: int
    FLAG_WORK_PHONE: int
    FLOORSMAX_AVG: float | None
    FLOORSMAX_MEDI: float | None
    FLOORSMAX_MODE: float | None
    FLOORSMIN_AVG: float | None
    FLOORSMIN_MEDI: float | None
    FLOORSMIN_MODE: float | None
    FONDKAPREMONT_MODE: str | None
    HOUR_APPR_PROCESS_START: int
    HOUSETYPE_MODE: str | None
    LANDAREA_AVG: float | None
    LANDAREA_MEDI: float | None
    LANDAREA_MODE: float | None
    LIVE_CITY_NOT_WORK_CITY: int
    LIVE_REGION_NOT_WORK_REGION: int
    LIVINGAPARTMENTS_AVG: float | None
    LIVINGAPARTMENTS_MEDI: float | None
    LIVINGAPARTMENTS_MODE: float | None
    LIVINGAREA_AVG: float | None
    LIVINGAREA_MEDI: float | None
    LIVINGAREA_MODE: float | None
    NAME_EDUCATION_TYPE: str
    NAME_FAMILY_STATUS: str
    NAME_HOUSING_TYPE: str
    NAME_INCOME_TYPE: str
    NAME_TYPE_SUITE: str | None
    NONLIVINGAPARTMENTS_AVG: float | None
    NONLIVINGAPARTMENTS_MEDI: float | None
    NONLIVINGAPARTMENTS_MODE: float | None
    NONLIVINGAREA_AVG: float | None
    NONLIVINGAREA_MEDI: float | None
    NONLIVINGAREA_MODE: float | None
    OBS_30_CNT_SOCIAL_CIRCLE: float | None
    OBS_60_CNT_SOCIAL_CIRCLE: float | None
    OCCUPATION_TYPE: str | None
    ORGANIZATION_TYPE: str | None
    OWN_CAR_AGE: float | None
    REGION_POPULATION_RELATIVE: float
    REGION_RATING_CLIENT: int
    REGION_RATING_CLIENT_W_CITY: int
    REG_CITY_NOT_LIVE_CITY: int
    REG_CITY_NOT_WORK_CITY: int
    REG_REGION_NOT_LIVE_REGION: int
    REG_REGION_NOT_WORK_REGION: int
    TOTALAREA_MODE: float | None
    WALLSMATERIAL_MODE: str | None
    WEEKDAY_APPR_PROCESS_START: str
    YEARS_BEGINEXPLUATATION_AVG: float | None
    YEARS_BEGINEXPLUATATION_MEDI: float | None
    YEARS_BEGINEXPLUATATION_MODE: float | None
    YEARS_BUILD_AVG: float | None
    YEARS_BUILD_MEDI: float | None
    YEARS_BUILD_MODE: float | None


class CleanDataList(RootModel[list[CleanData]]):
    pass

def data_validator(data: list[dict], model: str):
    try:
        if model == "RAW":
            RawDataList.model_validate(data)
            print("Dados da camada RAW validados com sucesso!")
            return True

        if model == "SILVER":
            CleanDataList.model_validate(data)
            print("Dados da camada SILVER validados com sucesso! /n"
                    "Arquivo com os dado")
            return True

    except ValueError:
        return ValueError(f"Erro na validação dos Dados da camada {model}, revise o modelo de contrato dos dados.")


def data_validator_row(data: pd.DataFrame, model: str):
    columns = data.columns.tolist()

    try:
        for row in data.itertuples(index=False):
            record = {
                col: None if pd.isna(value) else value
                for col, value in zip(columns, row)
            }
            if model == "RAW":
                RawData.model_validate(record)

            if model == "SILVER":

                CleanData.model_validate(record)

        print(f"Dados da camada {model} validados com sucesso!")
        return True

    except ValidationError as e:
        raise ValueError(f"Erro na validação dos Dados da camada {model}, revise o modelo de contrato dos dados.{e}")

