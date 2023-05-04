from tkinter import simpledialog
import pyperclip, pyautogui, time, numpy as np

"""
과목 딕셔너리
"""
expenses = {
    100: '과목1',
    101: '과목2',
    103: '과목3',
    104: '과목4',
    105: '과목5',
    106: '과목6',
    107: '과목7',
    108: '과목8'
}

"""
시간 간격 지정
"""
Sleep_Time = 0.3
Interval_Time = 0.2


"""
인자로 받은 number를 소수 첫째 자리에서 반올림한 결과를 반환하는 함수 선언
"""
def round_to_10(number):
    return round(number, 1)

"""
expenses 딕셔너리에서 인자로 받은 expense_code의 인덱스를 찾아 반환하는 함수 선언
list(expenses.keys())는 expenses의 키를 리스트로 반환
index() 메서드를 사용하여 expense_code가 해당 리스트에서 몇 번째 인덱스에 있는지 찾는 함수
"""
def find_expense_index(expense_code):
    return list(expenses.keys()).index(expense_code)

"""
min_value와 max_value 사이의 임의의 정수를 반환하는 함수 선언
반환되는 값은 min_value를 포함하고, max_value를 포함함
np.random.randint() 함수는 NumPy 라이브러리에서 제공하는 함수로,
인자로 받은 범위 내에서 임의의 정수를 생성함
"""
def generate_random_expense(min_value, max_value):
    return np.random.randint(min_value, max_value + 1)

"""
인자로 받은 value를 클립보드에 복사하고, 그 값을 현재 컴퓨터 화면에서
선택한 위치에 붙여넣고, 엔터 키를 누름
pyperclip.copy() 함수를 사용해 value를 클립보드에 복사하고,
pyautogui.hotkey() 함수를 사용해 복사된 값을 붙여넣기 함
그리고 pyautogui.press() 함수를 사용해 엔터키를 누르는 동작을 수행함
"""
def paste_clipboard_and_press_enter(value, enter_count = 1):
    pyperclip.copy(value)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(Sleep_Time)
    pyautogui.press('enter', presses=enter_count, interval=Interval_Time)

def main():
    
    """
    simpledialog 모듈을 사용해 사용자로부터 입력값 받기
    """
    #? 입력 구간
    # 필수 입력 사항 사용자 입력 받기
    total_income_input = simpledialog.askstring(title='제목', prompt='내용')
    if total_income_input is None:
        return
    income_rate_input = simpledialog.askstring(title='제목', prompt='내용')
    if income_rate_input is None:
        return
    
    # 입력받은 문자열을 int형변환
    total_income = int(total_income_input)
    income_rate = int(income_rate_input)

    # 선택 입력 사항
    income_tax_input = simpledialog.askstring(title='제목',prompt='내용')
    income_tax = int(income_tax_input) if income_tax_input else None
    if income_tax is not None:
        net_income = income_tax
    emergency_fund_input = simpledialog.askstring(title='제목', prompt='내용')
    emergency_fund = int(emergency_fund_input) if emergency_fund_input else None
    if emergency_fund is None:
        total_budgt = int(total_income) * ((100 - income_rate) / 100)
    else:
        total_budgt = int(total_income * ((100 / income_rate) / 100)) - emergency_fund

    #? 계산 구간
    # 비용 범위 설정
    entertainment_min = 11000000
    entertainment_max = 11999999

    """
    generate_random_expense 함수를 호출해 entertainment_expense 변수를 랜덤한 값으로 생성함
    이때, 함수의 입력값으로 entertainment_min, entertainment_max를 사용
    """
    # 비용 랜덤값 설정
    entertainment_expense = generate_random_expense(entertainment_min, entertainment_max)
    """
    round_to_10 함수를 호출해 entertainment_expense 값을 10의 배수로 반올림
    """
    entertainment_expense = round_to_10(entertainment_expense)
    """
    expense_values 변수를 선언하고 0으로 초기화
    """
    expense_values = [0] * len(expenses)

    """
    find_expense_index 함수를 호출해 813이라는 인덱스를 찾고,
    해당 인덱스의 값에 entertainment_expense 값을 할당
    """
    # 비용 저장
    expense_values[find_expense_index(813)] = entertainment_expense