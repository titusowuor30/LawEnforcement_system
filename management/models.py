from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.conf import settings
from django.utils.safestring import mark_safe



SCHOOL_STATUS = (
      ('Graduated','Graduated'),
      ('Current','Current'),
      ('Dropped_out','Dropped out'),
)

WORK_STATUS = (
      ('Current', 'Current'),
      ('Transfered', 'Transfered'),
)

CASE_STATUSES = (
      ('Closed', 'Closed'),
      ('Open', 'Open'),
      ('Solved', 'Solved'),
      ('Secret', 'Secret'),
)


class Role(models.Model):
  '''
  The Role entries are managed by the system,
  automatically created via a Django data migration.
  '''
  HEAD_OF_DEPARTMENT_OFFICER = 1
  COUNTY_SECURITY_OFFICER=2
  REGIONAL_SECURITY_OFFICER = 3
  MINISTER_OF_SECURITY = 4
  ADMIN = 5
  ROLE_CHOICES = (
      (HEAD_OF_DEPARTMENT_OFFICER, 'Head of department officer'),
      (COUNTY_SECURITY_OFFICER, 'County security officer'),
      (REGIONAL_SECURITY_OFFICER, 'Regional security officer'),
      (MINISTER_OF_SECURITY, 'Minister of security'),
      (ADMIN, 'admin')
  )
  id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)

  def __str__(self):
      return self.get_id_display()



class User(AbstractUser):
      roles = models.ManyToManyField(Role)

class Subjects(models.Model):
    crime_history=models.ManyToManyField('Crime',default='None',blank=True,null=True)
    academic_history=models.ManyToManyField('Academic_history',default='None')
    work_history=models.ManyToManyField('Work_history',default='None')
    residence=models.ManyToManyField('Residence',default='None')
    fname=models.CharField(max_length=100)
    middle_name=models.CharField(max_length=100)
    lname=models.CharField(max_length=100)
    birth_certificate_number=models.CharField(max_length=100,unique=True)
    id_no=models.CharField(max_length=100,primary_key=True,unique=True)
    phone=models.CharField(max_length=15,unique=True)
    image=models.FileField(upload_to='uploads/users/',default='uploads/users/default.jpg')
    fingerprint_image=models.FileField(upload_to='uploads/users/firgerprints/')

    def __str__(self):
        return self.fname

    def  Fingerprint_Image(self):
        return mark_safe('<img src="/../../media/%s" width="50" height="50" />' % (self.fingerprint_image))
    def  User_Image(self):
        return mark_safe('<img src="/../../media/%s" width="50" height="50" />' % (self.image))

    Fingerprint_Image.allow_tags = True      
    User_Image.allow_tags = True         

    class Meta:
        verbose_name_plural='Subjects'

class Residence(models.Model):
    country=models.CharField(max_length=100,default='Kenya')
    region_or_provinve=models.CharField(max_length=100,default='Nairobi')
    state_or_county=models.CharField(max_length=100,default='Nairobi')
    sub_county=models.CharField(max_length=100,default='Madhare North')
    location=models.CharField(max_length=100,default='Uthiru')
    sub_location=models.CharField(max_length=100,default='kilimani')
    village=models.CharField(max_length=100,default='machau')
    zip_code=models.CharField(max_length=100,default='41200')
    postal_address=models.CharField(max_length=100,default='P.O BOX 45-41200 Nairobi-Kenya')
    street=models.CharField(max_length=100,default='Mfangano')
    apartment=models.CharField(max_length=100,default='Jek\'s Chambers')

    def __str__(self):
        return self.country


class Academic_history(models.Model):
    institution_name=models.CharField(max_length=100,default='None')
    _from=models.DateTimeField()
    _to=models.DateTimeField(blank=True,null=True)
    status=models.CharField(max_length=50,choices=SCHOOL_STATUS,default='Graduated')

    def __str__(self):
        return self.institution_name

    class Meta:
        verbose_name_plural='Academic history' 

class Work_history(models.Model):
    institution_name=models.CharField(max_length=100)
    _from=models.DateTimeField()
    _to=models.DateTimeField(blank=True,null=True,help_text='leave blank if current')
    status=models.CharField(max_length=50,choices=WORK_STATUS,default='Graduated')
    insurance_name=models.CharField(max_length=100,default='NHIF')
    insurance_id=models.CharField(max_length=100,default='12355',unique=True)
    bank_name=models.CharField(max_length=100,default='National Bank')
    bank_account_number=models.CharField(max_length=100,default='1260777345621',unique=True)   

    def __str__(self):
        return self.institution_name

    class Meta:
        verbose_name_plural='Work history' 


class Crime(models.Model):
    suspect=models.ForeignKey('Subjects',on_delete=models.CASCADE,related_name='crimes')
    title=models.CharField(max_length=100,default='None')
    location=models.CharField(max_length=100,default='Nairobi')
    time=models.DateTimeField()
    description=models.TextField(max_length=255,default='Description here')
    scene_image=models.FileField(upload_to='uploads/users/suspects/')
    status=models.CharField(choices=CASE_STATUSES,max_length=100,default='Closed') 
    featured=models.BooleanField(default=False) 

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural='Crime Records'
        ordering=['-time']       


class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    image=models.ImageField(upload_to='uploads/users/%Y%m%d/',default='uploads/users/default.jpg')
    email = models.EmailField(max_length=100)
    website=models.URLField(max_length=255,null=True,blank=True)
    biography=models.TextField(max_length=255,null=True,blank=True)

    def __str__(self):
        return self.user.username

    def  user_image(self):
        return mark_safe('<img src="/../../media/%s" width="50" height="50" />' % (self.image))  
    user_image.allow_tags = True         

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

