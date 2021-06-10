from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from helpers.models import TrackingModel
from django.conf import settings


from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import (
    PermissionsMixin, AbstractBaseUser, BaseUserManager)


MEMBERSHIP_CHOICES = (('Premium','pre'),('Free','free'))

class Membership(models.Model):
    slug = models.SlugField(null=True, blank=True)
    membership_type = models.CharField(
    choices=MEMBERSHIP_CHOICES, default='Free',max_length=30)
    def __str__(self):
       return self.membership_type

class MyUserManager(BaseUserManager):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,related_name='user_membership', on_delete=models.CASCADE)
    membership = models.ForeignKey(Membership, related_name='user_membership', on_delete=models.SET_NULL, null=True)
    use_in_migrations = True

    
    def _create_user(self, username, email, password, membership_type,**extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('Username must be set')
        if not email:
            raise ValueError('Email must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        membership_type=self.model(membership_type)
        user = self.model(username=username, email=email, membership_type=membership_type,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
        


class User(AbstractBaseUser, PermissionsMixin, TrackingModel):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    is_verified = models.BooleanField(
        _('verified'),
        default=False,
        help_text=_(
            'Designates whether this user has verified their email on sign up. '
        ),
    )

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = MyUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']



    @property
    def token(self):
        return ''

    '''@property
    def token(self):
        token = jwt.encode({
            "username": self.username,
            "email": self.email,
            "exp": datetime.utcnow() + timedelta(hours=23)
        }, settings.SECRET_KEY, algorithm='HS256')
        return token'''