from typing import Match
import pandas as pd
from tkinter.constants import TRUE

class Dataframe:

    cursor = None
    connection = None
    data = None

    def __init__(self, path):
        # Remove circular dependency by adding the import in the function we use the class
        from Main.AppUI import AppUI
        from Main.Enums import Conditions

        self.path = path
        data_xls = pd.read_excel(self.path, dtype=str, index_col=None)
        df = data_xls.to_csv(r'ConvertedFile.csv', encoding='utf-8', index=False)
        readFile = pd.read_csv('ConvertedFile.csv', delimiter= ",")
        
        if readFile.empty == TRUE :
           AppUI.showError()
        else :
             AppUI.showSuccessPopup()

    def executeQuery(self, column, condition, value, df): 
            #check if variable df is empty, if it is populate it
            if not df:     
                readFile = pd.read_csv('ConvertedFile.csv', index_col=None)
                self.dataFrame = pd.DataFrame(readFile)
            else:
                self.dataFrame = df
 
            if not isinstance(condition, Conditions):
                raise TypeError('conditions must be an instance of Conditiond Enum')
            
            for condition in (Conditions):
                if condition== Conditions.EQUAL:
                    if self.dataFrame[column].dtypes != str:
                        print(self.dataFrame[value].dtype)
                        self.dataFrame = self.dataFrame[self.dataFrame[value] == float(value)] 
                    else:
                        self.dataFrame = self.dataFrame[self.dataFrame[value] == value]
                if condition == Conditions.GREATER:
                        self.dataFrame = self.dataFrame[self.dataFrame[value] > value]
                if condition == Conditions.SMALLER:
                        self.dataFrame = self.dataFrame[self.dataFrame[value] < value]
                if condition == Conditions.GREATER_OR_EQUAL:
                        self.dataFrame = self.dataFrame[self.dataFrame[value] >= value]
                if condition == Conditions.SMALLER_OR_EQUAL:
                        self.dataFrame = self.dataFrame[self.dataFrame[value] <= value]
            
        
    def saveFile(self):
        xlsWriter = pd.ExcelWriter('Output.xlsx')
        self.dataFrame.to_excel(xlsWriter, sheet_name='FilteredData', index=False)
        xlsWriter.close()
    