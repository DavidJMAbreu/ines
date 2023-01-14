import math
from time import sleep
import streamlit #used to present data on screen

#used to get data from .wav file
import speech_recognition as recon
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence
#used to recognize faster
from multiprocessing import Process

# create a speech recognition object
r = recon.Recognizer()

# the function splits the audio file into smaller chunks to faster recognize the audio
def divide_audio_into_small_chunks(file_path):
    # open the audio file using pydub
    sound = AudioSegment.from_wav(file_path)  
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    # process each chunk 
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")

    

recognized_array = []

def speech_recognition(process_id):
    global recognized_array

    print(f"Process {process_id}")

    chunk_filename = os.path.join("audio-chunks", f"chunk{process_id}.wav")
    # recognize the chunk
    with recon.AudioFile(chunk_filename) as source:
        audio_listened = r.record(source)
        # try converting it to text
        try:
            text = r.recognize_google(audio_listened)
            recognized_array.append({"id":process_id,"data":text})
        except recon.UnknownValueError as e:
            print("Error:", str(e))

    
    print(f"Process {process_id} finished")
    
        
if __name__ == "__main__":

    divide_audio_into_small_chunks("test_file.wav")
    print("Audio chunks exported")

    print(len(os.listdir("./audio-chunks/")))
        
    processes = []
    process_quantity = len(os.listdir("./audio-chunks/"))
    for process_id in range(0,process_quantity):
        proc = Process(target=speech_recognition, args=(process_id+1,))
        processes.append(proc)
        proc.start()

    for process in processes:
        process.join()
    
    recognized_array.sort(key=lambda x: x.id)
    print(recognized_array)



        

