"""
Implementation of add reviewer logic
"""

import sys
import json


# import requests


def get_reviewers(datainput):
    """
    :param datainput:
    :return:
    """
    print(datainput)
    # return json.dumps(["ReshmaManoharan"])
    #print(["Arunrajg"])
    sys.stdout.write("{}".format(["Arunrajg"]))
    #return ["ReshmaManoharan", "sasikumar6795"]

get_reviewers(str(sys.argv[1]))