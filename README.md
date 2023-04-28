# cvm-data-exporter

Command-Line Interface (CLI) to collect information from public companies and financial statements with the possibility to export to MongoDB or JSON file. 

This CLI extracts open data from the CVM, or "Comissão de Valores Mobiliários" portal.

## Requirements

- Set environment variable `MONGO_MASTER_URI`;
- Install `pipenv`, run `pipenv sync` and `pipenv shell`.
