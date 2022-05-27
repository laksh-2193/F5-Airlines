from django.contrib import admin
from matplotlib.pyplot import cla
from .models import Offers, UserDetails, Places, Flightroutes, Flights, Ticket, Passenger

@admin.register(Offers)
class OffersAdmin(admin.ModelAdmin):
    list_display = ('id','code','maxdis','desc','title')

@admin.register(UserDetails)
class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ('id','name','contactno','dob','emailid','password','verified')

@admin.register(Places)
class PlacesAdmin(admin.ModelAdmin):
    list_display = ('acronym','placename','lattitude','longitude')


@admin.register(Flightroutes)
class FlightroutesAdmin(admin.ModelAdmin):
    list_display = ('routeno','origin','destination')

@admin.register(Flights)
class FlightsAdmin(admin.ModelAdmin):
    list_display = ('flightno','routeno','departure','arrival','basefare')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('pnr','contact','flightdate','flightno','booking','paidamt')

@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ('name','dob','pnr','bookingID')

