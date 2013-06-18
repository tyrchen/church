from django import forms
import requests
from church.models import Team
from settings import API_SERVER


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        exclude = ('created', 'updated', 'slug')
        widgets = {
            'members': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
        }

    def clean_members(self):
        data = self.cleaned_data['members']

        for uid in map(lambda x: x.strip(), data.split(',')):
            user = requests.get(API_SERVER + '/directory/employees/%s.json' % uid).json()
            if not user:
                raise forms.ValidationError("You have input the wrong alias %s!" % uid)
        return data
