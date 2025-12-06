from dataclasses import dataclass

import pandas as pd


@dataclass
class ExtractedData:
    patient: pd.DataFrame
    doctor: pd.DataFrame
    service: pd.DataFrame
    insurance: pd.DataFrame
    header: pd.DataFrame
    detail: pd.DataFrame
    gender: pd.DataFrame
    doc_group: pd.DataFrame
    srv_group: pd.DataFrame


@dataclass
class TransformedData:
    dim_doctor: pd.DataFrame
    dim_patient: pd.DataFrame
    dim_service: pd.DataFrame
    dim_insurance: pd.DataFrame
    fact_reception: pd.DataFrame
