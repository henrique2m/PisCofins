import PySimpleGUI as view
import datetime
import json
import os
import Popup
import Chews
import Global

class WindowRegisterCompetence:
    def Start(self, listCompany=[]):



        countList = len(listCompany)
       
        popup = Popup.Popup()

        if countList == 0:
            popup.alert('INFORME', 'NÃO EXISTE NENHUMA EMPRESA CADASTRADA.')
            return False

        file = Global.DATABASE()

        colTwo = [
            [view.Frame('COMPETÊNCIA:',
                [
                    [view.Input(key='competence')]
                ], background_color='#6272a4'
            )],
            [view.Frame('BASE DE CALCULO:',
                [
                  [view.Input(key="calculateBase")] 
                ], background_color='#6272a4'
            )],
            [view.Frame('IMPOSTO:',
                [
                    [
                        view.Radio('PIS', 'tax', key='pis', background_color='#6272a4'),
                        view.Radio('COFINS', 'tax', key='cofins', background_color='#6272a4')
                    ]
                ], background_color='#6272a4'
            )]
        ]
        
        
        layout = [
            [view.Text('EMPRESAS', background_color='#6272a4')],
            [
                view.Listbox(
                    values=listCompany,size=(20, 9), 
                    key='listCompany',
                    ),
                view.Column(colTwo)
            ],
            [
                view.Button('ADICIONAR',
                     key='submit', 
                     button_color=['#ffffff','#3CB371']
                ), 
                view.Button('CANCELAR', 
                    key='cancel', 
                    button_color=['#ffffff','#ff5555']
                )
            ] 
           
        ]

        window = view.Window('ADICIONAR COMPETÊNCIA', 
                                layout, 
                                icon=Global.ICON(),
                                location=(830, 220),
                                size=(400, 240)
                            )

        while True:
            event, values = window.Read()

            if event in (view.WIN_CLOSED, 'cancel'):
                break
            elif event == 'submit':
                
                countListSelect = len(values['listCompany'])
                listSelect = '' if countListSelect == 0  else values['listCompany'][0]

                competence = values['competence']
                pis = values['pis']
                cofins = values['cofins']
                calculateBase = values['calculateBase']

                def isFloat(number):
                    try:
                        float(number)
                        return True
                    except:
                        return False
                
                chews = Chews.Chews()

                if listSelect == '':
                    popup.alert('INFORME', 'POR FAVOR, ESCOLHA UMA EMPRESA.')

                elif competence == '':
                    popup.alert('INFORME', 'POR FAVOR, INFORME UMA COMPETÊNCIA.')

                elif not chews.isMonthYear(competence):
                    popup.alert('INFORME', 'POR FAVOR, INFORME UM FORMATO DE COMPÊNCIA VALIDO(00-0000).')

                elif not isFloat(calculateBase):
                    popup.alert('INFORME', 'POR FAVOR, INFORME UM VALOR CONTÁBEL.')

                elif pis == False and cofins == False:
                    popup.alert('INFORME', 'POR FAVOR, SELECIONE UM IMPOSTO.')

                elif calculateBase == '':
                    popup.alert('INFORME', 'POR FAVOR, INFORME UM UMA BASE DE CALCULO.')

                else:

                    with open(file, 'r') as json_file:
                        dados = json.load(json_file)

                    count = len(dados)
                                   
                    competenceData = dados

                    status = True

                    for index in range(count):
                        if 'competence' in competenceData[index]:
                            competenceIndex = competenceData[index]['competence']

                            if competenceIndex['competence'] == competence:
                                if competenceIndex['foreignKey'] == listSelect:
                                        if competenceIndex['pis'] == True and pis:
                                            popup.alert('INFORME', 'A COMPETÊNCIA JÁ EXISTE.')
                                            status = False

                                        if status :
                                            if competenceIndex['cofins'] and cofins:
                                                popup.alert('INFORME', 'A COMPETÊNCIA JÁ EXISTE.')
                                                status = False
                               
                    
                    if status :
                        competenceNew = {
                            "competence": {
                                'foreignKey': listSelect,
                                'competence': competence,
                                'pis': pis,
                                'cofins': cofins,
                                'calculateBase': round(float(calculateBase), 2),
                                'credit': 0,
                                'update': [],
                                'date': '{}'.format(datetime.datetime.now())
                            } 
                        }

                        dados.append(competenceNew)

                        with open(file, 'w') as json_file:
                            json.dump(dados, json_file, indent=4)
                        
                        popup.alert('INFORME', 'COMPETÊNCIA ADICIONADA COM SUCESSO.')
                        break
                    else:
                        status = True

        window.close()

                   