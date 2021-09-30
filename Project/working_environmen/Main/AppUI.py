from calendar import c
import PySimpleGUI as sg
from tkinter.constants import TRUE
import tkinter as tk
import pandas as pd
import os
from UI.Dataframes.Dataframes import Dataframe

class AppUI: 

    dataframe = None
    
    def __init__(self):

        [sg.FileBrowse()]

        layout = [[sg.Text("Choose a xls file: ", key='-TEXT-'), sg.FileBrowse()],
                [sg.Submit(), sg.Cancel()], [sg.Text('Filter dataframe')],
                [sg.Text('Enter column'), sg.InputText(), sg.Text('Enter query'), sg.InputText(), sg.Submit()],
                [sg.Text('Value filterning')]]

        window = sg.Window('My File Browser', layout, size=(800,800))
    
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
                break
            if event == "Submit":
                self.dataframe = Dataframe(values['Browse'])
            if event == "Submit0":
                Dataframe.executeQuery(self.dataframe, values[0], values[1])

    
    def showError():
        sg.Popup('Opps!', 'Converted file is empty')

    def showSuccessPopup():
        sg.Popup('Now you can enter queries')


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
 

myApp = AppUI()
