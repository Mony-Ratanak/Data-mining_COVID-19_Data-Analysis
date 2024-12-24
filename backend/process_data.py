import pandas as pd

class PreprocessData:
    def __init__(self):
        pass

    def process_data(self, file_path):
        try:
            # Attempt to read with UTF-8 encoding first
            clean_data = pd.read_csv(file_path, encoding='utf-8')
        except UnicodeDecodeError:
            # Fallback to another encoding if UTF-8 fails
            clean_data = pd.read_csv(file_path, encoding='latin1')
        
        #drop missing value
        clean_data.dropna()
        
        clean_data['Primary Factor'] = clean_data['Primary Factor'].fillna('Unknown')
        
        return clean_data