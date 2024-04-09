from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

from examination.models import Examination
from examination.serializers import ExaminationSerializer
from professional.models import Professional


@api_view(['GET', 'POST'])
def examination_general_controller(request: Request) -> Response:
    methods = {
        'GET': find_all_examination,
    }

    if request.method in methods:
        return methods[request.method](request)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def examination_with_professional_id_controller(request: Request, professional_id: int) -> Response:
    methods = {
        'GET': find_all_examinations_by_professional_id,
        'POST': create_examination
    }
    try:
        professional = Professional.objects.get(pk=professional_id)

        if request.method in methods:
            return methods[request.method](request, professional)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    except Professional.DoesNotExist:
        return Response({'message': 'Professional not found!'}, status=status.HTTP_404_NOT_FOUND)


def create_examination(request: Request, professional: Professional) -> Response:
    examination_payload = request.data
    examination_payload['professional'] = professional.pk

    examination = ExaminationSerializer(data=examination_payload)

    if examination.is_valid():
        examination.save()
        return Response(examination.data, status=status.HTTP_200_OK)

    return Response(examination.errors, status=status.HTTP_400_BAD_REQUEST)


def find_all_examinations_by_professional_id(_request: Request, professional: Professional) -> Response:
    examinations = Examination.objects.filter(professional=professional)
    serialized_examinations = ExaminationSerializer(examinations, many=True)

    return Response(serialized_examinations.data, status=status.HTTP_200_OK)


def find_all_examination(_request: Request) -> Response:
    examinations = Examination.objects.all()
    serialized_examinations = ExaminationSerializer(examinations, many=True)

    return Response(serialized_examinations.data, status=status.HTTP_200_OK)


def todo(request):
    return Response()
