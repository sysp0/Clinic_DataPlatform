from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, BigInteger
from src.db import SourceBase

class Province(SourceBase):
    __tablename__ = 'Province'
    __table_args__ = {'schema': 'dbo'}

    ProvinceCode = Column(Integer, primary_key=True)
    ProvinceName = Column(String(100))

class City(SourceBase):
    __tablename__ = 'City'
    __table_args__ = {'schema': 'dbo'}

    CityPK = Column(Integer, primary_key=True)
    ProvinceCode = Column(Integer, ForeignKey('dbo.Province.ProvinceCode'))
    CityCode = Column(Integer)
    CityTitle = Column(String(100))
    CityLongitude = Column(Float)
    CityLatitude = Column(Float)
    GeoLocation = Column(String(200))

class ClinicInfo(SourceBase):
    __tablename__ = 'ClinicInfo'
    __table_args__ = {'schema': 'dbo'}

    ClinicCode = Column(Integer, primary_key=True)
    ClinicName = Column(String(200))
    ClinicAddress = Column(String(500))
    CityPK = Column(Integer, ForeignKey('dbo.City.CityPK'))
    Tel = Column(String(50))
    Mobile = Column(String(50))
    ClinicPicture = Column(String(500)) # Assuming URL or path

class GenderType(SourceBase):
    __tablename__ = 'GenderType'
    __table_args__ = {'schema': 'dbo'}

    GenderTypeCode = Column(Integer, primary_key=True)
    GenderTypeTitle = Column(String(50))

class Patient(SourceBase):
    __tablename__ = 'Patient'
    __table_args__ = {'schema': 'dbo'}

    PatientPK = Column(BigInteger, primary_key=True)
    NationalCode = Column(String(20))
    FirstName = Column(String(100))
    LastName = Column(String(100))
    GenderTypeCode = Column(Integer, ForeignKey('dbo.GenderType.GenderTypeCode'))
    Mobile = Column(String(20))

class DoctorGroup(SourceBase):
    __tablename__ = 'DoctorGroup'
    __table_args__ = {'schema': 'dbo'}

    DoctorGroupCode = Column(Integer, primary_key=True)
    DoctorGroupTitle = Column(String(100))

class Doctor(SourceBase):
    __tablename__ = 'Doctor'
    __table_args__ = {'schema': 'dbo'}

    DoctorPK = Column(Integer, primary_key=True)
    DoctorGroupCode = Column(Integer, ForeignKey('dbo.DoctorGroup.DoctorGroupCode'))
    DoctorCode = Column(Integer)
    FirstName = Column(String(100))
    LastName = Column(String(100))
    FullNameGabz = Column(String(200))
    NezamPezeshkiCode = Column(String(50))
    NationalCode = Column(String(20))
    GenderTypeCode = Column(Integer, ForeignKey('dbo.GenderType.GenderTypeCode'))
    Tel = Column(String(50))
    CityPK = Column(Integer, ForeignKey('dbo.City.CityPK'))
    Mobile = Column(String(50))
    DoctorPicture = Column(String(500))

class RelationshipType(SourceBase):
    __tablename__ = 'RelationshipType'
    __table_args__ = {'schema': 'dbo'}

    RelationshipTypeCode = Column(Integer, primary_key=True)
    RelationshipTypeTitle = Column(String(100))

class CustomerType(SourceBase):
    __tablename__ = 'CustomerType'
    __table_args__ = {'schema': 'dbo'}

    CustomerTypeCode = Column(Integer, primary_key=True)
    CustomerTypeTitle = Column(String(100))

class Shift(SourceBase):
    __tablename__ = 'Shift'
    __table_args__ = {'schema': 'dbo'}

    ShiftCode = Column(Integer, primary_key=True)
    ShiftTitle = Column(String(100))
    ShiftTimeStart = Column(String(10))
    ShiftTimeEnd = Column(String(10))

class UserGroup(SourceBase):
    __tablename__ = 'UserGroup'
    __table_args__ = {'schema': 'dbo'}

    UserGroupCode = Column(Integer, primary_key=True)
    UserGroupTitle = Column(String(100))

class User(SourceBase):
    __tablename__ = 'User'
    __table_args__ = {'schema': 'dbo'}

    UserPK = Column(Integer, primary_key=True)
    UserGroupCode = Column(Integer, ForeignKey('dbo.UserGroup.UserGroupCode'))
    UserName = Column(String(100))
    Password = Column(String(200))
    FirstName = Column(String(100))
    LastName = Column(String(100))
    UserPicture = Column(String(500))

class InsuranceType(SourceBase):
    __tablename__ = 'InsuranceType'
    __table_args__ = {'schema': 'dbo'}

    InsuranceTypeCode = Column(Integer, primary_key=True)
    InsuranceTypeTitle = Column(String(100))
    InsurancePicture = Column(String(500))

class ServiceGroup(SourceBase):
    __tablename__ = 'ServiceGroup'
    __table_args__ = {'schema': 'dbo'}

    ServiceGroupCode = Column(Integer, primary_key=True)
    ParentServiceGroupCode = Column(Integer, ForeignKey('dbo.ServiceGroup.ServiceGroupCode'), nullable=True) # Self-referencing
    ServiceGroupTitle = Column(String(200))

class Service(SourceBase):
    __tablename__ = 'Service'
    __table_args__ = {'schema': 'dbo'}

    ServiceCode = Column(Integer, primary_key=True)
    ServiceGroupCode = Column(Integer, ForeignKey('dbo.ServiceGroup.ServiceGroupCode'))
    ServiceTitle = Column(String(200))

class InsuranceService(SourceBase):
    __tablename__ = 'InsuranceService'
    __table_args__ = {'schema': 'dbo'}

    InsuranceServicePK = Column(Integer, primary_key=True)
    InsuranceTypeCode = Column(Integer, ForeignKey('dbo.InsuranceType.InsuranceTypeCode'))
    ServiceCode = Column(Integer, ForeignKey('dbo.Service.ServiceCode'))

class PatientReceptionHeader(SourceBase):
    __tablename__ = 'PatientReceptionHeader'
    __table_args__ = {'schema': 'dbo'}

    PatientReceptionHeaderPK = Column(BigInteger, primary_key=True)
    PatientPK = Column(BigInteger, ForeignKey('dbo.Patient.PatientPK'))
    DoctorPK = Column(Integer, ForeignKey('dbo.Doctor.DoctorPK'))
    InsuranceTypeCode = Column(Integer, ForeignKey('dbo.InsuranceType.InsuranceTypeCode'))
    InsuranceCode = Column(String(50))
    CustomerTypeCode = Column(Integer, ForeignKey('dbo.CustomerType.CustomerTypeCode'))
    RelationshipTypeCode = Column(Integer, ForeignKey('dbo.RelationshipType.RelationshipTypeCode'))
    ReceptionDate_Shamsi = Column(String(10))
    ReceptionDate = Column(DateTime)
    ReceptionTime = Column(String(10))
    ShiftCode = Column(Integer, ForeignKey('dbo.Shift.ShiftCode'))
    UserPK = Column(Integer, ForeignKey('dbo.User.UserPK'))

class PatientReceptionDetail(SourceBase):
    __tablename__ = 'PatientReceptionDetail'
    __table_args__ = {'schema': 'dbo'}

    PatientReceptionDetailPK = Column(BigInteger, primary_key=True)
    PatientReceptionHeaderPK = Column(BigInteger, ForeignKey('dbo.PatientReceptionHeader.PatientReceptionHeaderPK'))
    ServiceCode = Column(Integer, ForeignKey('dbo.Service.ServiceCode'))
    InsuranceAmount = Column(Float)
    PatientAmount = Column(Float)
    ServiceAmount = Column(Float)
    Discount = Column(Float)