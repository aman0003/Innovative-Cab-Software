from django import forms

class PredictionForm(forms.Form):
    #name = forms.CharField(max_length = 15)
    Pickup_Address = forms.ChoiceField(choices=[('-73.9654,40.7829','Central Park'),('-73.9855,40.7580', 'Times Square' )])
    Dropoff_Address = forms.ChoiceField(choices=[('-73.9772,40.7527','Grand Central Terminal'),('-73.9969,40.7061', 'Brooklyn Bridge' ), ('-73.948433,40.812350', 'South Harlem'), ('-74.0048,40.7480', 'The High Line')])
    Passengers = forms.IntegerField()
    Year = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Enter any Year'}))