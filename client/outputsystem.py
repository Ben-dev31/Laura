
import pyttsx3

class OutputSystem:
    def __init__(self, outtype = 'default', lang='fr'):
        self.outputs = []
        self.outtype = outtype # 'default', 'console', 'graphic', 'file'
        if self.outtype == 'default':
            self.engine = pyttsx3.init()
            self.engine.setProperty('voice', lang)
            self.engine.setProperty('rate', 130)
    def out(self, text):
        if self.outtype == 'default':
            self.engine.say(text)
            self.engine.runAndWait()
        elif self.outtype == 'console':
            print(text)
        elif self.outtype == 'graphic':
            # Placeholder for graphical output implementation
            pass
        elif self.outtype == 'file':
            with open('output.txt', 'a') as f:
                f.write(text + '\n')
        self.outputs.append(text)

    def get_outputs(self):
        return self.outputs
    def clear_outputs(self):
        self.outputs = []
    def set_outtype(self, outtype):
        self.outtype = outtype
        if self.outtype == 'default':
            self.engine = pyttsx3.init()

    def get_outtype(self):
        return self.outtype
    def reset(self):
        self.clear_outputs()
        if self.outtype == 'default':
            self.engine = pyttsx3.init()
            self.engine.setProperty('voice', 'fr')
    def shutdown(self):
        if self.outtype == 'default':
            self.engine.stop()

if __name__ == "__main__":
    output_system = OutputSystem()
    output_system.out("Ce message sera lu à haute voix.")
    #output_system.shutdown()