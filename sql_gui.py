import PySimpleGUI as sg
import sqlite3
def getUserData():
    sg.theme('DarkAmber')	# Add a touch of color
    # All the stuff inside your window.
    layout = [  [sg.Text('')],
                [sg.Text('Enter Username: '), sg.InputText()],
                [sg.Text('Enter Password:  '), sg.InputText()],
                [sg.Button('Ok')] ]

    # Create the Window
    window = sg.Window('Sign Up', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        print('You entered ', values)
        if("@" not in values[0] or "." not in values[0] or len(values[0]) == 0 or len(values[1]) == 0):
            sg.Popup('Username is invalid')
            continue
        else:
            conn = sqlite3.connect('/opt/mycroft/skills/useridentification-skill/allUsers/Users.db')
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM User")
            number_of_entries = c.fetchone()[0]
            if number_of_entries != 0:
                c = conn.cursor()
                c.execute("SELECT userId FROM User WHERE userId=" + values[0])
                if not c.fetchall():
                    sg.Popup('Username is already used')
                else:
                    c = conn.cursor()
                    c.execute("INSERT INTO User VALUES (?, ?, ?, ?)", (number_of_entries + 1, values[0], values[1], 0))
                    conn.commit()
                    break
            else:
                c = conn.cursor()
                c.execute("INSERT INTO User VALUES (?, ?, ?, ?)", (number_of_entries + 1, values[0], values[1], 0))
                conn.commit()
                break
    window.close()
    

getUserData()
