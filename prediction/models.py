from django.db import models


class fare_prediction(models.Model):

    PLACES1 = (
        ('-73.9654,40.7829','Central Park'),
        ('-73.9855,40.7580', 'Times Square' )
    )
    
    PLACES2 = (
        ('-73.9772,40.7527','Grand Central Terminal'),
        ('-73.9969,40.7061', 'Brooklyn Bridge'),
        ('-73.948433,40.812350', 'South Harlem'),
        ('-74.0048,40.7480', 'The High Line')

    )
    
    Pickup_Address = models.CharField(max_length = 15, choices=PLACES1)
    Dropoff_Address = models.CharField(max_length = 15, choices=PLACES2)
    Passengers = models.IntegerField()
    Year = models.IntegerField()
    #distance = models.FloatField(default=0)
    #JKF_distance = models.FloatField(default=0)

    def __str__(self):
       return '{}'.format(self.name)

