Maths Solver 🧮
Maths Solver is a web application that extracts and solves mathematical expressions from images. It leverages Optical Character Recognition (OCR) to detect math problems in pictures and provides solutions through a user-friendly interface.

🚀 Features
Upload images containing mathematical expressions

Automatic detection and extraction of math problems using OCR

Solves basic arithmetic expressions

Web interface built with Flask

🛠️ Technologies Used
Python

Flask

Tesseract OCR

HTML/CSS

📦 Installation

Clone the repository:


git clone https://github.com/nathancoolusername/Maths-Solver.git
cd Maths-Solver

Create and activate a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt


Install Tesseract OCR:

Ubuntu:

sudo apt update
sudo apt install tesseract-ocr

macOS (using Homebrew):

brew install tesseract

Windows:
Download the installer from Tesseract at UB Mannheim and follow the installation instructions.

Run the application:

python personal_project.py
Access the app:

Open your browser and navigate to http://localhost:5000.

