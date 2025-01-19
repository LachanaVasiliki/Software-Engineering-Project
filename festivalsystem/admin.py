# Εγγραφή μοντέλων στο admin panel του Django

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import gettext_lazy as _
from .models import User, Festival, Track, Organizer, Artist, Reviewer, Perfomance, Review

admin.site.register(User)
# Διαμόρφωση της εμφάνισης του μοντέλου User στο admin
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

class FestivalAdminForm(forms.ModelForm):
    class Meta:
        model = Festival
        fields = '__all__'
        widgets = {
            'organizers': forms.ModelMultipleChoiceField,
        }
        

    organizers = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(verbose_name='Users', is_stacked=False),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['organizers'].initial = self.instance.organizer_set.values_list('user', flat=True)

    def save(self, commit=True):

        instance = super().save(commit=False)
        instance.save()

        selected_users = self.cleaned_data.get('organizers', [])
        organizers = Organizer.objects.filter(user__in=selected_users, festivals=instance)
        existing_organizers = set(organizers.values_list('user', flat=True))
        new_organizers = []

        for user in selected_users:
            if user not in existing_organizers:
                organizer, created = Organizer.objects.get_or_create(user=user)
                organizer.festivals.add(instance)
                new_organizers.append(organizer)

        organizers = Organizer.objects.filter(pk__in=[organizer.pk for organizer in organizers])
        new_organizers = Organizer.objects.filter(pk__in=[organizer.pk for organizer in new_organizers])

        for organizer in organizers.union(new_organizers):
            organizer.festivals.add(instance)

        return instance
    
    def get_organizers(self, obj):
        organizers = obj.organizers.all()
        return ', '.join(str(organizer) for organizer in organizers)
    
    get_organizers.short_description = 'Organizers'


class FestivalAdmin(admin.ModelAdmin):
    form = FestivalAdminForm

admin.site.register(Festival, FestivalAdmin)
admin.site.register(Track)
admin.site.register(Artist)
admin.site.register(Organizer)
admin.site.register(Reviewer)
admin.site.register(Perfomance)
admin.site.register(Review)