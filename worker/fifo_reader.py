import os
import threading

FIFO_PATH = '/fifo/spotout'
BUFFER_SIZE = 4096

class PCMReader(threading.Thread):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self.running = True

    def run(self):
        if not os.path.exists(FIFO_PATH):
            os.mkfifo(FIFO_PATH)
        with open(FIFO_PATH, 'rb') as fifo:
            while self.running:
                data = fifo.read(BUFFER_SIZE)
                if data:
                    self.callback(data)

    def stop(self):
        self.running = False
