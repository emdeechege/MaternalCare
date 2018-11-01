from django.contrib.auth.models import User
from django.contrib.auth.models import User, AbstractBaseUser
from django.contrib import admin
from django.db import models
from django import forms
from datetime import datetime


# -- Location

class Location(models.Model):
    location = models.CharField(max_length=50)


class LocationAdmin(admin.ModelAdmin):
    search_fields = ('location',)


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        exclude = []
        fields = ()


# -- Patient


class Patient(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    id_number = models.CharField(max_length=8, unique=True)
    birthday = models.DateField()
    location = models.ForeignKey(Location)

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __unicode__(self):
        return f'{self.first_name} {self.last_name}'


class PatientAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)
    search_fields = ('first_name', 'last_name', 'id_number')
    list_display = ('__unicode__', 'birthday', 'id_number', )


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        exclude = ['user']

# --


class DoctorSpeciality(models.Model):
    specialty = models.CharField(max_length=30, primary_key=True)

    def __unicode__(self):
        return self.specialty

    class Meta:
        verbose_name_plural = 'Doctors specialties'


class DoctorSpecialityAdmin(admin.ModelAdmin):
    search_fields = ('specialty', )


class Doctor(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    specialty = models.ForeignKey(DoctorSpeciality)

    def __unicode__(self):
        return self.first_name + ' ' + self.last_name


class DoctorAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)
    search_fields = ('first_name', 'last_name', )
    list_filter = ('specialty',)
    list_display = ('__unicode__', 'specialty',)

# --


class MidWifeSpeciality(models.Model):
    specialty = models.CharField(max_length=60)

    def __unicode__(self):
        return self.specialty

    class Meta:
        verbose_name_plural = 'MidWifes specialties'


class MidWifeSpecialityAdmin(admin.ModelAdmin):
    search_fields = ('specialty', )


class MidWife(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    specialty = models.ForeignKey(MidWifeSpeciality)
    # degree_CHOICES = (
    #     ('A', 'Associate Degree in Nursing'),
    #     ('D', 'Diploma in Nursing'),
    #     ('L', 'Licensed Practical Nurse'),
    #     ('AD', 'Advanced practice registered nurses'),
    # )
    # degree = models.CharField(max_length=30, choices=degree_CHOICES)

    def __unicode__(self):
        return self.first_name + ' ' + self.last_name


class NurseAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)
    search_fields = ('first_name', )
    list_filter = ('specialty',)
    list_display = ('__unicode__', 'specialty')

# --


class Medication(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=500)
    grams = models.IntegerField()

    def __unicode__(self):
        return self.name


class MedicationsForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Medication
        exclude = []
        fields = ()


class MedicationAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_display = ('name', 'grams')
    form = MedicationsForm


class MedPrice(models.Model):
    date = models.DateTimeField()
    medication = models.ForeignKey(Medication)
    price = models.IntegerField()

    def __unicode__(self):
        return f'{self.medication.name} {self.date}'

    class Meta:
        verbose_name_plural = 'Medications Prices'


class MedPriceAdmin(admin.ModelAdmin):
    raw_id_fields = ('medication', )
    search_fields = ('medication', )
    list_display = ('medication', 'price', 'date')
    list_filter = ('date', )

# --


class Visit(models.Model):
    date = models.DateTimeField(auto_now_add=datetime.utcnow)
    patient = models.ForeignKey(Patient)
    doctor = models.ForeignKey(Doctor)
    comments = models.CharField(max_length=2000)

    def __unicode__(self):
        return f'{self.patient} {self.doctor}'


class VisitForm(forms.ModelForm):
    comments = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Visit
        exclude = []
        fields = ()


class VisitAdmin(admin.ModelAdmin):
    search_fields = ('patient__first_name', 'patient__last_name',
                     'doctor__user__first_name', 'doctor__user__last_name')
    raw_id_fields = ('patient', 'doctor')
    list_display = ('patient', 'doctor', 'date')
    list_display_links = ('patient', 'doctor')
    form = VisitForm

# --


class Prescription(models.Model):
    visit = models.ForeignKey(Visit)
    medication = models.ForeignKey(Medication)
    quantity = models.IntegerField()
    length = models.IntegerField()

    def __unicode__(self):
        return f'{self.visit} {self.visit} {self.visit}'

    def patient(self):
        return self.visit

    def doctor(self):
        return self.visit


class PrescriptionAdmin(admin.ModelAdmin):
    search_fields = ('medication__name', 'visit__patient__last_name', 'visit__patient__first_name',
                     'visit__doctor__user__last_name', 'visit__doctor__user__first_name')
    raw_id_fields = ('visit', 'medication', )
    list_display = ('patient', 'doctor', 'medication', 'quantity', 'length')
    list_display_links = ('patient', 'doctor', 'medication')

# --


class Department(models.Model):
    name = models.CharField(max_length=50)
    director = models.ForeignKey(User, null=True)
    staff = models.ManyToManyField(User, related_name='+')

    def __unicode__(self):
        return self.name


class DepartmentAdmin(admin.ModelAdmin):
    search_fields = ('name', 'director__last_name', 'director__first_name',)
    list_display = ('name', 'director', )
    raw_id_fields = ('director', )
    filter_horizontal = ('staff', )

# --


class Vaccine(models.Model):
    name = models.CharField(max_length=100)
    live = models.NullBooleanField()
    absorved = models.NullBooleanField()
    inactivated = models.NullBooleanField()
    oral = models.NullBooleanField()

    def __unicode__(self):
        return self.name


class VaccineAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_display = ('name', 'live', 'absorved', 'inactivated', 'oral')
    list_filter = ('live', 'absorved', 'inactivated', 'oral', )


class VaccineApplied(models.Model):
    date = models.DateTimeField()
    vaccine = models.ForeignKey(Vaccine)
    patient = models.ForeignKey(Patient)
    nurse = models.ForeignKey(MidWife)

    def __unicode__(self):
        return f'{self.patient} {self.nurse} {self.date}'

    class Meta:
        verbose_name_plural = 'Vaccines usage'


class VaccineAppliedAdmin(admin.ModelAdmin):
    search_fields = ('vaccine__name', 'patient__user__last_name', 'patient__user__first_name',
                     'nurse__user__last_name', 'nurse__user__first_name')
    list_display = ('patient', 'nurse', 'vaccine', 'date')
    raw_id_fields = ('patient', 'nurse', 'vaccine', )
    list_display_links = ('patient', 'nurse',)
