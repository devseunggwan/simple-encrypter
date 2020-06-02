import random
import numpy as np

# Choice Key Bit


def Bit(Code: int) -> int:
    Bit = {'1': 128, '2': 256, '3': 512, '4': 1024,
           '5': 2048, '6': 4096, "7": 8192, "8": 16384}
    return Bit[Code]


#Slicing & Padding
# Bintext: Text, Bit: 128, Switch: Text(Encode or Decode) or Key
def Slicetext(Bintext: str, Bit: int, Switch: int) -> list:
    X = [""] * ((len(Bintext) // Bit) + Switch)
    for i in np.arange(0, ((len(Bintext)//Bit)+Switch)*Bit, Bit):
        if(len(Bintext[i:]) == 0):
            break
        elif(len(Bintext[i:]) < Bit):
            X[i // Bit] = Bintext[i:]
            if((((len(Bintext)//Bit)+1)*Bit) - len(Bintext) < 7):

                # '0' 패딩 개수가 '7' 이하일 때 '0'으로만 padding
                for SupplyZero in np.arange(len(Bintext), ((len(Bintext) // Bit) + 1) * Bit):
                    X[(i // Bit)] += "0"
            else:
                # '0' 패딩 개수가 '7' 이상일 때 '0' 7개를 padding
                for SupplyZero in np.arange(len(Bintext), (len(Bintext)+7)):
                    X[(i//Bit)] += "0"

                # '0' 과 '1' 를 빈 곳 끝까지 padding
                X[(i//Bit)] += bin(random.randrange(pow(2, (((len(Bintext)//Bit)+1)*Bit -
                                                            ((len(Bintext)+7)) - 1)), pow(2, (((len(Bintext)//Bit)+1)*Bit-((len(Bintext)+7))))))[2:]

        # (0:Bit) 수 만큼 Slice 실행
        else:
            X[i//Bit] = Bintext[i:(i+Bit)]
    return X

# 문자->ASCII->2진수


def BinText(Text: str):
    Testcase = ""
    for i in Text:
        # 문자->ASCII->2진수화
        T = str(bin(ord(i))[2:])
        if(len(T) < 7):
            Testcase += (((7 - len(T)) * "0") + T)        # 7Bit 아닐시 7비트형으로 만듬
        else:
            Testcase += T                                           # 2진수 문자 저장
    return Testcase


# 2진수 -> 10진수
def TextBin(Text: str) -> int:
    Tenlist = ""
    for X in np.arange(0, len(Text), 7):
        if (("1" not in ((Text[X:X+7] or Text[X:]))) == True):
            break
        Tenlist += chr(int(("0b"+Text[X:X+7]), 2))
    return Tenlist

# 복호화(XOR) 연산 모듈
# key: 키, binary: 자르기횟수 N (pow(2, N-1)


def KeyDevide(Key: str, binary: int) -> str:
    ReturnValue = ""
    if binary == 0:
        return Key
    Key = list(Key)
    boxNum = pow(2, binary)
    field = len(Key) // boxNum
    nextIndex = len(Key) // (2 ** (binary - 1))
    for i in np.arange(0, len(Key), nextIndex):
        Key[i:i+field], Key[i+field:i+field *
                            2] = Key[i+field:i+field*2], Key[i:i+field]
    for Y in np.arange(0, len(Key)):
        ReturnValue += Key[Y]
    return ReturnValue


def Change(Text: str, Key: str):
    for X in np.arange(1, 1025):
        if (len(Key) == int(pow(2, X))):
            repeat = X
            break

    for Y in np.arange(0, repeat + 1):
        Key = KeyDevide(Key, Y)
        Text = CryptCode(Text, Key, len(Key))

    return Text


# 암호화(XOR) 연산 모듈
def CryptCode(Text: str, Key: str, Bit: int) -> str:
    Code = ""
    for i in np.arange(0, Bit):
        if(Key[i] != Text[i]):
            Code += "1"
        elif(Key[i] == Text[i]):
            Code += "0"
    return Code


# 2진수를 한글로 바꾸는 모듈
def NarasarangEncoding(Code: str) -> str:
    Save = ""
    for i in np.arange(0, ((len(Code)//6)*6), 6):
        Save += NarasarangEncode(Code[i:i+6])
    Save += NarasarangEncode(Code[((len(Code)//6)*6):] +
                             ((6-(len(Code) % 6))*"0"))
    return Save


# 한글을 2진수로 바꾸는 모듈
def NarasarangDecoding(Code: str) -> str:
    Save = ""
    for X in np.arange(0, len(Code)):
        Save += NarasarangDecode(Code[X])
    return Save[:((len(Save)-(((int(np.log2(len(Save))) % 2)*2)+2)))]


# Base64 기반 이진수 한글화 코드 변환기
def NarasarangEncode(Code: str) -> str:
    Dictionary = {
        "000000": "가", "000001": "나", "000010": "다", "000011": "라", "000100": "마", "000101": "바", "000110": "사", "000111": "아", "001000": "자", "001001": "차", "001010": "카", "001011": "타", "001100": "파", "001101": "하", "001110": "거", "001111": "너", "010000": "더", "010001": "러", "010010": "머", "010011": "버", "010100": "서", "010101": "어", "010110": "저", "010111": "처", "011000": "커", "011001": "터", "011010": "퍼", "011011": "허", "011100": "고", "011101": "노", "011110": "도", "011111": "로", "100000": "모", "100001": "보", "100010": "소", "100011": "오", "100100": "조", "100101": "초", "100110": "코", "100111": "토", "101000": "포", "101001": "호", "101010": "구", "101011": "누", "101100": "두", "101101": "루", "101110": "무", "101111": "부", "110000": "수", "110001": "우", "110010": "주", "110011": "추", "110100": "쿠", "110101": "투", "110110": "푸", "110111": "후", "111000": "밥", "111001": "술", "111010": "껌", "111011": "집", "111100": "물", "111101": "불", "111110": "강", "111111": "꿈"
    }
    return Dictionary[Code]

# Base64 기반 한글화 코드 이진수 변환기


def NarasarangDecode(Code):
    Dictionary = {
        "가": "000000", "나": "000001", "다": "000010", "라": "000011", "마": "000100", "바": "000101", "사": "000110", "아": "000111", "자": "001000", "차": "001001", "카": "001010", "타": "001011", "파": "001100", "하": "001101", "거": "001110", "너": "001111", "더": "010000", "러": "010001", "머": "010010", "버": "010011", "서": "010100", "어": "010101", "저": "010110", "처": "010111", "커": "011000", "터": "011001", "퍼": "011010", "허": "011011", "고": "011100", "노": "011101", "도": "011110", "로": "011111", "모": "100000", "보": "100001", "소": "100010", "오": "100011", "조": "100100", "초": "100101", "코": "100110", "토": "100111", "포": "101000", "호": "101001", "구": "101010", "누": "101011", "두": "101100", "루": "101101", "무": "101110", "부": "101111", "수": "110000", "우": "110001", "주": "110010", "추": "110011", "쿠": "110100", "투": "110101", "푸": "110110", "후": "110111", "밥": "111000", "술": "111001", "껌": "111010", "집": "111011", "물": "111100", "불": "111101", "강": "111110", "꿈": "111111"
    }
    return Dictionary[Code]
