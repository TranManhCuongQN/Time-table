# Timetable scheduling
## To run this project
### Install **virtualenv** first
    pip install virtualenv
### Clone this project
    git clone https://github.com/HoaAyWK/Timetable.git
    cd TimeTable
### Run the following command in the base directory of this project
    virtualenv env
>you can use any name insted of **env**
### Activate your virtual enviroment
    source env/bin/activate
>on Windows, virtualenv creates a batch file \env\Scripts\activate.bat, to activate virtualenv in Windows, activate script in the Scripts folders: path\to\env\Scripts\activate.bat
### Install dependencies 
    pip install -r requirements.txt
### Now you can run the project with this command
    python manage.py runserver
### Then go to port `http://127.0.0.1:8000/timetable/`
 
