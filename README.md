# ITRF_2014_to_ETRF_2014
converts ITRF 2014 (WGS84) to ETRF2014(ETRS89)

<br>

## Functions
1) cartesian_3D_from_lon_lat ( )
<br>
This function converts latitude and longitude degree values into 3D cartesian coordinates.

```python
cartesian_3D_from_lon_lat(long_degrees,lat_degrees,elevation_metres)
##returns 3d Coordinates (metres) in x, y and Z
```
<br>

2) lon_lat_from_cartesian_3D ( )
<br>
This function converts X,Y,Z 3D cartesian coordinates into latitudes, longitudes and elevations values.

```python
lon_lat_from_cartesian_3D(x_coord,y_coord,z_coord)
##returns longitudes(in degrees), latitude(in degrees) and elevation(in metres)
```

3) ITRF2014_ETRF2014 ( )
<br>

Converts ITRF2014 coordinates into ETRF2014 coordinates.
<br>
ITRF(2014) has been used to approximate WGS84 coordinates while ETRF2014 ensures the transformed coordinates are within the ETRS89 system.

###  **Parameters**
Important for the stations to have velocity information incase different epochs are used.
<br>
x_coord=x coordinate of the station (metres)
<br>
y_coord= y coordinate of the station(metres)
<br>
z_coord= z coordinate of the station(metres)
<br>

x_velocity, y_velocity, z_velocity = the velocity of the station (metres per year)
<br>
NB: x_velocity = 0,y_velocity=0 and z_velocity = 0 if ITRF_Epoch=ETRF_Epoch,
<br>
ITRF_epoch= the date (in decimal years) of the data measurement
<br>
ETRF_epoch= The date(in decimal years) of the data in the new system. one can go either to the past, present or future


```python
ITRF2014_ETRF2014(x_coord,y_coord,z_coord,x_velocity,y_velocity,z_velocity,ITRF_epoch,ETRF_epoch)

##returns ETRF2014 coodrinates
