from django.contrib import admin
from .models import UserType, User_Category, UserHistory, CustomUser, SubCategory, Category, Product


admin.site.register(UserType)
admin.site.register(UserHistory)
admin.site.register(User_Category)
admin.site.register(CustomUser)
admin.site.register(SubCategory)
admin.site.register(Category)
admin.site.register(Product)
