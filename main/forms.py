from django import forms


class Invest(forms.Form):
    ticer = forms.CharField(widget=forms.TextInput(attrs={'id': 'ticker', 'placeholder': 'Параметр'}))
    country = forms.CharField(widget=forms.TextInput(attrs={'id': 'country', 'placeholder': 'Параметр'}))
    data_start = forms.CharField(widget=forms.TextInput(attrs={'id': 'date-start', 'placeholder': 'Параметр'}))
    data_end = forms.CharField(widget=forms.TextInput(attrs={'id': 'date-end', 'placeholder': 'Параметр'}))
    action_buy = forms.CharField(widget=forms.TextInput(attrs={'id': 'action-buy', 'placeholder': 'Параметр'}))
    CHOICES = [('strategy1', 'Стратегия 1'),
               ('strategy2', 'Стратегия 2'),
               ('strategy3', 'Стратегия 3'),
               ('strategy4', 'Стратегия 4')]
    Countries = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={'name': 'language'}))
