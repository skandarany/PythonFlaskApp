from setuptools import setup, find_packages

setup(
    name="cv_processor",  # Replace with your project name
    version="1.0.0",  # Update as needed
    description="A Flask application for processing CVs using OCR and extracting skills",
    author="SKander Mufti",
    author_email="skander.mufti@piterion.com",
    #url="http://your_project_url.com",  # Replace with the project URL if applicable
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask",
        "psycopg2-binary",
        "pytesseract",
        "Pillow",
        "pdf2image",
        "pdfplumber",
        "spacy",
        "skillNer",
        "werkzeug",
    ],
    entry_points={
        "console_scripts": [
            "cv_processor=app.py:main",  # Replace `your_main_module` with your main Python file without `.py`.
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
