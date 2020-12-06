from django.contrib import admin

from .models import Node, TreeTable

admin.site.register([Node, TreeTable])
