from django.core.management.base import BaseCommand
from scripts.seed_posts import run

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
      run()