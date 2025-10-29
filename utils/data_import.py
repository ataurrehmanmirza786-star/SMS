import pandas as pd
from controllers.address_controller import AddressController

def import_addresses_from_csv(file_path, controller):
    """Import addresses from a CSV file."""
    df = pd.read_csv(file_path)
    
    for _, row in df.iterrows():
        address_data = {
            'category': row['category'],
            'number': str(row['number']),
            'row': str(row['row']),
            'block': row['block'],
            'total_floors': int(row['total_floors'])
        }
        controller.add_address(address_data)
    
    return True
