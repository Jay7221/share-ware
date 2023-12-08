from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

class AppContainer(BoxLayout):
    def show_settings_menu(self):
        # Create an instance of the SettingsMenu and display it
        settings_menu = SettingsMenu()
        settings_menu.open()


class SettingsMenu(Popup):
    def __init__(self, **kwargs):
        super(SettingsMenu, self).__init__(**kwargs)

        # Create a GridLayout for the menu content
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)

        # Add options to the menu
        network_address_label = Label(text=f"Network Address: {App.get_running_app().network_address}")
        ip_address_label = Label(text=f"IP Address: {App.get_running_app().ip_address}")
        network_address_input = TextInput(hint_text='Network Address', text=App.get_running_app().network_address)
        ip_address_input = TextInput(hint_text='IP Address', text=App.get_running_app().ip_address)

        # Bind the TextInput widgets to the actual attributes
        network_address_input.bind(text=self.on_network_address_change)
        ip_address_input.bind(text=self.on_ip_address_change)

        # Other widgets remain unchanged
        send_toggle_button = ToggleButton(text='Send to Network', group='send_option', state='down' if App.get_running_app().send_to_network else 'normal', on_press=self.on_toggle_press)

        layout.add_widget(network_address_label)
        layout.add_widget(network_address_input)
        layout.add_widget(ip_address_label)
        layout.add_widget(ip_address_input)
        layout.add_widget(send_toggle_button)

        self.content = layout

    def on_toggle_press(self, instance):
        app = App.get_running_app()
        app.send_to_network = instance.state == 'down'
        instance.text = 'Send to Network' if app.send_to_network else 'Send to IP'

    def on_network_address_change(self, instance, value):
        App.get_running_app().network_address = value

    def on_ip_address_change(self, instance, value):
        App.get_running_app().ip_address = value


class ScrollApp(ScrollView):
    def __init__(self, **kwargs):
        super(ScrollApp, self).__init__(**kwargs)

        self.clicked_buttons = []  # List to store names of clicked buttons

        layout = StackLayout(spacing=10, size_hint_y=None)

        for i in range(20):
            btn = Button(text=f"App {i + 1}", size=(100, 100), size_hint=(None, None), on_press=self.on_button_click)
            layout.add_widget(btn)

        self.add_widget(layout)

    def on_button_click(self, instance):
        # Toggle button color and update the list of clicked buttons
        if instance.text not in self.clicked_buttons:
            instance.background_color = (0.2, 0.6, 1, 1)  # Change color to blue
            self.clicked_buttons.append(instance.text)
        else:
            instance.background_color = (1, 1, 1, 1)  # Change color back to default
            self.clicked_buttons.remove(instance.text)

        # Print the list of clicked buttons
        print("Clicked Buttons:", self.clicked_buttons)


class MyApp(App):
    network_address = "Default Network Address"
    ip_address = "Default IP Address"
    send_to_network = False

    def build(self):
        return AppContainer()


if __name__ == '__main__':
    MyApp().run()
