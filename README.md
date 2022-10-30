[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

#### The task is to collect data from three resources: 
1. [oriencoop.cl](https://oriencoop.cl/sucursales.htm) 
2. [som1.ru](https://som1.ru/shops/)
3. [naturasiberica.ru](https://naturasiberica.ru/our-shops/)
#### Resulted scripts for parsing:
1. [Script 1](https://github.com/swankyalex/Parsing_Test_Assignment/blob/master/src/script1.py)
2. [Script 2](https://github.com/swankyalex/Parsing_Test_Assignment/blob/master/src/script2.py)
3. [Script 3](https://github.com/swankyalex/Parsing_Test_Assignment/blob/master/src/script3.py)

#### Resulted data is [here](https://github.com/swankyalex/Parsing_Test_Assignment/tree/master/collected%20data):
## Usage
This package allows you to parse data from all links provided above
1. Clone this repository to your machine.
2. Make sure Python 3.9 and [Pipenv](https://pipenv.pypa.io/en/latest/) (requirements.txt also provided) are installed on your machine.
3. Install the project dependencies (*run of the following commands in a terminal, from the root of a cloned repository*):
```sh
pipenv install / pipenv install --dev #to install with dev-packages (black, isort)
```
or if you have [Make](https://www.gnu.org/software/make/) util
```sh
make venv / make venv-dev #to install with dev-packages (black, isort)
```

4. Run script with one of the following commands:
```sh
pipenv run python src/script1.py #or script2.py/script3.py 
```
```sh
make parse1 #parse2/parse3
```
```sh
make parse-all #to parse all resources sequentially
```
**The data in JSON format will be saved to the folder *data* in root directory**

5. Also CSV format supported. Just add the option *-o csv*:
```sh
pipenv run python src/script1.py -o csv #or script2.py -o csv/script3.py -o csv
```
```sh
make parse1-csv #parse2-csv/parse3-csv
```
```sh
make parse-all-csv #to parse all resources sequentially
```
**The data in CSV format will be saved to the folder *data* in root directory**

6. If you installed dev dependencies you also can automatically format code with one
of the following commands:
```sh
make format #run black and isort sequentially
```
or
```sh
pipenv run [black/isort]
```




