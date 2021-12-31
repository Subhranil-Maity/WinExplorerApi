import pickle

a = {
    "test": {
        "name": "test",
        "access": {
            "read": True,
            "write": True,
            "delete": True
        },
        "pass": "testllb"
    }
}

def TokenReset():
    with open('Token.pickle', 'wb') as handle:
        pickle.dump(a, handle, protocol=pickle.HIGHEST_PROTOCOL)
if __name__ == '__main__':
    TokenReset()