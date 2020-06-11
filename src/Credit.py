import json
import os
import Popup
import datetime
import Global
import PySimpleGUI as view

class WindowCredit:
    def calculate(self, listCompany=[]):

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

            listCompetence = []

            for index in range(count):
                if 'competence' in datas[index]:
                    if datas[index]['competence']['foreignKey'] == name:
                        if tax == 'pis':
                             if datas[index]['competence']['pis'] == True:
                                listCompetence.append(datas[index]['competence']['competence'])
                        elif tax == 'cofins':
                             if datas[index]['competence']['cofins'] == True:
                                listCompetence.append(datas[index]['competence']['competence'])

            if listCompetence == []:
                return False
            
            return listCompetence

        def update(name ='', competenceSelect='', tax = '', valueUsed =''):
            with open(file, 'r') as json_file:
                datas = json.load(json_file)

            count = len(datas)

            datasUp = {
                'valueUsed': round(float(valueUsed), 2),
                'date': '{}'.format(datetime.datetime.now()),
            }

            for index in range(count):
                if 'competence' in datas[index]:
                    competence = datas[index]['competence']
                   
                    if competence['foreignKey'] == name :
                        if competence['competence'] == competenceSelect:
                            
                            valueUsed = float(valueUsed)
                            calculateBase = float(competence['calculateBase'])
                            credit = float(competence['credit'])
                    
                            if competence['update'] == []:
                                if valueUsed > calculateBase:
                                    popup.alert('ERRO', 'O VALOR USUADO É MAIOR QUE O CRÉDITO DISPONÍVEL.')
                                    return False
                            else:
                                if valueUsed > credit:
                                    popup.alert('ERRO', 'O VALOR USUADO É MAIOR QUE O CRÉDITO DISPONÍVEL.')
                                    return False


                            if tax == 'pis':
                                if  competence['pis'] == True:
                                    if competence['credit'] == 0:
                                        competence['credit'] = round(calculateBase - valueUsed, 2)

                                    else:
                                        competence['credit'] = round(credit - valueUsed, 2)
                                   
                            elif tax == 'cofins':
                                if  competence['cofins'] == True:
                                    if competence['credit'] == 0:
                                        competence['credit'] = round(calculateBase - valueUsed, 2)
                                        
                                    else:
                                        competence['credit'] = round(credit - valueUsed, 2)

                            competence['update'].append(datasUp)
                            datas[index] = { "competence": competence }

                            with open(file, 'w') as json_file:
                                json.dump(datas, json_file, indent=4)
                            
                            message = 'O VALOR DE CRÉDITO RESTANTE É DE: R$ {:.2f}'.format(competence['credit'])
                            popup.alert('INFORME', message)
                            return True

            popup.alert('ERRO', 'COMPETÊNCIA NÃO ENCONTRADA.')
            return False
                      
                            
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
            [view.Frame('VALOR USADO',
                [
                  [view.Input(size=(18, 1), key='calculate')]  
                ], background_color='#6272a4'
            )],
            [
                view.Button('LISTAR', 
                    size=(17, 1),
                    key='list',
                    button_color=['#ffffff','#282a36']
                )
            ]
        ]
        
        colThree = [
            [view.Text('COMPETÊNCIAS:', background_color='#6272a4')],
            [view.Listbox(values=[], size=(15,7), key='competence')]
        ]      

        layout = [
            [   
                view.Column(colOne),
                view.Column(colTwo, element_justification='center'),
                view.Column(colThree)
            ],            
            [
                view.Button('ATUALIZAR',
                    key="submit", 
                    button_color=['#ffffff','#3CB371']
                ), 
                view.Button('CANCELAR',
                    key="cancel",
                    button_color=['#ffffff','#ff5555']
                )
            ]
        ]  

        window = view.Window('ATUALIZAÇÃO DE CRÉDITOS',
                                layout,
                                icon=Global.ICON(),
                                location=(830, 220),
                            )

        while True:
            
            event, values = window.Read()
             
            if event in (view.WIN_CLOSED, 'cancel'):
                    break

            if event == 'list' or event == 'submit':

                companySelect = '' if values['company'] == [] else values['company'][0]

                if companySelect == '':
                    popup.alert('INFORME', 'POR FAVOR, SELECIONE UMA EMPRESA.')

                elif not values['pis'] and not values['cofins']:
                    popup.alert('INFORME', 'POR FAVOR, SELECIONE UM IMPOSTO.')

                elif event == 'list':
                    tax = 'pis' if values['pis'] == True else 'cofins'

                    listCompetence = index(companySelect, tax)

                    if listCompetence:
                        window['competence'].update(listCompetence)
                    else:
                        popup.alert('INFORME', 'NÃO EXISTE COMPETÊNCIA RELACIONADA A ESSE IMPOSTO.')

                elif event == 'submit':
                    if values['competence'] == []:
                         popup.alert('INFORME', 'POR FAVOR, SELECIONE UMA COMPETÊNCIA.')
                    elif values['calculate'] == '' or values['calculate'] == None:
                         popup.alert('INFORME', 'POR FAVOR, INFORME UM VALOR A SER DESCONTADO.')
                    else:
                        name = values['company'][0]
                        competence = values['competence'][0]
                        discount = values['calculate']
                        tax = 'pis' if values['pis'] == True else 'cofins'

                        try:
                            float(discount)
                            update(name, competence, tax, discount)
                            window['calculate'].update('')
                        except:
                            popup.alert('ERRO', 'POR FAVOR, INFORME UM VALOR CONTÁBEL.')
            else:
                break

        window.close()