from datetime import datetime

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

from examination.models import Examination
from examination.serializers import ExaminationSerializer
from professional.models import Professional


@api_view(['GET'])
def examination_general_controller(request: Request) -> Response:
    methods = {
        'GET': find_all_examination,
    }

    if request.method in methods:
        return methods[request.method](request)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'PATCH'])
def examination_with_id_controller(request: Request, examination_id: int) -> Response:
    methods = {
        'PATCH': update_examination,
        'GET': lambda _r, e: Response(ExaminationSerializer(e).data)
    }

    try:
        examination = Examination.objects.get(pk=examination_id)

        if request.method in methods:
            return methods[request.method](request, examination)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    except Examination.DoesNotExist:
        return Response({'message': 'Examination not found!'}, status=status.HTTP_404_NOT_FOUND)


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
        return Response(examination.data, status=status.HTTP_201_CREATED)

    return Response(examination.errors, status=status.HTTP_400_BAD_REQUEST)


def find_all_examinations_by_professional_id(_request: Request, professional: Professional) -> Response:
    examinations = Examination.objects.filter(professional=professional)
    serialized_examinations = ExaminationSerializer(examinations, many=True)

    return Response(serialized_examinations.data, status=status.HTTP_200_OK)


def find_all_examination(_request: Request) -> Response:
    examinations = Examination.objects.all()
    serialized_examinations = ExaminationSerializer(examinations, many=True)

    return Response(serialized_examinations.data, status=status.HTTP_200_OK)


def update_examination(request: Request, examination: Examination) -> Response:
    examination_payload = request.data

    if 'date' in examination_payload:
        date_str = examination_payload['date']
        if not isinstance(date_str, str):
            return Response({'message': 'Invalid type for date attribute'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            examination.date = date_obj
        except ValueError:
            return Response({'message': 'Invalid date format. Please use "YYYY-MM-DD HH:MM:SS"'},
                            status=status.HTTP_400_BAD_REQUEST)

    if 'professional' in examination_payload:
        if not isinstance(examination_payload['professional'], int):
            return Response({'message': 'professional must be integer'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            professional = Professional.objects.get(pk=examination_payload['professional'])
            examination.professional = professional
        except Professional.DoesNotExist:
            return Response({'message': 'Professional not found!'})

    examination.save()

    return Response(ExaminationSerializer(examination).data, status=status.HTTP_200_OK)
