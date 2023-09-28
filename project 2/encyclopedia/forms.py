from django import forms


class CreateNewPage(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(
        attrs={'placeHolder': "Enter the article title",
               'class': 'my-custom-textarea',
               }))
    content = forms.CharField(label="", widget=forms.Textarea(
        attrs={'placeHolder': "Enter the text of the new article", 'cols': 10, 'rows': 5 , 'resize': None
               }))

class EditPage(forms.Form):
    content = forms.CharField(label="", widget=forms.Textarea(
        attrs={ 'cols': 10, 'rows': 5
               }))
