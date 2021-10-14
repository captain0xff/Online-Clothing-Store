'''Check if the required modules are available or not.'''
def version_compare(ava,req):
    req=req.split('.')
    not_satisfied=False
    for i in range(len(ava)):
        if int(req[i])>int(ava[i]):
            print(req[i],ava[i])
            not_satisfied=True
            break
    return not_satisfied


def main():
    needed_requirements={
        'PySimpleGUI':'4.45.0',
        'mysql.connector':'8.0.26',
        'tkinter':'8.6'
    }

    available_requirements={
        'PySimpleGUI':None,
        'mysql.connector':None,
        'tkinter':None
    }

    needed_modules=0

    try:
        import PySimpleGUI
        available_requirements['PySimpleGUI']=PySimpleGUI.__version__.split('.')
    except ModuleNotFoundError:
        available_requirements['PySimpleGUI']=False
    try:
        import mysql.connector
        available_requirements['mysql.connector']=mysql.connector.__version__.split('.')
    except ModuleNotFoundError:
        available_requirements['mysql.connector']=False
    try:
        import tkinter
        available_requirements['tkinter']=str(tkinter.TkVersion).split('.')
    except ModuleNotFoundError:
        available_requirements['tkinter']=False
    
    install_msg='{name} is missing! Please install the module. For more information check the modules documentation.'
    update_msg='{name} is too old! Please consider updating the module. For more information check the modules documentation.'
    satisfied_msg='{name} is found.'
    for i in available_requirements:
        if not available_requirements[i]:
            print(install_msg.format(name=i))
            needed_modules+=1
        elif version_compare(available_requirements[i],needed_requirements[i]):
            print(update_msg.format(name=i))
            needed_modules+=1
        else:
            print(satisfied_msg.format(name=i))
    
    if needed_modules:
        print('Please install the missing modules.')
    else:
        print('Success!!! You are good to go.')
    
    


if __name__=='__main__':
    main()
