from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.contrib.auth.models import User, AbstractBaseUser
from django.contrib import admin
from django.db import models
from django import forms
from datetime import datetime
from datetime import date, datetime
from django.utils import timezone
import numpy as np
import pandas as pd
from itertools import groupby


TIME_CHOICES = (
    ('6', '6:00 am'),
    ('7', '7:00 am'),
    ('8', '8:00 am'),
    ('9', '9:00 am'),
    ('10', '10:00 am'),
    ('11', '11:00 am'),
    ('12', '12:00 am'),
    ('13', '1:00 pm'),
    ('14', '2:00 pm'),
    ('15', '3:00 pm'),
    ('16', '4:00 pm'),
    ('17', '5:00 pm'),
    ('18', '6:00 pm'),
)


days = ['Monday', 'Tuesday', 'Wednesday',
        'Thursday', 'Friday', 'Saturday', 'Sunday']
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

    def __str__(self):
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
    photo = models.FileField(
        upload_to='images', default='default.jpg', null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    specialty = models.ForeignKey(DoctorSpeciality, null=True)
    consultation_fee = models.FloatField(default=0, null=True)

    @classmethod
    def create_doctor(cls, user, fee):
        cls.objects.create(user=user, consultation_fee=fee)
        
    def make_appointments(self):
        days = pd.date_range('2012-05-25', '2012-06-27', freq='D')
        appointments = []
        for day in days:
            app = Appointment.objects.create(doctor=self, day=day)
            appointments.append(app)
        return appointments

    @property
    def booked_slots(self):
        apps = list(self.appointments.all().order_by('day'))
        objects = []
        for k, v in groupby(apps, lambda x: x.day):
            objects.append(list(v))
        return objects

    @property
    def booked_days(self):
        apps = list(self.appointments.all().order_by('day'))
        ls = []
        for k, v in groupby(apps, lambda x: x.day):
            ls.append(k)
        return ls

    @property
    def all_appointments(self):
        return self.appointments.all().order_by('day')

    @property
    def full_name(self):
        return f'Dr.{self.first_name.capitalize()} {self.last_name.capitalize()}'

    @classmethod
    def search_doctors_by_term(cls, search_term):
        by_first_name = cls.objects.filter(first_name__icontains=search_term)
        by_last_name = cls.objects.filter(last_name__icontains=search_term)
        search_results = list(by_first_name) + list(by_last_name)
        return search_results

    @classmethod
    def get_one_doctor(cls, doctor_id):
        user = User.objects.get(pk=doctor_id)
        return cls.objects.get(pk=user)

    @classmethod
    def get_all_doctors(cls):
        return cls.objects.all()

    def patients(self):
        return Patient.doctor_patients(self)

    def delete_doctor(self):
        self.delete()


    def average_service(self):
        service_ratings = list(
            map(lambda x: x.service_rating, self.reviews.all()))
        return np.mean(service_ratings)

    def average_professionalism(self):
        professionalism_ratings = list(
            map(lambda x: x.professionalism_rating, self.reviews.all()))
        return np.mean(professionalism_ratings)

    def average_friendliness(self):
        friendliness_ratings = list(
            map(lambda x: x.friendliness_rating, self.reviews.all()))
        return np.mean(friendliness_ratings)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        exclude = ['user']


class DoctorAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)
    list_display = ('first_name', 'last_name', )
    list_filter = ('specialty',)
    list_display = ('__str__', 'specialty',)

# --


class DoctorProfile(models.Model):
    doctor = models.OneToOneField(
        Doctor, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=100)
    score = models.IntegerField(default=0)
    registration_number = models.CharField(max_length=100)
    registration_date = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)  
    facility = models.CharField(max_length=100)
    postal_address = models.CharField(max_length=100)
    speciality = models.CharField(max_length=100)
    sub_speciality = models.CharField(max_length=100)
    qualifications = models.CharField(max_length=100)


class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        exclude = ['doctor']



# --

class DoctorWorkingHours(models.Model):
    doctor = models.OneToOneField(
        Doctor, on_delete=models.CASCADE, related_name='working_hours')
    working_from = models.CharField(max_length=20, choices=TIME_CHOICES)
    working_to = models.CharField(max_length=20, choices=TIME_CHOICES)

    @property
    def appointment_slots(self):
        start = self.working_from
        end = self.working_to
        ls = list(range(int(start), int(end)))
        dc = {6: '6:00 am', 7: '7:00 am', 8: '8:00 am', 9: '9:00 am', 10: '10:00 am', 11: '11:00 am',
              12: '12:00 am', 13: '1:00 pm', 14: '2:00 pm', 15: '3:00 pm', 16: '4:00 pm', 17: '5:00 pm', 18: '6:00 pm'}
        slots = []
        for i in ls:
            slots.append(dc.get(i))
        return slots

    def __str__(self):
        return f'from-{self.working_from} to-{self.working_to}'


class DoctorWorkingHoursForm(forms.ModelForm):
    class Meta:
        model = DoctorWorkingHours
        exclude = ['doctor']


class DoctorWorkingHoursAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'working_from', 'working_to',)


# -- Patient


class Patient(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    photo = models.FileField(
        upload_to='images', default='default.jpg', null=True)
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

    @classmethod
    def get_patient(cls, pt):
        return cls.objects.get(user=pt)

    def save_patient(self, user):
        self.user = user
        self.save()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class PatientAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)
    search_fields = ('first_name', 'last_name', 'id_number')
    list_display = ('__str__', 'birthday', 'id_number', )


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        exclude = ['user', 'doctors']

# --


class Appointment(models.Model):
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name='appointments', null=True)
    day = models.DateField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    time_slot = models.CharField(max_length=20, choices=TIME_CHOICES, null=True)
    is_booked = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)

    @property
    def complete_appointment(self):
        self.is_completed = True
        self.save()

    @classmethod
    def book_appointment(cls, appointment, doctor, patient):
        # appointment = cls.objects.get(appointment_id)
        appointment.doctor = doctor
        appointment.patient = patient
        appointment.booked = True
        appointment.save()

    def __str__(self):
        return f'{self.doctor} {self.patient} {self.time_slot}'


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        exclude = ['doctor', 'patient', ]


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'day', 'patient', 'time_slot',
                    'is_booked', 'is_completed',)


# --


class AppointmentDetails(models.Model):
    appointment = models.ForeignKey(
        Appointment, on_delete=models.CASCADE, related_name='details')
    notes = models.TextField()


class AppointmentDetailsForm(forms.ModelForm):
    class Meta:
        model = AppointmentDetails
        exclude = ['appointment']


class AppointmentDetailsAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'notes',)


# --


class MidWifeSpeciality(models.Model):
    specialty = models.CharField(max_length=60)

    def __str__(self):
        return self.specialty

    class Meta:
        verbose_name_plural = 'MidWifes specialties'


class MidWifeSpecialityAdmin(admin.ModelAdmin):
    search_fields = ('specialty', )


class MidWife(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    photo = models.FileField(
        upload_to='images', default='default.jpg', null=True)
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

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class MidWifeAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)
    search_fields = ('first_name', )
    list_filter = ('specialty',)
    list_display = ('__str__', 'specialty')

# --


class Medication(models.Model):
    image = models.FileField(
        upload_to='images', default='default.jpg', null=True)
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.PositiveIntegerField(default=0)
    grams = models.IntegerField(default=0)

    def __str__(self):
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

    def __str__(self):
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

    def __str__(self):
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

    def __str__(self):
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

    def __str__(self):
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

    def __str__(self):
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

    def __str__(self):
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

    class Meta:
        verbose_name_plural = 'Doctor reviews'

    doctor = models.ForeignKey(Doctor, null=True)
    patient = models.ForeignKey(Patient, null=True)
    review = models.TextField()

    def __str__(self):
        return self.review


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


class Posts(models.Model):
    title = models.CharField(max_length=300)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=datetime.utcnow)
    posted_by = models.ForeignKey(User, null=True)

    @property
    def all_comments(self):
        return self.comments.all()[:5][::-1]

    def save_posts(self):
        self.save()

    def __str__(self):
        return self.title


class Comment(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(
        Posts, on_delete=models.CASCADE, related_name='comments', null=True)
    comment = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.comment

    def save_comment(self):
        self.save()

    @classmethod
    def get_comment(cls):
        comment = Comment.objects.all()
        return comment
