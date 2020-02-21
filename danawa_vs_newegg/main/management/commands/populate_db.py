from django.core.management.base import BaseCommand
from main.models import A

class Command(BaseCommand):
    #args = '<foo bar ...>'
    #help = 'our help string comes here'

    def _create_tags(self):
        tlisp = A(name='Lisp')
        tlisp.save()

    def _report_all(self):
        print(A.objects.all())
        

    def handle(self, *args, **options):
        self._create_tags()
        self._report_all()
        print(options)