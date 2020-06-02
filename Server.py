import numpy as np
import hashlib
import random
from flask import Flask, jsonify, request
import Moudle

app = Flask(__name__)


# Key Supply
@app.route("/getKeyRequest", methods=['POST'])
def Givekey():
    Bit = request.get_json()

    required = ['Bit']
    if not all(k in Bit for k in required):
        return 'Missing values', 400

    key = str(hex(random.randrange(
        pow(2, (Moudle.Bit(Bit['Bit'])-1)), pow(2, Moudle.Bit(Bit['Bit'])))))[2:]
    response = {
        # 'Serial Number': str(hashlib.sha256(key.encode()).hexdigest()),
        'Add a new key': key
    }
    return jsonify(response), 201


# Encrypting Code
@app.route("/getEncryptResponse", methods=["POST"])
def Verse1():
    values = request.get_json()
    required = ['Text', 'Key']
    if not all(k in values for k in required):
        return 'Missing values', 400

    __EPuzzle__ = ""
    # 16진수에서 2진수로 변환한 키
    EBinKey = str(bin(int('0x' + values['Key'], 16)))[2:]
    # Text에서 2진수로 변환한 평문
    EBinText = Moudle.BinText(values['Text'])
    # 2진수로 변환한 평문을 비트 수 만큼 슬라이싱
    ESliceText = Moudle.Slicetext(EBinText, 128, 1)
    ESliceKey = Moudle.Slicetext(EBinKey, 128, 0)

    for Key in ESliceKey:
        for Text in range(0, len(ESliceText)):
            ESliceText[Text] = Moudle.Change(ESliceText[Text], Key)

    for X in np.arange(0, len(ESliceText)):
        __EPuzzle__ += ESliceText[X]

    # 암호화한 2진수를 한글로 인코딩
    Encode = Moudle.NarasarangEncoding(__EPuzzle__)

    response = {
        'Encode': Encode,
        "EBinKey": EBinKey,
        "EBinText": EBinText,
        "ESliceText": ESliceText,
        "ESliceKey": ESliceKey
    }

    return jsonify(response), 201


# Decrypting Code
@app.route("/getDecryptResponse", methods=["POST"])
def Verse2():
    values = request.get_json()

    required = ['EncryptText', 'Key']
    if not all(k in values for k in required):
        return 'Missing values', 400

    __DPuzzle__ = ""

    DBinKey = str(bin(int('0x' + values['Key'], 16)))[2:]
    DBinText = Moudle.NarasarangDecoding(values['EncryptText'])
    DSliceText = Moudle.Slicetext(DBinText, 128, 0)
    DSliceKey = Moudle.Slicetext(DBinKey, 128, 0)

    for Key in DSliceKey:
        for Text in range(0, len(DSliceText)):
            DSliceText[Text] = Moudle.Change(DSliceText[Text], Key)
    for X in np.arange(0, len(DSliceText)):
        __DPuzzle__ += DSliceText[X]

    Decode = Moudle.TextBin(__DPuzzle__)

    response = {
        'Decode': Decode,
        "DBinKey": DBinKey,
        "DBinText": DBinText,
        "DSliceText": DSliceText,
        "DSliceKey": DSliceKey
    }

    return jsonify(response), 201


if __name__ == '__main__':
    app.run(debug=True)
