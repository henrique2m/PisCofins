import json
import Company
import Competence
import Credit
import Consult
import Global
import PySimpleGUI as view

def listCompany():
    file = Global.DATABASE()

    with open(file, 'r') as json_file:
        dados = json.load(json_file)

    count = len(dados)

    listCompany = []

    for index in range(count):
        if 'company' in dados[index]:
            listCompany.append(dados[index]['company']['name'])
    
    return listCompany

view.theme_background_color('#6272a4')


logo = Global.LOGO()

layout = [
    [ view.Image(logo, background_color="#6272a4", )],
    [ view.Frame('OPÇÕES',
            [
                [
                    view.Button('CADASTRAR EMPRESA',
                                    size=(12,5),
                                    key="registerCompany",
                                    button_color=['#ffffff','#282a36']
                                ), 
                    view.Button('ADICIONAR COMPETÊNCIA', 
                                    size=(12,5), 
                                    key="addCompetence",
                                    button_color=['#ffffff','#282a36']
                                )
                   
                ],
                [ 
                    view.Button('ATUALIZAR CRÉDITOS', 
                                    size=(12,5), 
                                    key="updateCredit",
                                    button_color=['#ffffff','#282a36']
                                ),
                    view.Button('CONSULTAR', 
                                    size=(12,5), 
                                    key="consultCredit",
                                    button_color=['#ffffff','#282a36']
                                )   
                ]
            ], background_color='#6272a4'
        ) 
    ]
]


window = view.Window('CRÉDITOS FISCAIS', 
                        layout, 
                        element_justification='center', 
                        icon=Global.ICON(),
                    )

while True:
    event, values = window.read()

    if event in (view.WIN_CLOSED, 'exit'):
        break
    elif event == 'registerCompany':
        company = Company.WindowRegisterCompany()
        company.Start()
    elif event == 'addCompetence':
        companies = listCompany()
        competence = Competence.WindowRegisterCompetence()
        competence.Start(companies)
    elif event == 'updateCredit':
        companies = listCompany()
        credit =  Credit.WindowCredit()
        credit.calculate(companies)
    elif event == 'consultCredit':
        companies = listCompany()
        consult = Consult.WindowCreditConsult()
        consult.select(companies)
        

window.close()

