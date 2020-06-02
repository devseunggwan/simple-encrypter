import hashlib
from flask import Flask, jsonify, request
from Crypto import Random
from Crypto.PublicKey import RSA


app = Flask(__name__)
IPAD = "00110110"
OPAD = "01011100"

def xor(key1, key2):
    res = "0b"
    for i, j in zip(key1[2:], key2[2:]):
        if(i == j): res += "0"
        else: res += "1"
    return res

@app.route("/rsa", methods=['GET'])
def createRSA():
    random_generator = Random.new().read
    key = RSA.generate(1024, random_generator)

    priKey = key.exportKey()
    pubKey = key.publickey().exportKey()


    response = {
        'publickey': str(pubKey),
        'privateKey': str(priKey)
    }

    return jsonify(response), 201



@app.route("/sha512", methods=['POST'])
def createSHA512():
    req = request.get_json()

    required = ['Text']
    if not all(k in req for k in required):
        return 'Missing values', 400

    Hash = hashlib.sha512(req["Text"].encode('utf-8')).hexdigest()

    response = {
        'SHA-512': Hash
    }

    return jsonify(response), 201


@app.route("/hmac", methods=['POST'])
def hmac():
    req = request.get_json()
    required = ['Key', 'Message']
    if not all(k in req for k in required):
        return 'Missing values', 400

    binKey = bin(int("0x" + req['Key'], 16))[2:]
    binKey += "0"*(len(binKey) % 8)

    ipadKey = hex(int(xor(("0b" + (IPAD * (len(binKey)//8))), ("0b" + binKey)), 2))
    opadKey = hex(int(xor(("0b" + (OPAD * (len(binKey)//8))), ("0b" + binKey)), 2))

    resMsg = hashlib.sha512((ipadKey + req["Message"]).encode('utf-8')).hexdigest()
    resMsg = hashlib.sha512((opadKey + resMsg).encode("utf-8")).hexdigest()

    response = {
        'res': resMsg
    }

    return jsonify(response), 200


if __name__ == '__main__':
    app.run(debug=True)
