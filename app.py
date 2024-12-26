from flask import Flask,Response,request,jsonify,render_template, send_file
from backend.process_data import PreprocessData
from backend.plot import FactorPlot
from backend.Clustering import Clustering, getPlot
from backend.linear import linear,getPlotLinar

app = Flask(__name__, template_folder='templates')


# write the app logic here 
processdata = PreprocessData()
data = processdata.process_data('./datasets/data.csv')
cluster_model = Clustering(data)
linear_model = linear(data)


@app.route('/')
def index():
    return render_template('./index.html') 

@app.route("/plot.png")
def plot():
    plot_output = FactorPlot(data)

    # Return the plot as a PNG response
    return Response(plot_output.getvalue(), mimetype='image/png')


@app.route('/predict', methods=['POST'])
def predict_severity():
    try:
        # Get input from the user
        input_data = request.json
        input_factor = input_data.get('factor', '')
        viz_type = input_data.get('type', '')

        if not input_factor:
            return jsonify({"error": "Input factor is required"}), 400

        input_factor = input_factor.upper()

        if viz_type == 'bar':
            output = getPlot(input_factor,cluster_model,viz_type)
        elif viz_type == 'pie':
            output = getPlot(input_factor,cluster_model,viz_type)
        else:
            return jsonify({"error": "Invalid visualization type"}), 400

        return send_file(output, mimetype='image/png')
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@app.route('/predictLinaer', methods=['POST'])
def predict_severity_linear():
    try:
        # Get input from the user
        input_data = request.json
        input_factor = input_data.get('factor', '')
        viz_type = input_data.get('type', '')

        if not input_factor:
            return jsonify({"error": "Input factor is required"}), 400

        input_factor = input_factor.upper()

        if viz_type == 'bar':
            output = getPlotLinar(input_factor,linear_model,viz_type)
        elif viz_type == 'pie':
            output = getPlotLinar(input_factor,linear_model,viz_type)
        else:
            return jsonify({"error": "Invalid visualization type"}), 400

        return send_file(output, mimetype='image/png')
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)