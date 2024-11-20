import pygetwindow as gw
import pyautogui
import pyperclip
import time
import subprocess

# Launch a program by its full path


def playMusicUsingBrowser(subject):
    program_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    subprocess.Popen([program_path])
    # Список ключевых слов, которые могут быть в заголовках браузеров
    # browser_keywords = ["Chrome", "Firefox", "Edge", "Opera", "Safari"]

    # Получение всех окон
    # windows = gw.getAllTitles()

    # # Поиск окна браузера
    # for title in windows:
    #     if any(keyword in title for keyword in browser_keywords):
    #         window = gw.getWindowsWithTitle(title)[0]
    #         window.activate()  # Активируем найденное окно
    # print(f"Активировано окно: {title}")
    time.sleep(1)  # Небольшая пауза, чтобы окно активировалось

    pyautogui.hotkey("ctrl", "t")
    time.sleep(1)  # Небольшая пауза, чтобы окно активировалось
    # pyautogui.typewrite('https://music.youtube.com/search?q=расслабляющая+музыка', interval=0.1)  # interval добавляет задержку между символами
    # Копируем текст в буфер обмена
    # replace all spaces with +
    # subject = subject.replace(" ", "+")

    pyperclip.copy(f'https://music.youtube.com/search?q={subject.replace(" ", "+")}')

    # Вставляем текст через Ctrl+V
    pyautogui.hotkey("ctrl", "v")
    time.sleep(1)  # Небольшая пауза, чтобы окно активировалось
    pyautogui.press('enter')
    time.sleep(3)   # Небольшая пауза, чтобы окно активировалось
    pyautogui.press('tab')
    time.sleep(1)  # Небольшая пауза, чтобы окно активировалось
    pyautogui.press('tab')
    time.sleep(1)  # Небольшая пауза, чтобы окно активировалось
    pyautogui.press('tab')
    time.sleep(1)  # Небольшая пауза, чтобы окно активировалось
    pyautogui.press('enter')
    time.sleep(3)   # Небольшая пауза, чтобы окно активировалось
    pyautogui.press('tab')
    time.sleep(1)  # Небольшая пауза, чтобы окно активировалось
    pyautogui.press('tab')
    time.sleep(1)  # Небольшая пауза, чтобы окно активировалось
    pyautogui.press('enter')
    time.sleep(1)  # Небольшая пауза, чтобы окно активировалось
    
    pyautogui.press('tab')
    time.sleep(1)  # Небольшая пауза, чтобы окно активировалось
    pyautogui.press('enter')
    return

    # print("Не найдено ни одного окна браузера.")

# Вызываем функцию
# activate_browser_window()