'''
Utility app to pull updates for selected Git local repositories.

Basically loops through a list of directories, go into each directory,
and runs "git pull origin master" command to update each local repository.

Created on Feb 10, 2017

@author: vivian
'''

from kivy.app import App
from kivy.uix.settings import SettingsWithTabbedPanel
from kivy.logger import Logger
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.button import Button
from functools import partial
from kivy.uix.listview import ListItemButton
import os
import shlex
from subprocess import Popen, PIPE
from docutils.parsers.rst.directives import path
#from kivy.core.window import Window

# Define GUI with KV language
kv = '''
#: import main gitpulltool
#: import ListAdapter kivy.adapters.listadapter.ListAdapter
#: import ListItemButton kivy.uix.listview.ListItemButton

RootWidget:

<RootWidget>:
    orientation: "vertical"
    path_list: path_list_view

    BoxLayout:
        orientation: "horizontal"
        size_hint_y: 0.1
        Button:
            text: 'Update repositories'
            on_release: root.update_repositories()
            size_hint_x: 0.22
        Label:
            text: ""
            size_hint_x: 0.05
        Button:
            text: 'Add local repository'
            on_release: root.handle_add()
            size_hint_x: 0.23
        Button:
            text: 'Remove local repository'
            on_release: root.del_path()
            size_hint_x: 0.24
        Label:
            text: ""
            size_hint_x: 0.05
        Button:
            text: 'Configure app'
            on_release: app.open_settings()
            size_hint_x: 0.18
        Button:
            text: "Exit"
            on_press: app.stop() 
            size_hint_x: 0.12
    ListView:
        id: path_list_view
        size_hint_y: 0.9
        adapter:
            ListAdapter(data=[], cls=main.PathButton)
'''

# This JSON defines entries we want to appear in our App configuration screen
json = '''
[
    {
        "type": "path",
        "title": "Git location",
        "desc": "Choose where the git executable can be found",
        "section": "Setup",
        "key": "git_location"
    },
    {
        "type": "path",
        "title": "Default Git directory",
        "desc": "Choose the default directory were local repositories can be found",
        "section": "Setup",
        "key": "default_git_repo"
    }
]
'''

def execute_shell_cmd(cmd):
    """
    Execute the external command and get its exitcode, stdout and stderr.
    """
    args = shlex.split(cmd)
    proc = Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    exitcode = proc.returncode
    return exitcode, out, err


class PathButton(ListItemButton):
    pass


class PathChooser(BoxLayout):
    """ Opens a FileChooserListView dialog box for user to choose a file to load.
    """
    add_path = ObjectProperty(None)
    cancel = ObjectProperty(None)
    def __init__(self, add_path, cancel, default_path, root, **kwargs):
        super(PathChooser, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.default_path = default_path
        self.cancel = cancel
        self.add_path = add_path
        self.build_window()


    def build_window(self):
        """ Method to draw GUI elements.
        """
        filechooser = FileChooserListView(path=self.default_path)
        filechooser.dirselect = True
        ok_button = Button(text="OK", on_press=partial(self.add_path, filechooser))
        cancel_button = Button(text="Cancel", on_press=self.cancel)
        button_row = BoxLayout(size_hint_y=0.05)
        button_row.add_widget(ok_button)
        button_row.add_widget(cancel_button)
        self.add_widget(filechooser)
        self.add_widget(button_row)


class RootWidget(BoxLayout):
    path_list = ObjectProperty()
    git_location = ""
    default_git_repo = ""

    def dismiss_popup(self, *args):
        """ Closes any popup that is opened.
        """
        self._popup.dismiss()


    def handle_add(self, *args):
        """ Handler when "Add local repository" button is pressed.
        """
        content = PathChooser(add_path=self.add_path, cancel=self.dismiss_popup,
                            default_path=self.default_git_repo, root=self)
        self._popup = Popup(title="Select directory", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()


    def add_path(self, filechooser, *args):
        """ Called by PathChooser to set the path and filename of the source file.
        """
        self.path_list.adapter.data.extend([filechooser.selection[0]])
        self.path_list._trigger_reset_populate()
        repo_list_string = ",".join(self.path_list.adapter.data)
        self.config.set('Setup', 'repo_list', repo_list_string)
        print("repo list: "+ self.config.get('Setup', 'repo_list'))
        self.config.write()
        self.dismiss_popup()

        
    def del_path(self, *args):
        """ Handler when "Remove local directory" button is pressed.
        """
        if self.path_list.adapter.selection:
            selection = self.path_list.adapter.selection[0].text
            self.path_list.adapter.data.remove(selection)
            self.path_list._trigger_reset_populate()


    def add_data_from_config(self, repo_list):
        """ Adds the paths obtained from ConfigParser to the path list.
        
            repo_list is a CSV string, which needs to be split into a Python list.
        """
        self.path_list.adapter.data.clear()
        for path in repo_list.split(","):
            self.path_list.adapter.data.append(path)
        self.path_list._trigger_reset_populate()

    
    def set_config(self, config):
        self.config = config
        
        
    def update_repositories(self):
        """ Handler when "Update repositories" button is pressed.
        """
        git_cmd = self.config.get("Setup", "git_location") + " " + "pull origin master"
        current_dir = os.getcwd()
        for path in self.config.get("Setup", "repo_list").split(","):
            if path == "":
                pass
            else:
                os.chdir(path)
                print("Changing to: " + os.getcwd())
                print(git_cmd)
                exitcode, out, err = execute_shell_cmd(git_cmd)
                print(out)
        os.chdir(current_dir)


class GitPullApp(App):

    def build(self):
        """
        Build and return the root widget.
        """
        # The line below is optional. You could leave it out or use one of the
        # standard options, such as SettingsWithSidebar, SettingsWithSpinner
        # etc.
        self.settings_cls = SettingsWithTabbedPanel
        
        # We apply the saved configuration settings or the defaults
        self.root = Builder.load_string(kv)
        self.root.default_git_repo = self.config.get('Setup', 'default_git_repo')
        self.root.set_config(self.config)
        print("Repo: " + self.config.get('Setup', 'repo_list'))
        self.root.add_data_from_config(self.config.get('Setup', 'repo_list'))
        return self.root


    def build_config(self, config):
        """
        Set the default values for the configs sections.
        """
        config.setdefaults('Setup', {'git_location': 'git', 'default_git_repo': '', 'repo_list': ''})


    def build_settings(self, settings):
        """
        Add our custom section to the default configuration object.
        """
        # We use the string defined above for our JSON, but it could also be
        # loaded from a file as follows:
        #     settings.add_json_panel('My Label', self.config, 'settings.json')
        settings.add_json_panel('Setup', self.config, data=json)


    def on_config_change(self, config, section, key, value):
        """
        Respond to changes in the configuration.
        """
        Logger.info("main.py: App.on_config_change: {0}, {1}, {2}, {3}".format(
            config, section, key, value))

        if section == "Setup":
            if key == "git_location":
                self.root.git_location = value
            elif key == 'default_git_repo':
                self.root.default_git_repo = value


def main():
    app = GitPullApp()
    app.run()
    #dynamically resize window
    #Window.size = (300, 100)
    
    
if __name__ == "__main__":
    main()





