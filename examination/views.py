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
        'GET': lambda: print(),
        'POST': lambda: print()
    }

    if request.method in methods:
        return methods[request.method](request)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def examination_with_professional_id_controller(request: Request, professional_id: int) -> Response:
    methods = {
        'GET': lambda: print(),
        'POST': create_examination
    }

    if request.method in methods:
        return methods[request.method](request, professional_id)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


def create_examination(request: Request, professional_id: int) -> Response:
    try:
        professional = Professional.objects.get(pk=professional_id)
        examination_payload = request.data
        examination_payload['professional'] = professional_id

        examination = ExaminationSerializer(data=examination_payload)

        if examination.is_valid():
            examination.save()
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)
    except Professional.DoesNotExist:
        return Response({'message': 'Professional not found!'}, status=status.HTTP_404_NOT_FOUND)
