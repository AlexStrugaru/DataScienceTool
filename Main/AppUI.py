from calendar import c
from tkinter.font import BOLD
import PySimpleGUI as sg
from tkinter.constants import TRUE
import os
import pandas
from PySimpleGUI.PySimpleGUI import Table, Window
from pandas.core.frame import DataFrame
from Enums import Conditions    
from Dataframes import Dataframe

class AppUI: 
   
    # Class members
    window = None
    dataframe = DataFrame()
    conditionParameter = Conditions
    
    def __init__(self):

        [sg.FileBrowse()]

        sg.theme('LightGrey1')
        layout = [[sg.Text("Choose a xls file: ", key='-TEXT-'), sg.FileBrowse()],
                [sg.Submit(), sg.Cancel()], [sg.Text('FILTER DATAFRAME', font=BOLD)],
                [sg.HorizontalSeparator(color='Blue')],
                [sg.Text('There is possible to apply up to 4 conditions, each condition is applyed to the previous dataframe resulted \n (eq. cond1 -> Submit -> df -> Cond 2 -> Submit -> df modified with additional condition -> df1)')], 
                [sg.Text('Enter 1st column', key='-TEXT1-'), sg.InputText(), sg.Combo(values=['==', '<', '>','>=', '<='], key='fac1', default_value='=='), sg.Text('Enter 1st query'), sg.InputText(), sg.Submit(), sg.Text('Query1', key='QUERY1',text_color='blue')],
                [sg.Text('Enter 2nd column', key='-TEXT2-'), sg.InputText(), sg.Combo(values=['==', '<', '>','>=', '<='], key='fac2', default_value='=='), sg.Text('Enter 2nd query'), sg.InputText(), sg.Submit(), sg.Text('Query2', key='QUERY2',text_color='blue')],
                [sg.Text('Enter 3rd column', key='-TEXT3-'), sg.InputText(), sg.Combo(values=['==', '<', '>','>=', '<='], key='fac3', default_value='=='), sg.Text('Enter 3rd query'), sg.InputText(), sg.Submit(), sg.Text('Query3', key='QUERY3',text_color='blue')],
                [sg.Text('Enter 4th column', key='-TEXT4-'), sg.InputText(), sg.Combo(values=['==', '<', '>','>=', '<='], key='fac4', default_value='=='), sg.Text('Enter 4th query'), sg.InputText(), sg.Submit(), sg.Text('Query4', key='QUERY4',text_color='blue')],
                [sg.Button(button_text="Export file")],
                [sg.HorizontalSeparator(color='Blue')],
                [sg.Text('PLOTTING', font=BOLD)]]

        self.window = sg.Window('Data Science Application', layout, size=(1000,800))
    
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
                break
            if event == "Submit":
                self.dataframe = Dataframe(values['Browse'])
            if event == "Submit0":
                # Send the selected operator to Conditions enum
                condition = self.assignEnumValue(values['fac1'])
                      # Check if the user entered values in the fields
                if values[1] is '' or values[2] is '':
                    self.showErrorWithString('Please complete Column and Query')
                    break
                self.dataframe = Dataframe.executeQuery(self.dataframe, values[1], condition, values[2], self.dataframe)
                self.showDataframeTable(self.dataframe)
            if event == "Submit1":
                self.dataframe = Dataframe.executeQuery(self.dataframe, values['fac2'], values[13], values[14])
            if event == "Submit2":
                 self.dataframe = Dataframe.executeQuery(self.dataframe, values['fac3'], values[20], values[21])
            if event == "Submit3":
                self.dataframe = Dataframe.executeQuery(self.dataframe, values['fac4'], values[27], values[28])
            if event == "Export file":
                Dataframe.saveFile()

        self.window.close()
    
    def assignEnumValue(self, value):
        if value == '<':
            return Conditions.SMALLER
        if value == '>':
            return Conditions.GREATER
        if value == '==':
            return Conditions.EQUAL
        if value == '>=':
            return Conditions.GREATER_OR_EQUAL
        if value == '<=':
            return Conditions.SMALLER_OR_EQUAL

    def showDataframeTable(self, dataFrame):
        self.dataframe == dataFrame
        data = self.dataframe.values.tolist()
        
        # check if the actual iloc has a value
        if 0 <= self.dataframe.iloc[0].tolist() < len(data):
            self.showErrorWithString('Índex out of bounds')
        
        header_list = self.dataframe.iloc[0].tolist()
        layout = [[sg.Submit(), sg.Cancel()],
                [sg.Table(values=data, headings=header_list, display_row_numbers=True, auto_size_columns=False, num_rows=min(25, len(data)))],
                [sg.Button(button_text="Export resulted df as xlsx file")]]
        dataframeWindow = sg.Window('Table', layout, grab_anywhere=False)
        while True:
            event, values = dataframeWindow.read()
            if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
                break
            if event == "Export resulted df as xlsx file":
             Dataframe.saveFile()   
        dataframeWindow.close()
    
    def showError():
        sg.Popup('Opps!', 'Converted file is empty')

    def showSuccessPopup():
        sg.Popup('Now you can enter queries')

    def showErrorInDataType():
        sg.Popup('Data type of the specified column is not numeric')
    
    def showErrorWithString(self, s):
        sg.Popup('Error', s)


myApp = AppUI()
