# Election Scraper

This is the third project for Engeto Python Academy.

## Project Description

This project enables users to extract results of elections to the Chamber of Deputies of the Parliament of the Czech Republic in 2017.

Election results are extracted per region. All results are available on [this website](https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ).

## Libraries Installation

You can find the list of libraries that are used in the code in `requirements.txt`. To install the libraries, you can create a new virtual environment and use these commands:

```shell
pip3 install -r requirements.txt
```

## Running the Script

To run the script in the command line, you have to enter two arguments:

1. Link to a website with election results for a specific region.
2. Name of the csv file that will be generated and will contain the extracted data.

```shell
python projekt_3.py 'link' 'csv name.csv'
```

## Example

Election results for the region of Prague:

First argument: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=1&xnumnuts=1100

Second argument: `vysledky_praha.csv`

Running the script:
```shell
python projekt_3.py 'https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=1&xnumnuts=1100' 'vysledky_praha.csv'
```

Data extraction:
```shell
Downloading data from url: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=1&xnumnuts=1100
Saving data to file: vysledky_praha.csv
Ending projekt_3.py
```

Output (first three rows in the csv file):

```csv
town code,town name,registered,envelopes,valid,Občanská demokratická strana,...
500054,Praha 1,21556,14167,14036,2770,9,13,657,12,1,774,392,514,41,6,241,14,44,2332,5,0,12,2783,1654,1,7,954,3,133,11,2,617,34
500224,Praha 10,79964,52277,51895,8137,40,34,3175,50,17,2334,2485,1212,230,15,1050,35,67,9355,9,8,30,6497,10856,37,53,2398,12,477,69,53,2998,162
```
