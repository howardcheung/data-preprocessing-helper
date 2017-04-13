﻿#!/usr/bin/python
"""
    This script file contains methods to define the graphical user interface
    of the tool.

    Author: Howard Cheung
    email: howard.at@gmail.com
"""

# import python internal modules
from webbrowser import open as webbrowseropen
from os.path import isfile

# import third party modules
import wx

# import user-defined modules


# define global variables
class MainGUI(wx.Frame):
    """
        Class to hold the object for the main window of the application
    """

    def __init__(self, parent, title):
        """
            This is the initilization function for the GUI.

            Inputs:
            ==========
            parent: wx.Frame
                parent object

            title: str
                title of the window
        """
        super(MainGUI, self).__init__(
            parent, title=title, size=(625, 400)
        )  # size of the application window

        self.initui()
        self.Centre()
        self.Show()

    def initui(self):
        """
            Initialize the position of objects in the UI
        """

        # define the panel
        panel = wx.Panel(self)

        # define layer size
        begin_depth = 20
        layer_diff = 40
        first_blk = 20
        second_blk = 200
        third_blk = 475

        # sizer = wx.GridBagSizer(1, 1)  # making a grid in your box

        # title
        # leave space at the top, left and bottom from the text to the
        # other object
        
        # position: (from top to bottom, from left to right)
        wx.StaticText(panel, label=u''.join([
            u'Time-of-change value data to data',
            u'at constant time intervals'
        ]), pos=(20, begin_depth))

        # Inputs to the data file path
        text = wx.StaticText(
            panel, label=u'Data file path:', pos=(20, begin_depth+layer_diff)
        )

        # require additional object for textbox
        # with default path
        self.dfpath = wx.TextCtrl(
            panel, value=u'../dat/time_of_change.csv',
            pos=(200, begin_depth+layer_diff), size=(250, 20)
        )
        button = wx.Button(
            panel, label=u'Browse...', pos=(475, begin_depth+layer_diff)
        )
        button.Bind(wx.EVT_BUTTON, self.OnOpen)

        # ask for existence of header as a checkbox
        text = wx.StaticText(
            panel, label=u'Existence of a header row:',
            pos=(20, begin_depth+layer_diff*2)
        )
        self.header = wx.CheckBox(
            panel, pos=(200, begin_depth+layer_diff*2)
        )
        self.header.SetValue(True)

        # Inputs to the directory to save the plots
        text = wx.StaticText(
            panel, label=u'Path to save file:',
            pos=(20, begin_depth+layer_diff*3)
        )

        # require additional object for textbox
        # with default path
        self.newdfpath = wx.TextCtrl(
            panel, value=u'../testplots/example.csv',
            pos=(200, begin_depth+layer_diff*3), size=(250, 20)
        )
        button = wx.Button(
            panel, label=u'Browse...', pos=(475, begin_depth+layer_diff*3)
        )
        button.Bind(wx.EVT_BUTTON, self.SaveOpen)

        # Inputs to the format time string
        text = wx.StaticText(panel, label=u''.join([
            u'Format of time string \nin the first column:'
        ]), pos=(20, begin_depth+layer_diff*4))

        # # require additional object for textbox
        self.timestring = wx.TextCtrl(
            panel, value=u'%m/%d/%y %I:%M:%S %p CST',
            pos=(200, begin_depth+layer_diff*4), size=(250, 20)
        )

        # a button for instructions
        button = wx.Button(
            panel,
            label=u'Instructions to enter the format of the time string',
            pos=(200, begin_depth+layer_diff*4+20)
        )
        button.Bind(wx.EVT_BUTTON, self.TimeInstruct)

        # add start time check boxes
        text = wx.StaticText(panel, label=u''.join([
            u'Start time in the new data file:'
        ]), pos=(20, begin_depth+layer_diff*5+20))

        # create spin control for the date and time
        self.start_yr = wx.SpinCtrl(
            panel, value='2017', min=1, max=4000,
            pos=(200, begin_depth+layer_diff*5+20), size=(50, 20)
        )
        text = wx.StaticText(panel, label=u''.join([
            u'Year'
        ]), pos=(200, begin_depth+layer_diff*5+40))
        self.start_mon = wx.ComboBox(
            panel, pos=(270, begin_depth+layer_diff*5+20), size=(50, 20),
            choices=[str(ind) for ind in range(1, 13)]
        )
        self.start_mon.SetValue('1')
        text = wx.StaticText(panel, label=u''.join([
            u'Month'
        ]), pos=(270, begin_depth+layer_diff*5+40))
        self.start_day = wx.ComboBox(
            panel, pos=(270, begin_depth+layer_diff*5+20), size=(50, 20),
            choices=[str(ind) for ind in range(1, 13)]
        )
        text = wx.StaticText(panel, label=u''.join([
            u'Month'
        ]), pos=(270, begin_depth+layer_diff*5+40))
        

        # buttons at the bottom
        # button_ok = wx.Button(panel, label=u'Analysis')
        # button_ok.Bind(wx.EVT_BUTTON, self.Analyzer)
        # sizer.Add(button_ok, pos=(8, 4))

    def ShowMessage(self):
        """
            Function to show message about the completion of the analysis
        """
        wx.MessageBox(
            u'Processing Completed', u'Status', wx.OK | wx.ICON_INFORMATION
        )

    def OnClose(self, evt):
        """
            Function to close the main window
        """
        self.Close(True)

    def OnOpen(self, evt):
        """
            Function to open a file
            Reference:
            https://wxpython.org/Phoenix/docs/html/wx.FileDialog.html
        """
        # proceed asking to the user the new directory to open
        openFileDialog = wx.FileDialog(
            self, 'Open file', '', '',
            ''.join([
                'csv files (*.csv)|*.csv;|',
                'xls files (*.xls)|*.xls;|',
                'xlsx files (*.xlsx)|*.xlsx'
            ]), wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        )

        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return False  # the user changed idea...

        # proceed loading the file chosen by the user
        # this can be done with e.g. wxPython input streams:
        filepath = openFileDialog.GetPath()
        self.dfpath.SetValue(filepath)

        if not isfile(filepath):
            wx.LogError('Cannot open file "%s".' % openFileDialog.GetPath())
            return False

    def SaveOpen(self, evt):
        """
            Function to open a file
            Reference:
            https://wxpython.org/Phoenix/docs/html/wx.DirDialog.html
        """
        # proceed asking to the user the new file to open

        openFileDialog = wx.FileDialog(
            self, 'Open file', '', '',
            ''.join([
                'csv files (*.csv)|*.csv'
                # 'xls files (*.xls)|*.xls;|',  # to be done
                # 'xlsx files (*.xlsx)|*.xlsx'  # to be done
            ]), wx.FD_SAVE
        )

        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return False  # the user changed idea...

        # proceed saving the file chosen by the user
        # this can be done with e.g. wxPython input streams:
        filepath = openFileDialog.GetPath()
        self.newdfpath.SetValue(filepath)

    def TimeInstruct(self, evt):
        """
            Function to open instructions for time string
        """
        webbrowseropen(
            u''.join([
                u'https://docs.python.org/3.5/library/datetime.html',
                u'#strftime-and-strptime-behavior'
            ])
        )

    def Analyzer(self, evt):
        """
            Function to initiate the main analysis.
        """
        # Run the analyzer

        # function to be called upon finishing processing
        wx.CallLater(0, self.ShowMessage)


# define functions
def gui_main():
    """
        Main function to intiate the GUI
    """
    app = wx.App()
    MainGUI(None, title=u'Data Preprocessing Helper')
    app.MainLoop()


# run the method for the GUI
if __name__ == '__main__':
    gui_main()
