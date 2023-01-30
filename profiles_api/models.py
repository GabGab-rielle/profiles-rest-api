from django.db import models
# the imports below are the standard base classes required to overriding/customising the default django user model
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager


class UserProfileManager(BaseUserManager):
  """Manager for user profiles"""
  
  def create_user(self, email, name, password=None):
    """Create a new user profile"""
    if not email:
      raise ValueError('Users must have an email address')

    email = self.normalize_email(email) # converts email to lowercase
    user = self.model(email=email, name=name) # creates new model
    
    user.set_password(password) # encrypts the password (converts to hash)
    user.save(using=self._db) # save object to database

    return user

  def create_superuser(self, email, name, password):
    """Create and save a new superuser (admin) with given details"""
    user = self.create_user(email, name, password)

    user.is_superuser = True # is_superuser is automatically created by PermissionsMixin
    user.is_staff = True
    user.save(using=self._db)

    return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
  """Database model for users in the system"""
  email = models.EmailField(max_length=255, unique=True)
  name = models.CharField(max_length=255)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)

  objects = UserProfileManager()

  USERNAME_FIELD = 'email' # this overrides the standard django username field with email (required field)
  REQUIRED_FIELDS = ['name'] # user can also specify their name (optional field)

  # below are functions that django will interact with the custom user model
  def get_full_name(self):
    """Retrieve full name of user"""
    return self.name

  def get_short_name(self):
    """Retrieve short name of user"""
    return self.name

  def __str__(self):
    """Return string representation of our user"""
    return self.email