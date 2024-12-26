from flask import Flask, request,Response, jsonify, render_template
from backend.process_data import PreprocessData
from backend.plot import FactorPlot

app = Flask(__name__, template_folder='templates')


# write the app logic here 
processdata = PreprocessData()
data = processdata.process_data('./datasets/data.csv')




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
    pass

if __name__ == '__main__':
    app.run(debug=True)