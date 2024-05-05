from rest_framework import serializers
import re

def password_validator(password):
    pattern = r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,32}$'
    password_message = 'The password must be between 8 and 32 characters long and include at least one digit, one uppercase letter, and one lowercase letter.'

    if not bool(re.match(pattern, password)):
        raise serializers.ValidationError({'error': password_message})
    
def username_validator(username):
    pattern = r'^[a-zA-Z0-9_]{3,30}$'
    username_message = 'The username must be between 3 and 32 characters long and can be made up of letters, numbers and underscores.'
    
    if not bool(re.match(pattern, username)):
        raise serializers.ValidationError({'error': username_message})
    
def first_name_validator(first_name):
    pattern = r'^[a-zA-Z-]{3,100}$'
    first_name_message = 'The first_name must be between 3 and 100 characters long and can be made up of letters and hyphen.'
    
    if not bool(re.match(pattern, first_name)):
        raise serializers.ValidationError({'error': first_name_message})

def last_name_validator(last_name):
    pattern = r'^[a-zA-Z-]{3,100}$'
    last_name_message = 'The last_name must be between 3 and 100 characters long and can be made up of letters and hyphen.'
    
    if not bool(re.match(pattern, last_name)):
        raise serializers.ValidationError({'error': last_name_message})