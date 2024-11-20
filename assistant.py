from groq import Groq
from functionlib.clipboard import get_clipboard_text
# from functionLib.clipboard import set_clipboard_text
from functionlib.vision import vision_prompt
from functionlib.webcam import web_cam_capture
from functionlib.screenFunctions import take_screenshot
from functionlib.speech import speak
# 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
import re
import time
import os
from faster_whisper import WhisperModel
import speech_recognition as sr
from lib.playsound import playsound
from functionlib.music import playMusicUsingBrowser
import threading

source = sr.Microphone()

start_time = None
wake_detected = False

r = sr.Recognizer()
# wake_word = 'jarvis'

wake_words = ['чучело', 'давай', 'слушай', 'Слушай сюда', 'хапс', 'ХАПС', 'playbox', 'Now play', 'play now', 'play me']

wake_screenshot_words = ['скриншот', 'скрин']

def start_listening():
    with source as s:
        r.adjust_for_ambient_noise(s, duration=2)
        while True:
            try:
                print("Listening...")
                audio = r.listen(source, timeout=5, phrase_time_limit=10)
                callback(r, audio)
            except sr.WaitTimeoutError:
                print("No speech detected. Listening again...")
            except KeyboardInterrupt:
                print("Stopping listening...")
                break


groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# def callback(recognizer, audio):
#     global start_time

sys_msg = (
    "You are a multi-modal AI voice assistant. Your user may or may not have attached a photo for context "
    "(either a screenshot or a webcam capture). Any photo has already been processed into a highly detailed "
    "text prompt that will be attached to their transcribed voice prompt. Generate the most useful and "
    "factual response possible, carefully considering all previous generated text in your response before "
    "adding new tokens to the response. Do not expect or request images, just use the context if added. "
    "Use all of the context of this conversation so your response is relevant to the conversation. Make "
    "your responses clear and concise, avoiding any verbosity. Response language is always Russian."
)

convo = [{'role': 'system', 'content': sys_msg}]

print('hi9')
def groq_prompt(prompt, img_context):
    if img_context:
        prompt = f'USER PROMPT: {prompt}\n\n    IMAGE CONTEXT: {img_context}'
    convo.append({'role': 'user', 'content': prompt})



    chat_completion = groq_client.chat.completions.create(messages=convo, model='llama3-70b-8192')
    response = chat_completion.choices[0].message
    # print(f'Groq response {response}')
    convo.append(response)

    return response.content
def function_call(prompt):
    sys_msg = (
        "You are an AI function calling model. You will determine whether extracting the user's clipboard content, "
        "taking a screenshot, capturing the webcam, or calling no functions is best for a voice assistant to respond "
        "to the user's prompt. The webcam can be assumed to be a normal laptop webcam facing the user. You will "
        "respond with only one selection from this list: ['terminate conversation', 'extract clipboard', 'take screenshot', 'play music', 'None'].\n"
        "Do not respond with anything but the most logical selection from that list with no explanations. Format the "
        "function call name exactly as I listed."
    )

    function_convo = [
        {'role': 'system', 'content': sys_msg},
        {'role': 'user', 'content': prompt}
    ]

    chat_completion = groq_client.chat.completions.create(
        messages=function_convo, 
        model="llama3-70b-8192"
    )
    response = chat_completion.choices[0].message

    return response.content

def playMusicPrompt(prompt):
    sys_msg = (
        "You are a music recommendation assistant. Your task is to decide the most suitable music genre or artist "
        "based on the user's prompt, which may describe a mood, activity, or specific preferences. "
        "If the prompt is related to mood, activity or genre respond with a short subject (e.g., 'Jazz', 'Morning routine', 'Walk in park', 'music for study', 'Sad mood'). "
        "If the prompt suggests a specific preference or known artist, respond with only the artist's name. "
        "Do not include punctuation, explanations, or additional text. Keep your response concise and to the point."
    )

    function_convo = [
        {'role': 'system', 'content': sys_msg},
        {'role': 'user', 'content': prompt}
    ]

    chat_completion = groq_client.chat.completions.create(
        messages=function_convo,
        model="llama3-70b-8192"
    )
    response = chat_completion.choices[0].message

    return response.content.strip()

num_cores = os.cpu_count()

whisper_size = 'base'
whisper_model = WhisperModel(
    whisper_size,
    device='cpu',
    compute_type='int8',
    num_workers=num_cores,
    cpu_threads=num_cores
)

def wav_to_text(audio_path):
    segments, _ = whisper_model.transcribe(audio_path)
    text = ''.join([segment.text for segment in segments])
    return text


def extract_prompt(transcribed_text, wake_words ,wake_detected=False):
    print("Extracting prompt")
    print(f'Transcribed text {transcribed_text}, wake detected {wake_detected}')

    

    """
    Extracts the prompt from transcribed text if any of the wake words are detected.
    
    Args:
        transcribed_text (str): The text to search for a wake word and extract a prompt.
        wake_words (list): A list of possible wake words.

    Returns:
        str: The extracted prompt if a wake word is found, otherwise None.
    """
    print(f"Transcribed Text: {transcribed_text}")
    # print(f"Wake Words: {wake_words}")

    if wake_detected:
        return transcribed_text.strip()
    # Build a regex pattern that matches any wake word from the list
    wake_words_pattern = '|'.join(re.escape(word) for word in wake_words)
    # print(f'Wake Words Pattern: {wake_words_pattern}')

    # pattern = rf'\b({wake_words_pattern})[\s,.?!]*([A-Za-z0-9].*)'
    pattern = rf'\b(?:{wake_words_pattern})[\s,.?!]*([\w\s]*)'
    # print(f"Pattern: {pattern}")

    # Search for the wake word in the transcribed text
    match = re.search(pattern, transcribed_text, re.IGNORECASE)
    if match:
        playsound('./boop.mp3')  # Play sound on detecting a wake word
        prompt = match.group(1).strip()  # Extract the prompt after the wake word
        return prompt
    else:
        return None

def construct_success_response(task_name, task_argument):
    sys_msg = (
        "You are a highly efficient AI assistant. Your task is to confirm the successful completion of a task based "
        "on the task name and its associated argument provided to you. "
        "- Use the `task_name` to identify what was done.\n"
        "- Use the `task_argument` to specify the details of the task.\n"
        "- Construct a response that clearly communicates success, directly acknowledges the task, and provides "
        "any relevant details from the argument.\n"
        "- Give descriptive response about user selection\n"

        "\n"
        "Example Outputs:\n"
        "- For `task_name`: 'set alarm' and `task_argument`: '7:00 AM', respond: 'The alarm has been set for 7:00 AM.'\n"
        "- For `task_name`: 'play song' and `task_argument`: 'Bohemian Rhapsody', respond in style of DJ on radio turning some track on. You can give feedback to user, describe user preference, give suggestion for next artist or ask a question\n"
        "- For `task_name`: 'send email' and `task_argument`: 'to John about the meeting', respond: 'The email to John about the meeting has been sent.'\n"
        "\n"
        "When the task name or argument is unclear, respond with: 'I'm sorry, I couldn't complete the task as requested. Please provide more details. Task execution would require some time, so say few more words. Respond in russian'"
    )

    function_convo = [
        {'role': 'system', 'content': sys_msg},
        {'role': 'user', 'content': f"Task Name: {task_name}, Task Argument: {task_argument}"}
    ]

    chat_completion = groq_client.chat.completions.create(
        messages=function_convo,
        model="llama3-70b-8192"
    )
    response = chat_completion.choices[0].message

    return response.content.strip()

def callback(recognizer, audio):
    global wake_detected, start_time
    prompt_audio_path = 'prompt.wav'
    with open(prompt_audio_path, 'wb') as f:
        f.write(audio.get_wav_data())

    prompt_text = wav_to_text(prompt_audio_path)
    clean_prompt = None
    # clean_prompt = extract_prompt(prompt_text, wake_words)


    # Check for wake word
    if not wake_detected:
        clean_prompt = extract_prompt(prompt_text, wake_words)
        if clean_prompt:
            print("Wake word detected!")
            wake_detected = True
            start_time = time.time()
            print(f"Prompt after wake word: {clean_prompt}")
            return  # Skip to the next iteration for 5-second listening
    else:
        # During 5-second listening window
        elapsed_time = time.time() - start_time
        if elapsed_time <= 15:
            clean_prompt = prompt_text
            print(f"Prompt within 15 seconds: {clean_prompt}")
                # Perform actions based on prompt
        else:
            print("15-second listening window ended.")
            wake_detected = False
            playsound('./boop2.mp3')

    print(f"clean_prompt: {clean_prompt}")
    print(f"prompt_text: {prompt_text}")

    if clean_prompt:
        call = function_call(clean_prompt)

        print(f'call: {call}')
        if 'play music' in call:
            groqMusicResponse = playMusicPrompt(clean_prompt)
            print('Suggesting music.')
            print(f"Groq Response: {groqMusicResponse}")
            successResponseText = construct_success_response('play music', groqMusicResponse)
            playsound('./boop.mp3')
            speak_thread = threading.Thread(target=speak, args=(successResponseText,))
            music_thread = threading.Thread(target=playMusicUsingBrowser, args=(groqMusicResponse,))

            # Start threads
            speak_thread.start()
            music_thread.start()
            speak_thread.join()
            music_thread.join()
            # speak(successResponseText)
            # playMusicUsingBrowser(groqMusicResponse)
            return
            # suggest_music(clean_prompt)
        if 'terminate conversation' in call:
            clean_prompt = 'Закончили разговор. Больше помощи не требуется пока что.'
            start_time = None
            wake_detected = False
            print("Terminating conversation.")
            response = groq_prompt(prompt=clean_prompt, img_context=visual_context)
            speak(response)
            return

        if 'take screenshot' in call:
        # if any(word in call for word in wake_screenshot_words):
            print('Taking screenshot.')
            take_screenshot()
            visual_context = vision_prompt(prompt=clean_prompt, photo_path='screenshot.jpg')

        # elif 'capture webcam' in call:
        #     print('Capturing webcam.')
        #     web_cam_capture()
        #     visual_context = vision_prompt(prompt=clean_prompt, photo_path='webcam.jpg')

        elif 'extract clipboard' in call:
            print('Extracting clipboard text.')
            paste = get_clipboard_text()
            clean_prompt = f'{clean_prompt} \n\n CLIPBOARD CONTENT: {paste}'
            visual_context = None

        else:
            visual_context = None
        response = groq_prompt(prompt=clean_prompt, img_context=visual_context)
        speak(response)
        start_time = time.time()
        wake_detected = True

        playsound('./boop2.mp3')
        print(response)
print(any(word in 'скрин.' for word in wake_screenshot_words))
start_listening()