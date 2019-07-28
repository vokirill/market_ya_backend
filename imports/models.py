from django.db import models

# Create your models here.

class Imports_queries(models.Manager):

    def get_max_import_id(self):
        return self.aggregate(models.Max('import_id'))
    def get_data_for_patch(self, imports_id, citizens):
        return self.filter(import_id = imports_id, citizen_id = citizens)
    def get_import_data(self, imports_id):
        return self.filter(import_id=imports_id)

class Imports(models.Model):

    import_id = models.IntegerField(blank=False)
    citizen_id = models.IntegerField(blank=False)
    town = models.CharField(max_length=200, blank=False)
    street = models.CharField(max_length=200,blank=False)
    building = models.CharField(max_length=50, blank=False)
    appartment = models.IntegerField(blank=False)
    name = models.CharField(max_length=1000,blank=False)
    birth_date = models.DateField(blank=False)
    gender = models.CharField(max_length=6,blank=False)
    relatives = models.CharField(max_length=1000,blank=False)
    objects = Imports_queries()







