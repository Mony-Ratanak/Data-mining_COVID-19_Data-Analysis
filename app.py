from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder='templates')


# write the app logic here 













@app.route('/')
def index():
    return render_template('./index.html') 

if __name__ == '__main__':
    app.run(debug=True)