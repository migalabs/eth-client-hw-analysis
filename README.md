# Ethereum Consensus Clients Hardware Analysis V2
This repository collects all the scripts and generates the figures used in the Ethereum Consensus Client's hardware resource analysis. 

## The Analysis
This Analysis was performed during the month of May in 2023.
It consisted of running the 5 main clients (Prysm, Lighthouse, Teku, Nimbus and Lodestar)

## Running the clients

In order to run the 5 main CL clients we have developed our own Ethereum docker-compose setup that can be used 
to launch them in a single command. Please refer [here](https://github.com/migalabs/nodeth) for more information.

## Data Collection

Data has been collected using a Jupyter Notebook and a Prometheus. Please refer to the `report.ipynb` file, where you may find a page containing the data collection details.
After the execution, you may find several CSV files have been downloaded (under `{network}/csv/`).

## Data Plotting

Data has been plotted using the same Jupyter Notebook `report.ipynb`. The last page contains details about the plots. These plots are built from the CSV files downloaded previously with the same document.




Maintained by [MigaLabs](http://migalabs.io)