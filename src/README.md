★소스 실행 설정 안내★
========================

### 1. object detection 설치 (models 폴더 다운로드)
https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/installation.md


해당 링크를 보고 해당 소스 폴더에 models 폴더를 추가한다.

### 2. Chrome driver 또는 phantomjs driver 파일 다운로드 후 복사
main.py파일과 같은 위치에 Chrome driver 또는 phantomjs driver 파일을 다운로드 후 복사해 넣는다.
(크롤링 시 사용할 파일들)

### 3. 소스 설명
- 폴더 구조

: 모듈폴더, Data폴더, 모델폴더(object detection), main.py 파일로 구성되어 있다

: 즉

  |-module   <- py파일들이 모여있다.
  
  |-models    <- 이 부분은 직접 설치 후 생성  해야한다.
  
  |-data         <- csv파일을 불러오거나 저장할 폴더 / 포스터 이미지 파일이 저장될 폴더이다. 직접 생성
  
  |-main.py   <- 모든 실행을 가능하게하는 파이썬 파일

### 4. 파일 저장 경로 설정
:py파일 내 설정된 모든 파일 저장 및 파일 불러오기 경로를 본인이 실행하려는 폴더 경로로 지정해 줘야 한다.

:아래에 파일명에 따른 경로 설정 내용을 설명하겠다.

## module >merge_csv.py

data = pd.read_csv("/home/itwill02/project/test/data/"+str(i)+".csv")  -  data폴더로 지정

data1 = pd.read_csv("/home/itwill02/project/test/data/mdict"+str(i)+".csv") -  data폴더로 지정

a1.to_csv('/home/itwill02/project/test/data/'+str(i)+'.csv',mode='w',encoding='utf-8')   -  data폴더로 지정


## module >img_text_change.py

sys.path.append('/home/itwill02/models/research') -models 경로

sys.path.append('/home/itwill02/models/research/object_detection/utils')  -models 경로

cnt = len(os.listdir('/home/itwill02/project/data/poster1'))   -  data폴더로 지정

for i in (os.listdir('/home/itwill02/project/data/poster1')):   -  data폴더로 지정

file_name = '/home/itwill02/project/data/poster1/'+i   -  data폴더로 지정

df.to_csv("/home/itwill02/project/data/poster1/od_d.csv",mode="w",encoding="utf-8")   -  data폴더로 지정


## module >img_save.py

data = csv.reader(open('/home/itwill02/project/test/mdict'+str(year)+'.csv', 'r')) #csv 저장할 폴더 지정

for j in (os.listdir('/home/itwill02/project/data/poster1/')): #포스터(이미지 폴더) 가 저장되는 폴더 지정  data폴더로 지정

driver = webdriver.PhantomJS("/home/itwill02/project/phantomjs")     #pahntomjs가 있는 폴더 지정

with open('/home/itwill02/project/data/poster1/' + str(mn)+'.jpg', 'wb') as w: #이미지 파일 저장 폴더 지정  data폴더로 지정


## main.py

sys.path.append('/home/itwill02/project/test/module')  - 이 부분은 모듈 경로를 써준다.

url = '/home/itwill02/project/test/'                                   - 이 부분은 csv파일 저장 경로를 써준다. data폴더로 지정

result1 = pd.read_csv('/home/itwill02/project/test/data/total_res.csv')   -데이터 파일의 경로를 써준다. total_res.csv는 컬러데이터를 뺀 모든 정보가 들어있는 파일

result2 = pd.read_csv('/home/itwill02/project/test/data/total_color_data.csv')   - 데이터 파일 경로를 써준다. total_color_data.csv파일은 컬러 정보가 들어 있는 파일

test = pd.read_csv("/home/itwill02/project/test/data/youplz.csv")  -예측해볼 데이터가 들어있는 파일 경로를 써준다. youplz.csv는 에측할 포스터에서 추츨한 정보가 보관되어 있는 파일


### 5. main.py 실행안내

데이터 수집 및 정제 부분은 따로 실행하여도 되고 한번에 실행하여도 된다.
순서대로 진행하여도 된다.

