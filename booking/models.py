
from enum import auto
from pyexpat import model
from django.db import models

# Create your models here.

class Offers(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10)
    maxdis = models.IntegerField()
    desc = models.CharField(max_length=1000)
    title = models.CharField(max_length=200)

class UserDetails(models.Model):
     id = models.AutoField(primary_key=True)
     name = models.CharField(max_length=100)
     contactno = models.CharField(max_length=20, unique=True)
     dob = models.DateField()
     emailid = models.EmailField(max_length=100, unique=True)
     password = models.CharField(max_length=100)
     verified = models.CharField(max_length=100,default="no")


class Places(models.Model):
    acronym = models.CharField(max_length=5, primary_key=True)
    placename = models.CharField(max_length=20)
    lattitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    def __str__(self):
        return self.acronym

class Flightroutes(models.Model):
    routeno = models.AutoField(primary_key=True)
    origin = models.ForeignKey(Places,on_delete=models.CASCADE, related_name="origin")
    destination = models.ForeignKey(Places,on_delete=models.CASCADE, related_name="destination")
    def __str__(self):
        return str(self.routeno)

class Flights(models.Model):
    flightno = models.CharField(max_length=10, unique=True)
    routeno = models.ForeignKey(Flightroutes,on_delete=models.CASCADE,related_name='routen')
    departure = models.TimeField()
    arrival = models.TimeField()
    basefare = models.IntegerField()

class Ticket(models.Model):
    pnr = models.CharField(max_length=10,unique=True)
    contact = models.CharField(max_length=100)
    flightdate = models.CharField(max_length=15)
    flightno = models.CharField(max_length=10)
    booking = models.IntegerField(max_length=10, unique=True)
    paidamt = models.IntegerField(max_length=10)
    def __str__(self):
        return self.pnr


class Passenger(models.Model):
    name = models.CharField(max_length=10)
    dob = models.CharField(max_length=10)
    pnr = models.ForeignKey(Ticket,on_delete=models.CASCADE,related_name="pnr_status")
    bookingID = models.IntegerField(max_length=10)


