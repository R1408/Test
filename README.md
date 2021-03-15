# Test


create a <b>python_test</b> directory and clone the project inside this directory

or
download the zip file from [DRC_test](https://codeload.github.com/R1408/Test/zip/develop)
and extract the file

##The floder structure should be
## If you clone the project
```
python_test -- Test
            -- venv
            -- requirements
```
##If you download zip file
```
Test-development -- Test
                 -- venv
                 -- requirements
```
open python_test or Test-development directory

create virtual environment if it is not created
```
if you use pycharm got to the setting go to the project name python interpreter
select python version

```
install requirements if it is not installed

###for install requirements
```
pip install -r requirements.txt
```

create manualy database test

go inside the test directory (cd test)

Run following command
```
 python manage.py db init
 python manage.py db migrate
 python manage.py db upgrade
```

configure env file in your project

run main.py file

###open below URL 
```  http://localhost:5000/```