from book.models import Contact
from django.shortcuts import get_object_or_404, get_list_or_404
from book.serializers import ContactSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from book.permissions import IsOwner


class ContactList(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get(self, request, format=None):
        if 'name' in request.query_params:
            contacts = get_list_or_404(Contact, owner=request.user,
                                         name=request.query_params['name'])
        elif 'number' in request.query_params:
            contacts = get_list_or_404(Contact, owner=request.user,
                                        numbers__number=request.query_params[
                'number'])
        else:
            contacts = Contact.objects.filter(owner=request.user)
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ContactDetail(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get(self, request, pk, format=None):
        contact = get_object_or_404(Contact, owner=request.user, pk=pk)
        serializer = ContactSerializer(contact)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        contact = get_object_or_404(Contact, owner=request.user, pk=pk)
        serializer = ContactSerializer(contact, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        contact = get_object_or_404(Contact, pk=pk, owner=request.user)
        contact.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
