@ These tests are written by Rimma Gizzatova

# Test automation repo for Security Password Generator

Frameworks full documantations:
PyTest documentation https://docs.pytest.org
Playwright documentation https://playwright.dev/python/docs/intro

## Quality Assurance Automated Testing

### Prerequirements:
- Make sure that Python 3.12.4 is installed on your machine, if not installation instructions are here: [https://www.python.org/downloads/release/python-3124/]
- Make sure you have pip installed, in terminal run command pip --version. If not installed follow this instractions [https://pip.pypa.io/en/stable/installation/]
- Make sure you have pipenv installed globally, chack it running command 
pipenv --version
If not installed, run command
pip install pipenv
Check again if it's installed by checking its version
- Optional, to be able viaully see tests reports - Make sure allure is installed on your machine, if not follow this documentation for installation [https://allurereport.org/docs/install/]

### Set up the project locally and install virtual environment for this project
1. Clone the repo, running command
git clone [https://github.com/risummerit/security-password-generator.git]
2. Go to the project directory for further steps

### in project directory:
1. This step should be done only once, install virtual invironments for this project with python 3.12.4 -- pipenv --python 3.12.4
2. Activate the virtual environment -- pipenv shell
3. Once pipenv is activated, Install all the dependencies from Pipfile -- pipenv install
4. Open project in VS Code running command --- code .
5. In VS Code terminal run tests using command -- pytest -vs
6. If you would like to run spesific tests, check pytest.ini file for list of markers (filters), for example, you can run tesst only for checking slider running
pytest -vs -m password_length_slider
7. Also, you could run file with tests -- pytest -vs <\path to the file with tests that you would like to run> . All tests saved in test-suite folder
8. Optional - after you ran tests, to visually see test results run command -- allure serve allure_reports
