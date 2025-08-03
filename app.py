from flask import Flask, render_template, request, send_file
import os
import pandas as pd
from fpdf import FPDF
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/convert', methods=['POST'])
def convert():
    file = request.files['excel_file']
    if file and file.filename.endswith(('.xls', '.xlsx')):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        df = pd.read_excel(filepath)
        temp_txt = os.path.splitext(filepath)[0] + '_temp.txt'
        pdf_path = os.path.splitext(filepath)[0] + '.pdf'

        df.to_csv(temp_txt, sep='\t', index=False)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=10)

        with open(temp_txt, "r") as f:
            for line in f:
                pdf.cell(200, 10, txt=line.strip(), ln=True)

        pdf.output(pdf_path)
        return send_file(pdf_path, as_attachment=True)

    return "Invalid file format", 400

if __name__ == '__main__':
    app.run(debug=True)
