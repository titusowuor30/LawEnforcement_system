from django.contrib import admin
from .models import *
from  django.contrib.auth.models  import  Group 


admin.site.unregister(Group)  # unregister groups

# Register your models here.
class  RoleAdmin(admin.ModelAdmin):
    list_display=('id',)

class  UserAdmin(admin.ModelAdmin):
    list_display=('username','first_name','last_name','email','date_joined',)
    search_fields=['roles',]

class  SubjectsAdmin(admin.ModelAdmin):
    list_display=('fname','lname','middle_name','birth_certificate_number','id_no','phone','User_Image','Fingerprint_Image')

class  ProfileAdmin(admin.ModelAdmin):
    list_display=('user','biography','website','user_image')
class  WorkAdmin(admin.ModelAdmin):
    list_display=('institution_name','status','insurance_name','insurance_id','bank_name','bank_account_number')

class  CrimeAdmin(admin.ModelAdmin):
    list_display=('suspect','title','location','featured','status','scene_image')

class  AcademicAdmin(admin.ModelAdmin):
    list_display=('institution_name','status',)


class  ResidenceAdmin(admin.ModelAdmin):
    list_display=('country','region_or_provinve','sub_county','postal_address','street','apartment')

admin.site.register(Role,RoleAdmin)
admin.site.register(User,UserAdmin)
admin.site.register(Subjects,SubjectsAdmin)
admin.site.register(Profile,ProfileAdmin)
admin.site.register(Work_history,WorkAdmin)
admin.site.register(Crime,CrimeAdmin)
admin.site.register(Academic_history,AcademicAdmin)
admin.site.register(Residence,ResidenceAdmin)

