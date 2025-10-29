from database.models import Address, session
from sqlalchemy import func

class AddressController:
    def __init__(self):
        self.session = session
    
    def get_all_addresses(self):
        return self.session.query(Address).all()
    
    def get_address_by_id(self, address_id):
        return self.session.query(Address).filter(Address.id == address_id).first()
    
    def add_address(self, address_data):
        from database.models import Category, Block
        
        address = Address(
            category=Category[address_data['category']],
            number=address_data['number'],
            row=address_data['row'],
            block=Block[address_data['block']],
            total_floors=address_data['total_floors']
        )
        self.session.add(address)
        self.session.commit()
        return address
    
    def update_address(self, address_id, address_data):
        from database.models import Category, Block
        
        address = self.get_address_by_id(address_id)
        if address:
            address.category = Category[address_data['category']]
            address.number = address_data['number']
            address.row = address_data['row']
            address.block = Block[address_data['block']]
            address.total_floors = address_data['total_floors']
            self.session.commit()
        return address
    
    def delete_address(self, address_id):
        address = self.get_address_by_id(address_id)
        if address:
            self.session.delete(address)
            self.session.commit()
        return address
    
    def get_total_addresses(self):
        return self.session.query(Address).count()
    
    def get_addresses_by_category(self):
        result = self.session.query(Address.category, func.count(Address.id)).group_by(Address.category).all()
        return {category.value: count for category, count in result}
    
    def get_addresses_by_block(self):
        result = self.session.query(Address.block, func.count(Address.id)).group_by(Address.block).all()
        return {block.value: count for block, count in result}
    
    def get_floors_by_address(self, address_id):
        from database.models import Floor
        return self.session.query(Floor).filter(Floor.address_id == address_id).all()
    
    def get_floor_by_id(self, floor_id):
        from database.models import Floor
        return self.session.query(Floor).filter(Floor.id == floor_id).first()
    
    def add_floor(self, address_id, floor_data):
        from database.models import Floor
        
        floor = Floor(
            address_id=address_id,
            floor_number=floor_data['floor_number'],
            is_owner=floor_data['is_owner'],
            is_tenant=floor_data['is_tenant'],
            is_commercial=floor_data['is_commercial'],
            is_shop=floor_data['is_shop'],
            is_vacant=floor_data['is_vacant'],
            shop_count=floor_data['shop_count']
        )
        self.session.add(floor)
        self.session.commit()
        return floor
    
    def update_floor(self, floor_id, floor_data):
        floor = self.get_floor_by_id(floor_id)
        if floor:
            floor.floor_number = floor_data['floor_number']
            floor.is_owner = floor_data['is_owner']
            floor.is_tenant = floor_data['is_tenant']
            floor.is_commercial = floor_data['is_commercial']
            floor.is_shop = floor_data['is_shop']
            floor.is_vacant = floor_data['is_vacant']
            floor.shop_count = floor_data['shop_count']
            self.session.commit()
        return floor
    
    def delete_floor(self, floor_id):
        floor = self.get_floor_by_id(floor_id)
        if floor:
            self.session.delete(floor)
            self.session.commit()
        return floor
    
    def update_shop_count(self, floor_id, shop_count):
        floor = self.get_floor_by_id(floor_id)
        if floor:
            floor.shop_count = shop_count
            self.session.commit()
        return floor
