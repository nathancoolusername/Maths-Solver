from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import re
import sympy as sp
from sympy.parsing.sympy_parser import (parse_expr, standard_transformations, 
                                        implicit_multiplication_application)
import os

app = Flask(__name__)

pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(image_path):
    img = Image.open(image_path)
    img = img.convert('L')
    img = img.filter(ImageFilter.MedianFilter())
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2)
    return img

def solve_math_from_image(image_path):
    img = preprocess_image(image_path)
    extracted_text = pytesseract.image_to_string(img)
    cleaned_text = extracted_text.replace('\n', ' ').replace('\x0c', '').replace('\r', '')
    expressions = re.split(r'[,.:;]+', cleaned_text)
    results = []
    for expr in expressions:
        try:
            if '=' in expr:
                left_side, right_side = expr.split('=')
                transformations = (standard_transformations + (implicit_multiplication_application,))
                left_expr = parse_expr(left_side, transformations=transformations)
                right_expr = parse_expr(right_side, transformations=transformations)
                equation = sp.Eq(left_expr, right_expr)
                result = sp.solve(equation)
            else:
                transformations = (standard_transformations + (implicit_multiplication_application,))
                expression = parse_expr(expr, transformations=transformations)
                result = sp.simplify(expression)
            
            results.append((expr.strip(), result))
        
        except (sp.SympifyError, ValueError, SyntaxError) as e:
            results.append((expr.strip(), f"Error: {e}"))
    
    return results

@app.route('/', methods=['GET', 'POST'])
def index():
    extracted_expressions = None
    results = None
    uploaded_image = None
    
    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)
        
        image = request.files['image']
        
        if image.filename == '':
            return redirect(request.url)
        
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(filepath)
            
            results = solve_math_from_image(filepath)
            
            if results:
                extracted_expressions = [expr for expr, _ in results]
            
            uploaded_image = filename
    
    return render_template('index.html', extracted_expressions=extracted_expressions, results=results, uploaded_image=uploaded_image)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
