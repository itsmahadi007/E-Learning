# E-Learning
 Basic Web app
 installation process:
 
 
    1. install python venv
        for linux:
        install:          python3 -m pip install virtualenv
        create venv:      python3 -m venv <any name for env>
        active(bash/zsh): source env/bin/activate

        for windows:
        install:             python -m pip install virtualenv
        create venv:         python -m venv <anynameforenv>
        active(powerShell):  .\env\Scripts\Activate.ps1
        active(cmd.exe):     .\env\Scripts\activate
        Powershell must need to unrestricted:  Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser

    2. Install file from requiements.txt 
            pip3 install -r requirements.txt

    3. Run web the application by 
        python manage.py runserver
    (For better understanding use Mysql of postgre db)

        
