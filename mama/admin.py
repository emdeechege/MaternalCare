from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *

admin.site.register(Department, DepartmentAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(MidWife, MidWifeAdmin)
admin.site.register(DoctorSpeciality, DoctorSpecialityAdmin)
admin.site.register(MidWifeSpeciality, MidWifeSpecialityAdmin)


admin.site.register(Medication, MedicationAdmin)
admin.site.register(MedPrice, MedPriceAdmin)
admin.site.register(Prescription, PrescriptionAdmin)

admin.site.register(Vaccine, VaccineAdmin)
admin.site.register(VaccineApplied, VaccineAppliedAdmin)
admin.site.register(LiveChat, LiveChatAdmin)

admin.site.register(Visit, VisitAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(DoctorWorkingHours, DoctorWorkingHoursAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(AppointmentDetails, AppointmentDetailsAdmin)
