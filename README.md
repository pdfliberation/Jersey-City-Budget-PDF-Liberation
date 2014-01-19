This is a project to liberate 3,800 pages of data from PDF found on the Jersey City Website: http://www.cityofjerseycity.com/pub-info.aspx?id=2430.  You can find the corresponding GIST here:  https://gist.github.com/adlukasiak/8500562

To run, open python notebook:

	ipython notebook

This project uses ABBYY Cloud OCR SDK Api and tabula Api.

About ABBYY Cloud OCR SDK:

* github:  https://github.com/abbyysdk/ocrsdk.com/tree/master/Python

	AbbyyOnlineSdk.py
	MultipartPostHandler.py
	process.py

*You can run it on a command line to test:

	process.py <input fie> <output file> -pdf

About tabula:
 
*webpage:  http://tabula.nerdpower.org/

This project is under construction.  To be added:

* conversion from searchable pdf to csv using tabula
* data scraping (extract only the line items ignoring the rollup + link all spending items to accounts, programs, divisions and departments)
* upload the scraped data as .csv and hierarchical .json into data.openjerseycity.org so it can be used for visualization projects
