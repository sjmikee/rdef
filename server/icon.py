import threading
from pystray import MenuItem as item, Menu as menu, Icon as icon
import pystray
from PIL import Image

state = True
defend = True


class systrayIcon():
    def start_icon_thread(self):
        print('[*] Starting systray icon')
        icon_thread = threading.Thread(target=self.start_icon)
        icon_thread.start()

    def start_icon(self):
        global state
        global defend
        image = Image.open("resources\icon.png")
        self.icon = pystray.Icon(
            'RDEF', image, 'RDEF notifications', menu=menu(item('Notifications', self.on_clicked_notifications, checked=lambda item: state), item('Defend', self.on_clicked_defend, checked=lambda item: defend)))
        self.icon.run()

    def icon_notify(self, message):
        global state
        if state:
            self.icon.notify(message)

    def icon_remove_notification(self):
        self.icon.remove_notification()

    def on_clicked_notifications(self, icon, item):
        global state
        state = not item.checked
        print(state)

    def on_clicked_defend(self, icon, item):
        global defend
        defend = not item.checked
        print(defend)

    def defend_state(self):
        global defend
        return defend
