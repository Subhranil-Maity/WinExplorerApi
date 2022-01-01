from flask import *
import os
import pickle
import shutil

os.system("cls")
app = Flask(__name__)

seperator = "@@@"

# %3A = :
# %5C = \
# %5E = ^


with open('Token.pickle', 'rb') as handle:
    globalToken = pickle.load(handle)
with open('Admin.pickle', 'rb') as handle:
    globalAdmin = pickle.load(handle)
    AdminPass = globalAdmin['pass']


def haveAccess(token, tpass):
    try:
        raw = globalToken[token]
        if raw['pass'] == tpass:
            return True, raw['access']
    except:
        return False, {
            "read": False,
            "write": False,
            "delete": False
        }


def deleteAccess(token, tpass, apass):
    if apass == AdminPass:
        try:
            gpass = globalToken[token]['pass']
            if tpass == gpass:
                globalToken.pop(token)
                with open('Token.pickle', 'wb') as handle:
                    pickle.dump(globalToken, handle, protocol=pickle.HIGHEST_PROTOCOL)
                return True, {
                    "error": ""
                }
        except Exception as e:
            if e == '\'token\'':
                result = {
                    "error": "token does not exists"
                }
                return False, result

            return False, {}
    else:
        return False, {}


def createAccess(tpass, write, read, delete):
    pass


@app.route('/dir/<string:token>/<string:loc>', methods=['GET'])
def getdir(token: str, loc):
    try:
        tokenh = token.split(seperator)
        if len(tokenh) == 2:
            have, whatHave = haveAccess(token=tokenh[0], tpass=tokenh[1])
            if have:
                if whatHave['read']:
                    result = {
                        "path": loc,
                        "content": os.listdir(loc)
                    }
                else:
                    result = {
                        "error": "Not Have Access To Read"
                    }
            else:
                result = {
                    "error": "Token Value Not Accepted"
                }
        else:
            result = {
                "error": "token not properly encoded"
            }
    except:
        result = {
            "error": "token not properly encoded"
        }
    return result


@app.route('/mkdir/<string:token>/<string:loc>/<string:name>', methods=['GET'])
def mkdir(token, loc, name):
    try:
        tokenh = token.split(seperator)
        if len(tokenh) == 2:
            have, whatHave = haveAccess(token=tokenh[0], tpass=tokenh[1])
            if have:
                if whatHave['write']:
                    error = ""
                    try:
                        os.system("mkdir " + loc + "\\" + name)
                    except Exception as e:
                        error = str(e)
                    result = {
                        "path": loc,
                        "error": error
                    }
                else:
                    result = {
                        "error": "Not Have Access To Write"
                    }
            else:
                result = {
                    "error": "Token Value Not Accepted"
                }
        else:
            result = {
                "error": "token not properly encoded"
            }
    except:
        result = {
            "error": "token not properly encoded"
        }
    return result


@app.route('/touch/<string:token>/<string:loc>/<string:name>', methods=['GET'])
def touch(token, loc, name):
    try:
        tokenh = token.split(seperator)
        if len(tokenh) == 2:
            have, whatHave = haveAccess(token=tokenh[0], tpass=tokenh[1])
            if have:
                if whatHave['read']:
                    error = ""
                    try:
                        os.system("type nul >>" + loc + "\\" + name)
                    except Exception as e:
                        error = str(e)
                    result = {
                        "path": loc,
                        "error": error
                    }
                else:
                    result = {
                        "error": "Not Have Access To Read"
                    }
            else:
                result = {
                    "error": "Token Value Not Accepted"
                }
        else:
            result = {
                "error": "token not properly encoded"
            }
    except:
        result = {
            "error": "token not properly encoded"
        }
    return result


@app.route('/deleteaccess/<string:apass>/<string:token>/<string:tpass>', methods=['GET'])
def adelete(apass, token, tpass):
    boolstatus, result = deleteAccess(tpass=tpass, apass=apass, token=token)
    return result


@app.route('/delete/<string:token>/<string:path>', methods=['GET'])
def delete(token, path:str):
    # result = {}
    try:
        tokenh = token.split(seperator)
        if len(tokenh) == 2:
            have, whatHave = haveAccess(token=tokenh[0], tpass=tokenh[1])
            if have:
                if whatHave['delete']:
                    print(path)
                    if os.path.isdir(path):
                        # os.system("del /f " + path)
                        # print(path)
                        result = {
                            "error": os.system("rmdir /q /s " + path)
                        }
                    elif os.path.isfile(path):
                        result = {
                            "error": os.system("del /f " + path)
                        }
                    else:
                        result = {
                            "error": "File or Folder Does not Exists"
                        }
                else:
                    result = {
                        "error": "Not Have Access To Delete"
                    }
            else:
                result = {
                    "error": "Token Value Not Accepted"
                }
        else:
            result = {
                "error": "token not properly encoded"
            }
    except:
        result = {
            "error": "token not properly encoded"
        }
    return result


# "path": os.getcwd().replace("\\", "/"),
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
