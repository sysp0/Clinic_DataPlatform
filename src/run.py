from src.db import source_engine, warehouse_engine
from src.models.clinic_db import (
    Patient, Doctor, Service,
    InsuranceType, PatientReceptionHeader, PatientReceptionDetail,
    GenderType, DoctorGroup, ServiceGroup,
)
from src.etl import extract, transform, load


def main():
    models = {
        "Patient": Patient,
        "Doctor": Doctor,
        "Service": Service,
        "InsuranceType": InsuranceType,
        "Header": PatientReceptionHeader,
        "Detail": PatientReceptionDetail,
        "GenderType": GenderType,
        "DoctorGroup": DoctorGroup,
        "ServiceGroup": ServiceGroup,
    }
    extracted = extract(source_engine, models)
    transformed = transform(extracted)
    load(transformed, warehouse_engine)
