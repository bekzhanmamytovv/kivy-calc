import os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty, StringProperty, ListProperty
from kivy.clock import Clock
from kivy.core.window import Window

Window.clearcolor = (0.05, 0.03, 0.03, 1)

KV = '''
#:import hex kivy.utils.get_color_from_hex

<MainScreen>:
    orientation: 'vertical'
    padding: ['18dp', '18dp', '18dp', '10dp']
    spacing: '14dp'

    # Верхний заголовок
    BoxLayout:
        size_hint_y: None
        height: '40dp'
        orientation: 'vertical'
        Label:
            text: 'Beksfly Notes'
            font_size: '22sp'
            bold: True
            color: 0.95, 0.95, 0.95, 1
            halign: 'center'
            valign: 'middle'
            text_size: self.size

    # Индикатор статуса
    BoxLayout:
        size_hint_y: None
        height: '16dp'
        AnchorLayout:
            Widget:
                size_hint: None, None
                size: '8dp', '8dp'
                canvas:
                    Color:
                        rgba: (0.9, 0.1, 0.15, 1) if root.is_recording else (0.4, 0.35, 0.35, 1)
                    Ellipse:
                        pos: self.pos
                        size: self.size

    # Центральная карточка (Таймер + Волна + Кнопка)
    BoxLayout:
        orientation: 'vertical'
        size_hint_y: 0.52
        padding: ['20dp', '20dp', '20dp', '24dp']
        spacing: '12dp'
        canvas.before:
            Color:
                rgba: 0.11, 0.08, 0.08, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [26]

        Label:
            text: root.timer_text
            font_size: '48sp'
            bold: True
            color: (1, 0.95, 0.95, 1)
            size_hint_y: None
            height: '60dp'

        # Аудиоволна (эквалайзер)
        BoxLayout:
            size_hint_y: None
            height: '40dp'
            spacing: '4dp'
            padding: ['30dp', '0dp']
            canvas.before:
                Color:
                    rgba: (0.8, 0.2, 0.25, 0.8) if root.is_recording else (0.4, 0.3, 0.32, 0.5)
                # Полосы волны
                Rectangle:
                    pos: self.x + self.width * 0.10, self.center_y - 6
                    size: 3, 12
                Rectangle:
                    pos: self.x + self.width * 0.20, self.center_y - 14
                    size: 3, 28
                Rectangle:
                    pos: self.x + self.width * 0.30, self.center_y - 8
                    size: 3, 16
                Rectangle:
                    pos: self.x + self.width * 0.40, self.center_y - 18
                    size: 3, 36
                Rectangle:
                    pos: self.x + self.width * 0.50, self.center_y - 12
                    size: 3, 24
                Rectangle:
                    pos: self.x + self.width * 0.60, self.center_y - 19
                    size: 3, 38
                Rectangle:
                    pos: self.x + self.width * 0.70, self.center_y - 10
                    size: 3, 20
                Rectangle:
                    pos: self.x + self.width * 0.80, self.center_y - 15
                    size: 3, 30
                Rectangle:
                    pos: self.x + self.width * 0.90, self.center_y - 5
                    size: 3, 10

        # Кнопка Записи с неоновым свечением
        AnchorLayout:
            Button:
                size_hint: None, None
                size: '96dp', '96dp'
                background_normal: ''
                background_color: 0, 0, 0, 0
                on_release: root.toggle_recording()
                canvas.before:
                    # Внешнее свечение
                    Color:
                        rgba: (0.7, 0.05, 0.1, 0.35) if root.is_recording else (0.35, 0.05, 0.08, 0.2)
                    Ellipse:
                        pos: self.x - 8, self.y - 8
                        size: self.width + 16, self.height + 16
                    # Тонкое контурное кольцо
                    Color:
                        rgba: (0.95, 0.2, 0.25, 0.9) if root.is_recording else (0.5, 0.15, 0.18, 0.6)
                    Line:
                        circle: (self.center_x, self.center_y, 44)
                        width: 1.5
                    # Внутренний круг
                    Color:
                        rgba: (0.8, 0.08, 0.12, 1) if root.is_recording else (0.45, 0.05, 0.08, 1)
                    Ellipse:
                        pos: self.x + 8, self.y + 8
                        size: self.width - 16, self.height - 16
                    # Иконка Квадрат / Круг
                    Color:
                        rgba: 1, 1, 1, 1
                    RoundedRectangle:
                        pos: (self.center_x - 10, self.center_y - 10) if root.is_recording else (self.center_x - 7, self.center_y - 7)
                        size: (20, 20) if root.is_recording else (14, 14)
                        radius: [4] if root.is_recording else [7]

    # Кнопка экспорта в Gemini
    Button:
        text: 'Share to Gemini for Notes'
        size_hint_y: None
        height: '46dp'
        background_normal: ''
        background_color: 0.18, 0.13, 0.14, 1
        color: 0.9, 0.88, 0.88, 1
        font_size: '14sp'
        canvas.before:
            Color:
                rgba: 0.3, 0.2, 0.22, 0.6
            Line:
                rounded_rectangle: [self.x, self.y, self.width, self.height, 14]
                width: 1

    # Список последних лекций
    BoxLayout:
        orientation: 'vertical'
        padding: ['14dp', '10dp']
        spacing: '8dp'
        canvas.before:
            Color:
                rgba: 0.09, 0.06, 0.07, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [20]

        # Элемент 1
        BoxLayout:
            size_hint_y: None
            height: '42dp'
            Label:
                text: '▶'
                size_hint_x: None
                width: '26dp'
                color: 0.8, 0.2, 0.25, 1
            BoxLayout:
                orientation: 'vertical'
                Label:
                    text: 'Introduction to AI'
                    font_size: '14sp'
                    bold: True
                    halign: 'left'
                    valign: 'middle'
                    text_size: self.size
                    color: 0.9, 0.9, 0.9, 1
                Label:
                    text: 'Lecture audio'
                    font_size: '11sp'
                    halign: 'left'
                    valign: 'middle'
                    text_size: self.size
                    color: 0.5, 0.45, 0.45, 1
            Label:
                text: '•••'
                size_hint_x: None
                width: '30dp'
                color: 0.5, 0.45, 0.45, 1

        # Элемент 2
        BoxLayout:
            size_hint_y: None
            height: '42dp'
            Label:
                text: 'ıll'
                size_hint_x: None
                width: '26dp'
                color: 0.8, 0.2, 0.25, 1
            BoxLayout:
                orientation: 'vertical'
                Label:
                    text: 'Quantum Mechanics 101'
                    font_size: '14sp'
                    bold: True
                    halign: 'left'
                    valign: 'middle'
                    text_size: self.size
                    color: 0.9, 0.9, 0.9, 1
                Label:
                    text: 'Recent audio'
                    font_size: '11sp'
                    halign: 'left'
                    valign: 'middle'
                    text_size: self.size
                    color: 0.5, 0.45, 0.45, 1
            Label:
                text: '•••'
                size_hint_x: None
                width: '30dp'
                color: 0.5, 0.45, 0.45, 1
'''

class MainScreen(BoxLayout):
    is_recording = BooleanProperty(False)
    timer_text = StringProperty("00:42:15")
    seconds = 2535

    def toggle_recording(self):
        self.is_recording = not self.is_recording
        if self.is_recording:
            self.seconds = 0
            self.timer_text = "00:00:00"
            self.event = Clock.schedule_interval(self.tick, 1)
        else:
            if hasattr(self, 'event'):
                self.event.cancel()

    def tick(self, dt):
        self.seconds += 1
        m, s = divmod(self.seconds, 60)
        h, m = divmod(m, 60)
        self.timer_text = f"{h:02d}:{m:02d}:{s:02d}"

class BeksflyNotesApp(App):
    def build(self):
        Builder.load_string(KV)
        return MainScreen()

if __name__ == '__main__':
    BeksflyNotesApp().run()
