# MAL Data Visualizations

This repo contains my visualization project for anime on MyAnimeList, made using data acquired from MAL using their API.

The data was processed using Pandas and plotted using Plotly.

## Usage
To run, create the python virtual environment and install the requirements:
```sh
python -m venv virt
source virt/bin/activate
pip install -r requirements.txt
```

To generate the visualizations, run main.py with arguments for the visualization to generate:
```sh
python main.py plot histogramisekaimembers
```
Interactive plots will be stored in the plots directory in the project root. Create it if it doesn't exist.

## Getting the Dataset
This repo doesn't include the dataset used to generate the plots. You can generate it by running the following:

```sh
python main.py scrape anime
```
The program expects an authentication token to the MAL API stored in a file called `auth`. You'll have to acquire this yourself.

Note: Collecting the data takes multiple days.
