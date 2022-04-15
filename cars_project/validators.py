from django.core.exceptions import ValidationError

def only_letters_validator(value):
    for ch in value:
        if not ch.isalpha():
            raise ValidationError('Value must containt only letters!')



def positive_number(value):
    if value < 0:
        raise ValidationError('Number cannot be less than 0!')


def validate_image(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    megabyte_limit = 5.0
    if filesize > megabyte_limit*1024*1024:
        raise ValidationError(f"Max file size is {megabyte_limit} MB")