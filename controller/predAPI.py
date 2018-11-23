from flask import Flask, request, jsonify
from trendModel.predService import predTill, predDays
import datetime
import numpy as np
import sys
import os
sys.path.append(os.path.abspath('../'))
sys.path.append(os.path.abspath('../trendModel/'))
app = Flask(__name__)


@app.route('/')
def home():
    return app.send_static_file('index.html')


@app.route('/api/', methods=['GET'])
def getPredTill():
    args_days = request.args.get('days')
    args_days = int(args_days)
    args_lang = request.args.get('language')
    # print(args_lang)
    # date=datetime.datetime.strptime(args_date,'%Y%m%d')
    # check constraint
    lang_list = ['C#', 'C++', 'CSS', 'HTML', 'Java', 'JavaScript', 'PHP', 'Python', 'Ruby', 'TypeScript', 'Perl', 'C']
    if args_lang not in lang_list:
        return jsonify(
            "[ERROR]: No model found for %s, please try another languages" % args_lang
        )
    if args_days <=0 :
        return jsonify(
            "[ERROR]: Illegal number, days must be bigger than 0."
        )

    pred = predDays(args_days, args_lang)
    pred = pred.tolist()
    return jsonify(pred)


if __name__ == '__main__':
    # get localhost:2222/api/date=20180101&language=Python
    app.run(host="172.31.31.247", port=2222)
    # "+"和"#"转成ASCII码值 '%2B'和'%23'
