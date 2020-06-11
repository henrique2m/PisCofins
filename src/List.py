import PySimpleGUI as view
import os
import Popup
import Global

class windowListCredit:
    def index(self, listSelect=[]):

        countList = len(listSelect)
       
        popup = Popup.Popup()

        if countList == 0:
            popup.alert('INFORME', 'NÃO FORAM ENCONTRADAS COMPETÊNCIAS .')
            return False
        
        col = [
            [view.Text('COMPETÊNCIAS: ', background_color='#6272a4')],
        ]

        for index in range(countList):
                competence = listSelect[index]

                if competence['update'] == []:
                    credit = competence['calculateBase']
                else:
                    credit = competence['credit']

                arrayDateTime =  competence['date'].split('.')
                
                dateTime = arrayDateTime[0]

                tax = 'pis' if competence['pis'] == True else 'cofins'

                cell = [view.Frame(competence['foreignKey'],
                    [
                        
                        [
                            view.Text('COMPETÊNCIA: ', background_color='#6272a4'),
                            view.Text(competence['competence'], background_color='#6272a4')
                        ],
                        [
                            view.Text('IMPOSTO: ', background_color='#6272a4', ),
                            view.Text('{}'.format(tax.upper()), background_color='#6272a4')
                        ],
                        [
                            view.Text('BASE DE CALCULO: ', background_color='#6272a4', ),
                            view.Text('R$ {:.2f}'.format(competence['calculateBase']),
                                         background_color='#6272a4'
                                    )
                        ],
                        [
                            view.Text('CRÉDITO: ', background_color='#6272a4'),
                            view.Text('R$ {:.2f}'.format(credit), background_color='#6272a4') 
                        ],
                        [
                            view.Text('DATA/HORA: ', background_color='#6272a4'),
                            view.Text('{}'.format(dateTime), background_color='#6272a4') 
                        ]
                    ], 
                    background_color='#6272a4'
                )]

                col.append(cell)
        
        layout = [
           [view.Column(col, 
                scrollable=True, 
                vertical_scroll_only=True,
                size=(350, 400)
            )]
        ]


        window = view.Window('CRÉDITOS',
                                layout, 
                                font='Courier 12',
                                icon=Global.ICON(),  
                                location=(138, 220),                              
                            )
        window.read()
        window.close()