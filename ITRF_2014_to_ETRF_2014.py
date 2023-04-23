#-------------------------------------------------------------------------------
# Name:        ITRF2014 to ETRF2014
# Purpose:     converts from WGS84 (implemented in ITRF2014) to ETRF2014
#
# Author:      Caleb
#
# Created:     10/04/2023
# Copyright:   (c) Acer 2023
# Licence:     <Motor_ai>
#-------------------------------------------------------------------------------
import pyproj
import numpy as np

#create 3d cartesian coordinates from geograpical latlon

def cartesian_3D_from_lon_lat(long_degrees,lat_degrees,elevation_metres):
    geocent_cartesian_3D=pyproj.Proj(proj='geocent',ellps='WGS84',datum='WGS84')
    geographic_latlon=pyproj.Proj(proj='latlong',ellps='WGS84',datum='WGS84')
    x_coord,y_coord,z_coord=pyproj.transform(geographic_latlon,geocent_cartesian_3D,long_degrees,lat_degrees,elevation_metres,radians=False)
    return x_coord,y_coord,z_coord

def lon_lat_from_cartesian_3D(x_coord,y_coord,z_coord):
    """
    built in datums:WGS84, GGRS87, NAD38, NAD27, potsdam, carthage, hermannskogel, ire65, nzgd49, OSGB336.
    built in ellipsoids: GRS80,airy,bessel,clrk66,intl,WGS60,WGS66,WGS72,WGS84,sphere
    """
    geocent_cartesian_3D=pyproj.Proj(proj='geocent',ellps='GRS80',datum='WGS84') #ETRS utilises the GRS80 ellipsoid.Unfortunately ETRS89 datum is not inbuilt
    geographic_latlon=pyproj.Proj(proj='latlong',ellps='GRS80',datum='WGS84')
    long_degrees,lat_degrees,elevation_metres=pyproj.transform(geocent_cartesian_3D,geographic_latlon,x_coord,y_coord,z_coord,radians=False)
    return long_degrees,lat_degrees,elevation_metres

def ITRF2014_ETRF2014(x_coord,y_coord,z_coord,ITRF_epoch,**kwargs):#,x_velocity,y_velocity,z_velocity,ITRF_epoch,ETRF_epoch

    x_velocity=kwargs.get("x_velocity",0)
    y_velocity=kwargs.get("y_velocity",0)
    z_velocity=kwargs.get("z_velocity",0)
    ETRF_epoch=kwargs.get("ETRF_epoch",ITRF_epoch)

    """converts stations from one system to another. Important for the stations to have velocity information incase different epochs are used
        x_coord=x coordinate of the station
        y_coord= y coordinate of the station
        z_coord= z coordinate of the station

        x_velocity, y_velocity, z_velocity = the velocity of the station (metres per year)
        NB: x_velocity = 0,y_velocity=0 and z_velocity = 0 if ITRF_Epoch=ETRF_Epoch,
        ITRF_epoch= the date (in decimal years) of the data measurement
        ETRF_epoch= The date(in decimal years) of the data in the new system. one can go either to the past, present or future
    """


    station_point_array=np.array([x_coord,y_coord,z_coord])
    station_velocity_array=np.array([x_velocity,y_velocity,z_velocity])


    #Epoch of observation
    observation_epoch=ITRF_epoch
    #ETRS frame. apparently this variable is constant
    ETRS_F=1989

    ##Transformation parameters for ITRF2014 to ETRF 2014, epoch of observation 2010.0
    #translation
    tx_ty_tz=[0.0,0.0,0.0]
    #translation rate
    txa_tya_tza=[0.0,0.0,0.0]

    #rotation
    Rx_Ry_Rz=[1.785,11.151,-16.170]
    #rotation rate
    Rxa_Rya_Rza=[0.085,0.531,-0.770]

    #scalefactor
    scale_factor=0.00*(10**-9)

    ##create transformation equation

    """ NB: be careful of units
        Translations in mm, transform to m
        rotations in mas/yr, transform to rad/yr
        mas= milliarcsecond, rad=radians
        1 mas = 4.8481368E-9 rad
        or 1 rad=206264806.2471 mas
        or
        1) convert from milliarcseconds to arc seconds ( multiply by 0.001)
        2) convert from arcsecond to degrees (divide by 3600)
        3) convert from degrees to radians multiply by (pi/180) """

    #rotation matrix and transformation matrix in SI Units
    t_array=(np.array(tx_ty_tz))/1000 ##change to metres
    scale_factor_array=np.array([scale_factor,scale_factor,scale_factor])
    rotation_rate_array=(np.array([[0,-Rxa_Rya_Rza[2],Rxa_Rya_Rza[1]],[Rxa_Rya_Rza[2],0,-Rxa_Rya_Rza[0]],[-Rxa_Rya_Rza[1],Rxa_Rya_Rza[0],0]]))/206264806.247

    #Helmerts equation
    station_array_transformed=np.add(station_point_array,np.add(t_array,(np.matmul(rotation_rate_array,(station_point_array*(observation_epoch-ETRS_F)))))) # can only add 2 arrays at a time
    station_velocity_tranformed=np.add(station_velocity_array,np.matmul(rotation_rate_array,station_point_array))

    #suitable for transformng between different epochs
    station_points_ETRF2014=np.add(station_array_transformed,np.multiply(station_velocity_tranformed,(ETRF_epoch-ITRF_epoch)))

    return station_points_ETRF2014,station_velocity_tranformed


##example
##point_WGS={"point_1":[13.2800773632584,52.5590577266679,52],"point_2":[13.2794211487789,52.5589930345805,52], "point_3":[13.2744297717056,52.5583876998492,52],"point_4":[13.2757328445624,52.5567500230764,52],"point_5":[13.2820647074073,52.5573715784962,52],"point_6":[13.2816052239415,52.5592062497805,52],"point_7":[13.2805364214469,52.5572212462728,52]}
##print(len(point_WGS))
##
##for i in range(1,len(point_WGS)+1):
##
##    x,y,z=cartesian_3D_from_lon_lat(point_WGS["point_{}".format(i)][0],point_WGS["point_{}".format(i)][1],point_WGS["point_{}".format(i)][2])
##
##    new_station,new_velocity=ITRF2014_ETRF2014(x_coord=x,y_coord=y,z_coord=z,ITRF_epoch=2023.02,x_velocity=0,y_velocity=0,z_velocity=0,ETRF_epoch=2023.02)
##
##    long,lat,elev=lon_lat_from_cartesian_3D(new_station[0],new_station[1],new_station[2])
##
##    print("point_{}".format(i),long,lat,elev)

