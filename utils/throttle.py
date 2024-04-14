from rest_framework.throttling import UserRateThrottle

class LoginThrottle(UserRateThrottle):
    rate = '5/minute'
    scope = 'login'

class DefaultThrottle(UserRateThrottle):
    rate = '10/minute'
