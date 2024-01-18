from flask import Flask, render_template, request, send_file
import pyttsx3
import PyPDF2
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    pdf_file = request.files['pdf_file']
    
    # Save the uploaded PDF file
    pdf_path = 'uploads/' + pdf_file.filename
    pdf_file.save(pdf_path)

    # Convert PDF to MP3
    speaker = pyttsx3.init()
    pdfreader = PyPDF2.PdfFileReader(open(pdf_path, 'rb'))

    mp3_files = []

    for page_num in range(pdfreader.numPages):
        text = pdfreader.getPage(page_num).extractText()
        clean_text = text.strip().replace('\n', ' ')
        mp3_path = f'converted_files/story_page_{page_num}.mp3'
        speaker.save_to_file(clean_text, mp3_path)
        speaker.runAndWait()
        mp3_files.append(mp3_path)

    # Combine all MP3 files into one
    combined_file_path = 'converted_files/combined_story.mp3'
    os.system(f'ffmpeg -i "concat:{"|".join(mp3_files)}" -acodec copy {combined_file_path}')

    # Clean up temporary files
    for mp3_file in mp3_files:
        os.remove(mp3_file)
    os.remove(pdf_path)

    return send_file(combined_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
