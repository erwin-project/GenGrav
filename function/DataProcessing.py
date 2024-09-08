import requests
import numpy as np
import pandas as pd
from io import StringIO
from function import GetMessageAPI, GetParamAPI


def GetBougerDensity(grav_dataset, topo_dataset):
    constant = 0.0419  # constant in g/cm^3 per meter
    RhoBouger = grav_dataset.values / (constant * topo_dataset.values)

    return RhoBouger
