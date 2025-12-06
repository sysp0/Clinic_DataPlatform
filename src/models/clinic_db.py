import pandas as pd
import pandera.pandas as pa
from pandera.typing import Series


class BaseSchema(pa.DataFrameModel):
    class Config:
        strict = True

class Province(BaseSchema):
    ProvinceCode: int = pa.Field(ge=0, unique=True)
    ProvinceName: str

class City(BaseSchema):
    CityPK: int = pa.Field(ge=0, unique=True)
    ProvinceCode: int = pa.Field(ge=0)
    CityCode: int = pa.Field(ge=0)
    CityTitle: str
    CityLongitude: float
    CityLatitude: float
    GeoLocation: str

class ClinicInfo(BaseSchema):
    ClinicCode: int = pa.Field(ge=0, unique=True)
    ClinicName: str
    ClinicAddress: str
    CityPK: int = pa.Field(ge=0)
    Tel: str
    Mobile: str
    ClinicPicture: str

class GenderType(BaseSchema):
    GenderTypeCode: int = pa.Field(ge=0, unique=True)
    GenderTypeTilte: str

class Patient(BaseSchema):
    PatientPK: int = pa.Field(ge=0, unique=True)
    NationalCode: str
    FirstName: str
    LastName: str
    GenderTypeCode: int = pa.Field(ge=0)
    Mobile: str

class DoctorGroup(BaseSchema):
    DoctorGroupCode: int = pa.Field(ge=0, unique=True)
    DoctorGroupTiltle: str

class Doctor(pa.DataFrameModel):
    DoctorPK: Series[int] = pa.Field(unique=True)
    FirstName: Series[str] = pa.Field(nullable=True)
    LastName: Series[str] = pa.Field(nullable=True)
    NationalCode: Series[str] = pa.Field(nullable=True, coerce=True)
    NezamPezeshkiCode: Series[str] = pa.Field(nullable=True, coerce=True)
    DoctorPicture: Series[bytes] = pa.Field(nullable=True)
    
    DoctorGroupCode: Series[int] = pa.Field(nullable=True)

    class Config:
        coerce = True
class RelationshipType(BaseSchema):
    RelationshipTypeCode: int = pa.Field(ge=0, unique=True)
    RelationshipTypeTitle: str

class CustomerType(BaseSchema):
    CustomerTypeCode: int = pa.Field(ge=0, unique=True)
    CustomerTypeTitle: str

class Shift(BaseSchema):
    ShiftCode: int = pa.Field(ge=0, unique=True)
    ShiftTitle: str
    ShiftTimeStart: str
    ShiftTimeEnd: str

class UserGroup(BaseSchema):
    UserGroupCode: int = pa.Field(ge=0, unique=True)
    UserGroupTitle: str

class User(BaseSchema):
    UserPK: int = pa.Field(ge=0, unique=True)
    UserGroupCode: int = pa.Field(ge=0)
    UserName: str
    Password: str
    FirstName: str
    LastName: str
    UserPicture: str

class InsuranceType(BaseSchema):
    InsuranceTypeCode: int = pa.Field(ge=0, unique=True)
    InsuranceTypeTitle: str

class ServiceGroup(BaseSchema):
    ServiceGroupCode: int = pa.Field(ge=0, unique=True)
    ParentServiceGroupCode: int = pa.Field(ge=0, nullable=True)
    ServiceGroupTitle: str

class Service(BaseSchema):
    ServiceCode: int = pa.Field(ge=0, unique=True)
    ServiceGroupCode: int = pa.Field(ge=0)
    ServiceTitle: str

class InsuranceService(BaseSchema):
    InsuranceServicePK: int = pa.Field(ge=0, unique=True)
    InsuranceTypeCode: int = pa.Field(ge=0)
    ServiceCode: int = pa.Field(ge=0)

class PatientReceptionHeader(pa.DataFrameModel):
    PatientReceptionHeaderPK: Series[int] = pa.Field(unique=True)
    ReceptionDate: Series[pd.Timestamp] = pa.Field(nullable=True)
    PatientPK: Series[int] = pa.Field(nullable=True)
    DoctorPK: Series[int] = pa.Field(nullable=True)
    InsuranceTypeCode: Series[int] = pa.Field(nullable=True)
    PatientAmount: Series[float] = pa.Field(nullable=True, coerce=True)
    InsuranceAmount: Series[float] = pa.Field(nullable=True, coerce=True)
    Discount: Series[float] = pa.Field(nullable=True, coerce=True)

    class Config:
        coerce = True

class PatientReceptionDetail(BaseSchema):
    PatientReceptionDetailPK: int = pa.Field(ge=0, unique=True)
    PatientReceptionHeaderPK: int = pa.Field(ge=0)
    ServiceCode: int = pa.Field(ge=0)
    InsuranceAmount: float
    PatientAmount: float
    ServiceAmount: float
    Discount: float