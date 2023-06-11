import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class SimpleChatBot:
    def __init__(self, filepath):
        self.questions, self.answers = self.load_data(filepath)
               
    def load_data(self, filepath):
        data = pd.read_csv(filepath)
        questions = data['Q'].tolist()  # 질문열만 뽑아 파이썬 리스트로 저장
        answers = data['A'].tolist()   # 답변열만 뽑아 파이썬 리스트로 저장
        return questions, answers

    
    #레벤슈타인 거리 구하기
    def calc_distance(selef, a, b):
        ''' 레벤슈타인 거리 계산하기 '''
        
        if a == b: return 0 # 같으면 0을 반환
        a_len = len(a) # a 길이
        b_len = len(b) # b 길이
        if a == "": return b_len
        if b == "": return a_len
        # 2차원 표 (a_len+1, b_len+1) 준비하기 --- (※1)
        # matrix 초기화의 예 : [[0, 1, 2, 3], [1, 0, 0, 0, 0], [2, 0, 0, 0, 0], [3, 0, 0, 0, 0], [4, 0, 0, 0, 0]]
        # [0, 1, 2, 3]
        # [1, 0, 0, 0]
        # [2, 0, 0, 0]
        # [3, 0, 0, 0] 
        matrix = [[] for i in range(a_len+1)] # 리스트 컴프리헨션을 사용하여 1차원 초기화
        for i in range(a_len+1): # 0으로 초기화
            matrix[i] = [0 for j in range(b_len+1)]  # 리스트 컴프리헨션을 사용하여 2차원 초기화
        # 0일 때 초깃값을 설정
        for i in range(a_len+1):
            matrix[i][0] = i
        for j in range(b_len+1):
            matrix[0][j] = j
        # 표 채우기 --- (※2)
        
        # print(matrix,'----------')
        
        for i in range(1, a_len+1):
            ac = a[i-1]
            # print(ac,'=============')
            for j in range(1, b_len+1):
                bc = b[j-1] 
                # print(bc)
                cost = 0 if (ac == bc) else 1  #  파이썬 조건 표현식 예:) result = value1 if condition else value2
                matrix[i][j] = min([
                    matrix[i-1][j] + 1,     # 문자 제거: 위쪽에서 +1
                    matrix[i][j-1] + 1,     # 문자 삽입: 왼쪽 수에서 +1   
                    matrix[i-1][j-1] + cost # 문자 변경: 대각선에서 +1, 문자가 동일하면 대각선 숫자 복사
                ])
                #print(matrix)
            # print(matrix,'----------끝')
        return matrix[a_len][b_len]   
    

              
# CSV 파일 경로를 지정하세요.
filepath = 'ChatbotData.csv'

# 간단한 챗봇 인스턴스를 생성합니다.
chatbot = SimpleChatBot(filepath)

# while True:
input_sentence = input('Q : ')

#samples 리스트의 각 요소에 대해 calc_distance(base, n) 함수를 호출하여 레벤슈타인 거리를 계산하고, 이를 기준으로 리스트를 정렬
r = sorted(chatbot.questions, key = lambda n: chatbot.calc_distance(input_sentence,n))  

i = 0
for n in r:
    if i==0:
        print('찾은 질문 : ' , n)
    
        print('1. 레벤슈타인 거리 : ', chatbot.calc_distance(input_sentence, n))
        print('2. 질문의 인덱스   : ', chatbot.questions.index(n))
        print('3. chat의 답변   : ', chatbot.answers[chatbot.questions.index(n)])
        i=i+1
    else :
        break
