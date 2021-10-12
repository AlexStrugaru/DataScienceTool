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
        
        sg.theme('LightGrey1')
        layout = [[sg.Text("Choose a xls file: ", key='-TEXT-'), sg.FileBrowse()],
                [sg.Submit(), sg.Cancel()], [sg.Text('FILTER DATAFRAME', font=BOLD)],
                [sg.HorizontalSeparator(color='Blue')],
                [sg.Text('There is possible to apply up to 4 conditions, each condition is applyed to the previous dataframe resulted \n (eq. cond1 -> Submit -> df -> Cond 2 -> Submit -> df modified with additional condition -> df1)')], 
                [sg.Text('Enter 1st column', key='-TEXT1-'), sg.InputText(), sg.Combo(values=['==', '<', '>','>=', '<='], key='fac1', default_value='=='), sg.Text('Enter 1st query'), sg.InputText(), sg.Submit(), sg.Text('Query1', key='QUERY1',text_color='blue')],
                [sg.Button(button_text="Export file")],
                [sg.HorizontalSeparator(color='Blue')],
                [sg.Text('PLOTTING', font=BOLD)],
                [sg.InputText('X', size=(5, 1)),
                sg.InputText('Y', size=(5, 1)),
                sg.InputCombo(values=('point', 'line')),
                sg.InputCombo(values=(matplotlib_colours)),
                sg.InputCombo(values=(matplotlib_linestyles)),
                sg.InputText('Enter Legend Label', size=(20, 1))],
                [sg.Text('_'  * 100, size=(100, 1))],
                [sg.Button('Plot')]]

        self.window = sg.Window('Data Science Application', layout, size=(1000,800))
    
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
                break
            if event == "Submit":
                self.convertToCVS(values['Browse'])
            if event == "Submit0":
                self.performEDA(values[1], values[2], values['fac1'])
            if event == "Export file":
                xlsWriter = pd.ExcelWriter(r'FilteredFile.xlsx')
                self.dataframe.to_excel(xlsWriter, sheet_name='FilteredData', index=False)
                xlsWriter.close()
            if event == "Plot":
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
                    ax.plot(self.dataframe[xcols[0]], self.dataframe[ycols[0]], color=next(plot_colour), linestyle=next(plot_line), label=r'{}'.format(legendLabels[0]))
    
                # Work out the minimum and maximum values in the columns to get the plotting range correct
                xmin = self.dataframe[xcols[0]].min()
                xmax = self.dataframe[xcols[0]].max()
                ymin = self.dataframe[ycols[0]].min()
                ymax = self.dataframe[ycols[0]].max()
                # Set axis limits
                plt.xlim(xmin, None)
                plt.ylim(ymin, None)
                # Set the x and y axis labels from the user specified ones above
                plt.xlabel(r'{}'.format(xAxisLabel))
                plt.ylabel(r'{}'.format(yAxisLabel))
                # Show the legend
                plt.legend()

                # Finally show the plot on screen
                plt.show() 

        self.window.close()
    
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
    
    def showError(self):
        sg.Popup('Opps!', 'Converted file is empty')

    def showSuccessPopup(self):
        sg.Popup('Now you can enter queries')

    def showErrorInDataType():
        sg.Popup('Data type of the specified column is not numeric')
    
    def showErrorWithString(self, s):
        sg.Popup('Error', s)

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
        if condition!= Conditions.EQUAL:
                if self.dataframe[column].values.dtype == str or self.dataframe[column].values.dtype == object:
                    self.showErrorInDataType()
                    return

        if column in df.columns:
            self.dataframe = DataframeManager.updateDataframe(self.dataframe, column, value, condition)
        else:
            self.showErrorWithString("There is no column with this name")

    def convertToCVS(self, path):
        data_xls = pd.read_excel(path, dtype=str, index_col=None)
        current_date = dt.datetime.now()
        df = data_xls.to_csv('ConvertedFile.csv', encoding='utf-8', index=False)
        self.dataframe = pd.read_csv('ConvertedFile.csv', delimiter= ",")
        
        if self.dataframe.empty == TRUE :
            self.showError()
        else :
            self.showSuccessPopup()

myApp = AppUI()
