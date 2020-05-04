# pip install validate_email
# pip install py3dns

from validate_email import validate_email

is_valid = validate_email('dskgregu222@gmail.com', verify=True)
print(is_valid)
