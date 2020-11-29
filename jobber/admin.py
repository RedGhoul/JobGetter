from django.contrib import admin
from jobber.models import JobPositionItem, JobCitySetItem, JobTypeFind, MaxResultsPerCity, Host, JobTransparencyLinks, MaxAge

# Register your models here.
admin.site.register(JobPositionItem)
admin.site.register(JobCitySetItem)
admin.site.register(JobTypeFind)
admin.site.register(MaxResultsPerCity)
admin.site.register(Host)
admin.site.register(JobTransparencyLinks)
admin.site.register(MaxAge)