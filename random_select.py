import pandas as pd
import numpy as np


def random_select(fpath):
    data = pd.read_csv(fpath)
    newdata = data.sample()