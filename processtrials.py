import xlrd
import random
import kivy
from ArAdjust import Reverser, Reshaper, isArabic

class ArInput(TextInput):
    # A custom bidi widget
    # TODO: move cursor to the correct position
    def __init__(s, **kwargs):
        super(ArInput, s).__init__(**kwargs)
        s.text = ''         # the visible label on the input widgets
        s.str = ''          # the underlying string on the widget

    def insert_text(s, substring, from_undo=False):
        # adds typed character to end of underlying string. Formats it
        s.str = s.str + substring
        s.format()

    def do_backspace(s, from_undo=False, mode='bkspc'):
        # removes rightmost character to underlying string. Formats it.
        s.str = s.str[:len(s.str) - 1]
        s.format()

    def format(s):
        # adjusts string output for language
        if any(isArabic(f) for f in s.text):
            s.text = Reshaper(Reverser(s.str))
        else:
            s.text = s.str

class OS(Screen):
    # The open file screen
    def __init__(s, *args, **kwargs):
        super(OS, s).__init__(*args, **kwargs)

    # passes file path to and changes to trials screen
    def _success(s, selection):
        s.manager.screens[1].loadfile(selection[0])
        s.manager.current = 'Trials'

    # clears text Input
    # TODO: do this.
    def _cancel(s):
        pass


class TS(Screen):
    # trials screen: where the user will see a flashcard item, enter a guess,
    # learn result, see correct answer and other information
    def __init__(s, *args, **kwargs):
        super(TS, s).__init__(*args, **kwargs)
        s.trials = []       # Input List of rows, nested with cell data
        s.headings = []     # Pull the first row to separate
        s.BA = False        # If user is testing from Language in col B
        s.word = 0          # Index of the row from trials list
        s.token = 0         # Index of the token string in the row
        s.goal = 1          # Index of the goal string in the row

    def loadfile(s, filename="static/Test.xlsx"):
        # load file and run ArAdjust on cells that contain arabic characters
        s.trials = [[Reshaper(Reverser(c.value)) if any(isArabic(y) for y in c.value) else str(c.value) for c in row] for row in
                    xlrd.open_workbook(filename).sheet_by_index(0).get_rows() if row]
        # load first row into headings
        s.headings = s.trials.pop(0)
        for head in s.headings:
            s.ids.Heads.add_widget(Label(text=head, font_name='times', font_size=2 * int(s.ids.Heads.height/len(s.headings))))
        random.seed()
        random.shuffle(s.trials)
        s.word = 0
        s.token = 0
        s.goal = 1
        s.loadword()

    def loadword(s):
        if s.BA:
            s.token = 1
            s.goal = 0
        s.ids.Tok.text = s.trials[s.word][s.token]

    def result(s):
        if s.ids.Resp.text.lower() == s.trials[s.word][s.goal].lower():
            s.ids.Success.text = 'RIGHT!'
            s.ids.Success.color = (165, 50, 135, 1)
        else:
            s.ids.Success.text = 'WRONG!'
            s.ids.Success.color = (50, 165, 135, 1)

    def next(s):
        s.result()
        s.ids.Deets.clear_widgets()
        for data in s.trials[s.word]:
            s.ids.Deets.add_widget(Label(text=data,
                                         font_name='times',
                                         font_size=1.5 * int(s.ids.Heads.height/len(s.headings))
                                         )
                                   )
        s.word += 1
        s.ids.Resp.str = s.ids.Resp.text = ''
        s.loadword()


class SS(Screen):
    def __init__(s, *args, **kwargs):
        super(SS, s).__init__(*args, **kwargs)

    def on_pre_enter(s):
        s.TScr = s.manager.screens[1]
        s.ids.AB_Lab.text = f'{s.TScr.headings[0]} to {s.TScr.headings[1]}'
        s.ids.BA_Lab.text = f'{s.TScr.headings[1]} to {s.TScr.headings[0]}'

    def setTrue(s):
        s.TScr.BA = True
        s.TScr.loadword()

    def setFalse(s):
        s.TScr.BA = False
        s.TScr.loadword()
