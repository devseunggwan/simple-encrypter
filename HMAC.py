import hashlib
from flask import Flask, jsonify, request
from Crypto import Random
from Crypto.PublicKey import RSA


app = Flask(__name__)
IPAD = "00110110"
OPAD = "01011100"

# XOR 연산 손수 만듬
def xor(key1, key2):
    res = "0b"
    #첫번째 키랑 두번째 키랑 zip으로 묶어서 XOR 연산
    for i, j in zip(key1[2:], key2[2:]):
        if(i == j): res += "0"
        else: res += "1"
    return res

# RSA 비밀키와 공용키를 생성
@app.route("/rsa", methods=['GET'])
def createRSA():
    # RSA 비밀키를 생성하기 위해 임의의 난수 생성
    random_generator = Random.new().read

    # RSA 생성
    key = RSA.generate(1024, random_generator)


    # Private Key
    priKey = key.exportKey()
    # Private Key
    pubKey = key.publickey().exportKey()


    response = {
        'publickey': str(pubKey),
        'privateKey': str(priKey)
    }

    return jsonify(response), 201


# 평문을 SHA512 방식으로 암호화
@app.route("/sha512", methods=['POST'])
def createSHA512():
    req = request.get_json()

    required = ['Text']
    if not all(k in req for k in required):
        return 'Missing values', 400

    # 평문을 SHA-512 방식으로 암호화
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

    # ipad와 key를 xor
    ipadKey = hex(int(xor(("0b" + (IPAD * (len(binKey)//8))), ("0b" + binKey)), 2))
    # opad와 key를 xor
    opadKey = hex(int(xor(("0b" + (OPAD * (len(binKey)//8))), ("0b" + binKey)), 2))

    # ipadkey + message = sha512
    resMsg = hashlib.sha512((ipadKey + req["Message"]).encode('utf-8')).hexdigest()
    # opadkey + message = sha512
    resMsg = hashlib.sha512((opadKey + resMsg).encode("utf-8")).hexdigest()

    response = {
        'res': resMsg
    }

    return jsonify(response), 200


if __name__ == '__main__':
    app.run(debug=True)
