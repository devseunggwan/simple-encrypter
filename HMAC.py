import hashlib
from flask import Flask, jsonify, request
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
import hmac


app = Flask(__name__)
IPAD = "00110110"
OPAD = "01011100"


def xor(key1, key2):
    res = "0b"

    for i, j in zip(key1[2:], key2[2:]):
        if(i == j):
            res += "0"
        else:
            res += "1"
    return res


@app.route("/aes", methods=['POST'])
def encryptAES():
    req = request.get_json()

    required = ['IV', 'Key', 'Message', "Type"]
    if not all(k in req for k in required):
        return 'Missing values', 400

    aes = AES.new(req['Key'], AES.MODE_CBC, req['IV'])
    response = dict()

    if(req['Type'] == "Encrypt"):
        cipherText = aes.encrypt(req['Message'])
        response['Cipher Text'] = cipherText.hex()

    elif(req['Type'] == "Decrypt"):
        originText = aes.decrypt(bytes.fromhex(req['Message']))
        response['Original Text'] = str(originText)[2:-1]

    return jsonify(response), 201


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

    required = ['Message']
    if not all(k in req for k in required):
        return 'Missing values', 400

    Hash = hashlib.sha512(req["Message"].encode('utf-8')).hexdigest()

    response = {
        'SHA-512': Hash
    }

    return jsonify(response), 201


@app.route("/hmac", methods=['POST'])
def HMAC():
    req = request.get_json()
    required = ['Key', 'Message', 'keyType', 'resType']
    if not all(k in req for k in required):
        return 'Missing values', 400

    if(req['keyType'] == "RSA"):
        binKey = req['Key'].hex()

    elif(req['keyType'] == "SHA"):
        binKey = bin(int("0x" + req['Key'], 16))[2:]
        binKey += "0"*(len(binKey) % 8)

    ipadKey = hex(
        int(xor(("0b" + (IPAD * (len(binKey)//8))), ("0b" + binKey)), 2))
    opadKey = hex(
        int(xor(("0b" + (OPAD * (len(binKey)//8))), ("0b" + binKey)), 2))

    resMsg = hashlib.sha512(
        (ipadKey + req["Message"]).encode('utf-8')).hexdigest()
    resMsg = hashlib.sha512((opadKey + resMsg).encode("utf-8")).hexdigest()

    response = dict()
    if(req['resType'] == "0"):
        response['res'] = resMsg

    elif(req['resType'] == "1"):
        res = 0
        if(resMsg == req['hmac']):
            res = 1
        response['res'] = res

    return jsonify(response), 200


if __name__ == '__main__':
    app.run(debug=True)
