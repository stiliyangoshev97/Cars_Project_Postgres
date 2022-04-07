from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from profiles.models import Profile


UserModel = get_user_model()

# When User is being created, I want to execute the
# function bellow

#We do this after saving the information in the model
@receiver(post_save, sender=UserModel)
def user_created(sender, instance, created, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()


# Check if profile is complete
# We do this before saving the information in the model
# in pre-save we do not have created

@receiver(pre_save, sender = Profile)
def profile_is_complete(sender, instance, **kwargs):
    if instance.profile_photo and instance.first_name and instance.last_name and instance.phone_number:
        instance.is_complete = True
    else:
        instance.is_complete = False


# Check if user is verified



# Signals are used when we always wants in a certain situation
# to make something happen. It's also used for verifying the email
# address

