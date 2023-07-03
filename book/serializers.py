from rest_framework import serializers
from book.models import Contact, Number


class NumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Number
        fields = ['number']


class ContactSerializer(serializers.ModelSerializer):
    numbers = NumberSerializer(many=True)
    class Meta:
        model = Contact
        fields = ['id', 'name', 'description', 'numbers']

    def create(self, validated_data):
        return Contact.objects.create(
            name=validated_data['name'],
            description=validated_data['description'],
            owner=validated_data['owner'],
            numbers=validated_data['numbers']
        )

    def update(self, instance, validated_data):
        numbers = []
        for n in validated_data.pop('numbers'):
            numbers.append(n['number'])
        name = validated_data.get('name', instance.name)
        description = validated_data.get('description', instance.description)
        return Contact.objects.update_contact(instance, name, description,
                                              numbers)
