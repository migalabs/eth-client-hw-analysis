# Ethereum Consensus Clients Hardware Analysis V2
This repository collects all the scripts and generates the figures used in the Ethereum Consensus Client's hardware resource analysis. 

## The Analysis
This Analysis was performed during the month of May in 2023.
It consisted of running the 5 main clients (Prysm, Lighthouse, Teku, Nimbus and Lodestar)

## Running the clients

Inside this repository you may find several files with which you launch the nodes you intend to analyze.
The setup includes an execution node (always Nethermind), a consensus node (Lighthouse, Prysm, Teku, Nimbus, Lodestar) and some monitoring tools (such as Prometheus, Node Exporter or CAdvisor)

### Server

It is possible to run a metrics server, which should aborb all the generated metrics into a single prometheus instance.
This is very useful when the experiment involves several clients and machines. This way, analyzing the data is faster and easier, as everything is contained in a single instance.

Caddy is a Proxy server which will receive all the incoming traffic and redirect it to the metrics server.

1. Copy `Caddyfile.sample` into `Caddyfile`
2. You may configure some credentials if needed.
3. Copy `prometheus-template.yml` into `prometheus.yml` (prometheus folder). You may comment all the scrapes as this prometheus will be a server receiving the data.
4. Run `docker-compose up -d prometheus victoriametrics caddy` 
5. You may now use `http://user:password@yourIP/promhttp/api/v1/write` and `http://user:password@yourIP/victoria/api/v1/write` as remote write

### Clients

1. Decide which client to run
2. Copy `.env.sample` into `.env` and fill the variables. Tags refer to the client version (docker image).
3. Copy `prometheus-template.yml` into `prometheus.yml` (prometheus folder). See remote write above if needed, comment it otherwise.
4. You may configure which clients to scrape and the remote write (see server options above).
4. Run `docker-compose up -d nethermind <cl-node> prometheus cadvisor node-exporter`.


## Data Collection

Data has been collected using a Jupyter Notebook and a Prometheus. Please refer to the `report.ipynb` file, where you may find a page containing the data collection details.
After the execution, you may find several CSV files have been downloaded (under `{network}/csv/`).

## Data Plotting

Data has been plotted using the same Jupyter Notebook `report.ipynb`. The last page contains details about the plots. These plots are built from the CSV files downloaded previously with the same document.




Maintained by [MigaLabs](http://migalabs.io)