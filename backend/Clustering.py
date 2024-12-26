import io
import matplotlib
from sklearn.preprocessing import LabelEncoder
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
matplotlib.use('Agg')  # Use 'Agg' backend for non-GUI environments

model_accuracy = 0
le_factor = LabelEncoder()
le_injury = LabelEncoder()

def Clustering(df):
   # Step 1: Encode categorical variables
   df['Primary Factor Encoded'] = le_factor.fit_transform(df['Primary Factor'])

   df['Injury Type Encoded'] = le_injury.fit_transform(df['Injury Type'])

   # Step 2: Train a Classifier (Random Forest)
   X = df[['Primary Factor Encoded']]  # Features (Primary Factor)
   y = df['Injury Type Encoded']  # Target (Injury Type)

   # Train-test split
   X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

   # Initialize and train the Random Forest model
   model = RandomForestClassifier(n_estimators=100, random_state=42)
   model.fit(X_train, y_train)
   # Step 5: Evaluate model (optional)
   y_pred = model.predict(X_test)
   global model_accuracy 
   model_accuracy = accuracy_score(y_test, y_pred)
   print(f'{model_accuracy*100:.2f}%%')
   
   return model

def getPlot(input_factor='Unknown',model = None,viz_type = 'bar'):
   encoded_factor = le_factor.transform([input_factor])[0]  # Encode the input factor

   # Ensure the input is in DataFrame format with the correct column name
   input_data = pd.DataFrame([[encoded_factor]], columns=['Primary Factor Encoded'])

   # Get prediction probabilities
   pred_probs = model.predict_proba(input_data)[0]

   # Step 4: Visualize the likelihood of injury types for the given factor
   # Get injury type names
   injury_types = le_injury.classes_
   

   # Plot
   fig, ax = plt.subplots(figsize=(8, 6))
   
   
   if(viz_type == 'bar'):
      sns.barplot(x=injury_types, y=pred_probs, palette='viridis')
   elif(viz_type == 'pie'):
      ax.pie(pred_probs, labels=injury_types, autopct='%1.1f%%', startangle=90)
   elif(viz_type == 'line'):
      sns.lineplot(x=injury_types, y=pred_probs, palette='viridis')
      
      
      
   # Add percentage labels on top of bars
   for bar, prob in zip(ax.patches, pred_probs):
      percentage = f"{prob * 100:.1f}%"  # Convert probability to percentage
      ax.text(
         bar.get_x() + bar.get_width() / 2,  # X-coordinate (center of the bar)
         bar.get_height() + 0.01,  # Y-coordinate (just above the bar)
         percentage,  # Text to display
         ha='center',  # Horizontal alignment
         va='bottom',  # Vertical alignment
         fontsize=10,  # Font size
         color='black'  # Text color
      )
   plt.title(f"Prediction of Injury Types for '{input_factor}' with Clustering Model", fontsize=14)
   plt.xlabel('')
   plt.ylabel('Probability', fontsize=12)
   plt.xticks(rotation=45)
   plt.tight_layout()
   
   # Save the plot to an in-memory binary stream
   output = io.BytesIO()
   fig.savefig(output, format='png')
   plt.close(fig)
   output.seek(0)
   return output
   