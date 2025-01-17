from django.contrib import admin
from django.forms import ModelForm, FileField


from mainapp.models import Benefit, Talent, Course, Mentor,\
    StudentsWork, StudentsHomework, PromoCode, Preparation, Subscriber, Lesson, StudentCourse


admin.site.register(Lesson)
# admin.site.register(Benefit)
admin.site.register(Mentor)
admin.site.register(StudentsWork)
admin.site.register(StudentsHomework)
admin.site.register(PromoCode)
admin.site.register(Preparation)
admin.site.register(Subscriber)
admin.site.register(StudentCourse)


# Класс-обманка для загрузки файлов .svg через админку в модель Talent
class TalentModelForm(ModelForm):
    class Meta:
        model = Talent
        exclude = []
        field_classes = {
            'image': FileField,
        }


@admin.register(Talent)
class TalentAdmin(admin.ModelAdmin):
    list_display = 'title',
    form = TalentModelForm


# Класс-обманка для загрузки файлов .svg через админку в модель Benefit
class BenefitModelForm(ModelForm):
    class Meta:
        model = Benefit
        exclude = []
        field_classes = {
            'image': FileField,
        }


@admin.register(Benefit)
class BenefitAdmin(admin.ModelAdmin):
    list_display = 'title',
    form = BenefitModelForm


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
