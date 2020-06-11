import PySimpleGUI as view
import os
import Global

class Popup:
    def alert(self, title, message):

        layout = [
            [view.Text(message, key='message', background_color='#6272a4')],
            [view.Button('OK', button_color=['#ffffff','#282a36'])]
        ]
        
        window = view.Window(title, layout, icon=Global.ICON(), location=(830, 110))

        window.Read()
        
        window.close()
