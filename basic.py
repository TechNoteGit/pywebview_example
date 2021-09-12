import os
import webview
import pystray
import time
import multiprocessing
from pystray import MenuItem
from pystray import Menu
from multiprocessing import Process, Pipe
from PIL import Image


def webview_subprocess(child_pipe):
    window = webview.create_window('TechNote', 'https://technote.kr')
    webview.start(cmd_recv, [child_pipe], gui='cef', debug=True)


def cmd_recv(child_pipe):
    while True:
        cmd = child_pipe.recv()
        if cmd == 'show':
            webview.windows[0].show()
        elif cmd == 'hide':
            webview.windows[0].hide()


def send_cmd_to_window(parent_pipe, cmd):
    parent_pipe.send(cmd)


def quit_window(subprocess_handler):
    icon.stop()
    subprocess_handler.terminate()


if __name__ == '__main__':
    parent_pipe, child_pipe = Pipe()

    subprocess_handler = Process(target=webview_subprocess, args=(child_pipe,))
    subprocess_handler.start()

    # Using window tray
    base_path = os.path.dirname(os.path.abspath(__file__))
    image_path = Image.open(base_path + '/res/tray_icon.png')
    menu = Menu(MenuItem('Hide', lambda: send_cmd_to_window(parent_pipe, 'hide')),
                MenuItem('Show', lambda: send_cmd_to_window(parent_pipe, 'show')),
                MenuItem('Quit', lambda: quit_window(subprocess_handler)))
    icon = pystray.Icon('pyWebView_Sample', image_path, 'pyWebView', menu)
    icon.run()

    subprocess_handler.join()
