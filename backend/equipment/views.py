# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.parsers import MultiPartParser, FormParser
# from rest_framework.authentication import BasicAuthentication
# from rest_framework.permissions import IsAuthenticated

# import pandas as pd

# from django.db.models import Avg, Count

# from .models import Equipment, UploadSummary
# from .serializers import EquipmentSerializer


# class CSVUploadView(APIView):
#     authentication_classes = [BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     parser_classes = (MultiPartParser, FormParser)
#     parser_classes = (MultiPartParser, FormParser)

#     def post(self, request):
#         file = request.FILES.get('file')

#         if not file:
#             return Response({"error": "No file uploaded"}, status=400)

#         try:
#             df = pd.read_csv(file)
#         except Exception:
#             return Response({"error": "Invalid CSV file"}, status=400)

#         required_columns = [
#             'Equipment Name',
#             'Type',
#             'Flowrate',
#             'Pressure',
#             'Temperature'
#         ]

#         for col in required_columns:
#             if col not in df.columns:
#                 return Response({"error": f"Missing column: {col}"}, status=400)
        
                
        
#         Equipment.objects.all().delete()
       
#         for _, row in df.iterrows():
#             Equipment.objects.create(
#                 name=row['Equipment Name'],
#                 equipment_type=row['Type'],
#                 flowrate=row['Flowrate'],
#                 pressure=row['Pressure'],
#                 temperature=row['Temperature']
#             )

        
#         total_equipment = Equipment.objects.count()

#         averages = Equipment.objects.aggregate(
#             avg_flowrate=Avg('flowrate'),
#             avg_pressure=Avg('pressure'),
#             avg_temperature=Avg('temperature')
#         )

        
#         UploadSummary.objects.create(
#             total_equipment=total_equipment,
#             avg_flowrate=averages['avg_flowrate'],
#             avg_pressure=averages['avg_pressure'],
#             avg_temperature=averages['avg_temperature'],
#         )

       
#         summaries = UploadSummary.objects.order_by('-uploaded_at')
#         if summaries.count() > 5:
#             for summary in summaries[5:]:
#                 summary.delete()

#         return Response(
#             {"message": "CSV uploaded and summary saved"},
#             status=201
#         )



# class SummaryView(APIView):
#     authentication_classes = [BasicAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         total_equipment = Equipment.objects.count()

#         averages = Equipment.objects.aggregate(
#             avg_flowrate=Avg('flowrate'),
#             avg_pressure=Avg('pressure'),
#             avg_temperature=Avg('temperature')
#         )

#         type_distribution = (
#             Equipment.objects
#             .values('equipment_type')
#             .annotate(count=Count('equipment_type'))
#         )

#         return Response({
#             "total_equipment": total_equipment,
#             "averages": averages,
#             "type_distribution": type_distribution
#         })


# class EquipmentListView(APIView):
#     authentication_classes = [BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request):
#         equipments = Equipment.objects.all()
#         serializer = EquipmentSerializer(equipments, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

# class UploadHistoryView(APIView):
#     authentication_classes = [BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request):
#         summaries = UploadSummary.objects.order_by('-uploaded_at')[:5]

#         data = []
#         for s in summaries:
#             data.append({
#                 "total_equipment": s.total_equipment,
#                 "avg_flowrate": s.avg_flowrate,
#                 "avg_pressure": s.avg_pressure,
#                 "avg_temperature": s.avg_temperature,
#                 "uploaded_at": s.uploaded_at.strftime("%d %b %Y %H:%M")
#             })

#         return Response(data, status=status.HTTP_200_OK)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny

import pandas as pd

from django.db.models import Avg, Count

from .models import Equipment, UploadSummary
from .serializers import EquipmentSerializer


class CSVUploadView(APIView):
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        file = request.FILES.get('file')

        if not file:
            return Response({"error": "No file uploaded"}, status=400)

        try:
            df = pd.read_csv(file)
        except Exception:
            return Response({"error": "Invalid CSV file"}, status=400)

        required_columns = [
            'Equipment Name',
            'Type',
            'Flowrate',
            'Pressure',
            'Temperature'
        ]

        for col in required_columns:
            if col not in df.columns:
                return Response({"error": f"Missing column: {col}"}, status=400)

        # Clear old data
        Equipment.objects.all().delete()

        # Save new equipment data
        for _, row in df.iterrows():
            Equipment.objects.create(
                name=row['Equipment Name'],
                equipment_type=row['Type'],
                flowrate=row['Flowrate'],
                pressure=row['Pressure'],
                temperature=row['Temperature']
            )

        total_equipment = Equipment.objects.count()

        averages = Equipment.objects.aggregate(
            avg_flowrate=Avg('flowrate'),
            avg_pressure=Avg('pressure'),
            avg_temperature=Avg('temperature')
        )

        UploadSummary.objects.create(
            total_equipment=total_equipment,
            avg_flowrate=averages['avg_flowrate'],
            avg_pressure=averages['avg_pressure'],
            avg_temperature=averages['avg_temperature'],
        )

        summaries = UploadSummary.objects.order_by('-uploaded_at')
        if summaries.count() > 5:
            for summary in summaries[5:]:
                summary.delete()

        return Response(
            {"message": "CSV uploaded and summary saved"},
            status=201
        )


class SummaryView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        total_equipment = Equipment.objects.count()

        averages = Equipment.objects.aggregate(
            avg_flowrate=Avg('flowrate'),
            avg_pressure=Avg('pressure'),
            avg_temperature=Avg('temperature')
        )

        type_distribution = (
            Equipment.objects
            .values('equipment_type')
            .annotate(count=Count('equipment_type'))
        )

        return Response({
            "total_equipment": total_equipment,
            "averages": averages,
            "type_distribution": type_distribution
        })


class EquipmentListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        equipments = Equipment.objects.all()
        serializer = EquipmentSerializer(equipments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UploadHistoryView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        summaries = UploadSummary.objects.order_by('-uploaded_at')[:5]

        data = []
        for s in summaries:
            data.append({
                "total_equipment": s.total_equipment,
                "avg_flowrate": s.avg_flowrate,
                "avg_pressure": s.avg_pressure,
                "avg_temperature": s.avg_temperature,
                "uploaded_at": s.uploaded_at.strftime("%d %b %Y %H:%M")
            })

        return Response(data, status=status.HTTP_200_OK)

