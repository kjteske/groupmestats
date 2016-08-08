import os

import plotly
import yaml

DATA_DIR = os.path.join(os.path.expanduser('~'), ".groupmestats")

if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)

class PlotlySignInError(RuntimeError): pass

def plotly_sign_in():
    filename = os.path.join(DATA_DIR, "plotly_credentials.yaml")
    try:
        with open(filename, "r") as f:
            credentials = yaml.load(f)
            plotly.plotly.sign_in(credentials["username"], credentials["key"])
    except:
        # Right now plotly.sign_in() doesn't actually raise an exception if the
        # credentials are no good, you won't get an error until trying
        # to create a plot much later.
        print("Plotly sign in failed. Does %s contain the proper credentials?" % filename)
        raise PlotlySignInError()
