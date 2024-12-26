import pandas as pd
from mlxtend.preprocessing import TransactionEncoder

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
        
        #clean data
        clean_data['Primary Factor'] = clean_data['Primary Factor'].replace(r" - EXPLAIN IN NARRATIVE", "", regex=True)
        
        #drop missing value
        clean_data.dropna(subset=['Primary Factor', 'Injury Type'])
        
        clean_data['Primary Factor'] = clean_data['Primary Factor'].fillna('Unknown')
        
        return clean_data
    
    def process_transaction(self, file_path):

        # Load the dataset
        try:
            # Attempt to read with UTF-8 encoding first
            df = pd.read_csv(file_path, encoding='utf-8')
        except UnicodeDecodeError:
            # Fallback to another encoding if UTF-8 fails
            df = pd.read_csv(file_path, encoding='latin1')
        
        
        df['Primary Factor'] = df['Primary Factor'].replace(r" - EXPLAIN IN NARRATIVE", "", regex=True)
        # Convert 'Primary Factor' and 'Injury Type' to string type
        df['Primary Factor'] = df['Primary Factor'].astype(str)
        df['Injury Type'] = df['Injury Type'].astype(str)
        
        
        # Convert 'Primary Factor' and 'Injury Type' into a transaction-like format
        transactions = df[['Primary Factor', 'Injury Type']].values.tolist()

        # Initialize the Transaction Encoder
        te = TransactionEncoder()
        # Fit and transform the data
        transaction_data = te.fit_transform(transactions)

        # Convert to a DataFrame
        df_transactions = pd.DataFrame(transaction_data, columns=te.columns_)

        # Show the data format after transformation
        return df_transactions
