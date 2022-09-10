
<h1>TEXO BACKEND TEST</h1>

## The Problem

<p>
Develop a RESTful API that enables the reading of the winners and indicates the worst film category on the Golden Raspberry Awards.
</p>

> ### Requirements
>
> - Read the CSV file of movies and insert the data in a database on the start-up;
> - Obtain the producer with the greater interval between two consecutive awards and who gets the awards faster given the specified format;
> - The RESTful web service must be implemented in the level 2 of maturity of Richardson;
> - Only integration tests should be implemented. They must garantee that the obtained data are by the proposed data;
> - The database has to be in memory, and further installation should be required;
> - The application must have a readme containing instructions on how to use it and test it.

<br>
<h1>Solving approach</h1>

###  Data extraction

<p>
To load the .CSV into the system I choose to read it using Pandas so I can access the data easily by its headers also I can validate that all the columns are present on the file.
</p>
<br>

### Database
<p>
To correctly model the database, first I locate all the entities of the problem which are:

> - Movie
> - Studio
> - Producer
</p>
<p>

However, given the nature of the data (one movie can have multiple studios or producers) two intermediary tables have to be created:

> - MovieStudio
> - MovieProducer
</p>
<p>
The final architecture of the database has shown in the following diagram:

### Database architecture

![alt text](https://github.com/gaideski/api_h2/blob/main/database%20architecture.drawio.png?raw=true)
</p>
<br>

<p>
To fulfill the requirement, I've created an SQL query that returns the producers that won several times and the respective interval between the prizes won following the steps:

> - ### Query
> - Left join 'Producer' on 'MovieProducer' and select the producer name, producer id and movie id
> - Inner join the previous query with table 'Movie' and filter only the winners 
> - Calculate the lag (SQL function) between years over producerId (order the movies by year and partition by producer) and calling it diff
> - Filter the query for the 'diff' not null
> - When the producer won more than once, the previous win will be (release - diff) and the following 'release'
 
</p>

<br>

### API

The API was developed using Flask with the blueprint and focused mainly on the required information about the producers. The implementation only uses the HTTP verb GET due to the nature of the case.
<br>

<h1>Methodology</h1>

<p>
The chosen database was h2 for its fast deployment, embedded system, and requirements fulfilled. Also it is the recommended database from the test evaluator, on the requeriments of this database the jre must be installed on the machine.
</p>
The connection was done using jaydebeapi.
<br>

## Test objective

<p>
The integration test focuses on checking if the location, extraction, and insertion of the data on the current database was successful.
</p>
<br>

<h1>Usage</h1>




<br>
<h1> Running the code</h1>


### Running from command line :
> 1.  Download the project from github: 'git clone https://github.com/Gaideski/api_h2.git'
> 2.  Extract all the files to your choosen path
> 3.  Install the requirements 'pip install -r choosen/path/API_h2/requeriments.txt'
> 4.  Run 'python choosen/path/API_h2/movies_api/rest_api/app.py'

<br>


## Loading a new csv 'movie list'
<p>
Copy the .csv file into folder <strong>/path/to/project/api_h2/movies_api/csv</strong> before initializing the api.
</p>

The csv <strong>must</strong> have those headers:
year;title;studios;producers;winner

<br>

## Get the case output Json
<p>
Get request into 'localhost:5000/' will return the expected json
</p>
<br>
<h1>Integration test</h1>

### Running from the command line:

Follow the steps from the 'running the code' until step 3.<br>
Run ' python -m unittest discover choosen/path/API_h2/movies_api/rest_api/test "test_*" '

<h1>Extras</h1>

## Postman documentation
More documentation about the api is available at [REQUEST EXAMPLES](https://documenter.getpostman.com/view/2262340/VVJ6yaXP)


<h1>Docker build</h1>
The project also have a Dockerfile to build, you can try build it with:

> - ### Building
> - 
> - Open the terminal, cmd or alike
> - go to the Dockerfile dir
> - execute 'docker build -t texo_backend  .' 
> - then docker run 'docker run -d gaideski/texo_backend -p 5000:5000 -p 22:22'
> - try access from your browser


### Running 

It's possible also to run directly from docker hub using: 'docker run -d -p 5000:5000 -p 22:22 gaideski/texo_backend'


## Update the csv

To update the csv from the docker, just access the docker from sftp as 'sftp://root:screencast@localhost', replace the files from /app/movies-api/csv, and restart the docker