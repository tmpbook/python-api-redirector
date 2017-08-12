from flask import Flask, jsonify, request
app = Flask(__name__)

API_WHICH_YOU_WANT_REDIRECT = "http://api.xxx.com/"

import requests
import ast
import time


TEST_USER = 'integration-test'

@app.route("/", methods=['GET', 'POST'])
def redirect_to_internal_api():
    start = time.process_time()
    rt = {'RetCode': 1}

    if request.method == 'POST':
        request_body = request.data
        dict_body = ast.literal_eval(request_body.decode('utf-8'))


        # get REMOTE_USER from CGI/WSGI environment
        sso_user = request.environ.get('REMOTE_USER')
        dict_body['SSOUser'] = sso_user if sso_user else TEST_USER

        print(dict_body)
        try:
            api_return = requests.get(API_WHICH_YOU_WANT_REDIRECT, params=dict_body)
            # OR send json via body
            # api_return = requests.get(API_WHICH_YOU_WANT_REDIRECT, json=dict_body)
            rt['api_return'] = api_return.json()
            rt['RetCode'] = 0
        except Exception as error:
            rt['Message'] = '{}'.format(error)

    else:
        rt['Message'] = '{} not allowed'.format(request.method)

    elapsed = time.process_time()
    elapsed = elapsed - start
    rt['elapsed'] = elapsed
    return jsonify(rt)
