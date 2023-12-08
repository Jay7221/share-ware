
import os
import socket

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
from kivy.properties import StringProperty
from sender_utils import install_package_to_network, delete_package_to_network

PACKAGE_PATH = 'packages'
PACKAGES = os.listdir(PACKAGE_PATH)
SELECTED_PACKAGES = []


class AppContainer(BoxLayout):
    def show_settings_menu(self):
        # Create an instance of the SettingsMenu and display it
        settings_menu = SettingsMenu()
        settings_menu.open()


class SettingsMenu(Popup):
    def __init__(self, **kwargs):
        super(SettingsMenu, self).__init__(**kwargs)

        # Create a GridLayout for the menu content
        layout = GridLayout(cols=1, spacing=10)

        # Add options to the menu
        network_address_label = Label(
            text=f"Network Address: {App.get_running_app().network_address}")
        ip_address_label = Label(
            text=f"IP Address: {App.get_running_app().ip_address}")
        network_address_input = TextInput(
            hint_text='Network Address', text=App.get_running_app().network_address)
        ip_address_input = TextInput(
            hint_text='IP Address', text=App.get_running_app().ip_address)

        # Bind the TextInput widgets to the actual attributes
        network_address_input.bind(text=self.on_network_address_change)
        ip_address_input.bind(text=self.on_ip_address_change)

        # Other widgets remain unchanged
        send_toggle_button = ToggleButton(text='Send to Network', group='send_option', state='down' if App.get_running_app(
        ).send_to_network else 'normal', on_press=self.on_toggle_press)

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


BUTTON_COLOR = (1, 0, 0, 1)
SELECTED_BUTTON_COLOR = (0, 1, 0, 1)


class ScrollApp(ScrollView):
    def __init__(self, **kwargs):
        super(ScrollApp, self).__init__(**kwargs)

        self.clicked_buttons = []  # List to store names of clicked buttons

        layout = StackLayout(spacing=10, size_hint_y=None)

        for package in PACKAGES:
            btn = Button(text=package,
                         size_hint=(.2, 1), on_press=self.on_button_click, background_color=BUTTON_COLOR)
            layout.add_widget(btn)

        self.add_widget(layout)

    def on_button_click(self, instance):
        # Toggle button color and update the list of clicked buttons
        global SELECTED_PACKAGES
        if instance.text not in SELECTED_PACKAGES:
            instance.background_color = SELECTED_BUTTON_COLOR
            # Change color to blue
            SELECTED_PACKAGES.append(instance.text)
        else:
            # Change color back to default
            instance.background_color = BUTTON_COLOR
            SELECTED_PACKAGES.remove(instance.text)


class ControlPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        send_button = Button(text="Send", on_press=self.send_packages)
        receive_button = Button(text="Receive", on_press=self.receive_packages)
        delete_button = Button(text="Delete", on_press=self.delete_package)
        self.add_widget(send_button)
        self.add_widget(receive_button)
        self.add_widget(delete_button)

    def send_packages(self, instance):
        print(f"Sending Packages: {SELECTED_PACKAGES}")
        network_address = App.get_running_app().network_address
        for package in SELECTED_PACKAGES:
            try:
                install_package_to_network(package, network_address)
            except Exception as e:
                print(e)

    def delete_package(self, instance):
        print(f"Deleting Packages: {SELECTED_PACKAGES}")
        network_address = App.get_running_app().network_address
        for package in SELECTED_PACKAGES:
            try:
                delete_package_to_network(package, network_address)
            except Exception as e:
                print(e)

    def receive_packages(self, instance):
        print("Receiving packages")


class MyApp(App):
    network_address = StringProperty(socket.gethostbyname(socket.gethostname()))
    ip_address = StringProperty("default Ip Address")
    send_to_network = False

    def build(self):
        return AppContainer()


if __name__ == '__main__':
    MyApp().run()
