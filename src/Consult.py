import os
import PySimpleGUI as view
import Popup
import List
import json
import Global

class WindowCreditConsult:
    def select(self, listCompany=[]):
            
            countList = len(listCompany)
        
            popup = Popup.Popup()

            if countList == 0:
                popup.alert('INFORME', 'NÃO EXISTE NENHUMA EMPRESA CADASTRADA.')
                return False

            file = Global.DATABASE()
            
            def index(name = '', tax= ''):
                with open(file, 'r') as json_file:
                    datas = json.load(json_file)

                count = len(datas)

                listSelect = []

                for index in range(count):
                    if 'competence' in datas[index]:
                        if datas[index]['competence']['foreignKey'] == name:
                            if tax == 'pis':
                                if datas[index]['competence']['pis'] == True:
                                    listSelect.append(datas[index]['competence'])
                            elif tax == 'cofins':
                                if datas[index]['competence']['cofins'] == True:
                                    listSelect.append(datas[index]['competence'])

                if listSelect == []:
                    return False
            
                return listSelect

            colOne = [
                [view.Text('EMPRESAS:', background_color='#6272a4')],
                [view.Listbox(
                        values=listCompany,  
                        size=(15,7),
                        key='company'
                )]
            ]                     
                          
            colTwo = [
                [view.Frame('IMPOSTO',
                    [
                        [
                            view.Radio('PIS', 'tax', key='pis', background_color='#6272a4'),
                            view.Radio('COFINS', 'tax', key='cofins', background_color='#6272a4')
                        ]
                    ], background_color='#6272a4'
                )],
                [view.Button('CONSULTAR', 
                                    key='submit',
                                    button_color=['#ffffff','#3CB371'],
                                    size=(17,1)
                                )
                ],
                [view.Button('CANCELAR', 
                                    key='cancel',
                                    button_color=['#ffffff','#ff5555'],
                                    size=(17,1)
                                )
                ] 

            ]

            layout = [
                        [
                            view.Column(colOne),
                            view.Column(colTwo, element_justification='center')
                        ]
                    ]


            window = view.Window('CONSULTAR CRÉDITO',
                                    layout,
                                    location=(830, 220),
                                    icon=Global.ICON()
                                )
            

            while True:

                event, values = window.read()

                if event in (view.WIN_CLOSED, 'cancel'):
                    break

                elif event == 'submit':
                    popup = Popup.Popup()

                    companySelect = '' if values['company'] == [] else values['company'][0]

                    if companySelect == '':
                        popup.alert('INFORME', 'POR FAVOR, SELECIONE UMA EMPRESA.')
                    elif not values['pis'] and not values['cofins']:
                        popup.alert('INFORME', 'POR FAVOR, SELECIONE UM IMPOSTO.')
                    else:
                        tax = 'pis' if values['pis'] == True else 'cofins'
                        
                        listCosultCompany = index(companySelect, tax)

                        if listCosultCompany:
                           list_ = List.windowListCredit()
                           list_.index(listCosultCompany)                          
                        else:
                            popup.alert('INFORME', 'NÃO EXISTE COMPETÊNCIA RELACIONADA A ESSE IMPOSTO.')

            window.close()
