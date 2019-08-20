from django.db import models


# Create your models here.

class Imports_queries(models.Manager):

    def get_max_import_id(self):
        return self.aggregate(models.Max('import_id'))

    def get_data_for_patch(self, imports_id, citizens):
        return self.filter(import_id=imports_id, citizen_id=citizens)

    def get_data_for_patch_relatives(self, imports_id):
        return self.filter(import_id=imports_id)

    def get_import_data(self, imports_id):
        return self.filter(import_id=imports_id)


class Imports(models.Model):
    import_id = models.IntegerField(blank=False, null = False)
    citizen_id = models.IntegerField(blank=False, null = False)
    town = models.CharField(max_length=200, blank=False, null = False)
    street = models.CharField(max_length=200, blank=False, null = False)
    building = models.CharField(max_length=50, blank=False, null = False)
    apartment = models.IntegerField(blank=False, null = False)
    name = models.CharField(max_length=1000, blank=False, null = False)
    birth_date = models.DateField(blank=False, null=False)
    gender = models.CharField(max_length=6, blank=False, null = False)
    relatives = models.CharField(max_length=1000, blank=False, null = False)
    objects = Imports_queries()


def fourth_task_query(imports_id):
    query = '''
        WITH RECURSIVE split(import_id, citizen_id, relatives_id, rest) AS (
            SELECT  import_id, citizen_id, '', relatives || ',' FROM imports_imports  WHERE import_id
            UNION ALL
            SELECT import_id,
                   citizen_id, 
                   substr(rest, 0, instr(rest, ',')),
                   substr(rest, instr(rest, ',')+1)
            FROM split
            WHERE rest <> '')

        SELECT birt_month,
               citizen_id,
               COUNT(relative_id)
        FROM (
             SELECT c.citizen_id,
                    r.citizen_id AS relative_id,
                    r.birt_month
             FROM 
                 (
                 SELECT citizen_id, 
                        CAST(relatives_id AS integer) AS relative_id
                 FROM split 
                 WHERE relatives_id <> '' AND import_id = {0}
                 ) AS c
             INNER JOIN 
                (
                SELECT citizen_id,
                       CAST(STRFTIME('%m', birth_date) AS integer) as birt_month
                FROM imports_imports 
                WHERE import_id = {0}
                ) AS r
             ON  c.relative_id = r.citizen_id 
        ) AS x
        GROUP BY birt_month, citizen_id
    '''.format(imports_id)
    return query

def fifth_task_query(imports_id):
    query = '''
            SELECT town,
                   GROUP_CONCAT(DATE('now')-birth_date) AS year_string
            FROM imports_imports
            WHERE import_id = {}
            GROUP BY town;
    '''.format(imports_id)
    return query