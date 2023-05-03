import numpy as np
import pyperclip, pyautogui, time

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