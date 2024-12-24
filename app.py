from flask import Flask, request,Response, jsonify, render_template
from backend.process_data import PreprocessData
import matplotlib.pyplot as plt
import io 
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

app = Flask(__name__, template_folder='templates')


# write the app logic here 
processdata = PreprocessData()
data = processdata.process_data('./datasets/data.csv');












@app.route('/')
def index():
    return render_template('./index.html') 

@app.route("/plot.png")
def plot_png():
    import matplotlib.pyplot as plt

    # Example data (assuming 'data' is a DataFrame)
    fig, ax = plt.subplots(figsize=(7, 5))  # Increase figure size

    # Assuming injury_mapping and data setup as in your example
    injury_mapping = {
        "No injury/unknown": 0,
        "Non-incapacitating": 1,
        "Incapacitating": 2,
        "Fatal": 3
    }

    data["Injury Type"] = data["Injury Type"].replace(injury_mapping)
    grouped_data = data.groupby("Primary Factor")["Injury Type"].mean().sort_values()

    # Create a bar plot
    grouped_data.plot(kind="bar", color="#4CAF50", ax=ax)

    # Customize the plot
    ax.set_title("Average Accident Severity by Factor")
    ax.set_ylabel("Average Severity")
    ax.set_xlabel("Factor")
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right') 

    
    # Save the plot to a BytesIO object
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype="image/png")


if __name__ == '__main__':
    app.run(debug=True)