'''
File Splitter App

This app takes in a source file, and splits it into two separate files, with
odd lines in the first target file, and even lines in the second target file.

It was developed to help split a single-file corpus containing language-pair
lines, with source language text in one line, and the target language text
in the next line. This app will split the corpus into two files, one containing
the source language text, and the other containing the target language text.

Created on Feb 7, 2017

Feb 19, 2017:   Added checkbox to allow appending to target files.
                Add Exit button.

@author: vivian
'''
from functools import partial
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.textinput import TextInput
from kivy.config import Config
from kivy.uix.checkbox import CheckBox
#from kivy.core.window import Window

# Set the size of the main window.
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '300')

# This is the global variable containing the reference to the root widget.
root = None

class LoadDialog(BoxLayout):
    """ Opens a FileChooserListView dialog box for user to choose a file to load.
    """
    set_source_file = ObjectProperty(None)
    cancel = ObjectProperty(None)
    def __init__(self, set_source_file, cancel, **kwargs):
        super(LoadDialog, self).__init__(**kwargs)
        self.orientation = "vertical"
        global root
        self.size = root.size
        self.pos = root.pos
        self.default_path = root.default_path
        self.cancel = cancel
        self.set_source_file = set_source_file
        self.build_window()

    def build_window(self):
        """ Method to draw GUI elements.
        """
        filechooser = FileChooserListView(path=self.default_path)
        ok_button = Button(text="OK", on_press=partial(self.set_source_file, filechooser))
        cancel_button = Button(text="Cancel", on_press=self.cancel)
        button_row = BoxLayout(size_hint_y=None, height=30)
        button_row.add_widget(ok_button)
        button_row.add_widget(cancel_button)
        self.add_widget(filechooser)
        self.add_widget(button_row)


class SaveDialog(BoxLayout):
    """ Opens a FileChooserListView dialog box for user to choose a file to save to.
        The user can also key in a new filename in the text input box to save to a
        new file.
    """
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)
    set_target_file = ObjectProperty(None)
    def __init__(self, set_target_file, cancel, **kwargs):
        super(SaveDialog, self).__init__(**kwargs)
        self.orientation = "vertical"
        global root
        self.size = root.size
        self.pos = root.pos
        self.default_path = root.default_path
        self.cancel = cancel
        self.set_target_file = set_target_file
        self.build_window()


    def build_window(self):
        """ Method to draw GUI elements.
        """
        filechooser = FileChooserListView(path=self.default_path)
        text_input = TextInput(text="", multiline=False)
        ok_button = Button(text="OK", on_press=partial(self.set_target_file, filechooser, text_input))
        cancel_button = Button(text="Cancel", on_press=self.cancel)
        button_row = BoxLayout(size_hint_y=None, height=30)
        button_row.add_widget(ok_button)
        button_row.add_widget(cancel_button)
        text_input_row = BoxLayout(size_hint_y=None, height=30)
        text_input_row.add_widget(text_input)
        self.add_widget(filechooser)
        self.add_widget(text_input_row)
        self.add_widget(button_row)


class RootWidget(BoxLayout):

    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.build_main_window()
        self.default_path = "/home/" # The default path that FileChoosers will open to.
        global root
        root = self
        

    def dismiss_popup(self, *args):
        """ Closes any popup that is opened.
        """
        self._popup.dismiss()

    def show_load(self, *args):
        """ Handler when "Select Source File" button is pressed.
        """
        content = LoadDialog(set_source_file=self.set_source_file, cancel=self.dismiss_popup)
        self._popup = Popup(title="Select Source File", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def show_save1(self, *args):
        """ Handler when "Set Target File 1" button is pressed.
        """
        content = SaveDialog(set_target_file=self.set_target_file1, cancel=self.dismiss_popup)
        self._popup = Popup(title="Set Target File 1", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def show_save2(self, *args):
        """ Handler when "Set Target File 2" button is pressed.
        """
        content = SaveDialog(set_target_file=self.set_target_file2, cancel=self.dismiss_popup)
        self._popup = Popup(title="Set Target File 2", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()
        
    def close_app(self, *args):
        self.root_app.stop(self)

    def set_source_file(self, filechooser, *args):
        """ Called by LoadDialog to set the path and filename of the source file.
        """
        self.source_filename = filechooser.selection[0]
        print(self.source_filename)
        self.source_label.text = str(self.source_filename)
        # Message prompt to tell user what to do next.
        self.message_label.text = "Set name of first target file"
        self.dismiss_popup()
    
    def set_target_file1(self, filechooser, text_input, *args):
        """ Called by SaveDialog to set the path and filename of the first target file.
        """
        # If user did not enter a name in the text box, save to the selected file.
        # Otherwise, save to a new file with the file name given by the user.
        if text_input.text == "":
            self.target1_filename = filechooser.selection
        else:
            self.target1_filename = str(filechooser.path) + "/" + text_input.text
        self.target1_label.text = str(self.target1_filename)
        # Message prompt to tell user what to do next.
        self.message_label.text = "Set name of second target file"
        self.dismiss_popup()
    
    def set_target_file2(self, filechooser, text_input, *args):
        """ Called by SaveDialog to set the path and filename of the second target file.
        """
        # If user did not enter a name in the text box, save to the selected file.
        # Otherwise, save to a new file with the file name given by the user.
        if text_input.text == "":    
            self.target2_filename = filechooser.selection
        else:
            self.target2_filename = str(filechooser.path) + "/" + text_input.text
        self.target2_label.text = str(self.target2_filename)
        # Message prompt to tell user what to do next.
        self.message_label.text = "Ready to split file"
        self.dismiss_popup()

    def set_root_app(self, root_app):
        self.root_app = root_app


    def build_main_window(self):
        """ Method to draw GUI elements.
        """
        source_button = Button(text="Select Source File", on_press=self.show_load,
                               size_hint_x=0.4, size_hint_y=None, height=30)
        self.source_label = Label(text="", size_hint_x=0.6)
        target1_button = Button(text="Set Target File 1", on_press=self.show_save1,
                                size_hint_x=0.4, size_hint_y=None, height=30)
        self.target1_label = Label(text="", size_hint_x=0.6)
        target2_button = Button(text="Set Target File 2", on_press=self.show_save2,
                                size_hint_x=0.4, size_hint_y=None, height=30)
        self.target2_label = Label(text="", size_hint_x=0.6)
        execute_button = Button(text="Split File", on_press=self.split_file,
                                size_hint_x=None, width=100, size_hint_y=None, height=30,
                                pos_hint={'y': 0, 'center_x': .5})
        exit_button = Button(text="Exit", on_press=self.close_app,
                                size_hint_x=None, width=100, size_hint_y=None, height=30,
                                pos_hint={'y': 0, 'center_x': .5})
        self.message_label = Label(text="Choose file to split") # Message prompt to tell user what to do next.
        append_label = Label(text="Append", size_hint_x=0.4)
        self.append_checkbox = CheckBox(active="True", size_hint_x=0.05)
        spacer_label = Label(text="")
        checkbox_container = BoxLayout(padding=[10,0,5,0])
        checkbox_container.add_widget(self.append_checkbox)
        checkbox_container.add_widget(append_label)
        checkbox_container.add_widget(spacer_label)
        source_row = BoxLayout(orientation="horizontal", size_hint_y=0.15)
        target1_row = BoxLayout(orientation="horizontal", size_hint_y=0.15)
        target2_row = BoxLayout(orientation="horizontal", size_hint_y=0.15)
        execute_row = BoxLayout(orientation="horizontal", size_hint_y=0.15)
        exit_row = BoxLayout(orientation="horizontal", size_hint_y=0.15)
        message_row = BoxLayout(orientation="horizontal", size_hint_y=0.25)
        source_row.add_widget(source_button)
        source_row.add_widget(self.source_label)
        target1_row.add_widget(target1_button)
        target1_row.add_widget(self.target1_label)
        target2_row.add_widget(target2_button)
        target2_row.add_widget(self.target2_label)
        execute_row.add_widget(execute_button)
        execute_row.add_widget(checkbox_container)
        exit_row.add_widget(exit_button)
        message_row.add_widget(self.message_label)
        self.add_widget(source_row)
        self.add_widget(target1_row)
        self.add_widget(target2_row)
        self.add_widget(execute_row)
        self.add_widget(exit_row)
        self.add_widget(message_row)


    def split_file(self, *args):
        """ Method to handle actual logic for the app.
            Read in lines from source file, then save odd lines in one file,
            and even lines in another file.
            
            Note: In Python, although line numbering will start with 0, 1, 2,...
            the source file is being split according to normal human convention
            for odd and even line numbering, i.e. the first line in the source
            file will be stored in the array "odd_lines" while the second line
            will be stored in "even_lines".
        """
        if root.append_checkbox.active == True:
            open_flag = "a"
        else:
            open_flag = "w"
        with open(self.source_filename) as stream_in:
            lines = stream_in.readlines()
        odd_lines, even_lines = lines[::2], lines[1::2]
        with open(self.target1_filename, open_flag) as stream_out1:
            for odd_line in odd_lines:
                stream_out1.write(odd_line)
        with open(self.target2_filename, open_flag) as stream_out2:
            for even_line in even_lines:
                stream_out2.write(even_line)            
        self.message_label.text = "File split completed!"


class FileSplitterApp(App):
    def build(self):
        self.root_widget = RootWidget()
        self.root_widget.set_root_app(self)
        return self.root_widget


def main():
    app = FileSplitterApp()
    app.run()
    #dynamically resize window
    #Window.size = (300, 100)
    
    
if __name__ == "__main__":
    main()
