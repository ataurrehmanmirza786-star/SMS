class DynamicFilter:
    """Class to handle dynamic filtering of data."""
    
    def __init__(self, data):
        self.data = data
    
    def apply_filters(self, filters):
        """Apply filters to the data."""
        filtered_data = self.data
        
        for field, value in filters.items():
            if value:
                filtered_data = [item for item in filtered_data 
                                if str(getattr(item, field, '')).lower() == str(value).lower()]
        
        return filtered_data
