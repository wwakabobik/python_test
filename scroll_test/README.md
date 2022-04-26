This project is to handle and demonstrate ability to test presence of scrollbars for web elements and pages
using Selenium webdriver (using JavaScript calls and/or attributes directly).

``` bash
git clone git@github.com:wwakabobik/python_test.git
cd python_test/scroll_test
python -m venv venv (In cases where you still have Python 2.7 or older installed on your system, your python command might be python3)
source venv/bin/activate (Linux/Mac) -or- venv\Scripts\activate.bat (Windows CMD)
pip install -r requirements.txt
pytest tests
```

While integrating this code into your project, please split up:
1. common functions ("is_scrollable") into testing framework
2. test data - to separate data folder/file(s)
3. self-tests and pages to self-tests (if needed) 
