from database.models import Resident, Address, Floor, session
from sqlalchemy import and_, or_

class ResidentController:
    def __init__(self):
        self.session = session
    
    def get_all_residents(self):
        return self.session.query(Resident).filter(Resident.is_active == True).all()
    
    def get_resident_by_id(self, resident_id):
        return self.session.query(Resident).filter(Resident.id == resident_id).first()
    
    def add_resident(self, resident_data):
        resident = Resident(
            name=resident_data['name'],
            contact_number=resident_data.get('contact_number', ''),
            email=resident_data.get('email', ''),
            emergency_contact=resident_data.get('emergency_contact', ''),
            id_proof_number=resident_data.get('id_proof_number', ''),
            move_in_date=resident_data.get('move_in_date'),
            is_active=True
        )
        self.session.add(resident)
        self.session.commit()
        return resident
    
    def update_resident(self, resident_id, resident_data):
        resident = self.get_resident_by_id(resident_id)
        if resident:
            resident.name = resident_data['name']
            resident.contact_number = resident_data.get('contact_number', resident.contact_number)
            resident.email = resident_data.get('email', resident.email)
            resident.emergency_contact = resident_data.get('emergency_contact', resident.emergency_contact)
            resident.id_proof_number = resident_data.get('id_proof_number', resident.id_proof_number)
            resident.move_in_date = resident_data.get('move_in_date', resident.move_in_date)
            self.session.commit()
        return resident
    
    def delete_resident(self, resident_id):
        resident = self.get_resident_by_id(resident_id)
        if resident:
            resident.is_active = False
            self.session.commit()
        return resident
    
    def get_total_residents(self):
        return self.session.query(Resident).filter(Resident.is_active == True).count()
    
    def filter_residents(self, filters):
        query = self.session.query(Resident).filter(Resident.is_active == True)
        
        if 'name' in filters and filters['name']:
            query = query.filter(Resident.name.ilike(f"%{filters['name']}%"))
        
        if 'contact_number' in filters and filters['contact_number']:
            query = query.filter(Resident.contact_number.ilike(f"%{filters['contact_number']}%"))
        
        if 'address' in filters and filters['address']:
            query = query.join(Resident.addresses).filter(
                or_(
                    Address.number.ilike(f"%{filters['address']}%"),
                    Address.block.ilike(f"%{filters['address']}%")
                )
            )
        
        return query.all()
    
    def allot_address_to_resident(self, resident_id, address_id, floor_id=None):
        resident = self.get_resident_by_id(resident_id)
        address = self.session.query(Address).filter(Address.id == address_id).first()
        
        if resident and address:
            if address not in resident.addresses:
                resident.addresses.append(address)
                
                if floor_id:
                    floor = self.session.query(Floor).filter(Floor.id == floor_id).first()
                    if floor and floor.address_id == address_id:
                        resident.floor = floor
                
                self.session.commit()
                return True
        return False
    
    def remove_address_from_resident(self, resident_id, address_id):
        resident = self.get_resident_by_id(resident_id)
        address = self.session.query(Address).filter(Address.id == address_id).first()
        
        if resident and address and address in resident.addresses:
            resident.addresses.remove(address)
            
            if resident.floor and resident.floor.address_id == address_id:
                resident.floor = None
                
            self.session.commit()
            return True
        return False
    
    def get_residents_by_address(self, address_id):
        return self.session.query(Resident).join(Resident.addresses).filter(
            and_(Address.id == address_id, Resident.is_active == True)
        ).all()
    
    def get_residents_by_floor(self, floor_id):
        return self.session.query(Resident).filter(
            and_(Resident.floor_id == floor_id, Resident.is_active == True)
        ).all()
