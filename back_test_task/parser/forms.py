from django import forms

class CategorySearchForm(forms.Form):
    category = forms.CharField(label='Введите категорию', max_length=255)
    category_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    category_shard = forms.CharField(widget=forms.HiddenInput, required=False)
    category_query = forms.CharField(widget=forms.HiddenInput, required=False)