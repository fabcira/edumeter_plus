# Visualisation of Edumeter data in a friendly manner 
The Edumeter data comes in two shapes: 
1. with a set of summary diagrams showing how the module is performing wrt a set of dimensions
2. the full details of the students' responses in a spreadsheet.

The spreadsheet however is quuite difficult to interpret. This Jupyter notebook allows to analyse the data and to show it in a user friendly manner. 

## Setup
In order to run the notebook you need to:
1. download the files "Schede con le risposte" (hereafter schede) and "Statistiche" (stats) 
2. Save the Edumeter spreadsheets in XLSX format (i.e. using the latest version of Excel, rather than the version used by Edumeter - to go file > save as and select the type "Excel Workbook")
3. upload them to the Notebook into the foilder "data"
4. set the  parameters for each of the two files as specified below:

## Setup for  "Statistiche" 
Set up the file name, e.g.:
```
  stat_file = 'data/STATISTICHE_INTERAZIONE UOMO MACCHINA E TECNOLOGIE WEB.xlsx'
```


## Setup for "Schede con le risposte" 
Set:
1. the name of the file
2. the first data row index (where the name of the columns are (e.g. Dom. 1 - Conoscenze preliminari	Dom. 2 - Carico di studio	Dom. 3 - Materiale didatticoDom. 1 - Conoscenze preliminari	Dom. 2 - Carico di studio	Dom. 3 - Materiale didattico...) 
3. the last data row index

```
full_stat_file = 'data/SCHEDE_INTERAZIONE UOMO MACCHINA E TECNOLOGIE WEB.xlsx'
# the  row where the column names are i.e. the row containing (Dom. 1 - Conoscenze preliminari	Dom. 2 - Carico di studio	Dom. 3 - Materiale didatticoDom. 1 - Conoscenze preliminari	Dom. 2 - Carico di studio	Dom. 3 - Materiale didattico...) 
full_stats_headers_row = 14
# the last row with marks data 
full_stats_last_relevant_data_row = 169
```




