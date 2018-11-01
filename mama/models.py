from django.contrib.auth.models import User
from django.contrib.auth.models import User, AbstractBaseUser
from django.contrib import admin
from django.db import models
from django import forms
from datetime import datetime


# -- Location

class Location(models.Model):
    location = models.CharField(max_length=50)

    def delete_location(self):
        return self.delete()

    def __str__(self):
        return self.location


class LocationAdmin(admin.ModelAdmin):
    search_fields = ('location',)


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        exclude = []
        fields = ()


# -- Doctor classes


class DoctorSpeciality(models.Model):
    specialty = models.CharField(max_length=30, primary_key=True)

    def __unicode__(self):
        return self.specialty

    class Meta:
        verbose_name_plural = 'Doctors specialties'


class DoctorSpecialityAdmin(admin.ModelAdmin):
    search_fields = ('specialty', )


class DoctorSpecialityForm(forms.ModelForm):
    class Meta:
        model = DoctorSpeciality
        exclude = []


class Doctor(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    photo = models.FileField(upload_to='images', null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    specialty = models.ForeignKey(DoctorSpeciality)

    def patients(self):
        return Patient.doctor_patients(self)

    def delete_doctor(self):
        self.delete()

    def save_doctor(self, user):
        self.user = user
        self.save()

    def __unicode__(self):
        return self.first_name + ' ' + self.last_name


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        exclude = ['user']


class DoctorAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)
    list_display = ('first_name', 'last_name', )
    list_filter = ('specialty',)
    list_display = ('__unicode__', 'specialty',)


# -- Patient


class Patient(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    photo = models.FileField(upload_to='images', null=True)
    doctors = models.ManyToManyField(Doctor)
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

    @classmethod
    def doctor_patients(cls, doctor):
        return cls.objects.filter(doctor=doctor)

    def save_patient(self, user):
        self.user = user
        self.save()

    def __unicode__(self):
        return f'{self.first_name} {self.last_name}'


class PatientAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)
    search_fields = ('first_name', 'last_name', 'id_number')
    list_display = ('__unicode__', 'birthday', 'id_number', )


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        exclude = ['user', 'doctors']

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
    photo = models.FileField(upload_to='images', null=True)
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


class MidWifeAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)
    search_fields = ('first_name', )
    list_filter = ('specialty',)
    list_display = ('__unicode__', 'specialty')

# --


class Medication(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    grams = models.IntegerField()

    def __unicode__(self):
        return self.name


class MedicationsForm(forms.ModelForm):

    class Meta:
        model = Medication
        exclude = []


class MedicationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    form = MedicationsForm


class MedPrice(models.Model):
    date = models.DateTimeField(auto_now_add=datetime.utcnow)
    medication = models.ForeignKey(Medication, related_name='medication')
    price = models.IntegerField()

    @property
    def med_name(self):
        return self.medication.name

    def __unicode__(self):
        return f'{self.medication} {self.price}'

    class Meta:
        verbose_name_plural = 'Medications Prices'


class MedPriceForm(forms.ModelForm):
    class Meta:
        model = MedPrice
        exclude = []


class MedPriceAdmin(admin.ModelAdmin):
    raw_id_fields = ('medication', )
    search_fields = ('medication', )
    list_display = ('med_name', 'price', 'date')
    list_filter = ('date', )
    form = MedPriceForm

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
        exclude = ['date']
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


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        exclude = ['visit']


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


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        exclude = []


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


class VaccineForm(forms.ModelForm):
    class Meta:
        model = Vaccine
        exclude = []


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


# -- DoctorReview

class DoctorReview(models.Model):
    doctor = models.ForeignKey(Doctor, null=True)
    patient = models.ForeignKey(Patient, null=True)
    review = models.TextField()

    def __str__(self):
        return self.review

    class Meta:
        verbose_name_plural = 'Doctor reviews'


class DoctorReviewAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'review')


class DoctorReviewForm(forms.ModelForm):
    class Meta:
        model = DoctorReview
        exclude = ['doctor', 'patient']


# -- Live Chat

class LiveChat(models.Model):
    doctor = models.ForeignKey(Doctor, null=True)
    patient = models.ForeignKey(Patient, null=True)
    time = models.DateTimeField(auto_now_add=datetime.utcnow)
    review = models.TextField()
    pinned_message = models.BooleanField(default=False)

    def delete_message(self):
        self.delete()

    def pin_message(self):
        self.pinnned_message = True
        self.save()

    def __str__(self):
        return self.review


class LiveChatAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'review')


class LiveChatForm(forms.ModelForm):
    class Meta:
        model = LiveChat
        exclude = ['doctor', 'patient']
