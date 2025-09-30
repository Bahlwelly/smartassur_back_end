from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

class CustomUserManager (UserManager) :
    def create_user(self, telephone, password = ..., **extra_fields):
        if not telephone :
            raise ValueError ("Le numnero du telephone est obligatoir")
        
        extra_fields.setdefault('is_active', True)
        user = self.model(telephone = telephone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, telephone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(telephone, password, **extra_fields)



class User(AbstractUser):
    ROLES = (
        ('ADMIN', 'Admin'),
        ('MANAGER', 'Manager'),
        ('CLIENT', 'Client')
    )


    username = None
    role = models.CharField(choices=ROLES, default='CLIENT', max_length=20)
    telephone = models.CharField(max_length=8, unique=True)
    profile = models.ImageField(null=True, blank=True, upload_to='profiles/')
    company = models.ForeignKey("company.Company", null=True, blank=True, on_delete=models.SET_NULL,related_name='managers')

    USERNAME_FIELD = 'telephone'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.get_full_name()}"