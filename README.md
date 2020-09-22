# 개요

암호화 알고리즘을 사용하여 암, 복호화 할 수 있는 프로그램을 개발한다. 프로그램은 REST API로 제작하여 API 호출 시 반환 값으로 암, 복호화 값을 사용할 수 있도록 한다. 암호화 시 완전 이진트리 모양으로 문자를 섞고 한글로 인코딩하여 값을 반환한다. 복호화는 반대로 한글 인코딩을 풀고 완전 이진트리를 역으로 섞어 복호화를 진행한다.

사용한 제원은 다음과 같다.

- Language: Python 3.6.X
- API Server: Flask 1.X

# 사용 알고리즘

프로그램 제작 시 전치, 치환, 블록 알고리즘을 사용하여 내부 변환 모듈을 제작하였다.

- 전치(Transposition)
    - 문자 단위의 순서를 바꾸는 것이다.
    - 부여받은 키의 순서를 완전 이진트리 모양으로 변경할 때 사용하였고, 이와 인코딩된 문자를 XOR한다.
- 치환(Substitution)
    - 문자 단위를 다른 문자 단위로 바꾸는 것이다.
    - 한글 인코딩 시 사용하였다.
- 블록(Block) 암호화
    - 기밀성있는 정보를 정해진 블록 단위로 암호화하는 대칭키 시스템이다.
    - 인코딩 된 평문을 블록 단위로 나누어 대칭키를 사용해 암, 복호화를 하였다.

# 동작 **원리**

## 플로우 차트

### 암호화

1. 평문을 입력되면 평문을 ASCII 코드로 변환하여 이진화한다.
2. 서버로 부여받은 키를 라운드를 거치면서 섞고, 평문과 XOR한다.
3. 치환 테이블을 사용하여 6Bit씩 숫자에 맞는 한글로 인코딩된다.

![https://s3-us-west-2.amazonaws.com/secure.notion-static.com/c801e6e1-6be6-472a-aaa9-973028560ed2/Untitled.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/c801e6e1-6be6-472a-aaa9-973028560ed2/Untitled.png)

### 복호화

1. 암호문이 입력되면 치환 테이블을 사용하여 6Bit씩 한글에 맞는 숫자로 디코딩한다.
2. 암호화 시 사용했던 대칭키를 사용하여 암호화와 반대로 섞으면서 XOR을 진행한다.
3. ASCII 코드로 사용할 수 있도록 문장을 끊어서 복호화한다.

![https://s3-us-west-2.amazonaws.com/secure.notion-static.com/6ab98652-56a6-492f-9f48-260a5f6ba962/Untitled.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/6ab98652-56a6-492f-9f48-260a5f6ba962/Untitled.png)

# Server

### 대칭키 가져오기

- Request URL: getKeyRequest
- Method: POST
- Request Message
    - Bit: 암, 복호화에 사용할 대칭키의 Bit 수를 명세한다.

        ```json
        {
        		'1': 128, 
        		'2': 256, 
        		'3': 512, 
        		'4': 1024, 
        		'5': 2048, 
        		'6': 4096, 
        		'7': 8192, 
        		'8': 16384
        }
        ```

- Response Message
    - Add a new key: 요청된 Bit에 맞는 무작위 대칭키를 반환한다.

- Example

    ```json
    #URL(Test)
    http://localhost/getKeyRequest

    #Request
    {
    		'Bit': '1'
    }

    #Response
    {
    		'Add a new key': '128Bit Random Key'
    }
    ```

### 암호화

- Request URL: getEncryptResponse
- Method: POST
- Request Message
    - Text: 암호화를 할 문장을 적는다.
    - Key: 가져온 대칭키를 적는다.
- Response Message
    - Encode: 인코딩 된 문장이 반환된다.

- Example

    ```json
    #URL(Test)
    http://localhost/getEncryptResponse

    #Request
    {
    		'Text': 'Message'
    		'Key': '128Bit Random Key'
    }

    #Response
    {
    		'Encode': 'Encode Message'
    }
    ```

### 복호화

- Request URL: getDecryptResponse
- Method: POST
- Request Message
    - EncryptText: 암호화된 문장을 넣는다.
    - Key: 암호화 시 사용한 문장을 넣는다.
- Response Message
    - Decode: 복호화 된 평문이 반환된다.

- Example

    ```json
    #URL(Test)
    http://localhost/getDecryptResponse

    #Request
    {
    		'Text': 'Encode Message'
    		'Key': '128Bit Random Key'
    }

    #Response
    {
    		'Decode': 'Text'
    }
    ```

# 고려사항

1. 블록 알고리즘 특성 상, 블록으로 나눈 평문의 마지막은 대부분 블록 크기보다 작다. 그래서 블록 크기 만큼 평문의 마지막을 채우는데 0을 사용하였다. 복호화 시 패딩 제거할 때는 역순으로 진행하여 0을 제거하고 평문으로 변경하였다.
2. 서버 테스팅은 로컬(Localhost)에서만 진행했다. 그래서 외부로 호스팅할 때 사용하는 서버(Gunicorn, Nginx)은 사용하지 않았다.
