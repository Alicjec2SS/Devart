from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image as KivyImage
from kivy.uix.popup import Popup
from kivy.graphics.texture import Texture

import os
import zipfile
from PIL import Image as PILImage
from tkinter import filedialog
import threading
import sys


class ImageEntry(BoxLayout):
    def __init__(self, image_data, **kwargs):
        super().__init__(orientation='vertical', size_hint_y=None, height=160, spacing=5, padding=5, **kwargs)
        self.image_data = image_data

        self.label_id = Label(text=f"ID: {image_data['id']}", size_hint_y=None, height=30)
        self.add_widget(self.label_id)

        self.label_path = Label(text="Path: (no file)", size_hint_y=None, height=30)
        self.add_widget(self.label_path)

        self.image_widget = KivyImage(size_hint=(1, None), height=100)
        self.add_widget(self.image_widget)

        self.select_button = Button(text="Select Image", size_hint_y=None, height=40, on_press=self.select_image)
        self.add_widget(self.select_button)

    def select_image(self, instance):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.webp *.bmp")])
        if file_path:
            try:
                pil_image = PILImage.open(file_path)
                pil_image.thumbnail((100, 100))
                self.image_data['path'] = file_path

                texture = self.pil_to_texture(pil_image)
                self.image_widget.texture = texture
                self.label_path.text = os.path.basename(file_path)
            except Exception as e:
                print(f"Error loading image: {e}")

    def pil_to_texture(self, pil_image):
        pil_image = pil_image.convert('RGBA')
        w, h = pil_image.size
        data = pil_image.tobytes()
        texture = Texture.create(size=(w, h))
        texture.blit_buffer(data, colorfmt='rgba', bufferfmt='ubyte')
        return texture


class MainApp(App):
    def build(self):
        self.image_data_list = []

        self.root_box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.input_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        self.input_field = TextInput(hint_text='Number of pictures', input_filter='int', multiline=False)
        self.enter_button = Button(text="Enter", on_press=self.create_image_inputs)

        self.input_layout.add_widget(self.input_field)
        self.input_layout.add_widget(self.enter_button)
        self.root_box.add_widget(self.input_layout)

        self.scrollview = ScrollView(size_hint=(1, 1))
        self.image_grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.image_grid.bind(minimum_height=self.image_grid.setter('height'))
        self.scrollview.add_widget(self.image_grid)
        self.root_box.add_widget(self.scrollview)

        return self.root_box

    def create_image_inputs(self, instance):
        self.image_grid.clear_widgets()
        self.image_data_list.clear()

        try:
            count = int(self.input_field.text)
        except ValueError:
            return

        for i in range(count):
            image_info = {'id': str(i + 1), 'path': None}
            self.image_data_list.append(image_info)

            entry = ImageEntry(image_info)
            self.image_grid.add_widget(entry)

        self.save_button = Button(text="Dump to zip file...", size_hint_y=None, height=50)
        self.save_button.bind(on_press=self.save_images)
        self.image_grid.add_widget(self.save_button)

    def save_images(self, instance):
        def run():
            path = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("ZIP files", "*.zip")])
            if not path:
                return

            try:
                with zipfile.ZipFile(path, "w") as zipf:
                    for item in self.image_data_list:
                        if item['path']:
                            ext = os.path.splitext(item['path'])[1]
                            zipf.write(item['path'], f"{item['id']}{ext}")
            except Exception as e:
                print(f"Error zipping file: {e}")
                return

            popup = Popup(title='Done', content=Label(text='Export completed!'), size_hint=(None, None), size=(300, 200))
            popup.open()

        threading.Thread(target=run).start()


if __name__ == '__main__':
    MainApp().run()
