import pandas as pd
import matplotlib.pyplot as plt
import io
import seaborn as sns
import matplotlib

# Ensure Matplotlib uses a non-GUI backend to avoid GUI-related warnings in Flask
matplotlib.use('Agg')  # Use 'Agg' backend for non-GUI environments

def FactorPlot(df):
    # Check if the 'Primary Factor' column exists
    if 'Primary Factor' not in df.columns:
        print("Error: 'Primary Factor' column is missing from the DataFrame.")
        return None  # Return None if the column doesn't exist
    
    # Check if the DataFrame is empty
    if df.empty:
        print("Error: The DataFrame is empty.")
        return None  # Return None if the DataFrame is empty

    # Group by 'Primary Factor' and calculate the count of occurrences
    top_factors = df['Primary Factor'].value_counts().head(15)
    top_factors_df = top_factors.reset_index()
    top_factors_df.columns = ['Primary Factor', 'Count']

    # Create the plot
    try:
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(data=top_factors_df, x='Primary Factor', y='Count', palette='viridis', ax=ax)
        ax.set_title('Top 10 Primary Factors by Total Count', fontsize=16)
        ax.set_xlabel('', fontsize=12)
        ax.set_ylabel('Total Count', fontsize=12)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=10)

        # Add the count on top of each bar
        for p in ax.patches:
            ax.annotate(f'{p.get_height():,.0f}',  # The count value
                        (p.get_x() + p.get_width() / 2., p.get_height()),  # Position
                        ha='center', va='center', fontsize=10, color='black', 
                        xytext=(0, 5), textcoords='offset points')  # Add offset for text

        plt.tight_layout()

        # Save the plot to an in-memory binary stream
        output = io.BytesIO()
        fig.savefig(output, format='png')
        plt.close(fig)
        output.seek(0)
        return output
    except Exception as e:
        print(f"Error generating plot: {e}")
        return None  # Return None if there was an error generating the plot
