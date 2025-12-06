from src.utils import validate
from src.models.data import ExtractedData, TransformedData


def extract(engine, models: dict) -> ExtractedData:
    return ExtractedData(
        patient=validate(models["Patient"], "SELECT * FROM dbo.Patient", engine),
        doctor=validate(models["Doctor"], "SELECT * FROM dbo.Doctor", engine),
        service=validate(models["Service"], "SELECT * FROM dbo.Service", engine),
        insurance=validate(models["InsuranceType"], "SELECT * FROM dbo.InsuranceType", engine),
        header=validate(models["Header"], "SELECT * FROM dbo.PatientReceptionHeader", engine),
        detail=validate(models["Detail"], "SELECT * FROM dbo.PatientReceptionDetail", engine),
        gender=validate(models["GenderType"], "SELECT * FROM dbo.GenderType", engine),
        doc_group=validate(models["DoctorGroup"], "SELECT * FROM dbo.DoctorGroup", engine),
        srv_group=validate(models["ServiceGroup"], "SELECT * FROM dbo.ServiceGroup", engine),
    )


def transform(data: ExtractedData) -> TransformedData:
    # DimDoctor
    doctor = data.doctor.merge(data.doc_group, on="DoctorGroupCode", how="left")
    doctor["DoctorName"] = doctor["FirstName"] + " " + doctor["LastName"]
    dim_doctor = doctor.rename(
        columns={"DoctorPK": "DoctorID", "DoctorGroupTiltle": "Specialty"}
    )[["DoctorID", "DoctorName", "Specialty"]]

    # DimPatient
    patient = data.patient.merge(data.gender, on="GenderTypeCode", how="left")
    patient["FullName"] = patient["FirstName"] + " " + patient["LastName"]
    dim_patient = patient.rename(
        columns={"PatientPK": "PatientID", "GenderTypeTilte": "Gender"}
    )[["PatientID", "FullName", "Gender",]]

    # DimService
    service = data.service.merge(data.srv_group, on="ServiceGroupCode", how="left")
    dim_service = service.rename(
        columns={
            "ServiceCode": "ServiceID",
            "ServiceTitle": "ServiceName",
            "ServiceGroupTitle": "ServiceGroupName",
        }
    )[["ServiceID", "ServiceName", "ServiceGroupName"]]

    # DimInsurance
    dim_insurance = data.insurance.rename(
        columns={"InsuranceTypeCode": "InsuranceID", "InsuranceTypeTitle": "InsuranceName"}
    )[["InsuranceID", "InsuranceName"]]
    
    # FactReception
    fact = data.detail.merge(data.header, on="PatientReceptionHeaderPK", how="inner")
    fact_reception = fact.rename(
        columns={
            "DoctorPK": "DoctorID",
            "PatientPK": "PatientID",
            "ServiceCode": "ServiceID",
            "InsuranceTypeCode": "InsuranceID",
            "PatientAmount": "PatientShareAmount",
            "InsuranceAmount": "InsuranceShareAmount",
            "ServiceAmount": "TotalAmount",
            "Discount": "DiscountAmount",
        },
    )[["DoctorID", "PatientID", "ServiceID",
        "InsuranceID", "ReceptionDate", "PatientShareAmount",
        "InsuranceShareAmount", "TotalAmount", "DiscountAmount"]]

    return TransformedData(dim_doctor, dim_patient, dim_service, dim_insurance, fact_reception)


def load(data: TransformedData, engine):
    data.fact_reception.to_sql("Fact_Reception", engine, if_exists="replace", index=False)
    data.dim_doctor.to_sql("Dim_Doctor", engine, if_exists="replace", index=False)
    data.dim_patient.to_sql("Dim_Patient", engine, if_exists="replace", index=False)
    data.dim_service.to_sql("Dim_Service", engine, if_exists="replace", index=False)
    data.dim_insurance.to_sql("Dim_Insurance", engine, if_exists="replace", index=False)
