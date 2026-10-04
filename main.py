import os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
from kivy.core.window import Window

Window.clearcolor = (0.1, 0.08, 0.09, 1)

KV = '''
<BeksflyRoot>:
    orientation: 'vertical'
    canvas.before:
        Color:
            rgba: 0.1, 0.08, 0.09, 1
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        size_hint_y: None
        height: '56dp'
        padding: ['16dp', '0dp']
        canvas.before:
            Color:
                rgba: 0.55, 0.05, 0.08, 1
            Rectangle:
                pos: self.pos
                size: self.size
        Label:
            text: 'Beksfly'
            font_size: '22sp'
            bold: True
            color: 1, 1, 1, 1
            halign: 'left'
            valign: 'middle'
            text_size: self.size

    ScrollView:
        do_scroll_x: False
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: self.minimum_height
            padding: ['20dp', '20dp']
            spacing: '14dp'

            Label:
                text: 'Подать объявление'
                font_size: '18sp'
                bold: True
                color: 0.9, 0.9, 0.9, 1
                size_hint_y: None
                height: '30dp'
                halign: 'left'
                text_size: self.size

            TextInput:
                id: item_title
                hint_text: 'Название товара'
                multiline: False
                size_hint_y: None
                height: '46dp'
                background_color: 0.18, 0.14, 0.15, 1
                foreground_color: 1, 1, 1, 1
                hint_text_color: 0.6, 0.6, 0.6, 1
                padding: [12, 12]

            TextInput:
                id: item_price
                hint_text: 'Цена'
                multiline: False
                input_filter: 'float'
                size_hint_y: None
                height: '46dp'
                background_color: 0.18, 0.14, 0.15, 1
                foreground_color: 1, 1, 1, 1
                hint_text_color: 0.6, 0.6, 0.6, 1
                padding: [12, 12]

            TextInput:
                id: item_phone
                hint_text: 'Номер телефона (+996...)'
                multiline: False
                size_hint_y: None
                height: '46dp'
                background_color: 0.18, 0.14, 0.15, 1
                foreground_color: 1, 1, 1, 1
                hint_text_color: 0.6, 0.6, 0.6, 1
                padding: [12, 12]

            TextInput:
                id: item_tg
                hint_text: 'Telegram (@username)'
                multiline: False
                size_hint_y: None
                height: '46dp'
                background_color: 0.18, 0.14, 0.15, 1
                foreground_color: 1, 1, 1, 1
                hint_text_color: 0.6, 0.6, 0.6, 1
                padding: [12, 12]

            TextInput:
                id: item_wa
                hint_text: 'WhatsApp (номер)'
                multiline: False
                size_hint_y: None
                height: '46dp'
                background_color: 0.18, 0.14, 0.15, 1
                foreground_color: 1, 1, 1, 1
                hint_text_color: 0.6, 0.6, 0.6, 1
                padding: [12, 12]

            Button:
                text: '📷 Выбрать фотографию'
                size_hint_y: None
                height: '46dp'
                background_normal: ''
                background_color: 0.35, 0.1, 0.12, 1
                color: 1, 1, 1, 1
                on_release: root.open_file_chooser()

            Image:
                id: preview_image
                size_hint_y: None
                height: '180dp'
                allow_stretch: True
                keep_ratio: True
                source: ''

            Button:
                text: 'ОПУБЛИКОВАТЬ'
                size_hint_y: None
                height: '52dp'
                bold: True
                background_normal: ''
                background_color: 0.75, 0.08, 0.12, 1
                color: 1, 1, 1, 1
                on_release: root.publish()
'''

class BeksflyRoot(BoxLayout):
    selected_image_path = ""

    def open_file_chooser(self):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        chooser = FileChooserIconView(path='/sdcard/DCIM' if os.path.exists('/sdcard/DCIM') else os.path.expanduser('~'), filters=['*.png', '*.jpg', '*.jpeg'])
        btn_box = BoxLayout(size_hint_y=None, height='44dp', spacing=10)
        
        popup = Popup(title="Выберите фото", content=content, size_hint=(0.95, 0.9))

        def select(instance):
            if chooser.selection:
                self.selected_image_path = chooser.selection[0]
                self.ids.preview_image.source = self.selected_image_path
                popup.dismiss()

        btn_select = Button(text="Выбрать", background_normal='', background_color=(0.7, 0.1, 0.1, 1), on_release=select)
        btn_cancel = Button(text="Отмена", background_normal='', background_color=(0.2, 0.2, 0.2, 1), on_release=popup.dismiss)
        
        btn_box.add_widget(btn_cancel)
        btn_box.add_widget(btn_select)
        content.add_widget(chooser)
        content.add_widget(btn_box)
        popup.open()

    def show_alert(self, title, msg):
        pop = Popup(
            title=title,
            content=Label(text=msg, halign='center'),
            size_hint=(0.8, 0.35)
        )
        pop.open()

    def publish(self):
        title = self.ids.item_title.text.strip()
        price = self.ids.item_price.text.strip()
        phone = self.ids.item_phone.text.strip()

        if not title or not price or not phone:
            self.show_alert("Ошибка", "Заполните обязательные поля:\nназвание, цену и телефон!")
            return

        self.show_alert("Успех!", f"Товар '{title}' за {price}\nуспешно опубликован в Beksfly!")
        self.ids.item_title.text = ""
        self.ids.item_price.text = ""
        self.ids.item_phone.text = ""
        self.ids.item_tg.text = ""
        self.ids.item_wa.text = ""
        self.ids.preview_image.source = ""

class BeksflyApp(App):
    def build(self):
        Builder.load_string(KV)
        return BeksflyRoot()

if __name__ == '__main__':
    BeksflyApp().run()
