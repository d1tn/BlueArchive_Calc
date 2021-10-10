from django import forms
from commons.readcsv import *

class InputForm(forms.Form):
    charLv_From = forms.IntegerField(
            max_value = charLv["CurrentLv"].max(),
            min_value = charLv["CurrentLv"].min()
    )
    eqsFrom = eqLv[["CurrentLv","CurrentLv_text"]][:].dropna().to_numpy().tolist()
    eq1Lv_From = forms.fields.ChoiceField(
        choices = eqsFrom
    )
    eq2Lv_From = forms.fields.ChoiceField(
        choices = eqsFrom
    )
    eq3Lv_From = forms.fields.ChoiceField(
        choices = eqsFrom
    )
    exLv_From = forms.IntegerField(
            max_value = exLv["CurrentLv"].max(),
            min_value = exLv["CurrentLv"].min()
    )
    nsLv_From = forms.IntegerField(
            max_value = sklLv["CurrentLv"].max(),
            min_value = sklLv["CurrentLv"].min()
    )
    psLv_From = forms.IntegerField(
            max_value = sklLv["CurrentLv"].max(),
            min_value = sklLv["CurrentLv"].min()
    )
    ssLv_From = forms.IntegerField(
            max_value = sklLv["CurrentLv"].max(),
            min_value = sklLv["CurrentLv"].min()
    )

    charLv_To = forms.IntegerField(
            max_value = charLv["NextLv"].max(),
            min_value = charLv["NextLv"].min()
    )
    eqsTo = eqLv[["NextLv","NextLv_text"]][:].dropna().to_numpy().tolist()
    eq1Lv_To = forms.fields.ChoiceField(
        choices = eqsTo
    )
    eq2Lv_To = forms.fields.ChoiceField(
        choices = eqsTo
    )
    eq3Lv_To = forms.fields.ChoiceField(
        choices = eqsTo
    )
    exLv_To = forms.IntegerField(
            max_value = exLv["NextLv"].max(),
            min_value = exLv["NextLv"].min()
    )
    nsLv_To = forms.IntegerField(
            max_value = sklLv["NextLv"].max(),
            min_value = sklLv["NextLv"].min()
    )
    psLv_To = forms.IntegerField(
            max_value = sklLv["NextLv"].max(),
            min_value = sklLv["NextLv"].min()
    )
    ssLv_To = forms.IntegerField(
            max_value = sklLv["NextLv"].max(),
            min_value = sklLv["NextLv"].min()
    )
