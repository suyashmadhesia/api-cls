from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from clsroom.messages.serializes import MessageSerializer

from clsroom.models import Account, Classroom, Message


@api_view(['GET'])
def get_all_class(request, pk):
    res_data = []
    try:
        account = Account.objects.get(account_id=pk)
        classrooms = list(account.cls_room_id)
        for i in classrooms:
            class_detail = {}
            try:
                classroom = Classroom.objects.get(
                    cls_id=i.strip())
                if classroom.is_active:  # wether class is active or not if not active do not send to the user
                    class_detail["name"] = classroom.name
                    class_detail["owner"] = classroom.owner.name
                    class_detail["owner_acc_id"] = classroom.owner.account_id
                    res_data.append(class_detail)
            except:
                return Response({"error": "Invalid Fields"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({"data": res_data}, status=status.HTTP_200_OK)
    except:
        return Response({}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_class_messages(request, pk):
    messages = Message.objects.filter(cls_id=pk).order_by('created_at')
    serializer = MessageSerializer(messages, many=True)
    return Response({"data" :serializer.data}, status=status.HTTP_200_OK)
