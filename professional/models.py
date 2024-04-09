from django.db import models


class Professional(models.Model):
    class Meta:
        db_table = 'professionals'

    full_name = models.CharField(max_length=100)
    social_name = models.CharField(max_length=100, blank=True)
    profession = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)

    def __str__(self):
        return (f'Professional(full_name={self.full_name},'
                f'profession={self.profession},'
                f'address={self.address},'
                f'contact={self.contact})'
                )
