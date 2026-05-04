# # from django.http import JsonResponse
# # import json

# # def getData(request):
# #     if request.method == "POST":
# #         data = json.loads(request.body)
# #         username = data.get("username")
# #         password = data.get("password")

# #         if username == "admin" and password == "root123":
# #             return JsonResponse({"message": "Login successful"})
# #         else:
# #             return JsonResponse({"message": "Invalid credentials"})

# #     return JsonResponse({"message": "Send POST request"})
# from django.http import HttpResponse

# def home(request):
#     return HttpResponse("Backend running")
from django.http import JsonResponse
from django.views import View

# ✅ Base class
class BaseView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({"message": f"{self.__class__.__name__} GET"})

    def post(self, request, *args, **kwargs):
        return JsonResponse({"message": f"{self.__class__.__name__} POST"})
    def ro(request, campaign_code):
    return JsonResponse({"message": "RO download"})

def generate_quotation_api(request):
    return JsonResponse({"message": "Quotation generated"})

def generate_partner_quotation_api(request):
    return JsonResponse({"message": "Partner quotation"})

def dashboard_stats(request):
    return JsonResponse({"message": "Dashboard stats"})
