import speech_recognition as sr
from text_matching import similarity
import s3_connection
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import s3_connection
from pydub import AudioSegment
from pydub.silence import split_on_silence

def segment(input_file,output_file,min_silence_len=300,silence_thresh=-50):
    print("loading")
    audio=AudioSegment.from_wav(input_file)
    print("split")
    chunks=split_on_silence(audio,min_silence_len=min_silence_len,silence_thresh=silence_thresh)
    print("adding")
    output=AudioSegment.empty()
    for chunk in chunks:
        output+=chunk
    print("exporting")
    output.export(output_file, format="wav")
    s3_connection.upload_file(output_file,'studentproctordata')
    print("done")


def similarity():
    text1=s3_connection.fetch_file_content_from_s3('assignmentcontent','content.txt')
    text2=s3_connection.fetch_file_content_from_s3('studentproctordata','spoken_content.txt')

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([text1, text2])
    cosine_sim = cosine_similarity(vectors)[0][1]
    similarity_percentage = round(cosine_sim * 100, 2)

    return similarity_percentage

def audio_to_text(audio_file):
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio_data)
            existing_content = s3_connection.fetch_file_content_from_s3('studentproctordata', 'spoken_content.txt')
            content=existing_content+text
            s3_connection.update_file_on_s3('studentproctordata','spoken_content.txt',content)
            # with open(output_file, "w") as text_file:
            #     text_file.write(text)

        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            return None
            

audio_file = "recorded_audio.wav"
output_file = "spoken_content.txt"  
audio_to_text(audio_file)
print(similarity())
output_audio="segmented_audio.wav"
segment(audio_file,output_audio)
