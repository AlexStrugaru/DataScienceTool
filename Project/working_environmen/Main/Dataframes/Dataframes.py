import pandas as pd
from Project.working_environmen import AppUI
from tkinter.constants import TRUE

class Dataframe:

    cursor = None
    connection = None
    data = None

    def __init__(self, path):
        self.path = path
        data_xls = pd.read_excel(self.path, dtype=str, index_col=None)
        df = data_xls.to_csv(r'ConvertedFile.csv', encoding='utf-8', index=False)
        readFile = pd.read_csv('ConvertedFile.csv', delimiter= ",")
        
        if readFile.empty == TRUE :
           AppUI.showError()
        else :
             AppUI.showSuccessPopup()

    def executeQuery(self, column, query): 
            readFile = pd.read_csv('ConvertedFile.csv', index_col=None)
            self.dataFrame = pd.DataFrame(readFile)
            print(self.dataFrame)
            columnQuery = column.replace(' ', '').split(",")
            queryList = query.replace(' ', '').split(",")
            dataFrameQueryList = []
            for value in columnQuery:
                for item in queryList:
                    if self.dataFrame[value].dtypes != str:
                        print(self.dataFrame[value].dtype)
                        filteredDataFrame = self.dataFrame[self.dataFrame[value] == float(item)] 
                    else:
                        # dataFrameQueryList.append[(self.dataFrame[value] == item)]
                        filteredDataFrame = self.dataFrame[self.dataFrame[value] == item]    
            
            fullFilter = "&".join(queryList)
            
            print(filteredDataFrame)
            xlsWriter = pd.ExcelWriter('Output.xlsx')
            filteredDataFrame.to_excel(xlsWriter, sheet_name='FilteredData', index=False)
            xlsWriter.close()