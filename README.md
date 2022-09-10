
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

## Loading a new csv 'movie list'
<p>
Copy the .csv file into folder movies_api/csv before initializing the api.
</p>

The csv <strong>must</strong> have those headers:
year;title;studios;producers;winner

<br>

## Get the case output Json
<p>
Get request into 'localhost:5000/' will return the expected json
</p>


<br>
<h1> Running the code</h1>


### Running from command line :
<p>Call python path/to/movies_api/rest_api/app.py</p>

<br>
<h1>Integration test</h1>



### Running from the command line:
<p>python -m unittest discover path/to/movies_api/rest_api/test "test_*" </p>

<h1>Extras</h1>

## Postman documentation
More documentation about the api is available at [REQUEST EXAMPLES](https://documenter.getpostman.com/view/2262340/VVJ6yaXP)
