# eth-client-hw-analysis V2
Repo compiling all the images that came out from our Ethereum Consensus Client's hardware resource analysis 

## The Analysis
This Analysis was performed during the month of May in 2023.
It consisted of running the 5 main clients (Prysm, Lighthouse, Teku, Nimbus and Lodestar)

## Running the clients

In order to run the 5 main CL clients we have developed our own Ethereum docker-compose setup that can be used 
to launch them in a single command. Please refer [here](https://github.com/migalabs/eth2-clients-setup) for more information.

## Data Collection

Data has been collected using a Jupyter Notebook and a Prometheus. Please refer to the `report.ipynb` file, where you may find a page containig the data collection details.
After the execution, you may find several CSV files have been downloaded.

## Data Plotting

Data has been plotted using the same Jupyter Notebook `report.ipynb`. The last page contains details about the plots. These plots are built from the CSV downloaded previously with the same document.




Maintained by [MigaLabs](http://migalabs.io)