from flask import Flask, request, jsonify
from trendModel.predService import predTill
import datetime
import numpy as np
app= Flask(__name__)
@app.route('/')
def home():
    return app.send_static_file('index.html')


@app.route('/api/', methods=['GET'])
def getPredTill():
    args_date = request.args.get('date')
    args_lang = request.args.get('language')
    date=datetime.datetime.strptime(args_date,'%Y%m%d')

    pred=predTill(date,args_lang)
    pred=pred.tolist()
    return jsonify(pred)

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=2222)