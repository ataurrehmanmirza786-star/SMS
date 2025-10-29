from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey, Enum, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()

# Many-to-many relationship tables
address_resident_association = Table(
    'address_resident', Base.metadata,
    Column('address_id', Integer, ForeignKey('addresses.id')),
    Column('resident_id', Integer, ForeignKey('residents.id'))
)

user_permission_association = Table(
    'user_permission', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('permission_id', Integer, ForeignKey('permissions.id'))
)

class Category(enum.Enum):
    R = "Residential"
    A = "Administrative"
    AS = "Assisted Living"
    PB = "Public Building"

class Block(enum.Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"

class FloorType(enum.Enum):
    OWNER = "Owner"
    TENANT = "Tenant"
    COMMERCIAL = "Commercial"
    SHOP = "Shop"
    VACANT = "Vacant"

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100))
    email = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    permissions = relationship("Permission", secondary=user_permission_association)
    
class Permission(Base):
    __tablename__ = 'permissions'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    module = Column(String(50), nullable=False)
    can_view = Column(Boolean, default=False)
    can_add = Column(Boolean, default=False)
    can_edit = Column(Boolean, default=False)
    can_delete = Column(Boolean, default=False)

class Address(Base):
    __tablename__ = 'addresses'
    
    id = Column(Integer, primary_key=True)
    category = Column(Enum(Category), nullable=False)
    number = Column(String(20), nullable=False)
    row = Column(String(20), nullable=False)
    block = Column(Enum(Block), nullable=False)
    total_floors = Column(Integer, nullable=False)
    
    floors = relationship("Floor", back_populates="address")
    residents = relationship("Resident", secondary=address_resident_association, back_populates="addresses")

class Floor(Base):
    __tablename__ = 'floors'
    
    id = Column(Integer, primary_key=True)
    address_id = Column(Integer, ForeignKey('addresses.id'), nullable=False)
    floor_number = Column(Integer, nullable=False)
    
    # Floor type flags
    is_owner = Column(Boolean, default=False)
    is_tenant = Column(Boolean, default=False)
    is_commercial = Column(Boolean, default=False)
    is_shop = Column(Boolean, default=False)
    is_vacant = Column(Boolean, default=False)
    
    # Shop details
    shop_count = Column(Integer, default=0)
    
    address = relationship("Address", back_populates="floors")
    residents = relationship("Resident", back_populates="floor")

class Resident(Base):
    __tablename__ = 'residents'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    contact_number = Column(String(20))
    email = Column(String(100))
    emergency_contact = Column(String(100))
    id_proof_number = Column(String(50))
    move_in_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
    
    floor_id = Column(Integer, ForeignKey('floors.id'))
    floor = relationship("Floor", back_populates="residents")
    addresses = relationship("Address", secondary=address_resident_association, back_populates="residents")
    
    # Financial records
    financial_records = relationship("FinancialRecord", back_populates="resident")

class ChargeType(enum.Enum):
    MONTHLY = "Monthly"
    OCCASIONAL = "Occasional"

class Charge(Base):
    __tablename__ = 'charges'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False)
    charge_type = Column(Enum(ChargeType), nullable=False)
    description = Column(String(255))
    is_active = Column(Boolean, default=True)

class FinancialRecord(Base):
    __tablename__ = 'financial_records'
    
    id = Column(Integer, primary_key=True)
    resident_id = Column(Integer, ForeignKey('residents.id'), nullable=False)
    address_id = Column(Integer, ForeignKey('addresses.id'), nullable=False)
    charge_id = Column(Integer, ForeignKey('charges.id'), nullable=False)
    amount = Column(Float, nullable=False)
    due_date = Column(DateTime, nullable=False)
    paid_date = Column(DateTime)
    is_paid = Column(Boolean, default=False)
    notes = Column(String(255))
    
    resident = relationship("Resident", back_populates="financial_records")
    address = relationship("Address")
    charge = relationship("Charge")

class ComplaintStatus(enum.Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"
    CLOSED = "Closed"

class Complaint(Base):
    __tablename__ = 'complaints'
    
    id = Column(Integer, primary_key=True)
    resident_id = Column(Integer, ForeignKey('residents.id'), nullable=False)
    address_id = Column(Integer, ForeignKey('addresses.id'), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)
    status = Column(Enum(ComplaintStatus), default=ComplaintStatus.PENDING)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    resolved_at = Column(DateTime)
    
    resident = relationship("Resident")
    address = relationship("Address")
