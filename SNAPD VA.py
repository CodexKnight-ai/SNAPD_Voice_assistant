import speech_recognition as sr # to recognize user's voice
import pyttsx3 as p         #Speech to text
import wikipedia        
from newsapi import NewsApiClient
import datetime
from googletrans import Translator
import google.generativeai as genai   #Gemini
from rich import print    
from time import time as t
import pyautogui     # help in performing opening functions.
import speedtest
import pywhatkit    #play youtube video
import webbrowser 
import requests
from bs4 import BeautifulSoup

# Initialize text-to-speech engine
engine = p.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', 170)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Configure generative AI model
generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 300,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_ONLY_HIGH"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"},
]

model = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_config,
    safety_settings=safety_settings
)

genai.configure(api_key="AIzaSyCy2Wp-ssqKO9PLwMyffE13gJSWooh4U48")

# Initialize News API client
newsapi = NewsApiClient(api_key='bcaf8ac7fde14478852d399610f1e1b4')  # Replace with your actual News API key

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to get Wikipedia summary
def get_wikipedia_summary(query, sentences=1):
    try:
        page = wikipedia.page(query)
        summary = wikipedia.summary(query, sentences=sentences)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Disambiguation Error: {e.options}"
    except wikipedia.exceptions.PageError as e:
        return f"Page Error: {e}"

# Function to get top news headlines
def get_news(num_headlines=5):
    try:
        newsapi = NewsApiClient(api_key='bcaf8ac7fde14478852d399610f1e1b4')  # Replace with your actual News API key
        headlines = newsapi.get_top_headlines(language='en', country='in')
        articles = headlines.get('articles', [])[:num_headlines]
        if articles:
            news_text = f"Here are the top {num_headlines} news headlines for today in India:\n"
            for index, article in enumerate(articles, start=1):
                news_text += f"{index}. {article['title']}\n"
            return news_text
        else:
            return "Sorry, I couldn't retrieve the news at the moment."
    except Exception as e:
        return f"Error fetching news: {e}"
# Function to get current time
def get_current_time():
    try:
        now = datetime.datetime.now()
        return now.strftime("%H:%M")
    except Exception as e:
        return f"Error getting current time: {e}"
    
# Function to get current date
def get_current_date():
    today = datetime.datetime.now()
    return today.strftime("%A, %B %d, %Y")

# Function to translate a sentence
def translate_sentence(sentence, target_language='en'):
    try:
        translator = Translator()
        translation = translator.translate(sentence, dest=target_language)
        return translation.text
    except Exception as e:
        return f"Translation failed. Error: {e}"

def search_google(query):
    try:
        import wikipedia as googleScrap
        query = query.replace("SNAPD", "")
        query = query.replace("google search", "")
        query = query.replace("google", "")
        speak("This is what I found on Google")
        pywhatkit.search(query)
        result = googleScrap.summary(query, 1)
        speak(result)
    except Exception as e:
        speak(f"Google search failed. Error: {e}")

# Function to search YouTube
def search_youtube(query):
    try:
        speak("This is what I found for your search")
        query = query.replace("youtube search", "")
        query = query.replace("youtube", "")
        query = query.replace("SNAPD", "")
        web = "https://www.youtube.com/results?search_query=" + query
        webbrowser.open(web)
        pywhatkit.playonyt(query)
        speak("Done Sir")
    except Exception as e:
        speak(f"YouTube search failed. Error: {e}")

def close_application(application_name):
    pyautogui.hotkey('alt','f4')

# Function for Gemini voice assistant
def Gemini(prompt):
    messages = [
        {
            "parts": [
                {
                    "text": "You are a Powerful AI Assistant Named SNAPD. Hello, How are you?"
                }
            ],
            "role": "user"
        },
        {
            "parts": [
                {
                    "text": "Hello, I am doing well. How can I help you?"
                }
            ],
            "role": "model"
        }
    ]
    messages.append({
        "parts": [
            {
                "text": prompt + "***reply in less tokens***"
            }
        ],
        "role": "user"
    })

    response = model.generate_content(messages)

    messages.append({
        "parts": [
            {
                "text": response.text
            }
        ],
        "role": "model"})

    return response.text

# Initialize speech recognition
r = sr.Recognizer()

# Welcome message
print("Welcome BOSS, I am S.N.A.P.D, your dedicated voice assistant. How can I help you today?")
speak("Welcome BOSS, I am SNAPD, your dedicated voice assistant. How can I help you today?")
# print("----------------------------------------------------------------------------------")
# print("1. Wikipedia Search: Say 'Give me some information'...") 
# print("2. News Headline: Say 'Tell me the news...' ")  
# print('''3. Current time: Say "What's the time..." ''') 
# print('''4. Current Date: Say "What's the date..." ''') 
# print("5. Translate a sentence: Say 'I want to translate a sentence...' ") 
# print("6. Open an application: Say 'Open [..Application...]' ")
# print("7. Internet Speed Test: Say 'Tell me my internet speed...' ")
# print("8. Google Search: Say 'Google [...Query...]' ")  
# print("9. Youtube Search : Say 'Youtube [...Query...]' ") 
# print("10. Gemini AI: Say 'Gemini...' ")      
# print("11. Take Screenshot: Say 'Screenshot...' ") 
# print("12. Take your picture: Say 'Click my photo...'") 
# print("13. Temperature: Say 'Tell me the temperature...'")
# print("14. Closing the SNAPD: Say 'Go to sleep...'")
print("----------------------------------------------------------------------------------")



# Main loop for handling user commands
while True:
    try:
        with sr.Microphone() as source:
            r.energy_threshold = 10000
            r.adjust_for_ambient_noise(source, 1.2)
            print('listening...')
            audio = r.listen(source)
            text2 = r.recognize_google(audio)
            
            if any(word in text2.lower() for word in ["sleep","stop"]):
                print("Goodbye! Have a great day.")
                speak("Goodbye! Have a great day.")
                break
            elif any(word in text2.lower() for word in ["what ","can","you","do"]): 
                print("I can look up things on Wikipedia, tell you the latest news, give you the time and date, translate sentences, open apps, test your internet speed, search on Google and YouTube, chat with Gemini AI, take screenshots and photos, tell you the temperature, and go to sleep when you're done.")
                speak("I can look up things on Wikipedia, tell you the latest news, give you the time and date, translate sentences, open apps, test your internet speed, search on Google and YouTube, chat with Gemini AI, take screenshots and photos, tell you the temperature, and go to sleep when you're done.")
            elif "information" in text2.lower():
                speak("You need information related to which topic?")
                with sr.Microphone() as source:
                    r.energy_threshold = 10000
                    r.adjust_for_ambient_noise(source, 1.2)
                    print('listening...')
                    audio = r.listen(source)
                    infor = r.recognize_google(audio)

                speak("Searching {} in Wikipedia".format(infor))
                summary = get_wikipedia_summary(infor)
                print("Here is a summary of {} from Wikipedia: {}".format(infor, summary))
                speak("Here is a summary of {} from Wikipedia: {}".format(infor, summary))
                

       

            elif any(word in text2.lower() for word in ["news", "current affair"]):
                speak("Fetching the latest news headlines. Please wait.")
                news_text = get_news()
                print(news_text)
                speak(news_text)

            elif any(word in text2.lower() for word in ["time"]):
                current_time = get_current_time()
                print("The current time is {}".format(current_time))
                speak("The current time is {}".format(current_time))

            elif any(word in text2.lower() for word in ["date"]):
                current_date = get_current_date()
                print("Today is {}".format(current_date))
                speak("Today is {}".format(current_date))

            elif "translate" in text2.lower():
                speak("What sentence would you like to translate?")
                with sr.Microphone() as source:
                    r.energy_threshold = 10000
                    r.adjust_for_ambient_noise(source, 1.2)
                    print('listening...')
                    audio = r.listen(source)
                    sentence_to_translate = r.recognize_google(audio)

                speak("Which language would you like to translate to?")
                with sr.Microphone() as source:
                    r.energy_threshold = 10000
                    r.adjust_for_ambient_noise(source, 1.2)
                    print('listening...')
                    audio = r.listen(source)
                    target_language = r.recognize_google(audio).lower()

                try:
                    translated_sentence = translate_sentence(sentence_to_translate, target_language)
                    print(f"The translation to {target_language} is: {translated_sentence}")
                    speak(f"The translation to {target_language} is: {translated_sentence}")
                except Exception as e:
                    speak(f"Translation failed. Error: {e}")
        
            elif "open" in text2.lower():
                text2_lower=text2.lower().replace("open","")
                text2_lower=text2_lower.replace("SNAPD","")
                pyautogui.press("super")
                pyautogui.typewrite(text2_lower)
                pyautogui.sleep(2)
                pyautogui.press("enter")

            elif "close" in text2.lower():
                text2_lower=text2.lower().replace("close","").strip()
                text2_lower=text2_lower.replace("SNAPD","")
                close_application(text2_lower)
                
            elif "internet speed" in text2.lower():
                wifi=speedtest.Speedtest()
                upload_net=wifi.upload()/1048576
                download_net=wifi.download()/1048576
                print("Wifi upload speed is",upload_net)
                print("Wifi download speed is",download_net)
                speak(f"Wifi download speed is {download_net}")
                speak(f"Wifi upload speed is {upload_net}")
            
            elif "google" in text2.lower():
            
                import wikipedia as googleScrap
                text2_lower=text2.lower().replace("SNAPD","")
                text2_lower=text2_lower.replace("google search","")
                text2_lower=text2_lower.replace("google","")
                speak("This is what i found on google")
            
                try:
                    webbrowser.open_new_tab("https://www.google.com/search?q="+text2_lower)
            
                except:
                    speak("No speakable output available")
                
            elif "youtube" in text2.lower():
                speak("This is what I found for your search")
                text2_lower=text2.lower().replace("youtube search","")
                text2_lower=text2_lower.replace("youtube","")
                text2_lower=text2_lower.replace("SNAPD","")
                web="https://www.youtube.com/results?search_query="+text2_lower
                webbrowser.open(web)
                pywhatkit.playonyt(text2_lower)
                speak("Done Sir")
            
            elif "screenshot" in text2.lower():
                im=pyautogui.screenshot()
                im.save("ss.jpg")
                speak("Noted, Boss")
            
            elif "click my photo" in text2.lower():
                pyautogui.press("super")
                pyautogui.typewrite("camera")
                pyautogui.press("enter")
                pyautogui.sleep(2)
                speak("SMILE")
                pyautogui.press("enter")           
        
            elif "temperature" in text2.lower() or "weather" in text2.lower():
                search="temperature in Ahmedabad"
                url=f"https://www.google.com/search?q={search}"
                response=requests.get(url)
                if response.status_code==200:
                    data=BeautifulSoup(response.text,"html.parser")
                    temp=data.find("div",class_ ="BNeawe").text
                    print(f"current {search} is {temp}")
                    speak(f"current {search} is {temp}")
                else:
                    speak("Sorry, I could not fetch the temperature at the moment")            

            elif "gemini" in text2.lower():
                speak("How can I assist you with Gemini?")
                with sr.Microphone() as source:
                    r.energy_threshold = 10000
                    r.adjust_for_ambient_noise(source, 1.2)
                    print('listening...')
                    audio = r.listen(source)
                    gemini_query = r.recognize_google(audio)

            # Call Gemini function here
                gemini_response = Gemini(gemini_query)
                print(gemini_response)
                speak(gemini_response)
            

# Exception handling 
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Can you please repeat?")
    except sr.RequestError as e:
        speak("Sorry, I couldn't process your request at the moment. Please try again later.")
        print(f"Request error: {e}")
    except Exception as e:
        speak(f"An error occurred: {e}")
        print(f"Error: {e}")
            
            
