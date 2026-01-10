from rest_framework.throttling import UserRateThrottle

class JobCreateThrottle(UserRateThrottle):
    scope = "job_create"
