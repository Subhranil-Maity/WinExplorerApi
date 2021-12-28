from flask import *
import os

os.system("cls")
app = Flask(__name__)
'''
@app.route('/')  
def message():  
      return "Hello, World" 

@app.route('/get', methods=["GET"])
def testpost():
     return os.getcwd()

@app.route('/foo', methods=['POST']) 
def foo():
    data = request.json
    return jsonify(data)
'''


# %3A = :
# %5C = \

@app.route('/dir/<string:loc>', methods=['GET'])
def getdir(loc):
    return {
        "path": loc,
        "content": os.listdir(loc)
    }


@app.route('/mkdir/<string:loc>/<string:name>', methods=['GET'])
def mkdir(loc, name):
    error = ""
    try:
        os.system("mkdir " + loc + "\\" + name)
    except Exception as e:
        error = str(e)
    return {
        "path": loc,
        "error": error
    }


@app.route('/touch/<string:loc>/<string:name>', methods=['GET'])
def touch(loc, name):
    error = ""
    try:
        os.system("type nul >>" + loc + "\\" + name)
    except Exception as e:
        error = str(e)
    return {
        "path": loc,
        "error": error
    }


# "path": os.getcwd().replace("\\", "/"),
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
