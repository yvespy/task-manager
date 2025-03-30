from django import forms

from dashboard.models import Worker, Position, Task


class SignUpForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    position = forms.ModelChoiceField(queryset=Position.objects.all(), required=True, initial=Position.objects.first(),
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Worker
        fields = ["username", "first_name", "last_name", "email", "position", "password"]

    def save(self, commit=True):
        worker = super().save(commit=False)
        if commit:
            worker.set_password(self.cleaned_data["password"])
            worker.save()
        return worker


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "deadline", "priority", "task_type", "assignees", ]
        widgets = {
            "deadline": forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Enter task name"
        })
        self.fields["description"].widget.attrs.update({"class": "form-control", "placeholder": "Describe your task"})
        self.fields["deadline"].widget.attrs.update({"class": "form-control", "type": "datetime-local"})
        self.fields["priority"].widget.attrs.update({"class": "form-select"})
        self.fields["task_type"].widget.attrs.update({"class": "form-control"})
        self.fields["assignees"].widget.attrs.update({"class": "form-control"})
