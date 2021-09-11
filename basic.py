import webview
from multiprocessing import Process, Pipe


def webview_subprocess(child_pipe):
    window = webview.create_window('TechNote', 'https://technote.kr')
    webview.start(cmd_recv, [window, child_pipe], gui='cef', debug=True)


def cmd_recv(window, child_pipe):
    while True:
        cmd = child_pipe.recv()
        # To Do - cmd handler


if __name__ == '__main__':
    parent_pipe, child_pipe = Pipe()

    subprocess_handler = Process(target=webview_subprocess, args=(child_pipe,))
    subprocess_handler.start()
    subprocess_handler.join()
