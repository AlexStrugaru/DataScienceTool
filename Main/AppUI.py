from tkinter import font
from tkinter.font import BOLD
import PySimpleGUI as sg
from tkinter.constants import TRUE
import os
import pandas as pd
from PySimpleGUI.PySimpleGUI import Table, Window
from pandas.core.frame import DataFrame
from Enums import Conditions
import DataframeManager
from numpy import empty
from typing import Match
import matplotlib.pyplot as plt
import itertools

from Enums import CustomFonts

class AppUI: 
   
    # Class members
    window = None
    dataframe = DataFrame()
    conditionParameter = Conditions

    def __init__(self):

        [sg.FileBrowse()]
        # List the available colours for the plots
        matplotlib_colours = ["dodgerblue", "indianred", "gold", "steelblue", "tomato", "slategray", "plum", "seagreen", "gray"]
        # List the line-styles you want
        matplotlib_linestyles = ["solid", "dashed", "dashdot", "dotted"]
        # pad = ((left, right), (top, bottom))
        sg.theme('LightGrey1')
        col_layout = [sg.Text("")]
  
        layout = [[sg.Text("Choose a xls file: ", key='-TEXT-', font=CustomFonts.TITLE),
                sg.Input(font=CustomFonts.SUBTITLE, change_submits=True, key = "-IN-"),
                sg.FileBrowse(font=CustomFonts.BUTTON)],
                [sg.Submit(font=CustomFonts.BUTTON, pad=((10,20), (10, 40))), sg.Cancel(font=CustomFonts.BUTTON, pad=((0,0), (10, 40)))],
                [sg.Text('FILTER DATAFRAME', font=CustomFonts.SECTION)],
                [sg.HorizontalSeparator(color='Blue')],
                [sg.Text('There is possible to apply up to 4 conditions, each condition is applyed to the previous dataframe resulted \n (eq. cond1 -> Submit -> df -> Cond 2 -> Submit -> df modified with additional condition -> df1)', font=CustomFonts.SUBTITLE)], 
                [sg.Text('Enter 1st column', key='-TEXT1-', font=CustomFonts.SUBTITLE), 
                sg.InputText(font=CustomFonts.SUBTITLE), 
                sg.Combo(values=['==', '<', '>','>=', '<='], key='fac1', default_value='==', font=CustomFonts.SUBTITLE), 
                sg.Text('Enter 1st query', font=CustomFonts.SUBTITLE), 
                sg.InputText(font=CustomFonts.SUBTITLE), 
                sg.Submit(font=CustomFonts.BUTTON), 
                sg.Text('Query1', key='QUERY1',text_color='blue', font=CustomFonts.SUBTITLE)],
                [sg.Button(button_text="Export file", font=CustomFonts.BUTTON)],
                [sg.HorizontalSeparator(color='Blue')],
                [sg.Text('PLOTTING', font=CustomFonts.SECTION)],
                [sg.InputText('X', size=(20, 1),font=CustomFonts.SUBTITLE),
                sg.InputText('Y', size=(20, 1), font=CustomFonts.SUBTITLE),
                sg.InputCombo(values=('point', 'line'), font=CustomFonts.SUBTITLE),
                sg.InputCombo(values=(matplotlib_colours), font=CustomFonts.SUBTITLE),
                sg.InputCombo(values=(matplotlib_linestyles), font=CustomFonts.SUBTITLE),
                sg.InputText('Enter Legend Label', size=(20, 1), font=CustomFonts.SUBTITLE)],
                [sg.Text('_'  * 100, size=(100, 1), font=CustomFonts.SUBTITLE)],
                [sg.Button('Plot', font=CustomFonts.BUTTON)]]

        self.window = sg.Window('Data Science Application', layout, size=(1500,600))

        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED: # if user closes window
                break
            if event == 'Cancel':
                self.window['-IN-'].update('')
            if event == "Submit":
                self.convertToCVS(values['Browse'])
            if event == "Submit0":
                self.performEDA(values[1], values[2], values['fac1'])
            if event == "Export file":
                xlsWriter = pd.ExcelWriter(r'FilteredFile.xlsx')
                self.dataframe.to_excel(xlsWriter, sheet_name='FilteredData', index=False)
                xlsWriter.close()
            if event == "Plot":
                if self.dataframe.empty == TRUE:
                    try:
                        if os.path.exists('ConvertedFile.csv'):
                            self.dataframe = pd.read_csv('ConvertedFile.csv', index_col=None)
                            self.plotDataframe(values)
                        else:
                            self.showErrorWithString('No file found to convert into a dataframe')
                            return
                    except pd.errors.EmptyDataError:
                        self.showErrorWithString('No file found to convert into a dataframe')
                        return
                else:
                    self.plotDataframe(values)
        self.window.close()
    
    def plotDataframe(self, values):
        # Access the values which were entered and store in lists
        xAxisLabel = values[4]
        yAxisLabel = values[5]

        legendLabels   = []
        xcols          = []
        ycols          = []
        cols_to_use    = []
        plot_type      = []
        plot_colour    = []
        plot_line      = []
        i = 2            
        # Append the column indices to a list for later
        xcolindex = values[4]
        i += 1
        ycolindex = values[5] # index 3
        # Append the separate x and y column indices to their respective lists. These are used when plotting using Seaborn below
        xcols.append(xcolindex)
        ycols.append(ycolindex)
        # Append both the x and y to a combined list in order to construct the DataFrame object
        cols_to_use.append([xcolindex, ycolindex])
        # Append the type of plot [ scatter | line ]
        i += 1
        plot_type.append(values[6]) # index 4
        # Append the colour of the plot
        i += 1
        plot_colour.append(values[7]) # index 5
        # Append the linestyle of the plot
        i += 1
        plot_line.append(values[8]) # index 6
        # Append the user specified legend labels to a list for later
        i += 1
        legendLabels.append(values[9]) # index 7
        i += 1

        fig, ax = plt.subplots(figsize=(4, 4))
        plot_colour = itertools.cycle(plot_colour)
        plot_line = itertools.cycle(plot_line)
        if plot_type[0] == 'point':
            ax.scatter(self.dataframe[xcols[0]], self.dataframe[ycols[0]], color=next(plot_colour), s=10, label=r'{}'.format(legendLabels[0]))
        elif plot_type[0] == 'line':
            ax = plt.gca()
            fig = plt.figure(figsize=(12, 10), dpi=80)
            ax = fig.add_subplot(111)
            for column in self.dataframe.columns:
                ax.plot(self.dataframe[xcols[0]], self.dataframe[ycols[0]], linestyle=next(plot_line), color=next(plot_colour), label=r'{}'.format(legendLabels[0]))
    
        # Work out the minimum and maximum values in the columns to get the plotting range correct
        xmin = self.dataframe[xcols[0]].min()
        xmax = self.dataframe[xcols[0]].max()
        ymin = self.dataframe[ycols[0]].min()
        ymax = self.dataframe[ycols[0]].max()
        # Set axis limits
        plt.xlim(xmin, 100)
        plt.ylim(ymin, 100)
        # Set the x and y axis labels from the user specified ones above
        plt.xlabel(r'{}'.format(xAxisLabel))
        plt.ylabel(r'{}'.format(yAxisLabel))
        # Show the legend
        plt.legend()
        plt.grid(True)
        # Finally show the plot on screen
        plt.show() 
    
    def performEDA(self, value1, value2, condition):
        # Send the selected operator to Conditions enum
        condition = DataframeManager.assignEnumValue(condition)
        if value1 == '' or value2 == '':
            self.showErrorWithString('Please complete Column and Query')
            return
        self.executeQuery(value1, condition, value2, self.dataframe)
        self.showDataframeTable(self.dataframe)

    def showDataframeTable(self, df):
        if df.empty:
            self.showErrorWithString("Empty dataframe")
            return
        
        data = df.values.tolist()

        layout = [[sg.Button('New query'), sg.Cancel()],[sg.Table(values=data, headings=df.columns.tolist(), display_row_numbers=True, auto_size_columns=False, num_rows=min(25, len(data)))],]
       
        dataframeWindow = sg.Window('Table', layout, grab_anywhere=False)
        while True:
            event, values = dataframeWindow.read()
            if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
                break
            if event == "Export resulted df as xlsx file":
             DataframeManager.saveFile()
            if event == "New query":
                dataframeWindow.close()

        dataframeWindow.close()
    
    def showSuccessPopup(self):
        sg.Popup('Now you can enter queries')

    def showErrorInDataType():
        sg.Popup('Data type of the specified column is not numeric')
    
    def showErrorWithString(self, s):
        sg.Popup('Error', s, font==CustomFonts.ERROR, keep_on_top=True)

    def executeQuery(self, column, condition, value, df): 
        # Check if variable df is empty, if it is populate it
        if df.empty == True:   
            try:
                readFile = pd.read_csv('ConvertedFile.csv', index_col=None)
            except pd.errors.EmptyDataError:
                self.showErrorWithString('No file with this name found')
                return

            self.dataframe = pd.DataFrame(readFile)
            df = self.dataframe
        else:
            self.dataframe = df
 
        # Check if the send value for  the condition is a Conditions type enum
        if not isinstance(condition, Conditions):
                raise TypeError('conditions must be an instance of Conditiond Enum')

        # In case the condition is different than equal be sure the fields are numeric ones otherwise show error
        if condition != Conditions.EQUAL:
                if self.dataframe[column].values.dtype == str or self.dataframe[column].values.dtype == object:
                    self.showErrorWithString("Column contains different datatype than numeric")
                    return

        if column in df.columns:
            self.dataframe = DataframeManager.updateDataframe(self.dataframe, column, value, condition)
        else:
            self.showErrorWithString("There is no column with this name")

    def convertToCVS(self, path):
        file_name, file_extension = os.path.splitext(path)
        if file_extension != ".xlsx":
            self.showErrorWithString("File type should be xlsx")
            return
    
        data_xls = pd.read_excel(path, dtype=str, index_col=None)
        df = data_xls.to_csv('ConvertedFile.csv', encoding='utf-8', index=False)
        self.dataframe = pd.read_csv('ConvertedFile.csv', delimiter= ",")
        
        if self.dataframe.empty == TRUE :
            self.showErrorWithString('Opps!', 'Converted file is empty')
        else :
            self.showSuccessPopup()

myApp = AppUI()
