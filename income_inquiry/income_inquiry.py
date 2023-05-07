from selenium.webdriver.support.ui import WebDriverWait
from oauth2client.service_account import ServiceAccountCredentials
import logging, gspread, time


"""
경고 이상의 로그 메시지만 기록하고 나머지 정보는 필터링하기 위해 로그 레벨을 warning으로 설정
"""
# 로그 레벨을 WARNING으로 설정
logging.basicConfig(level=logging.WARNING)

# 인증 정보 로드
scope = [
    'url',
]
creds = ServiceAccountCredentials.from_json_keyfile_name(r'file root\file name.json', scope)
client = gspread.authorize(creds)
sheet_url = 'url'

# 시트 불러오기
doc = client.open_by_url(sheet_url)
sheet = doc.worksheet('sheet name')

# 시트의 특정 열을 복사해 딕셔너리 변환
dicts = dict(zip(sheet.col_values(2), sheet.col_vlues(3)))


"""
웹 드라이버(driver)가 특정 타이틀을 가진 창이나 페이지를 기다리는 기능을 수행
웹 애플리케이션의 특정 상태나 이벤트를 기다리는 동안 사용할 수 있음

WebDriverWait 객체를 생성해 웹 드라이버와 타임아웃 값을 전달
WebDriverWait 객체에 대해 until 메소드를 호출해 타이틀을 기다리는 조건을 정의함
조건은 람다 함수로 제공되며, 해당 함수는 드라이버의 타이틀이 목표 타이틀과 일치하는지 확인
WebDriverWait 객체는 주어진 타임아웃 내에서 조건이 충족될 때까지 기다림
조건이 충족되면 함수는 반환되고, 조건이 충족되지 않은 상태에서 타임아웃이 발생하면 'TimeoutException'이 발생
"""
def wait_for_window_title(driver, title, timeout = 10):
    WebDriverWait(driver, timeout).until(lambda d: d.title == title)


"""
특정 프린터의 모든 프린트 작업이 완료될 때까지 대기하는 기능 제공
프린트 작업이 완료된 후에 다음 작업을 수행할 수 있게 대기할 수 있음

wmi.WMI()를 사용해 wmi 모듈 초기화
c.Win32_PrintJob(DriverName=printer_name)을 사용해 특정 프린터의 프린트 작업 목록을 가져옴
DriverName 매개변수를 사용해 특정 프린터를 지정
만약 프린터의 작업 목록이 비어있다면, 루프를 탈출해 함수 종료
작업이 존재하는 경우, time.sleep(1)을 사용해 1초 동안 대기
이는 프린트 작업이 완료될 때까지 일정한 간격으로 체크하는 역할을 함
다시 루프의 시작으로 돌아가 작업 목록을 확인하는 과정 반복
"""
def wait_for_all_print_jobs(printer_name):
    c = wmi.WMI()
    while True:
        jobs = c.Win32_PrintJob(DriverName=printer_name)
        if not jobs:
            break
        time.sleep(1)