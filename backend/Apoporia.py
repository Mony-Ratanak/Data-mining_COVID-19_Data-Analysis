from mlxtend.frequent_patterns import apriori, association_rules

class ApoporiaModel:
    def __init__(self):
        pass

    def predict(self, df_transactions,primary_factor = 'UNKNOWN'):
        # Apply the Apriori algorithm to find frequent itemsets
        frequent_itemsets = apriori(df_transactions, min_support=0.01, use_colnames=True)
        print(frequent_itemsets.head())
        # Generate association rules
        rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0)
        print(rules)
        
        # Calculate confidence for each rule
        rules['confidence'] = rules['confidence'].apply(lambda x: round(x * 100, 2))  # Convert to percentage

        # Get rules where the antecedent contains the primary factor
        rules_with_primary_factor = rules[rules['antecedents'].apply(lambda x: primary_factor in str(x))]

        # Show the results
        print(rules_with_primary_factor[['antecedents', 'consequents', 'confidence']])
