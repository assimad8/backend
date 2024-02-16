import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

# Create your models here.


class UserManager(BaseUserManager):
    def get_object_by_public_id(self,public_id):
        try:
            instance = self.get(public_id=public_id)
            return instance
        except (ObjectDoesNotExist,ValueError,TypeError) :
            return Http404

    def create_user(self,username,email,password=None,**kwargs):
        """
        Create and return a `User` with an email,phone number,username and password
        """
        if username is None :
            raise TypeError('username must not be empty')
        if email is None :
            raise TypeError('email must not be empty')
        if password is None :
            raise TypeError('password must not be empty')
        user = self.model(username=username,email=email,**kwargs)
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    def create_superuser(self,username,email,password=None,**kwargs):
        if password is None :
            raise TypeError("Superuser must have password")
        if username is None :
            raise TypeError("Superuser must have username")
        if email is None :
            raise TypeError("Superuser must have email")
        super_user = self.create_user(username,email,password,**kwargs)
        super_user.is_superuser = True
        super_user.is_staff = True
        super_user.save(using=self._db)
        
        return super_user

class User(AbstractBaseUser,PermissionsMixin):
    public_id = models.UUIDField(db_index=True,unique=True,default=uuid.uuid4,editable=False)
    username = models.CharField(db_index=True,max_length=255,unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(db_index=True,unique=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    
    objects = UserManager()
    
    def __str__(self):
        return self.username

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"


