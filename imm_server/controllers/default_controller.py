import connexion
import six

from imm_server.models.immunomatch_ed_input import ImmunomatchEdInput  # noqa: E501
from imm_server.models.immunomatch_ed_output import ImmunomatchEdOutput  # noqa: E501
from imm_server.models.base_model_ import Model
# from imm_server.utils.log_handler import get_logger
from imm_server.utils.getlogger import getLogger
from imm_server.models.version import Version  # noqa: E501
from imm_server import util

from flask import Flask, request, jsonify
import os, re, json, subprocess, yaml
from pathlib import Path

## env setting
os.environ['PYTHONHOME'] = r"C:\Users\Jurat\AppData\Local\Programs\Python\Python37"
os.environ['PYTHONPATH'] = r"C:\Users\Jurat\AppData\Local\Programs\Python\Python37\Lib\site-packages"
os.environ['R_HOME'] = r"C:\Program Files\R\R-3.6.2"
os.environ['R_USER'] = r"C:\Users\Jurat\AppData\Local\Programs\Python\Python37\Lib\site-packages\rpy2"
##

## rpy2 setting
import rpy2
import rpy2.robjects as robjects
import importlib

from rpy2.robjects.packages import importr
from rpy2.robjects.packages import STAP
utils = importr('utils')
utils.install_packages('jsonlite')
utils.install_packages('dplyr')
utils.install_packages('ranger')

logger = getLogger('immunomatch_ed', 'C:/Users/Jurat/imm_python_server/imm_server/log')

def about_get():  # noqa: E501
    """ImmunoMatch System Version
    Obtain current version of ImmunoMatch # noqa: E501
    :rtype: Version
    """
    logger.info("getting ready to retrieve immunoMatch System version...")
    logger.warning('This is a WARNING message')
    logger.error('This is an ERROR message')
    spec_yaml = Path(r'C:\Users\Jurat\imm_python_server\imm_server\apispec\ImmMatch_API_1_0_0.yaml')
    with open(spec_yaml, 'r') as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as err:
            logger.error('about_get: Error: %s: %s' % (err, traceback.format_exc()))
            resp = jsonify({"error": err.messages}), 403
            return json.dumps(resp)
    ver = data['info']['version'].replace('.', ',')
    title = data['info']['title']
    output = ", ".join([title, ver]).split(",")
    names = ['name', 'mayor', 'minor', 'patch']
    sysVersion = {names[i]: output[i] for i in range(len(output))}
    # res = Version.from_dict(sysVersion)
    return(sysVersion)

## load R function for computing immuno-score
from imm_server.immR. immuno_score import immunomatch_ed
immuno_ed = STAP(immunomatch_ed, "immuno_ed")

# def immunomatch_ed_post(body):  # noqa: E501

def immunomatch_ed_post(body):  # noqa: E501
    """ImmunoMatch ED Execution interface
    Endpoint will return the output of the ImmunoMatch ED algoritm Machine Learning algorithm. # noqa: E501
    :param body: 
    :type body: dict | bytes
    :rtype: ImmunomatchEdOutput
    """
    '''if connexion.request.is_json:
        body = ImmunomatchEdInput.from_dict(connexion.request.get_json())  # noqa: E501
    body = Model.to_dict(body)
    body = json.dumps(body)'''
    logger.info("getting ready to retrieve immunoMatch score...")
    try:
        if connexion.request.is_json:
            body = connexion.request.json
    except ValueError as err:
            logger.error('immunomatch_ed_post: Error: %s: %s' % (err, traceback.format_exc()))
            resp = jsonify({"error": err.messages}), 403
            return json.dumps(resp)
    input_json = json.dumps(body)
    imm_score = immuno_ed.immscore(input_json)
    res = json.loads(str(imm_score))
    res = json.dumps(res, indent=4)
    return jsonify(json.loads(res))

# def log_get(type)  
def log_get():  # noqa: E501
    """Return log
     # noqa: E501
    :param type: log name
    :type type: str
    :rtype: str
    """
    body = connexion.request.args.to_dict()
    val = [body[k] for k in body]
    val = ''.join(val)
    if val == "combined":
        print("printing out combined log info including error, warning")
    elif val == "error":
         print("printing out error log info only")
    else:
        print("print out rlog info from running R functions")
        #  raise ValueError("Invalid direction "+ str(direction))

    return 'do some magic!'


def rsession_get():  # noqa: E501
    """Collect Information About The Current R Session
    Obtain r sessionInfo() # noqa: E501
    :rtype: str
    """
    logger.info("getting ready to retrieve R session info...")
    logger.warning('This is a WARNING message')
    logger.error('This is an ERROR message')
    rscript = 'C:/Program Files/R/R-3.6.0/bin/Rscript'.replace('/', '\\')
    output = subprocess.check_output([rscript,'--vanilla','-e','sessionInfo()'])
    output = output.decode('utf-8')
    lines = output.split('\n')
    lines = [re.sub(r'\r\n', ' ', line) for line in lines]
    return {'current R session info': lines}
