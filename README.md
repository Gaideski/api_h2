
<h1>TEXO BACKEND</h1>

<h2>Usage</h2>

## Loading a new csv 'movie list'
<p>
Copy the .csv file into folder movies_api/csv before initializing the api
</p>
The csv <strong>must</strong> have those headers:
year;title;studios;producers;winner

<br>

## Get the output Json
<p>
Get request into 'localhost:5000/' will return the expected json
</p>

## Database architecture

![alt text](https://github.com/gaideski/api_h2/blob/main/database%20architecture.drawio.png?raw=true)

<br>

## Database
<p>
The chosen database was h2 for its fast deployment and embedded system
</p>
The connection was done using jaydebeapi

<br>
<h1> Running the code</h1>


### Running from command line :
Call python path/to/app.py
