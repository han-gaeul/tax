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
    """
    전체 예산(total_budgt)과 entertainment_expense를 고려해 비용 범위를 설정하고,
    그 범위 내에서 랜덤한 값을 생성하는 코드
    """
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

    """    
    total_budgt과 entertainment_expense를 이용해 travel_min과 travel_max를 설정
    travel_min은 예산에서 entertainment_expense를 제외한 금액의 13%로, travel_max는 16%로 설정
    이후 generate_random_expense 함수를 이용해 travel_min과 travel_max 사이의 랜덤값이 travel_expense로 할당
    마지막으로 round_to_10 함수를 이용해 travel_expense를 10 단위로 반올림하고,
    해당 값을 expense_values 리스트에서 812번 인덱스 위치에 할당
    """
    # 교통비 범위 설정 및 랜덤값 생성
    travel_min = int((total_budgt - entertainment_expense) * 0.13)
    travel_max = int((total_budgt - entertainment_expense) * 0.16)
    travel_expense = generate_random_expense(travel_min, travel_max)
    travel_expense = round_to_10(travel_expense)
    expense_values[find_expense_index(812)] = travel_expense

    # 통신비 범위 설정 및 랜덤값 생성
    communication_min = 1600000
    communication_max = 3600000
    communication_expense = generate_random_expense(communication_min, communication_max)
    communication_expense = round_to_10(communication_expense)
    expense_values[find_expense_index(814)] = communication_expense

    # 보험료 범위 설정 및 랜덤값 생성
    insurance_min = 3000000
    insurance_max = 4500000
    insurance_expense = generate_random_expense(insurance_min, insurance_max)
    insurance_expense = round_to_10(insurance_expense)
    expense_values[find_expense_index(812)] = insurance_expense

    # 도서인쇄비 범위 설정 및 랜덤값 생성
    books_min = int((total_budgt - entertainment_expense) * 0.05)
    books_max = int((total_budgt- entertainment_expense) * 0.06)
    books_expense = generate_random_expense(books_min, books_max)
    books_expense = round_to_10(books_expense)
    expense_values[find_expense_index(826)] = books_expense

    # 사무용품비 범위 설정 및 랜덤값 생성
    office_supplies_min = int((total_budgt - entertainment_expense) * 0.05)
    office_supplies_max = int((total_budgt - entertainment_expense) * 0.06)
    office_supplies_expense = generate_random_expense(office_supplies_min, office_supplies_max)
    office_supplies_expense = round_to_10(office_supplies_expense)
    expense_values[find_expense_index(829)] = office_supplies_expense

    # 소모품비 범위 설정 및 랜덤값 생성
    consumables_min = int((total_budgt - entertainment_expense) * 0.26)
    consumables_max = int((total_budgt - entertainment_expense) * 0.29)
    consumables_expense = generate_random_expense(consumables_min, consumables_max)
    consumables_expense = round_to_10(consumables_expense)
    expense_values[find_expense_index(830)] = consumables_expense

    # 지급수수료 범위 설정 및 랜덤값 생성
    fees_min = int((total_budgt - entertainment_expense) * 0.28)
    fees_max = int((total_budgt - entertainment_expense) * 0.32)
    fees_expense = generate_random_expense(fees_min, fees_max)
    fees_expense = round_to_10(fees_expense)
    expense_values[find_expense_index(831)] = fees_expense

    # 총 경비와 계산된 경비의 차액을 소모품비에 더하기
    difference = total_budgt - sum(expense_values)
    expense_values[find_expense_index(830)] += difference