import sys
import os
import logging
import json
import requests
import base64

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

DESCRIPTION_FILE = 'description.txt'
AUTOGRADER_REL_PATH = '../autograder'
CASES_FOLDER = 'cases'
CONTAINER_NAME_ENV = 'KODETHON_CONTAINER_NAME'
USER_ID_ENV = 'KODETHON_USER_ID'
ACCESS_TOKEN_ENV = 'KODETHON_ACCESS_TOKEN'
ASSIGNMENT_ID_ENV = 'KODETHON_ASSIGNMENT_ID'
IMPORT_URL = 'http://localhost:3456/course/tests/import'
UPLOAD_URL = 'http://localhost:3456/containers/upload_file'

CASES_ZIP = 'cases.zip'
DRIVER_FILE = 'driver.py'

def beautifyTitle(title):
    title = title.replace('-', ' ')
    return title.title()

def generateCases(cases_path, answers_path):
    # Generate all the cases
    cases = []
    for filename in os.listdir(cases_path):
        fp = open(os.path.join(answers_path, filename), 'r')
        answer = fp.read()
        fp.close()
        cases.append({
            'arguments' : os.path.join(AUTOGRADER_REL_PATH, CASES_FOLDER, filename),
            'answer' : answer
        })
    return cases

def createTest(test):
    package = {
        'user_id' : os.environ[USER_ID_ENV],
        'access_token' : os.environ[ACCESS_TOKEN_ENV],
        'name' : os.environ[ASSIGNMENT_ID_ENV],
        'test_settings'  : json.dumps(test),
    }
    #print json.dumps(package, indent=4, sort_keys=True)
    r = requests.post(IMPORT_URL, data = package)

def uploadFiles(dirpath):
    dirname = os.path.basename(dirpath)
    title = beautifyTitle(dirname)   
    
    # Upload cases
    fp = open(os.path.join(dirpath, CASES_ZIP), 'r')
    content = fp.read()
    fp.close()
    package = {
        'user_id' : os.environ[USER_ID_ENV],
        'access_token' : os.environ[ACCESS_TOKEN_ENV],
        'name' : os.environ[ASSIGNMENT_ID_ENV],       
        'file_name' : CASES_ZIP,
        'destination' : os.path.join('/', title, os.path.basename(AUTOGRADER_REL_PATH)),
        'file_content' : base64.b64encode(content)
    }
    r = requests.post(UPLOAD_URL, data = package)
    
    # Upload driver file
    fp = open(os.path.join(dirpath, DRIVER_FILE), 'r')
    content = fp.read()
    fp.close()
    package = {
        'user_id' : os.environ[USER_ID_ENV],
        'access_token' : os.environ[ACCESS_TOKEN_ENV],
        'name' : os.environ[ASSIGNMENT_ID_ENV],       
        'file_name' : DRIVER_FILE,
        'destination' : os.path.join('/', title, os.path.basename(AUTOGRADER_REL_PATH)),
        'file_content' : base64.b64encode(content)
    }
    r = requests.post(UPLOAD_URL, data = package)

if __name__ == "__main__":
    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        logger.error("%s does not exist!" % file_path)
        sys.exit()

    if os.environ[CONTAINER_NAME_ENV] == None:
        logger.error("%s is not set." % CONTAINER_NAME_ENV)
        sys.exit()

    if os.environ[USER_ID_ENV] == None:
        logger.error("%s is not set." % USER_ID_ENV)
        sys.exit()

    if os.environ[ACCESS_TOKEN_ENV] == None:
        logger.error("%s is not set." % ACCESS_TOKEN_ENV)
        sys.exit()

    if os.environ[ASSIGNMENT_ID_ENV] == None:
        logger.error("%s is not set." % ASSIGNMENT_ID_ENV)
        sys.exit()

    dir_path = os.path.dirname(file_path)
    description_path = os.path.join(dir_path, DESCRIPTION_FILE)
    if not os.path.exists(description_path):
        logger.error("%s does not exist!" % description_path)
        sys.exit()

    fp = open(description_path, 'r')
    description = fp.read().strip()
    fp.close()

    cases_path = os.path.join(dir_path, CASES_FOLDER)
    if not os.path.exists(cases_path):
        logger.error("%s does not exist!" % cases_path)
        sys.exit()

    answers_path = os.path.join(dir_path, 'answers')
    if not os.path.exists(answers_path):
        logger.error("%s does not exist!" % answers_path)
        sys.exit()
        
    cases = generateCases(cases_path, answers_path)
    dirname = os.path.basename(dir_path)
    createTest({
        'test_name': beautifyTitle(dirname),
        'cases' : cases,
        'Style' : 'Diff',
        'Description' : description,
        'Run Command' : 'python %s/%s' % (AUTOGRADER_REL_PATH, DRIVER_FILE)
    }) 
    uploadFiles(dir_path)