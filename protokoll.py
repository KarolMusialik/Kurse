
class Protokoll:
    def __init__(self, f):
        self.file_protokoll = f

    def SchreibeInProtokoll(self, text):
        text = text + "\n"
        f = open(self.file_protokoll, "a")
        f.write(text)
        f.close()