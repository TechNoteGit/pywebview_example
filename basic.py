"""
  pywebview example
"""
import os
import webview
import pystray
import conn
from pystray import MenuItem
from pystray import Menu
from multiprocessing import Process, Pipe
from PIL import Image


def webview_subprocess(conn_parent, conn_child):
  window = webview.create_window('TechNote', 'https://technote.kr')
  window.closing += on_closing
  conn.parent = conn_parent
  conn.child = conn_child
  webview.start(cmd_recv, [], gui='cef', debug=True)


def on_closing():
  send_cmd_to_window('hide')
  return False
# https://github.com/r0x0r/pywebview/issues/573


def cmd_recv():
  while True:
    cmd = conn.child.recv()
    if cmd == 'show':
      print('Show - pywebview')
      webview.windows[0].show()
    elif cmd == 'hide':
      print('Hide - pywebview')
      webview.windows[0].hide()


def send_cmd_to_window(cmd):
  conn.parent.send(cmd)


def quit_window(process_handler):
  icon.stop()
  process_handler.terminate()


if __name__ == '__main__':
  conn.parent, conn.child = Pipe()

  subprocess_handler = Process(
    target=webview_subprocess, args=(conn.parent, conn.child))
  subprocess_handler.start()

  # Using window tray
  base_path = os.path.dirname(os.path.abspath(__file__))
  image_path = Image.open(base_path + '/res/tray_icon.png')
  menu = Menu(MenuItem('Hide', lambda: send_cmd_to_window('hide')),
              MenuItem('Show', lambda: send_cmd_to_window('show')),
              MenuItem('Quit', lambda: quit_window(subprocess_handler)))
  icon = pystray.Icon('pyWebView_Sample', image_path, 'pyWebView', menu)
  icon.run()

  subprocess_handler.join()
