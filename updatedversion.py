import speech_recognition as sr
import pyttsx3
import cv2
import os

# Initialize speech recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Path to sign language gesture videos (folder containing video files like .mp4, .avi)
sign_language_videos_path = r"C:\Users\ancyj\OneDrive\Desktop\snlnge"  # Update the path to your folder

# Dataset phrases
PHRASES = ["thank you", "i love you", "keep calm and stay home", "miss you", "nice to meet you", "happy new year", "hello"]

# Function to normalize text (e.g., lowercase and strip spaces)
def normalize_text(text):
    return text.lower().strip()

# Function to play a video file
def play_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Could not open video: {video_path}")
        return
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break  # End of video
        
        # Display the video frame
        cv2.imshow("Sign Language Avatar", frame)
        
        # Exit playback if 'q' is pressed
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

# Function to convert text into sign language
def text_to_sign_language(text):
    text = normalize_text(text)

    # First, check for phrase matches
    matched_phrases = []  # To store matched phrases

    # Check for phrase matches first
    for phrase in PHRASES:
        if phrase in text:
            matched_phrases.append(phrase)

    # If any phrase is matched, play video for that phrase
    for phrase in matched_phrases:
        phrase_video_path = os.path.join(sign_language_videos_path, f"{phrase.replace(' ', '_')}.mp4")
        if os.path.exists(phrase_video_path):
            print(f"Displaying sign for phrase: {phrase}")
            play_video(phrase_video_path)

    # Now process the remaining words (only words not part of a matched phrase)
    words = text.split()
    for word in words:
        # Skip words that are part of already matched phrases
        if word not in matched_phrases:
            word_video_path = os.path.join(sign_language_videos_path, f"{word}.mp4")
            if os.path.exists(word_video_path):
                print(f"Displaying sign for: {word}")
                play_video(word_video_path)
            else:
                print(f"No sign language video found for the word '{word}'")

# Function to recognize speech and convert it to text
def recognize_speech():
    with sr.Microphone() as source:
        print("Say something (or say 'exit' to stop)...")
        audio = recognizer.listen(source)
    
    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio")
        return None
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service")
        return None

# Main function to continuously listen and respond
def main():
    while True:
        # Recognize speech from the microphone
        recognized_text = recognize_speech()
        
        if recognized_text:
            # Check if the user wants to exit
            if recognized_text.lower() == "exit":
                print("Exiting...")
                break
            
            # Convert the recognized text to sign language
            text_to_sign_language(recognized_text)
            
            # Optionally, speak the recognized text aloud
            engine.say(recognized_text)
            engine.runAndWait()

if __name__ == "__main__":
    main()
