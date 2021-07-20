import sys
if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
else:
    import PySimpleGUI27 as sg
import time

sg.ChangeLookAndFeel('DarkTeal')
sg.SetOptions(element_padding=(0, 0))


class Timer:
    def __init__(self):

        self.layout = [[sg.Text('')],
                 [sg.Text('', size=(8, 2), font=('Helvetica', 20), justification='center', key='text')],
                 [sg.Button('Pause', key='button', button_color=('white', '#001480')),
                  sg.Button('Reset', button_color=('white', '#007339'), key='Reset'),
                  sg.Exit(button_color=('white', 'firebrick4'), key='Exit')]]

        self.window = sg.Window('Running Timer', self.layout, no_titlebar=True, auto_size_buttons=False, keep_on_top=True, grab_anywhere=True)

    def close(self):
        self.window.close()
        return

    def main_loop(self):
        current_time = 0
        paused = False
        start_time = int(round(time.time() * 100))
        while True:
            # --------- Read and update window --------
            if not paused:
                event, values = self.window.read(timeout=10)
                current_time = int(round(time.time() * 100)) - start_time
            else:
                event, values = self.window.read()
            if event == 'button':
                event = self.window[event].GetText()
            # --------- Do Button Operations --------
            if event == sg.WIN_CLOSED or event == 'Exit':  # ALWAYS give a way out of program
                self.window.close()
                return current_time
            if event == 'Reset':
                start_time = int(round(time.time() * 100))
                current_time = 0
                paused_time = start_time
            elif event == 'Pause':
                paused = True
                paused_time = int(round(time.time() * 100))
                element = self.window['button']
                element.update(text='Run')
            elif event == 'Run':
                paused = False
                start_time = start_time + int(round(time.time() * 100)) - paused_time
                element = self.window['button']
                element.update(text='Pause')

            # --------- Display timer in window --------
            self.window['text'].update('   {:02d}:{:02d}.{:02d}'.format((current_time // 100) // 60,
                                                                          (current_time // 100) % 60,
                                                                          current_time % 100))


def __call__():
    return Timer()