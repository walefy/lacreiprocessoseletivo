from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from .models import Professional
from .serializers import ProfessionalSerializer


@api_view(['GET', 'POST'])
def professional_general_controller(request: Request) -> Response:
    methods = {
        'GET': list_all_professionals,
        'POST': create_professional
    }

    if request.method in methods:
        return methods[request.method](request)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'DELETE'])
def professional_with_id_controller(request: Request, professional_id: int) -> Response:
    methods = {
        'GET': find_professional_by_id,
        'DELETE': delete_professional_by_id
    }

    if request.method in methods:
        return methods[request.method](request, professional_id)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


def list_all_professionals(request: Request) -> Response:
    professionals = Professional.objects.all()
    serialized_professionals = ProfessionalSerializer(professionals, many=True)
    return Response(serialized_professionals.data, status=status.HTTP_200_OK)


def create_professional(request: Request) -> Response:
    serializer = ProfessionalSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def find_professional_by_id(request: Request, professional_id: int) -> Response:
    try:
        professional = Professional.objects.get(pk=professional_id)
        serialized_professional = ProfessionalSerializer(professional)

        return Response(serialized_professional.data, status=status.HTTP_200_OK)
    except Professional.DoesNotExist:
        return Response({'message': 'professional not found!'}, status=status.HTTP_404_NOT_FOUND)


def delete_professional_by_id(request: Request, professional_id: int) -> Response:
    try:
        professional = Professional.objects.get(pk=professional_id)
        professional.delete()

        return Response({'message': 'professional deleted!'}, status=status.HTTP_200_OK)
    except Professional.DoesNotExist:
        return Response({'message': 'professional not found!'}, status=status.HTTP_404_NOT_FOUND)
