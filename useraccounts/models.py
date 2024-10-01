from django.db import models
from django.contrib.auth.models import  AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('This email is not given')
        email = self.normalize_email(email)
        user = self.model(email = email,  **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff = True')
        
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser = True')
        
        return self.create_user(email, password, **extra_fields)

class CustomUserModel(AbstractBaseUser):

    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    company_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    website_link = models.URLField(max_length=200, null=True, blank=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()
    
    class Meta:
        verbose_name_plural = 'Client Basic Info'

    def __str__(self):
        return self.email

    def has_module_perms(self, app_label): 
        return True
    
    def has_perm(self, parm, obj=None):
        return True