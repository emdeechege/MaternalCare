
# from django.contrib.auth.models import User, AbstractBaseUser
# from datetime import datetime
# from django import forms
# from django.db import models
# from django.contrib import admin
# class Allergy(models.Model):
#     allergy = models.CharField(max_length=50)


# class File(models.Model):
#     file = models.FileField(upload_to='files', null=True)


# class Category(models.Model):
#     category = models.CharField(max_length=50)


# class Medicine(models.Model):
#     category = models.ForeignKey(Category, related_name='medicines', null=True)
#     medicine_name = models.CharField(max_length=50)


# class DoctorSpeciality(models.Model):
#     specialty = models.CharField(max_length=30, primary_key=True)

#     def __unicode__(self):
#         return self.specialty

#     class Meta:
#         verbose_name_plural = 'Dofrom django.contrib.auth.models import User


# # -- Location

# class Location(models.Model):
#     location = models.CharField(max_length=50)


# class LocationAdmin(admin.ModelAdmin):
#     search_fields = ('location',)


# class LocationForm(forms.Form):
#     class Meta:
#         model = Location
#         exclude = []


# # -- Patient


# class Patient(models.Model):
#     user = models.OneToOneField(User, primary_key=True)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     id_number = models.CharField(max_length=8, unique=True)
#     birthday = models.DateField()
#     location = models.ForeignKey(Location)

#     GENDER_CHOICES = (
#         ('M', 'Male'),
#         ('F', 'Female'),
#     )
#     gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

#     def __unicode__(self):
#         return f'{self.first_name} {self.last_name}'


# class PatientAdmin(admin.ModelAdmin):
#     raw_id_fields = ('user',)
#     search_fields = ('first_name', 'last_name', 'id_number')
#     list_display = ('__unicode__', 'birthday', 'id_number', )


# class PatientForm(forms.ModelForm):
#     class Meta:
#         model = Patient
#         excclude = ['user', ]

# # --


# class DoctorSpeciality(models.Model):
#     specialty = models.CharField(max_length=30, primary_key=True)

#     def __unicode__(self):
#         return self.specialty

#     class Meta:
#         verbose_name_plural = 'Doctors specialties'


# class DoctorSpecialityAdmin(admin.ModelAdmin):
#     search_fields = ('specialty', )


# class Doctor(models.Model):
#     user = models.OneToOneField(User, primary_key=True)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     specialty = models.ForeignKey(DoctorSpeciality)

#     def __unicode__(self):
#         return self.first_name + ' ' + self.last_name


# class DoctorAdmin(admin.ModelAdmin):
#     raw_id_fields = ('user',)
#     search_fields = ('first_name', 'last_name', )
#     list_filter = ('specialty',)
#     list_display = ('__unicode__', 'specialty',)

# # --


# class MidWifeSpeciality(models.Model):
#     specialty = models.CharField(max_length=60)

#     def __unicode__(self):
#         return self.specialty

#     class Meta:
#         verbose_name_plural = 'MidWifes specialties'


# class MidWifeSpecialityAdmin(admin.ModelAdmin):
#     search_fields = ('specialty', )


# class MidWife(models.Model):
#     user = models.OneToOneField(User, primary_key=True)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     specialty = models.ForeignKey(MidWifeSpeciality)
#     # degree_CHOICES = (
#     #     ('A', 'Associate Degree in Nursing'),
#     #     ('D', 'Diploma in Nursing'),
#     #     ('L', 'Licensed Practical Nurse'),
#     #     ('AD', 'Advanced practice registered nurses'),
#     # )
#     # degree = models.CharField(max_length=30, choices=degree_CHOICES)

#     def __unicode__(self):
#         return self.first_name + ' ' + self.last_name


# class NurseAdmin(admin.ModelAdmin):
#     raw_id_fields = ('user',)
#     search_fields = ('first_name', )
#     list_filter = ('specialty',)
#     list_display = ('__unicode__', 'specialty')

# # --


# class Medication(models.Model):
#     name = models.CharField(max_length=150)
#     description = models.CharField(max_length=500)
#     grams = models.IntegerField()

#     def __unicode__(self):
#         return self.name


# class MedicationsForm(forms.ModelForm):
#     description = forms.CharField(widget=forms.Textarea)

#     class Meta:
#         model = Medication


# class MedicationAdmin(admin.ModelAdmin):
#     search_fields = ('name', )
#     list_display = ('name', 'grams')
#     form = MedicationsForm


# class MedPrice(models.Model):
#     date = models.DateTimeField()
#     medication = models.ForeignKey(Medication)
#     price = models.IntegerField()

#     def __unicode__(self):
#         return f'{self.medication.name} {self.date}'

#     class Meta:
#         verbose_name_plural = 'Medications Prices'


# class MedPriceAdmin(admin.ModelAdmin):
#     raw_id_fields = ('medication', )
#     search_fields = ('medication', )
#     list_display = ('medication', 'price', 'date')
#     list_filter = ('date', )

# # --


# class Visit(models.Model):
#     date = models.DateTimeField(auto_now_add=datetime.utcnow)
#     patient = models.ForeignKey(Patient)
#     doctor = models.ForeignKey(Doctor)
#     comments = models.CharField(max_length=2000)

#     def __unicode__(self):
#         return f'{self.patient} {self.doctor}'


# class VisitForm(forms.ModelForm):
#     comments = forms.CharField(widget=forms.Textarea)

#     class Meta:
#         model = Visit


# class VisitAdmin(admin.ModelAdmin):
#     search_fields = ('patient__first_name', 'patient__last_name',
#                      'doctor__user__first_name', 'doctor__user__last_name')
#     raw_id_fields = ('patient', 'doctor')
#     list_display = ('patient', 'doctor', 'date')
#     list_display_links = ('patient', 'doctor')
#     form = VisitForm

# # --


# class Prescription(models.Model):
#     visit = models.ForeignKey(Visit)
#     medication = models.ForeignKey(Medication)
#     quantity = models.IntegerField()
#     length = models.IntegerField()

#     def __unicode__(self):
#         return '%s | Prescribed by: %s (%s)' % (self.visit.patient, self.visit.doctor, self.visit.date)

#     def patient(self):
#         return self.visit.patient

#     def doctor(self):
#         return self.visit.patient


# class PrescriptionAdmin(admin.ModelAdmin):
#     search_fields = ('medication__name', 'visit__patient__last_name', 'visit__patient__first_name',
#                      'visit__doctor__user__last_name', 'visit__doctor__user__first_name')
#     raw_id_fields = ('visit', 'medication', )
#     list_display = ('patient', 'doctor', 'medication', 'quantity', 'length')
#     list_display_links = ('patient', 'doctor', 'medication')

# # --


# class Department(models.Model):
#     name = models.CharField(max_length=50)
#     director = models.ForeignKey(User, null=True)
#     staff = models.ManyToManyField(User, related_name='+')

#     def __unicode__(self):
#         return self.name


# class DepartmentAdmin(admin.ModelAdmin):
#     search_fields = ('name', 'director__last_name', 'director__first_name',)
#     list_display = ('name', 'director', )
#     raw_id_fields = ('director', )
#     filter_horizontal = ('staff', )

# # --


# class Vaccine(models.Model):
#     name = models.CharField(max_length=100)
#     live = models.NullBooleanField()
#     absorved = models.NullBooleanField()
#     inactivated = models.NullBooleanField()
#     oral = models.NullBooleanField()

#     def __unicode__(self):
#         return self.name


# class VaccineAdmin(admin.ModelAdmin):
#     search_fields = ('name', )
#     list_display = ('name', 'live', 'absorved', 'inactivated', 'oral')
#     list_filter = ('live', 'absorved', 'inactivated', 'oral', )


# class VaccineApplied(models.Model):
#     date = models.DateTimeField()
#     vaccine = models.ForeignKey(Vaccine)
#     patient = models.ForeignKey(Patient)
#     nurse = models.ForeignKey(Nurse)

#     def __unicode__(self):
#         return '%s | by  %s (%s)' % (self.patient, self.nurse, self.date)

#     class Meta:
#         verbose_name_plural = 'Vaccines usage'


# class VaccineAppliedAdmin(admin.ModelAdmin):
#     search_fields = ('vaccine__name', 'patient__user__last_name', 'patient__user__first_name',
#                      'nurse__user__last_name', 'nurse__user__first_name')
#     list_display = ('patient', 'nurse', 'vaccine', 'date')
#     raw_id_fields = ('patient', 'nurse', 'vaccine', )
#     list_display_links = ('patient', 'nurse',)


# ctors specialties'


# class Doctor(models.Model):
#     name = models.CharField(max_length=100)
#     national_id_no = models.IntegerField(default=00000000)
#     registration_no = models.IntegerField(default=00000)
#     hospital_name = models.CharField(max_length=100)
#     yearsofexperience = models.PositiveIntegerField()
#     speciality = models.ForeignKey(
#         DoctorSpeciality, null=True, related_name='speciality')
#     works_from = models.TimeField()
#     works_to = models.TimeField()

#     certification_CHOICES = (
#         ('A', 'American Board'),
#         ('B', 'Bachelor'),
#     )
#     certification = models.CharField(
#         max_length=30, choices=certification_CHOICES)

#     @property
#     def working_hours(self):
#         return self.works_to - self.works_from


#        user = models.OneToOneField(User, primary_key=True)
#        specialty = models.ForeignKey(DoctorSpeciality)
#        certification = models.CharField(
#            max_length=30, choices=certification_CHOICES)


# def create_user_doctor(sender, instance, created, **kwargs):
#        if created:
#            Doctor.objects.create(user=instance)

#    post_save.connect(create_user_doctor, sender=User)

#    def save_doctor(self):
#        self.save()

#    def delete_doctor(self):
#        self.delete()

#    @classmethod
#    def search_doctor(cls, search_term):
#        doctor = cls.objects.filter(user__username__icontains=search_term)
#        return doctors


# class Patient(models.Model):
#     GENDER_CHOICES = (
#         ((1), ('male')),
#         ((2), ('female')),)
#     name = models.TextField(max_length=200, null=True, blank=True, default=0)
#     date_of_birth = models.DateField(null=True)
#     bio = models.TextField(max_length=200, null=True,
#                            blank=True, default="bio")
#     maternity_status = models.DateTimeField(auto_now_add=True)
#     medicines = models.ForeignKey(Medicine, null=True)
#     next_of_kin = models.CharField(max_length=50, default='John/Jane Doe')
#     phone = models.IntegerField(null=True, blank=True)
#     number_of_children = models.IntegerField(null=True, blank=True)
#     gender_of_child = models.IntegerField(choices=GENDER_CHOICES, default=0)
#     profession = models.TextField(
#         max_length=200, null=True, blank=True, default="patient")
#     health_insurance_number = models.IntegerField(null=True, blank=True)
#     copy_of_identification = models.ImageField(
#         upload_to='identification/', null=True, blank=True, default=0)
#     user = models.OneToOneField(
#         User, on_delete=models.CASCADE, null=True, related_name="profile")
#     doctor = models.ForeignKey(Doctor, null=True)
#     email = models.TextField(max_length=200, null=True,
#                              blank=True, default=0)

#     def create_user_patient(self, sender, instance, created, **kwargs):
#         if created:
#             Patient.objects.create(user=instance)

#     # post_save.connect(create_user_patient, sender=User)

#     def save_patient(self):
#         self.save()

#     def delete_patient(self):
#         self.delete()

#     @classmethod
#     def search_patients(cls, search_term):
#         patients = cls.objects.filter(user__username__icontains=search_term)
#         return patients

#     @property
#     def copy_of_identification_url(self):
#         if self.copy_of_identification and hasattr(self.copy_of_identification, 'url'):
#             return self.copy_of_identification.url

#     def __str__(self):
#         return self.name


# class Record(models.Model):
#     patient = models.ForeignKey(Patient, null=True)
#     patient_id = models.IntegerField(default=00000000, null=True)
#     weight = models.IntegerField(default=0, null=True)
#     age = models.IntegerField(default=0, null=True)
#     height = models.IntegerField(default=0, null=True)
#     medical_history = models.TextField(
#         help_text='Enter patients medical history', null=True)
#     blood_pressure = models.IntegerField(default=0, null=True)
#     blood_type = models.CharField(max_lenght=15, null=True)
#     allergies = models.ForeignKey(Allergy, related_name='allergies', null=True)
#     files = models.ForeignKey(File, related_name='files', null=True)

#     def save_record(self):
#         self.save()


# class Comment(models.Model):
#     patient = models.ForeignKey(Patient, null=True)
#     doctor = models.ForeignKey(Doctor, null=True)

# from django.contrib.auth.models import User
# from django.contrib.auth.models import User, AbstractBaseUser
# from django.contrib import admin
# from django.db import models
# from django import forms
# from datetime import datetime


# # -- Location

# class Location(models.Model):
#     location = models.CharField(max_length=50)


# class LocationAdmin(admin.ModelAdmin):
#     search_fields = ('location',)


# class LocationForm(forms.Form):
#     class Meta:
#         model = Location
#         exclude = []


# # -- Patient


# class Patient(models.Model):
#     user = models.OneToOneField(User, primary_key=True)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     id_number = models.CharField(max_length=8, unique=True)
#     birthday = models.DateField()
#     location = models.ForeignKey(Location)

#     GENDER_CHOICES = (
#         ('M', 'Male'),
#         ('F', 'Female'),
#     )
#     gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

#     def __unicode__(self):
#         return f'{self.first_name} {self.last_name}'


# class PatientAdmin(admin.ModelAdmin):
#     raw_id_fields = ('user',)
#     search_fields = ('first_name', 'last_name', 'id_number')
#     list_display = ('__unicode__', 'birthday', 'id_number', )


# class PatientForm(forms.ModelForm):
#     class Meta:
#         model = Patient
#         excclude = ['user', ]

# # --


# class DoctorSpeciality(models.Model):
#     specialty = models.CharField(max_length=30, primary_key=True)

#     def __unicode__(self):
#         return self.specialty

#     class Meta:
#         verbose_name_plural = 'Doctors specialties'


# class DoctorSpecialityAdmin(admin.ModelAdmin):
#     search_fields = ('specialty', )


# class Doctor(models.Model):
#     user = models.OneToOneField(User, primary_key=True)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     specialty = models.ForeignKey(DoctorSpeciality)

#     def __unicode__(self):
#         return self.first_name + ' ' + self.last_name


# class DoctorAdmin(admin.ModelAdmin):
#     raw_id_fields = ('user',)
#     search_fields = ('first_name', 'last_name', )
#     list_filter = ('specialty',)
#     list_display = ('__unicode__', 'specialty',)

# # --


# class MidWifeSpeciality(models.Model):
#     specialty = models.CharField(max_length=60)

#     def __unicode__(self):
#         return self.specialty

#     class Meta:
#         verbose_name_plural = 'MidWifes specialties'


# class MidWifeSpecialityAdmin(admin.ModelAdmin):
#     search_fields = ('specialty', )


# class MidWife(models.Model):
#     user = models.OneToOneField(User, primary_key=True)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     specialty = models.ForeignKey(MidWifeSpeciality)
#     # degree_CHOICES = (
#     #     ('A', 'Associate Degree in Nursing'),
#     #     ('D', 'Diploma in Nursing'),
#     #     ('L', 'Licensed Practical Nurse'),
#     #     ('AD', 'Advanced practice registered nurses'),
#     # )
#     # degree = models.CharField(max_length=30, choices=degree_CHOICES)

#     def __unicode__(self):
#         return self.first_name + ' ' + self.last_name


# class NurseAdmin(admin.ModelAdmin):
#     raw_id_fields = ('user',)
#     search_fields = ('first_name', )
#     list_filter = ('specialty',)
#     list_display = ('__unicode__', 'specialty')

# # --


# class Medication(models.Model):
#     name = models.CharField(max_length=150)
#     description = models.CharField(max_length=500)
#     grams = models.IntegerField()

#     def __unicode__(self):
#         return self.name


# class MedicationsForm(forms.ModelForm):
#     description = forms.CharField(widget=forms.Textarea)

#     class Meta:
#         model = Medication


# class MedicationAdmin(admin.ModelAdmin):
#     search_fields = ('name', )
#     list_display = ('name', 'grams')
#     form = MedicationsForm


# class MedPrice(models.Model):
#     date = models.DateTimeField()
#     medication = models.ForeignKey(Medication)
#     price = models.IntegerField()

#     def __unicode__(self):
#         return f'{self.medication.name} {self.date}'

#     class Meta:
#         verbose_name_plural = 'Medications Prices'


# class MedPriceAdmin(admin.ModelAdmin):
#     raw_id_fields = ('medication', )
#     search_fields = ('medication', )
#     list_display = ('medication', 'price', 'date')
#     list_filter = ('date', )

# # --


# class Visit(models.Model):
#     date = models.DateTimeField(auto_now_add=datetime.utcnow)
#     patient = models.ForeignKey(Patient)
#     doctor = models.ForeignKey(Doctor)
#     comments = models.CharField(max_length=2000)

#     def __unicode__(self):
#         return f'{self.patient} {self.doctor}'


# class VisitForm(forms.ModelForm):
#     comments = forms.CharField(widget=forms.Textarea)

#     class Meta:
#         model = Visit


# class VisitAdmin(admin.ModelAdmin):
#     search_fields = ('patient__first_name', 'patient__last_name',
#                      'doctor__user__first_name', 'doctor__user__last_name')
#     raw_id_fields = ('patient', 'doctor')
#     list_display = ('patient', 'doctor', 'date')
#     list_display_links = ('patient', 'doctor')
#     form = VisitForm

# # --


# class Prescription(models.Model):
#     visit = models.ForeignKey(Visit)
#     medication = models.ForeignKey(Medication)
#     quantity = models.IntegerField()
#     length = models.IntegerField()

#     def __unicode__(self):
#         return '%s | Prescribed by: %s (%s)' % (self.visit.patient, self.visit.doctor, self.visit.date)

#     def patient(self):
#         return self.visit.patient

#     def doctor(self):
#         return self.visit.patient


# class PrescriptionAdmin(admin.ModelAdmin):
#     search_fields = ('medication__name', 'visit__patient__last_name', 'visit__patient__first_name',
#                      'visit__doctor__user__last_name', 'visit__doctor__user__first_name')
#     raw_id_fields = ('visit', 'medication', )
#     list_display = ('patient', 'doctor', 'medication', 'quantity', 'length')
#     list_display_links = ('patient', 'doctor', 'medication')

# # --


# class Department(models.Model):
#     name = models.CharField(max_length=50)
#     director = models.ForeignKey(User, null=True)
#     staff = models.ManyToManyField(User, related_name='+')

#     def __unicode__(self):
#         return self.name


# class DepartmentAdmin(admin.ModelAdmin):
#     search_fields = ('name', 'director__last_name', 'director__first_name',)
#     list_display = ('name', 'director', )
#     raw_id_fields = ('director', )
#     filter_horizontal = ('staff', )

# # --


# class Vaccine(models.Model):
#     name = models.CharField(max_length=100)
#     live = models.NullBooleanField()
#     absorved = models.NullBooleanField()
#     inactivated = models.NullBooleanField()
#     oral = models.NullBooleanField()

#     def __unicode__(self):
#         return self.name


# class VaccineAdmin(admin.ModelAdmin):
#     search_fields = ('name', )
#     list_display = ('name', 'live', 'absorved', 'inactivated', 'oral')
#     list_filter = ('live', 'absorved', 'inactivated', 'oral', )


# class VaccineApplied(models.Model):
#     date = models.DateTimeField()
#     vaccine = models.ForeignKey(Vaccine)
#     patient = models.ForeignKey(Patient)
#     nurse = models.ForeignKey(Nurse)

#     def __unicode__(self):
#         return '%s | by  %s (%s)' % (self.patient, self.nurse, self.date)

#     class Meta:
#         verbose_name_plural = 'Vaccines usage'


# class VaccineAppliedAdmin(admin.ModelAdmin):
#     search_fields = ('vaccine__name', 'patient__user__last_name', 'patient__user__first_name',
#                      'nurse__user__last_name', 'nurse__user__first_name')
#     list_display = ('patient', 'nurse', 'vaccine', 'date')
#     raw_id_fields = ('patient', 'nurse', 'vaccine', )
#     list_display_links = ('patient', 'nurse',)


# class NurseSpeciality(models.Model):
#     specialty = models.CharField(max_length=60)

#     def __unicode__(self):
#         return self.specialty

#     class Meta:
#         verbose_name_plural = 'Nurses specialties'


# class Nurse(models.Model):
#     user = models.OneToOneField(User, primary_key=True)
#     specialty = models.ForeignKey(NurseSpeciality)
#     degree_CHOICES = (
#         ('A', 'Associate Degree in Nursing'),
#         ('D', 'Diploma in Nursing'),
#         ('L', 'Licensed Practical Nurse'),
#         ('AD', 'Advanced practice registered nurses'),
#     )
#     degree = models.CharField(max_length=30, choices=degree_CHOICES)

#     def __unicode__(self):
#         return self.user.first_name + ' ' + self.user.last_name
