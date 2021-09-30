from calendar import c
from tkinter.font import BOLD
import PySimpleGUI as sg
from tkinter.constants import TRUE
import os
from Enums import Conditions    
from Dataframes import Dataframe

class AppUI: 
   

    # Class members
    dataframe = None
    window = None
    dataframe = None
    conditionParameter = Conditions
    def __init__(self):

        [sg.FileBrowse()]

        sg.theme('LightGrey1')
        layout = [[sg.Text("Choose a xls file: ", key='-TEXT-'), sg.FileBrowse()],
                [sg.Submit(), sg.Cancel()], [sg.Text('FILTER DATAFRAME', font=BOLD)],
                [sg.HorizontalSeparator(color='Blue')],
                [sg.Text('There is possible to apply up to 4 conditions, each condition is applyed to the previous dataframe resulted \n (eq. cond1 -> Submit -> df -> Cond 2 -> Submit -> df modified with additional condition -> df1)')], 
                [sg.Text('Enter 1st column', key='-TEXT1-'),[sg.Checkbox('== (equal))', default=False, key="-EQUAL1-"), sg.Checkbox('< (smaller))', default=False, key="-SMALLER1-"), sg.Checkbox('> (greater))', default=False, key="-GREATER1-"), sg.Checkbox('<= (smaller or equal))', default=False, key="-SEQUAL1-"), sg.Checkbox('<=(greater or equal))', default=False, key="-GEQUAL1-")], sg.InputText(), sg.Text('Enter 1st query'), sg.InputText(), sg.Submit(), sg.Text('Query1', key='QUERY1',text_color='blue')],
                [sg.Text('Enter 2nd column', key='-TEXT2-'), [sg.Checkbox('== (equal))', default=False, key="-EQUAL2-"), sg.Checkbox('< (smaller))', default=False, key="-SMALLER2-"), sg.Checkbox('> (greater))', default=False, key="-GREATER2-"), sg.Checkbox('<= (smaller or equal))', default=False, key="-SEQUAL2-"), sg.Checkbox('<=(greater or equal))', default=False, key="-GEQUAL2-")], sg.InputText(), sg.Text('Enter 2nd query'), sg.InputText(), sg.Submit(), sg.Text('Query2', key='QUERY2',text_color='blue')],
                [sg.Text('Enter 3rd column', key='-TEXT3-'), [sg.Checkbox('== (equal))', default=False, key="-EQUAL3-"), sg.Checkbox('< (smaller))', default=False, key="-SMALLER3-"), sg.Checkbox('> (greater))', default=False, key="-GREATER3-"), sg.Checkbox('<= (smaller or equal))', default=False, key="-SEQUAL3-"), sg.Checkbox('<=(greater or equal))', default=False, key="-GEQUAL3-")], sg.InputText(), sg.Text('Enter 3rd query'), sg.InputText(), sg.Submit(), sg.Text('Query3', key='QUERY3',text_color='blue')],
                [sg.Text('Enter 4th column', key='-TEXT4-'), [sg.Checkbox('== (equal))', default=False, key="-EQUAL4-"), sg.Checkbox('< (smaller))', default=False, key="-SMALLER4-"), sg.Checkbox('> (greater))', default=False, key="-GREATER4-"), sg.Checkbox('<= (smaller or equal))', default=False, key="-SEQUAL4-"), sg.Checkbox('<=(greater or equal))', default=False, key="-GEQUAL4-")], sg.InputText(), sg.Text('Enter 4th query'), sg.InputText(), sg.Submit(), sg.Text('Query4', key='QUERY4',text_color='blue')],
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
                self.dataframe = Dataframe.executeQuery(self.dataframe, values[6], values[7])
            if event == "Submit1":
                self.dataframe = Dataframe.executeQuery(self.dataframe, values[13], values[14])
            if event == "Submit2":
                 self.dataframe = Dataframe.executeQuery(self.dataframe, values[20], values[21])
            if event == "Submit3":
                self.dataframe = Dataframe.executeQuery(self.dataframe, values[27], values[28])
            if event == "Export file":
                Dataframe.saveFile()
    
    def showError():
        sg.Popup('Opps!', 'Converted file is empty')

    def showSuccessPopup():
        sg.Popup('Now you can enter queries')

myApp = AppUI()
