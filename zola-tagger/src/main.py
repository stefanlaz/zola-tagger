'''
Created on Feb 1, 2017

@author: Stefan
'''

import os
import io
import tagger
import utils
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage

class ToolTipLabel(Label):
    
    open = BooleanProperty()

class TagLabel(Label):
    
    def __init__(self, **kwargs):
        super(TagLabel, self).__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouse_pos)
        self.tooltip = ToolTipLabel(text=self.text)
    
    def on_mouse_pos(self, *args):
        if self.is_shortened and self.parent is not None:
            pos = args[1]
            inside = self.collide_point(*pos)
            if inside and not self.tooltip.open:
                self.tooltip.pos = pos
                Window.add_widget(self.tooltip)
                self.tooltip.open = True
            elif not inside and self.tooltip.open:
                Window.remove_widget(self.tooltip)
                self.tooltip.open = False
            elif inside and self.tooltip.open:
                self.tooltip.pos = pos
        elif self.parent is None:
            Window.remove_widget(self.tooltip)

class SongListLabel(TagLabel):
        
    full_name = StringProperty()
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.parent.parent.parent.getTags(self.full_name)
            return True
        else:
            return Label.on_touch_down(self, touch)

class HeaderLabel(Label):
    pass

class TagsGrid(GridLayout):
             
    def populateGrid(self, filename):
        self.clear_widgets()
        self.cols = 3
        #self.row_force_default = True
        self.add_widget(HeaderLabel(text='Tags'))
        self.add_widget(HeaderLabel(text='Current Value'))
        self.add_widget(HeaderLabel(text='New Value'))
        if os.path.isfile(filename):
            try:
                for tag in tagger.parseFile(filename):
                    if tag['id'].startswith('T'):
                        self.add_widget(TagLabel(text=tag['desc']))
                        self.add_widget(TagLabel(text=tag['content']))
                        self.add_widget(TextInput(size_hint_y=None, height=40))
                    elif tag['id'] == 'APIC':
                        image_label = TagLabel(text=tag['desc'], height=200)
                        self.add_widget(image_label)
                        image = Image(size_hint_y=None, height=200, texture=CoreImage(io.BytesIO(tag['content']), ext=tag['image_file_type']).texture)
                        self.add_widget(image)
            except (tagger.HeaderError, IOError, ValueError) as err:
                popup = Popup(title='Error',
                              content=Label(text=str(err)),
                              size_hint=(None, None), size=(400, 200))
                popup.open()
                
class SongList(GridLayout):
    pass

class MainWindow(BoxLayout):
    
    def on_dropfile(self, widget, filename):
        filename_str = filename.decode('utf-8')
        self.populateFileList(filename_str)
        
    def populateFileList(self, filename):
        try:
            self.remove_widget(self.ids.start_label)
        except ReferenceError:
            pass
        song_list = self.ids.songs
        song_list.clear_widgets()
        song_list.size_hint = (1, 1)
        if os.path.isfile(filename):
            song_list.add_widget(SongListLabel(text=utils.getParentFolderAndFileName(filename)))
        elif os.path.isdir(filename):
            for f in [os.path.join(filename, base_filename) for base_filename in os.listdir(filename) if os.path.splitext(base_filename)[1] == ".mp3"]:
                song_list.add_widget(SongListLabel(text=utils.getParentFolderAndFileName(f), full_name=f))
        self.ids.split.size_hint = (1, 1)
        tags_grid = self.ids.tags
        tags_grid.clear_widgets()
        tags_grid.size_hint = (1, 1)
        tags_grid.row_force_default = False
        tags_grid.add_widget(Label(text='Select a song from the left'))
        
    def getTags(self, filename):
        self.ids.tags.populateGrid(filename)

class ZolaTaggerApp(App):

    def build(self):
        root = MainWindow()
        Window.bind(on_dropfile=root.on_dropfile)
        Window.size = (1000, 800)
        return root

if __name__ == '__main__':
    try:
        ZolaTaggerApp().run()
    except Exception as err:
        print(err)