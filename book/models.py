from django.db import models
from django.core.validators import MinLengthValidator


class ContactManager(models.Manager):

    def create(self, name, description, owner, numbers):
        contact = Contact(name=name, description=description, owner=owner)
        contact.save()
        for num in numbers:
            number = Number(contact=contact, number=num['number'])
            number.save()
        return contact

    def update_contact(self, contact, name, description, numbers):
        contact_numbers = contact.numbers
        for cn in contact_numbers.all():
            if cn.number not in numbers and len(numbers) > 0:
                cn.number = numbers.pop()
                cn.save()
            elif len(numbers) == 0:
                cn.delete()
            else:
                numbers.remove(cn.number)
        for num in numbers:
            number = Number(number=num, contact=contact)
            number.save()
        contact.name = name
        contact.description = description
        contact.save()
        return contact


class Contact(models.Model):
    name = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, "Name must be greater than 2 "
                                              "characters")]
    )
    description = models.TextField()
    owner = models.ForeignKey('auth.User', related_name='contacts',
                              on_delete=models.CASCADE)
    objects = ContactManager()

    def __str__(self):
        return self.name


class Number(models.Model):
    number = models.CharField(
            max_length=12,
            validators=[MinLengthValidator(6, "Title must be greater than 6 "
                                              "characters")]
    )
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE,
                                related_name='numbers')

    def __str__(self):
        return self.number
