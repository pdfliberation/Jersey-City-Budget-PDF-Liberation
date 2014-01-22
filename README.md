## About the project

In Jersey City, we wanted the public to be more educated about the budget and city finances. So we started a project to convert the 37 scanned PDF documents and total of 3,871 pages available on the city's website into interactive visualizations.  Inspired by the OpenSpending and Open Budget Oakland projects, we quickly build a page with place for public comment, but then realized that getting the data out of the scanned PDFs is no simple task.  The PDF Liberation hackathon was our missing link.

At the PDF Liberation Hackathon, the goal was automate the process by creating a framework.  Our first step was to convert non searchable PDFs to searchable PDFs with the ABBYY Cloud OCR SDK API.  The second step was to convert searchable PDF files to CSV files using the non-interactive version of Tabula pable parser.  The results of the table parser are not completely accurate but can be cleaned up by programming some higher-level heuristics.  To complete the project, we would like to convert the CSV into a hierarchical data model and leverage existing solutions to publish budget visualizations. 

The PDF files with historical data can be found on the [Jersey City Website] (http://www.cityofjerseycity.com/pub-info.aspx?id=2430).  

You can find the corresponding Gist [here](https://gist.github.com/adlukasiak/8500562).

The extracted data will be uploaded to [Open JC Open Data Portal](https://data.openjerseycity.org/dataset/jersey-city-2013-budget-adopted-spending).

[OpenSpending](https://openspending.org/)-like visualization will be made to the public on the [Jersey City Budget](http://openjerseycity.org/JerseyCityBudget/) site.

This project is built by [Open JC](http://openjerseycity.org/), a [Code for America](http://codeforamerica.org/) brigade.

---

## Instructions to run the project

#### Open python notebook

On the command line, type:

`ipython notebook`

#### ABBYY Cloud OCR SDK:

This project uses [ABBYY Cloud OCR SDK Api](http://cloud.ocrsdk.com/Account/Welcome) and [tabula Api](https://source.opennews.org/en-US/articles/introducing-tabula/).

* Python code sample that was utilized: https://github.com/abbyysdk/ocrsdk.com/tree/master/Python

* You can manually run it on a command line to test:

	`process.py <input fie> <output file> -pdfSearchable`

#### Tabula:
 
* Browser version:  http://tabula.nerdpower.org/
* Command-line version:  https://github.com/jazzido/tabula-extractor

#### Next steps:

This project is under construction.  

To be added:

* Conversion from searchable pdf to csv using command-line [tabula-extractor](https://github.com/jazzido/tabula-extractor).  One table to one csv file.
* Data scraping.  Extract only the line items ignoring the rollups + link all spending to accounts, programs, divisions and departments, etc
* Upload the scraped data as .csv and hierarchical .json into data.openjerseycity.org so it can be used for visualization projects, like http://openjerseycity.org/JerseyCityBudget/.
