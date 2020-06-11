import sys
import json
import os
import PySimpleGUI as view
import datetime
import bradocs4py as validate
import Popup
import Global

class WindowRegisterCompany:
    def Start(self):

        layout = [
                
                    [
                        view.Text('CNPJ', background_color="#6272a4"),
                        view.Input(key='cnpj')
                    ],
                    [
                        view.Text('RAZÃO SOCIAL', background_color="#6272a4"),
                        view.Input(key='name')
                    ],
                    [
                        view.Button('CADASTRAR', 
                                        key='submit',
                                        button_color=['#ffffff','#3CB371']
                                    ),
                        view.Button('CANCELAR', 
                                        key='cancel',
                                        button_color=['#ffffff','#ff5555']
                                    )
                    ] 
                 ]


        window = view.Window('CADASTRAR EMPRESA',
                                 layout,
                                 location=(830, 220),
                                 icon=Global.ICON(),
                                 size=(300, 100)
                            )
        

        file = Global.DATABASE()
       

        while True:

            event, values = window.read()

            with open(file, 'r') as json_file:
                dados = json.load(json_file)

            count = len(dados)
            company = values

            if event in (view.WIN_CLOSED, 'cancel'):
                break

            elif event == 'submit':
                popup = Popup.Popup()

                if not validate.validar_cnpj(company['cnpj']):
                    popup.alert('ERRO', 'O CNPJ NÃO É VALIDO.')
                    
                elif company['cnpj'] == '' or company['name'] == '' :
                     popup.alert('ERRO', 'POR FAVOR, PREENCHA TODOS OS CAMPOS.') 

                else: 
                    status = True

                    for index in range(count):
                        if 'company' in dados[index]:
                            if dados[index]['company']['cnpj'] == company['cnpj']:
                                popup.alert('INFORME', 'A EMPRESA JÁ FOI CADASTRADA.')
                                status = False
                            if status:
                                if dados[index]['company']['name'] == company['name']:
                                    popup.alert('INFORME', 'A RAZÃO SOCIAL JÁ ESTÁ VINCULADA A UM CNPJ.')
                                    status = False

                    if status :
                        
                        company = {
                            "company": {
                                'cnpj': company['cnpj'],
                                'name': company['name'],
                                'date': '{}'.format(datetime.datetime.now()),
                            } 
                        }

                        dados.append(company)

                        with open(file, 'w') as json_file:
                            json.dump(dados, json_file, indent=4)

                        popup.alert('INFORME', 'EMPRESA CADASTRADA COM SUCESSO.')
                        break
                    else:
                        status = True

        window.close()
        
            
