
| Province     | Latitude (Decimal) | Longitude (Decimal) |
|--------------|-------------------|---------------------|
| Bocas del Toro | 9.350000 | -82.250000 |
| Coclé        | 8.083333 | -80.566667 |
| Colón        | 9.350000 | -79.883333 |
| Chiriquí     | 8.466667 | -82.466667 |
| Darién       | 8.000000 | -77.500000 |
| Herrera      | 8.183333 | -80.466667 |
| Los Santos   | 7.950000 | -80.466667 |
| Panamá       | 9.000000 | -79.533333 |
| Veraguas     | 8.416667 | -81.166667 |


you can use the ST_Y and ST_X functions to extract the coordinates. For example, you can use the following code to get the latitude and longitude for a point in a table called mytable:

~~~
# Import the necessary modules

import psycopg2
from psycopg2.extras import DictCursor

# Connect to the database

conn = psycopg2.connect("dbname=mydatabase user=myuser password=mypassword")


# Create a cursor for executing queries

cur = conn.cursor(cursor_factory=DictCursor)

# Execute a query to get the point

cur.execute("SELECT geom FROM mytable WHERE id = 1")

# Get the point from the query result

point = cur.fetchone()["geom"]


# Extract the latitude and longitude from the point

latitude = point.ST_Y()
longitude = point.ST_X()

# Print the latitude and longitude

print(latitude, longitude)
~~~

This code assumes that the geom column in mytable contains point geometries in a coordinate reference system that uses latitude and longitude (e.g. WGS 84). If your geometries are in a different coordinate reference system, you can use the ST_Transform function to transform them to WGS 84 before extracting the coordinates.

If you want to get the latitude and longitude for multiple points, you can use a FOR loop to iterate over the points in the query result and extract the coordinates for each one. For example:


~~~
# Import the necessary modules

import psycopg2
from psycopg2.extras import DictCursor

# Connect to the database

conn = psycopg2.connect("dbname=mydatabase user=myuser password=mypassword")

# Create a cursor for executing queries

cur = conn.cursor(cursor_factory=DictCursor)

# Execute a query to get the points

'cur.execute("SELECT geom FROM mytable")'

# Iterate over the points in the query result

for row in cur:
    # Get the point
    point = row["geom"]

    # Extract the latitude and longitude from the point
    latitude = point.ST_Y()
    longitude = point.ST_X()

    # Print the latitude and longitude
    print(latitude, longitude)
~~~