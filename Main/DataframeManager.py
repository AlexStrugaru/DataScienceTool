from typing import Match
import pandas as pd
from tkinter.constants import TRUE
from Enums import Conditions

   
def updateDataframe(dataframe, column, value, condition):
       
        if condition == Conditions.EQUAL:
                df = dataframe[dataframe[column] == value]
        if condition == Conditions.GREATER:
                df = dataframe[dataframe[column] > float(value)]
        if condition == Conditions.SMALLER:
                df = dataframe[dataframe[column] < float(value)]
        if condition == Conditions.GREATER_OR_EQUAL:
                df = dataframe[dataframe[column] >= float(value)]
        if condition == Conditions.SMALLER_OR_EQUAL:
                df = dataframe[dataframe[column] <= float(value)]

        return df

def exists(filename):
    try:
        with open(filename) as f:
            file_exists = True
    except FileNotFoundError:
        file_exists = False
    return file_exists