from django import forms

from dashboard.models import Worker, Position


class SignUpForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    position = forms.ModelChoiceField(queryset=Position.objects.all(), required=True, initial=Position.objects.first(), widget=forms.Select(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Worker
        fields = ["username", "first_name", "last_name" ,"email", "position", "password"]

    def save(self, commit=True):
        worker = super().save(commit=False)
        if commit:
            worker.set_password(self.cleaned_data["password"])
            worker.save()
        return worker
