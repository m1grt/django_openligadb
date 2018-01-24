from django import forms


class SearchTeam(forms.Form):
    team = forms.TextInput()
