from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from pdf2docx import Converter
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "temp_files"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 1. Meka thama adu wela thibbe - Browser eken balanna puluwan home page eka
@app.route('/')
def home():
    return "<h1>PDF to Word Converter Backend is Running!</h1><p>Send a POST request to <b>/convert</b> to process files.</p>"

@app.route('/convert', methods=['POST'])
def convert_pdf_to_word():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    pdf_file = request.files['file']
    if pdf_file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Path hadaganna widiya
    pdf_path = os.path.join(UPLOAD_FOLDER, pdf_file.filename)
    docx_filename = pdf_file.filename.rsplit('.', 1)[0] + ".docx"
    docx_path = os.path.join(UPLOAD_FOLDER, docx_filename)
    
    try:
        # PDF eka save kirima
        pdf_file.save(pdf_path)
        
        # Conversion Process
        cv = Converter(pdf_path)
        cv.convert(docx_path, start=0, end=None)
        cv.close()
        
        # Word file eka user ta yawima
        return send_file(docx_path, as_attachment=True)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        # File eka yawala iwara unama temp files ain karanna (Optional)
        # Note: send_file eken passe remove karaddi samahara welawata file eka lock wenna puluwan.
        # Eka nisa meka daddi parissamin.
        if os.path.exists(pdf_path): 
            os.remove(pdf_path)

if __name__ == '__main__':
    app.run(debug=True)