from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String

from src.db import WarehouseBase

class DimDoctor(WarehouseBase):
    __tablename__ = 'Dim_Doctor'

    DoctorID = Column(Integer, primary_key=True, comment="Original ID from Source")
    DoctorName = Column(String(255), comment="Full Name of Doctor")
    Specialty = Column(String(255), comment="From DoctorGroup e.g. Heart Specialist")

class DimPatient(WarehouseBase):
    __tablename__ = 'Dim_Patient'

    PatientID = Column(Integer, primary_key=True, comment="Original ID from Source")
    FullName = Column(String(255))
    Gender = Column(String(50), comment="Male/Female")

class DimService(WarehouseBase):
    __tablename__ = 'Dim_Service'

    ServiceID = Column(Integer, primary_key=True, comment="Original ID from Source")
    ServiceName = Column(String(500))
    ServiceGroupName = Column(String(255), comment="Category e.g. Visit, Lab, Surgery")

class DimInsurance(WarehouseBase):
    __tablename__ = 'Dim_Insurance'

    InsuranceID = Column(Integer, primary_key=True, comment="Original ID from Source")
    InsuranceName = Column(String(255), comment="e.g. Tamin Ejtemaei")

class FactReception(WarehouseBase):
    __tablename__ = 'Fact_Reception'

    FactID = Column(Integer, primary_key=True, autoincrement=True)
    
    DoctorID = Column(Integer, ForeignKey('Dim_Doctor.DoctorID'))
    PatientID = Column(Integer, ForeignKey('Dim_Patient.PatientID'))
    ServiceID = Column(Integer, ForeignKey('Dim_Service.ServiceID'))
    InsuranceID = Column(Integer, ForeignKey('Dim_Insurance.InsuranceID'))
    
    ReceptionDate = Column(DateTime, comment="Date of the reception")

    PatientShareAmount = Column(Numeric(18, 0), comment="Money paid by Patient")
    InsuranceShareAmount = Column(Numeric(18, 0), comment="Money paid by Insurance")
    TotalAmount = Column(Numeric(18, 0), comment="Sum of Patient + Insurance")
    DiscountAmount = Column(Numeric(18, 0), comment="Discount given")
