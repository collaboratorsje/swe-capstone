# INSTALL 

### Requirements
- Python 3.x

### Windows

Virtual Environment Setup

    python -m venv venv 

Activate Virtual Environment (Must do every time you launch, you'll see (venv) in your terminal) 

    .\venv\Scripts\Activate.ps1 

or 

    .\venv\Scripts\activate.bat 

Install Requirements

    python -m pip install -r .\requirements.txt

Launch with 

    python .\app.py

Open in browser at http://127.0.0.1:5000 or http://localhost:5000

### Mac
(Can't test, feel free to change if something is wrong or doesn't work)

Virtual Environment Setup

    python -m virtualenv venv 

Activate Virtual Environment (Must do every time you launch, you'll see (venv) in your terminal) 

    source ./venv/bin/activate

Install Requirements

    python -m pip install -r .\requirements.txt

Launch with 

    python .\app.py

Open in browser at http://127.0.0.1:5000 or http://localhost:5000