
class ReadOnlyFieldsMixin(object):
    readonly_fields = ()

    def __init__(self, *args, **kwargs):
        super(ReadOnlyFieldsMixin, self).__init__(*args, **kwargs)
        for field in (field for name, field in iter(self.fields.items()) if
                      name in self.readonly_fields):
            field.widget.attrs['disabled'] = 'true'
            field.required = False

    def clean(self):
        for f in self.readonly_fields:
            self.cleaned_data.pop(f, None)
        return super(ReadOnlyFieldsMixin, self).clean()