from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
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


"""
웹 드라이버를 사용해 팝업 창의 개수를 기다리는 기능 구현

end_time 변수를 timeout 시간만큼 현재 시간에 추가하여 설정
현재 시간이 end_time보다 작은 동안 아래의 동작 반복
window_handles 속성을 사용해 현재 열린 창의 개수를 확인
확인한 창의 개수가 min_windows 이상이고 max_windows 이하라면 True 반환
time.time() 함수를 호출해 시간 업데이트
timeout 시간이 경과되면 False를 반환
"""
def wait_for_popup_range(driver, min_windows, max_windows, timeout):
    end_time = time.time() + timeout
    while time.time() < end_time:
        window_count = len(driver.window_handles)
        if min_windows <= window_count <= max_windows:
            return True
        time.time()
    return False


"""
메인 함수 초기 설정
"""
def tax():
    """
    브라우저를 제어할 때 사용되는 옵션을 설정

    selenium을 사용해 Chrome 브라우저를 제어할 때 사용할 옵션을 설정하기 위해 Options() 객체 생성
    '--disable-extensions'는 브라우저의 확장 기능을 비활성화하는 옵션. 설치된 확장 프로그램이 동작하지 않게 함
    '--disable-popup-blocking'은 팝업창 차단 기능을 비활성화하는 옵션. 웹 페이지에서 팝업창이 열리더라도 브라우저가 차단하지 않고 허용
    '--disable-infobars'는 브라우저 상단의 정보 표시줄을 비활성화하는 옵션. 정보 표시줄에 표시되는 브라우저의 상태와 관련된 정보를 제거해 화면을 깔끔하게 함
    '--disable-notifications'는 웹 페이지의 알림 기능을 비활성화하는 옵션. 웹 페이지가 알림을 표시하지 않게 설정함
    '--start-maximized'는 브라우저를 최대화된 상태로 시작하는 옵션. 브라우저 창의 크기를 최대로 확장해 화면 전체를 차지하게 설정함 
    """    
    # 브라우저 꺼짐 방지 및 브라우저 최대화 설정
    chrome_options = Options()
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-popup-blocking')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('--start-maximized')


    """
    크롬 드라이버는 크롬 브라우저와 상호작용해 명령을 전달하고 웹 페이지를 제어하는 역할을 담당
    하지만 브라우저는 지속적으로 업데이트 되며 새로운 기능과 보안 패치가 추가됨
    따라서 드라이버도 주기적으로 업데이트 되어야 함
    
    ChromeDriverManager().install()는 최신 버전의 크롬 드라이버를 자동으로 다운로드 및 설치하는 도구인 ChromeDriverManager를 사용
    """
    # 크롬 웹 드라이버 업데이트
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    """
    JavaScript 코드를 실행해 현재 브라우저 세션의 navigator 객체의 webdriver 속성을 재정의 함
    이를 통해 웹 페이지에서 자동화 도구인 selenium의 존재를 감지할 수 있는 기능을 우회할 수 있음
    """
    # 봇 감지 우회를 위한 파라미터 설정
    driver.execute_script('Object.defineProperty(navigator, "webdriver", {get: () => false});')
    """
    driver 객체를 사용해 지정된 url의 웹 페이지를 열도록 지시함
    """
    driver.get('url')
    """
    driver 객체를 사용해 웹 페이지가 로드되기를 기다리는 대기 객체를 생성
    WebDriverWait 클래스는 특정 조건이 충족될 때까지 대기할 수 있는 기능을 제공
    최대 30초 동안 웹 페이지가 로드될 때까지 기다리고, 이후에는 해당 대기 객체를 사용해 웹 페이지의 요소를 찾거나 조작
    """
    wait = WebDriverWait(driver, 30)


    """
    핸들은 윈도우나 창을 고유하게 식별하는 값
    이를 통해 나중에 메인 창으로 돌아올 때 사용
    """
    # 메인 창의 핸들 저장
    main_window_handle = driver.current_window_handle
    """
    'EC.number_of_windows_to_be(2)'는 현재 열린 창의 개수가 2개가 될 때까지 기도리도록 설정하는 조건
    """
    # 팝업이 나타날 때까지 기다림
    wait.until(EC.number_of_windows_to_be(2))
    """
    driver 객체를 사용해 메인 창으로 다시 전환
    이를 통해 팝업 창을 다룬 후 원래의 메인 창으로 돌아올 수 있음
    'switch_to.window()' 메서드는 지정된 핸들에 해당하는 창으로 전환
    """
    # 메인 창으로 돌아오기
    driver.switch_to.window(main_window_handle)


    """
    By.CSS_SELECTOR로 CSS 선택자를 사용해 클릭 가능한 요소를 찾고
    id_login_btn 요소를 클릭
    By.ID로 웹 페이지에서 ID로 요소를 찾음 
    """
    # 아이디로 로그인 버튼 클릭
    time.sleep(1)
    id_login_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'selector')))
    id_login_btn.click()
    wait.until(EC.element_to_be_clickable((By.ID, 'id')))



    """
    여러 사용자의 계정을 반복하여 로그인하기 위해 dicts 딕셔너리의 각 항목에서 사용자 ID와 비밀번호를 하나씩 가져옴
    By.ID로 웹 페이지에서 ID로 요소를 찾고, 찾은 ID 입력 필드에 이전에 입력되어 있을 수 있는 내용을 제거하고 새로운 ID를 입력함
    user_pw도 user_id와 동일한 작업 반복
    마지막으로 로그인에 사용된 사용자 정보를 제거하기 위해 dicts 딕셔너리에서 첫 번째 키를 가져와 제거 후 반복문 종료
    """
    # 로그인
    for user_id, user_pw in dicts.items():
        id_input = driver.find_element(By.ID, 'id')
        pw_input = driver.find_element(By.ID, 'id')
        id_input.clear()
        id_input.send_keys(user_id)
        pw_input.clear()
        pw_input.send_keys(user_pw)
        currunt_key = list(dicts.keys())[0]
        del dicts[currunt_key]
        break


    """
    By.ID로 웹 페이지에서 ID로 요소를 찾고, 찾은 요소를 클릭
    """
    # 로그인 버튼 클릭
    login_btn_elem = driver.find_element(By.ID, 'id')
    login_btn_elem.click()
    time.sleep(3)


    # 메인 창의 핸들 저장
    main_window_handle = driver.current_window_handle
    # 로그인 후 팝업이 나타날 때까지 기다림
    wait_for_popup_range(driver, 3, 5, 30)
    # 메인 창으로 돌아오기
    driver.switch_to.window(main_window_handle)
    # 메인 프레임 전환
    driver.switch_to.default_content()
    # 버튼 클릭
    elements = driver.find_elements(By.CLASS_NAME, 'name')
    for elem in elements:
        if elem.text == 'text':
            elem.click()
            break

    # 프레임 전환
    wait.until(EC.presence_of_element_located((By.NAME, 'frame')))
    driver.switch_to.frame('frame')

    # 버튼 클릭
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'css_selector'))).click()