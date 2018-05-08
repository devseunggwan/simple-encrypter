import numpy as np
import hashlib
import random
from flask import Flask, jsonify, request
import Moudle

app = Flask(__name__)


#Key Supply
@app.route("/getKeyRequest", methods=['POST'])
def Givekey():
    Bit = request.get_json()

    required = ['Bit']
    if not all (k in Bit for k in required):
        return 'Missing values', 400

    key = str(hex(random.randrange (pow(2, (Moudle.Bit(Bit['Bit'])-1)), pow(2, Moudle.Bit(Bit['Bit'])))))[2:]
    response = {
        'Serial Number': str(hashlib.sha256(key.encode()).hexdigest()),
        'Add a new key': key
    }
    return jsonify(response), 201


#Encrypting Code
@app.route("/getEncryptResponse", methods=["POST"])
def Verse1():
    values = request.get_json()
    required = ['Text', 'Serial_Number', 'Key', 'Bit']
    if not all (k in values for k in required):
        return 'Missing values', 400

    EPuzzle = ""
    EBinKey = str(bin(int('0x' + values['Key'], 16)))[2:]                       # 16진수에서 2진수로 변환한 키
    EBinText = Moudle.BinText(values['Text'])                                   # Text에서 2진수로 변환한 평문
    ESlice = Moudle.Slicetext(EBinText, Moudle.Bit(values['Bit']), 1)           # 2진수로 변환한 평문을 비트 수 만큼 슬라이싱
    for X in np.arange(0,len(ESlice)):
        EPuzzle += Moudle.Change(ESlice[X],EBinKey)
    Encode = Moudle.NarasarangEncoding(EPuzzle)                    # 암호화한 2진수를 한글로 인코딩

    response = {
        'Encode': Encode
    }

    return jsonify(response), 201


#Decrypting Code
@app.route("/getDecryptResponse", methods=["POST"])
def Verse2():
    values = request.get_json()

    required = ['EncryptText', 'Serial_Number', 'Key', 'Bit']
    if not all (k in values for k in required):
        return 'Missing values', 400


    DPuzzle = ""
    DBinKey = str(bin(int('0x' + values['Key'], 16)))[2:]
    DBinText = Moudle.NarasarangDecoding(values['EncryptText'])
    DSlice = Moudle.Slicetext (DBinText, Moudle.Bit(values['Bit']), 0)
    for X in np.arange (0, len(DSlice)):
        DPuzzle += Moudle.Change (DSlice[X], DBinKey)
    Decode = Moudle.TextBin(DPuzzle)


    response = {
        'Decode': Decode
    }

    return jsonify(response), 201

if __name__ == '__main__':
    app.run(debug=True)
