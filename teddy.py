import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import webbrowser
import requests
import psutil
import re
import sys
import urllib.parse


listener = sr.Recognizer()


def speak(text):

    print("Teddy:", text)

    try:
        engine = pyttsx3.init("sapi5")

        voices = engine.getProperty("voices")

       
        if len(voices) > 1:
            engine.setProperty("voice", voices[1].id)

        engine.setProperty("rate", 170)
        engine.setProperty("volume", 1.0)

        engine.say(text)
        engine.runAndWait()
        engine.stop()

    except Exception as e:
        print("TTS Error:", e)

def listen():

    with sr.Microphone() as source:

        try:

     
            listener.adjust_for_ambient_noise(
                source,
                duration=0.3
            )

            audio = listener.listen(
                source,
                timeout=5,
                phrase_time_limit=8
            )

            command = listener.recognize_google(
                audio
            ).lower()

            print("You:", command)

            return command

        except sr.WaitTimeoutError:
            return ""

        except sr.UnknownValueError:
            return ""

        except sr.RequestError:
            print("Speech recognition service is unavailable.")
            speak("Sorry, I am having trouble connecting to the speech service.")
            return ""



def wait_for_teddy():

    print("\n--------------------------------")
    print("Teddy is sleeping...")
    print("Say: Hey Teddy")
    print("--------------------------------")

    while True:

        command = listen()

        if command == "":
            continue

        if (
            "hey teddy" in command
            or "hi teddy" in command
            or "hello teddy" in command
        ):

            speak("Yes, I'm listening.")

            return


def tell_time():

    current_time = datetime.datetime.now().strftime(
        "%I:%M %p"
    )

    speak(
        "The time now is " + current_time
    )



def tell_date():

    today = datetime.datetime.now().strftime(
        "%A, %d %B %Y"
    )

    speak(
        "Today's date is " + today
    )

def greeting():

    hour = datetime.datetime.now().hour

    if hour < 12:
        speak("Good morning.")

    elif hour < 18:
        speak("Good afternoon.")

    else:
        speak("Good evening.")

    speak("How can I help you?")



def tell_joke():

    try:

        joke = pyjokes.get_joke()

        speak(joke)

    except Exception:

        speak(
            "Sorry, I couldn't find a joke right now."
        )


def play_music(command):

    song = command.lower()

    song = song.replace("teddy", "")

    song = song.replace("play", "")
    song = song.replace("music", "")
    song = song.replace("song", "")

    song = song.strip()

    if song == "":

        speak(
            "What would you like me to play?"
        )

        return

    speak(
        "Playing " + song
    )

    try:

        pywhatkit.playonyt(song)

    except Exception as e:

        print("YouTube Error:", e)

        speak(
            "Sorry, I couldn't open YouTube."
        )

def google_search(command):

    query = command.lower()

    query = query.replace(
        "teddy",
        ""
    )

    query = query.replace(
        "search google",
        ""
    )

    query = query.replace(
        "search for",
        ""
    )

    query = query.replace(
        "search",
        ""
    )

    query = query.replace(
        "google",
        ""
    )

    query = query.strip()

    if query == "":

        speak(
            "What would you like me to search for?"
        )

        return

    speak(
        "Searching Google for " + query
    )

    url = (
        "https://www.google.com/search?q="
        + urllib.parse.quote(query)
    )

    webbrowser.open(url)


def wiki_search(command):

    query = command.lower()


    query = query.replace(
        "teddy",
        ""
    )

    query = query.replace(
        "who is",
        ""
    )

    query = query.replace(
        "what is",
        ""
    )

    query = query.replace(
        "tell me about",
        ""
    )

    query = query.replace(
        "what are",
        ""
    )

    query = query.replace(
        "who was",
        ""
    )

    query = query.replace(
        "wikipedia",
        ""
    )

    query = query.replace(
        "?",
        ""
    )

    query = query.strip()

    if query == "":

        speak(
            "What would you like to know?"
        )

        return

    print("Wikipedia search:", query)

    try:
        search_results = wikipedia.search(
            query,
            results=5
        )

        if not search_results:

            speak(
                "Sorry, I couldn't find information about "
                + query
            )

            return

   
        for result_name in search_results:

            try:

                result = wikipedia.summary(
                    result_name,
                    sentences=2,
                    auto_suggest=False
                )

                speak(result)

                return

            except wikipedia.exceptions.DisambiguationError:
                continue

            except wikipedia.exceptions.PageError:
                continue

        speak(
            "Sorry, I couldn't find information about "
            + query
            + " on Wikipedia."
        )

    except Exception as e:

        print("Wikipedia Error:", e)

        speak(
            "Sorry, I couldn't find information about "
            + query
            + " on Wikipedia."
        )


def weather():

    try:

        url = "https://wttr.in/Bengaluru?format=3"

        response = requests.get(
            url,
            timeout=10
        )

        if response.status_code == 200:

            result = response.text.strip()

            result = result.replace(
                "Bengaluru:",
                ""
            ).strip()

            speak(
                "The weather in Bengaluru is "
                + result
            )

        else:

            speak(
                "Sorry, I couldn't get the weather."
            )

    except Exception as e:

        print("Weather Error:", e)

        speak(
            "Sorry, I couldn't get the weather right now."
        )



def battery():

    try:

        battery_info = psutil.sensors_battery()

        if battery_info:

            percentage = battery_info.percent

            speak(
                "Your battery is at "
                + str(percentage)
                + " percent."
            )

        else:

            speak(
                "I couldn't find the battery information."
            )

    except Exception:

        speak(
            "I couldn't check the battery."
        )


def calculator(command):

    expression = command.lower()

    expression = expression.replace(
        "teddy",
        ""
    )

    
    expression = expression.replace(
        "what is",
        ""
    )

    expression = expression.replace(
        "calculate",
        ""
    )

    expression = expression.replace(
        "how much is",
        ""
    )

    expression = expression.replace(
        "multiplied by",
        "*"
    )

    expression = expression.replace(
        "divided by",
        "/"
    )

    expression = expression.replace(
        "plus",
        "+"
    )

    expression = expression.replace(
        "minus",
        "-"
    )

    expression = expression.replace(
        "times",
        "*"
    )

    expression = re.sub(
        r"\bx\b",
        "*",
        expression
    )

    expression = expression.replace(
        "?",
        ""
    )

    expression = expression.strip()

    print(
        "Calculator expression:",
        expression
    )

    if not re.fullmatch(
        r"[0-9+\-*/(). %]+",
        expression
    ):

        speak(
            "Sorry, I couldn't understand the calculation."
        )

        return

    try:

        result = eval(
            expression,
            {"__builtins__": None},
            {}
        )
         if isinstance(result, float) and result.is_integer():
            result = int(result)

        speak(
            "The answer is " + str(result)
        )

    except Exception:

        speak(
            "Sorry, I couldn't calculate that."
        )


def process_command(command):

    command = command.lower().strip()

    if command == "":
        return True



    if (
        "bye teddy" in command
        or "goodbye teddy" in command
        or "bye teddy" == command
        or command == "goodbye"
        or command == "bye"
        or command == "exit"
        or command == "stop"
        or command == "quit"
    ):

        speak(
            "Goodbye. See you later."
        )

        return False



    if (
        "calculate" in command
        or "plus" in command
        or "minus" in command
        or "times" in command
        or "multiplied by" in command
        or "divided by" in command
        or re.search(
            r"\d+\s*[+\-*/x]\s*\d+",
            command
        )
    ):

        calculator(command)

        return True



    if "time" in command:

        tell_time()

        return True



    if (
        "date" in command
        or "today's date" in command
        or "todays date" in command
    ):

        tell_date()

        return True


    if (
        "weather" in command
        or "temperature" in command
    ):

        weather()

        return True

    if (
        "battery" in command
        or "battery percentage" in command
    ):

        battery()

        return True



    if (
        "joke" in command
        or "funny" in command
    ):

        tell_joke()

        return True


    if (
        command.startswith("play ")
        or "play music" in command
        or "play song" in command
    ):

        play_music(command)

        return True


    if (
        command.startswith("search ")
        or command.startswith("google ")
        or "search google" in command
    ):

        google_search(command)

        return True


    if (
        "who is" in command
        or "who was" in command
        or "what is" in command
        or "what are" in command
        or "tell me about" in command
        or "wikipedia" in command
    ):

        wiki_search(command)

        return True


    if (
        "good morning" in command
        or "good afternoon" in command
        or "good evening" in command
        or command == "hello"
        or command == "hi"
    ):

        greeting()

        return True


    speak(
        "Sorry, I don't know how to do that yet."
    )

    return True


speak(
    "Hi, I am Teddy. Say Hey Teddy when you need me."
)



while True:

    wait_for_teddy()



    while True:

        print("\nTeddy is listening...")

        command = listen()

        if command == "":
            continue

        keep_running = process_command(command)

        if not keep_running:

            sys.exit()
