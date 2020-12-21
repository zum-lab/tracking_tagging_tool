# Tracking Tagging Tool Manual

## Directory Structure
```sh
├─ tracking_tagging_tool
│  │  README.md
│  │  requirements.txt
│  │  run.py
│  │  app.py
│  ├─module
│  │  │  tagging.py
│  └─static
│  │  └─images
│  │  │  └─t1_video_00001
│  │  │    │  t1_video_00001_00001.jpg
│  │  │    │  t1_video_00001_00002.jpg
│  │  │    │  ...
│  │  └─json
│  │    │  tracking_result_1.json
│  └─templates
│    │  index.html
│    │  fin.html
```

## How to run
* pip install -r requirements.txt
* json 파일 세팅
	- ex) static/json/tracking_result_1.json
* image 파일 세팅
	- ex) static/imagest1_video_00001/*.jpg
* run.py의 host, port 수정

```sh
$ cd tracking_tagging_tool
$ python run.py
```

## How to use
### 기능
* 현재/이전 Frame, Tagging된 Bounding Box 시각화
* json 파일, Video ID, Frame ID를 이용한 Frame 검색
* 기존 Bounding Box 수정 및 삭제
* 새로운 Bounding Box 생성
* Tagging된 Tracking ID의 Frame 별 이미지 시각화

### URL
* /
* /fin

### /
![home](https://github.com/zum-lab/tracking_tagging_tool/blob/master/PNG/home.png)
1. 현재 Frame의 이미지와 Tagging된 Bounding Box
	- 현재 Frame 속 Tagging된 Bounding Box를 시각화
2. Reload 버튼
	- 저장하기 전, 현재 frame 새로고침
3. Tracking ID 리스트
	- Tagging 된 Tracking ID Bounding Box 시각화 활성화/비활성화
    	* 활성화/비활성화 할 Tracking ID 클릭
	- 전체 Tracking ID Bounding Box 시각화 활성화/비활성화
    	* All 버튼 클릭
	- Tagging 된 Tracking ID의 Bounding Box 수정
    	* 수정할 Tracking ID 상단 EDIT 버튼 클릭
        * Frame 이미지 위에 Bounding Box 생성 (시작 지점 클릭 후 끝 지점 클릭)
		* 변경된 Bounding Box 확인
    - Tagging 된 Tracking ID의 Bounding Box 삭제
    	* 삭제할 Tracking ID 상단 DELETE 버튼 클릭
        * 삭제된 Bounding Box 확인
4. 새로운 Bounding Box 생성
	- Tracking ID의 타입 별로 Bounding Box 생성
    	* Tagging 할 Tracking ID 타입 선택
        * 새로운(new)/기존 Tracking ID 클릭
        * Frame 이미지 위에 Bounding Box 생성 (시작 지점 클릭 후 끝 지점 클릭)
5. Save 버튼
	- 수정, 삭제, 생성으로 변경된 Bounding Box를 json 파일에 저장
6. 검색기
	- 이전/다음 Frame 검색
    	* PREV/NEXT 버튼 클릭
	- 특정 Frame 검색
    	* json 파일, Video ID, Frame ID 설정 후 SEARCH 버튼 클릭
7. Show result 버튼
	- /fin 으로 redirect
    - Tagging 된 Tracking ID의 Frame 별 이미지 시각화
8. 이전 Frame 이미지와 Tagging된 Bounding Box
	- 바로 이전 Frame 이미지를 시각화하여 현재 Frame과 비교 가능

### /fin
![fin](https://github.com/zum-lab/tracking_tagging_tool/blob/master/PNG/fin.png)
1. Back 버튼
	- 현재의 json 파일, Video ID 정보를 가지고 Tagging 화면('/')으로 돌아가기
2. 검색기
	- 특정 Tracking ID의 Frame 별 이미지 검색
    	* json 파일, Video ID, Tracking ID 설정 후 자동 검색
3. Crop된 이미지들
	- Frame ID 별 Tagging 된 Tracking ID의 이미지
    - 이미지 클릭 시 Frame 이미지에 해당 Tracking ID만 활성화 된 Tagging 화면('/') 확인


## Ack
이 프로그램은 2019년도 과학기술정보통신부의 인공지능산업원천기술개발 사업의 일환으로 정보통신기획평가원의 지원을 받아 수행된 연구임 (과제번호 : 2019-0-01762)  
This work was supported by Institute of Information & communications Technology Planning & Evaluation (IITP) grant funded by the Korea government (MSIT)  


















