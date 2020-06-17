import PySimpleGUI as sg
import json
import pyperclip


with open('batch_db.json', 'r') as f:
    batch_db = json.load(f)

sg.theme('DarkBlue14')
layout = [
            [sg.Text('Enter SKU List', size=(30, 1), justification='center')],
            [sg.Multiline(size=(35, 20), do_not_clear=False)],  
            [sg.Button('Get Batch'), sg.Button('Exit')] 
        ]

def get_batch(sku):
    '''Takes a SKU and returns the batch number in list. If not found returns missing SKU'''
    batch_list =[]
    for sku in sku.split():
        if sku not in batch_db.keys():
            batch = sg.popup_get_text(f'{sku} no batch found. Enter below')
            add_batch(sku, batch)
            batch_list.append(batch)

        else:
            batch_list.append(batch_db[sku])
            
    return batch_list

def add_batch(sku,batch):
    '''Adds a batch and SKU to the Batch DB'''
    batch_db[sku] = batch
    return batch
    

# Create the Window
window = sg.Window('Get Batch Numbers', layout)

while True:

    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        with open('batch_db.json', 'w') as outfile:
            json.dump(batch_db, outfile)
        break

    elif event == 'Get Batch':
        batch_numbers = get_batch(values[0])
        if batch_numbers:
            sg.popup('Here are the requested batch numbers', 'Click Ok to copy and return to main screen',
                    '\n'.join(batch_numbers), background_color='gray', no_titlebar=True, keep_on_top=True)
            pyperclip.copy('\n'.join(batch_numbers))
        else:
            sg.popup('Enter SKU list to continue!', no_titlebar=True, keep_on_top=True)

window.close()
