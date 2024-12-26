from flask import Flask,Response, jsonify, render_template
from backend.process_data import PreprocessData
from backend.plot import FactorPlot
from backend.Clustering import Clustering,getPlot

app = Flask(__name__, template_folder='templates')


# write the app logic here 
processdata = PreprocessData()
data = processdata.process_data('./datasets/data.csv')
cluster_model = Clustering(data)


@app.route('/')
def index():
    return render_template('./index.html') 

@app.route("/plot.png")
def plot():
    plot_output = FactorPlot(data)

    # Return the plot as a PNG response
    return Response(plot_output.getvalue(), mimetype='image/png')


@app.route("/severity_plot.png")
def create_severity_plot():
    plot_output = getPlot('Unknown',cluster_model)
    # Return the plot as a PNG response
    return Response(plot_output.getvalue(), mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)