import pyperclip 

def get_clipboard_text():
    clipboard_content = pyperclip.paste()
    if isinstance(clipboard_content, str):
        return clipboard_content
    else:
        print("Clipboard content is not a string")
        return None

def set_clipboard_text(text):
    pyperclip.copy(text)
