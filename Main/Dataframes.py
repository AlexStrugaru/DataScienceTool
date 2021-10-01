from typing import Match
from numpy import empty
import pandas as pd
from tkinter.constants import TRUE
from Enums import Conditions
import datetime as dt

class Dataframe:

    cursor = None
    connection = None
    data = None
    apiUI = None

    def __init__(self, path):
        # Remove circular dependency by adding the import in the function we use the class
        from AppUI import AppUI

        self.path = path
        self.apiUI = AppUI()
        data_xls = pd.read_excel(self.path, dtype=str, index_col=None)
        df = data_xls.to_csv(r'ConvertedFile.csv', encoding='utf-8', index=False)
        readFile = pd.read_csv('ConvertedFile.csv', delimiter= ",")
        
        if readFile.empty == TRUE :
           self.apiUI.showError()
        else :
             self.apiUI.showSuccessPopup()

    def executeQuery(self, column, condition, value, df): 
        
            # Check if variable df is empty, if it is populate it
            if df.empty == True:     
                readFile = pd.read_csv('ConvertedFile.csv', index_col=None)
                self.dataFrame = pd.DataFrame(readFile)
            else:
                self.dataFrame = df
 
        # Check if the send value for  the condition is a Conditions type enum
            if not isinstance(condition, Conditions):
                raise TypeError('conditions must be an instance of Conditiond Enum')

        # In case the condition is different than equal be sure the fields are numeric ones otherwise show error
            if condition!= Conditions.EQUAL:
                if self.dataFrame[column].values.dtype != str or self.dataFrame[column].values.dtype == object:
                    self.apiUI.showErrorInDataType()
                    return

            if condition == Conditions.EQUAL:
                    self.dataFrame = self.dataFrame[self.dataFrame[column] == value]
            if condition == Conditions.GREATER:
                    self.dataFrame = self.dataFrame[self.dataFrame[column] > float(value)]
            if condition == Conditions.SMALLER:
                    self.dataFrame = self.dataFrame[self.dataFrame[column] < float(value)]
            if condition == Conditions.GREATER_OR_EQUAL:
                    self.dataFrame = self.dataFrame[self.dataFrame[column] >= float(value)]
            if condition == Conditions.SMALLER_OR_EQUAL:
                    self.dataFrame = self.dataFrame[self.dataFrame[column] <= float(value)]
            return self.dataFrame
        
    def saveFile(self):
        xlsWriter = pd.ExcelWriter(r'\\Logs\Documents\\' + dt.datetime.today().strftime("%d%m%Y")+'delmedf.xlsx')
        self.dataFrame.to_excel(xlsWriter, sheet_name='FilteredData', index=False)
        xlsWriter.close()
    