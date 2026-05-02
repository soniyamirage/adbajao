# from django.http import JsonResponse
# from django.views import View

# def getRoutes(request):
#     return JsonResponse({"message": "API working"})

# def dashboard(request):
#     return JsonResponse({
#         "users": 10,
#         "revenue": 5000,
#         "orders": 25
#     })

# class EngineModuleListView(View):
#     def get(self, request):
#         return JsonResponse({"message": "Engine Module working"})
from django.http import JsonResponse

def getRoutes(request):
    return JsonResponse({"message": "API working"})