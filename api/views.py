from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response


def getData(request):
    return JsonResponse({"message": "Data working"})

@csrf_exempt
def loginUser(request):
    if request.method == "POST":
        data = json.loads(request.body)

        username = data.get("username")
        password = data.get("password")

        if username == "admin" and password == "root123":
            return JsonResponse({"message": "Login successful"})
        else:
            return JsonResponse({"message": "Invalid credentials"})

    return JsonResponse({"message": "Only POST allowed"})

class RegisterView(View):
    def post(self, request):
        data = json.loads(request.body)
        return JsonResponse({
            "message": "User registered",
            "data": data
        })

class RequestOTPView(APIView):
    def post(self, request):
        return Response({"message": "OTP sent successfully"})

class ResetPasswordView(APIView):
    def post(self, request):
        return Response({"message": "Password reset successful"})

class SettingsListView(APIView):
    def get(self, request):
        return Response({"message": "Settings list working"})

class BookCampaignListView(APIView):
    def get(self, request):
        return Response({"message": "List"})

class BookCampaignDetailView(APIView):
    def get(self, request, pk):
        return Response({"message": "Detail"})

def ro(request):
    return HttpResponse("OK")

class CustomerQueryListView(APIView):
    def get(self, request):
        return Response({"message": "List"})

class CustomerQueryCreateView(APIView):
    def post(self, request):
        return Response({"message": "Created"})

class CustomerQueryDetailView(APIView):
    def get(self, request, pk):
        return Response({"message": "Detail"})

class CustomerQueryUpdateView(APIView):
    def put(self, request, pk):
        return Response({"message": "Updated"})

class CustomerQueryDeleteView(APIView):
    def delete(self, request, pk):
        return Response({"message": "Deleted"})
        
class SettingsCreateView(APIView):
    def post(self, request):
        return Response({"message": "Settings created successfully"})

class SettingsDetailView(APIView):
    def get(self, request, setting_id):
        return Response({"message": f"Settings detail for {setting_id}"})

class SettingsUpdateView(APIView):
    def put(self, request, setting_id):
        return Response({
            "message": f"Settings {setting_id} updated successfully"
        })

class SettingsDeleteView(APIView):
    def delete(self, request, setting_id):
        return Response({
            "message": f"Settings {setting_id} deleted successfully"
        })

class EngineSubmoduleListView(APIView):
    def get(self, request):
        return Response({"message": "Engine submodule list working"})

class EngineSubmoduleCreateView(APIView):
    def post(self, request):
        return Response({"message": "Engine submodule created successfully"})

class EngineSubmoduleDetailView(APIView):
    def get(self, request, id):
        return Response({"message": f"Engine submodule detail for {id}"})

class EngineSubmoduleUpdateView(APIView):
    def put(self, request, id):
        return Response({
            "message": f"Engine submodule {id} updated successfully"
        })

class EngineSubmoduleDeleteView(APIView):
    def delete(self, request, id):
        return Response({
            "message": f"Engine submodule {id} deleted successfully"
        })

class EngineActivityListView(APIView):
    def get(self, request):
        return Response({"message": "Engine activity list working"})

class EngineActivityCreateView(APIView):
    def post(self, request):
        return Response({"message": "Engine activity created successfully"})

class EngineActivityDetailView(APIView):
    def get(self, request, id):
        return Response({"message": f"Engine activity detail for {id}"})

class EngineActivityUpdateView(APIView):
    def put(self, request, id):
        return Response({
            "message": f"Engine activity {id} updated successfully"
        })

class EngineActivityDeleteView(APIView):
    def delete(self, request, id):
        return Response({
            "message": f"Engine activity {id} deleted successfully"
        })

class EngineModuleListView(APIView):
    def get(self, request):
        return Response({"message": "Engine module list working"})

class EngineModuleCreateView(APIView):
    def post(self, request):
        return Response({"message": "Engine module created successfully"})

class EngineModuleDetailView(APIView):
    def get(self, request, id):
        return Response({"message": f"Engine module detail for {id}"})

class EngineModuleUpdateView(APIView):
    def put(self, request, id):
        return Response({
            "message": f"Engine module {id} updated successfully"
        })

class EngineModuleDeleteView(APIView):
    def delete(self, request, id):
        return Response({
            "message": f"Engine module {id} deleted successfully"
        })
 
class SidebarMenuView(APIView):
    def get(self, request):
        return Response({
            "menu": ["Home", "Dashboard", "Settings"]
        })

class UserTypeListView(APIView):
    def get(self, request):
        return Response({
            "user_types": ["admin", "user", "partner"]
        })

class UserTypeCreateView(APIView):
    def post(self, request):
        return Response({"message": "User type created successfully"})

class UserTypeDetailView(APIView):
    def get(self, request, id):
        return Response({"message": f"User type detail for {id}"})

class UserTypeUpdateView(APIView):
    def put(self, request, id):
        return Response({
            "message": f"User type {id} updated successfully"
        })

class UserTypeDeleteView(APIView):
    def delete(self, request, id):
        return Response({
            "message": f"User type {id} deleted successfully"
        })

class ClientListView(APIView):
    def get(self, request):
        return Response({"message": "Client list working"})

class ClientCreateView(APIView):
    def post(self, request):
        return Response({"message": "Client created successfully"})

class ClientDetailView(APIView):        
    def get(self, request, id):
        return Response({"message": f"Client detail for {id}"})

class ClientUpdateView(APIView):
    def put(self, request, id):
        return Response({
            "message": f"Client {id} updated successfully"
        })

class ClientDeleteView(APIView):
    def delete(self, request, id):
        return Response({
            "message": f"Client {id} deleted successfully"
        })

class CouponListView(APIView):
    def get(self, request):
        return Response({"message": "Coupon list working"})

class CouponCreateView(APIView):
    def post(self, request):
        return Response({"message": "Coupon created successfully"})

class CouponDetailView(APIView):
    def get(self, request, id):
        return Response({"message": f"Coupon detail for {id}"})

class CouponUpdateView(APIView):
    def put(self, request, id):
        return Response({
            "message": f"Coupon {id} updated successfully"
        })

class CouponDeleteView(APIView):
    def delete(self, request, id):
        return Response({
            "message": f"Coupon {id} deleted successfully"
        })

class CouponGenerateCodeView(APIView):
    def get(self, request):
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        return Response({"coupon_code": code})

class CouponValidateView(APIView):
    def post(self, request):
        coupon = request.data.get("coupon_code")

        if coupon == "ABC123":
            return Response({"valid": True})
        return Response({"valid": False})
class CountryCreateView(APIView):
    def post(self, request):
        return Response({"message": "Country created successfully"})

class CountryListView(APIView):
    def get(self, request):
        return Response({"message": "Country list working"})

class CountryDetailView(APIView):
    def get(self, request, id):
        return Response({"message": f"Country detail for {id}"})

class CountryUpdateView(APIView):
    def put(self, request, id):
        return Response({
            "message": f"Country {id} updated successfully"
        })

class CountryDeleteView(APIView):
    def delete(self, request, id):
        return Response({
            "message": f"Country {id} deleted successfully"
        })

class CityCreateView(APIView):
    def post(self, request):
        return Response({"message": "City created successfully"})

class CityListView(APIView):
    def get(self, request):
        return Response({"message": "City list working"})

class CityDetailView(APIView):
    def get(self, request, id):
        return Response({"message": f"City detail for {id}"})

class CityUpdateView(APIView):
    def put(self, request, id):
        return Response({
            "message": f"City {id} updated successfully"
        })

class CityDeleteView(APIView):
    def delete(self, request, id):
        return Response({
            "message": f"City {id} deleted successfully"
        })

class CityByStateView(APIView):
    def get(self, request, state_code):
        return Response({
            "message": f"Cities for state {state_code}"
        })

class StateCreateView(APIView):
    def post(self, request):
        return Response({"message": "State created successfully"})

class StateListView(APIView):
    def get(self, request):
        return Response({"message": "State list working"})

class StateDetailView(APIView):
    def get(self, request, id):
        return Response({"message": f"State detail for {id}"})

class StateUpdateView(APIView):
    def put(self, request, id):
        return Response({
            "message": f"State {id} updated successfully"
        })

class StateDeleteView(APIView):
    def delete(self, request, id):
        return Response({
            "message": f"State {id} deleted successfully"
        })

class RODownloadView(APIView):
    def get(self, request, campaign_code):
        return Response({
            "message": f"RO download for campaign {campaign_code}"
        })

class StateByCountryView(APIView):
    def get(self, request, country_code):
        return Response({
            "message": f"States for country {country_code}"
        })

class ModuleDropdownView(APIView):
    def get(self, request):
        return Response({
            "modules": ["Engine", "Client", "Settings", "Coupon"]
        })

class UrlDropdownView(APIView):
    def get(self, request):
        return Response({
            "urls": [
                "/api/",
                "/api/settings/",
                "/api/clients/",
                "/api/coupons/"
            ]
        })

class ClientFollowupListView(APIView):
    def get(self, request):
        return Response({"message": "Client followup list working"})

class ClientFollowupCreateView(APIView):
    def post(self, request):
        return Response({"message": "Client followup created successfully"})

class ClientFollowupDetailView(APIView):
    def get(self, request, id):
        return Response({"message": f"Client followup detail for {id}"})

class ClientFollowupUpdateView(APIView):
    def put(self, request, id):
        return Response({
            "message": f"Client followup {id} updated successfully"
        })

class ClientFollowupDeleteView(APIView):
    def delete(self, request, id):
        return Response({
            "message": f"Client followup {id} deleted successfully"
        })

class AssociateListCreateView(APIView):
    def get(self, request):
        return Response({"message": "Associate list working"})

    def post(self, request):
        return Response({"message": "Associate created successfully"})

class AssociateDetailView(APIView):
    def get(self, request, id):
        return Response({"message": f"Associate detail for {id}"})

    def put(self, request, id):
        return Response({
            "message": f"Associate {id} updated successfully"
        })

    def delete(self, request, id):
        return Response({
            "message": f"Associate {id} deleted successfully"
        })

class UserListCreateView(APIView):
    def get(self, request):
        return Response({"message": "User list working"})

    def post(self, request):
        return Response({"message": "User created successfully"})

class UserDetailView(APIView):
    def get(self, request, id):
        return Response({"message": f"User detail for {id}"})

    def put(self, request, id):
        return Response({
            "message": f"User {id} updated successfully"
        })

    def delete(self, request, id):
        return Response({
            "message": f"User {id} deleted successfully"
        })

class UserProfileView(APIView):
    def get(self, request):
        return Response({
            "message": "User profile working"
        })

class CinemaCreateView(APIView):
    def post(self, request):
        return Response({"message": "Cinema created successfully"})

class CinemaListView(APIView):
    def get(self, request):
        return Response({"message": "Cinema list working"})

class CinemaDetailView(APIView):
    def get(self, request, id):
        return Response({"message": f"Cinema detail for {id}"})

class CinemaUpdateView(APIView):
    def put(self, request, id):
        return Response({
            "message": f"Cinema {id} updated successfully"
        })

class CinemaDeleteView(APIView):
    def delete(self, request, id):
        return Response({
            "message": f"Cinema {id} deleted successfully"
        })

class CinemaFilterOptionsView(APIView):
    def get(self, request):
        return Response({
            "languages": ["Hindi", "Marathi", "English"],
            "formats": ["2D", "3D", "IMAX"],
            "locations": ["City A", "City B"]
        })

class ContactCreateView(APIView):
    def post(self, request):
        return Response({"message": "Contact submitted successfully"})

class ContactListView(APIView):
    def get(self, request):
        return Response({"message": "Contact list working"})

class ContactDetailView(APIView):
    def get(self, request, id):
        return Response({"message": f"Contact detail for {id}"})

class ContactUpdateView(APIView):    
    def put(self, request, id):
        return Response({
            "message": f"Contact {id} updated successfully"
        })

class ContactDeleteView(APIView):
    def delete(self, request, id):
        return Response({
            "message": f"Contact {id} deleted successfully"
        })

class CartAddView(APIView):
    def post(self, request):
        return Response({"message": "Item added to cart"})

class CartListView(APIView):
    def get(self, request):
        return Response({"message": "Cart list working"})

class CartDetailView(APIView):
    def get(self, request, id):
        return Response({"message": f"Cart detail for {id}"})

class CartUpdateView(APIView):
    def put(self, request, id):
        return Response({
            "message": f"Cart {id} updated successfully"
        })

class CartDeleteView(APIView):
    def delete(self, request, id):
        return Response({
            "message": f"Cart {id} deleted successfully"
        })

class CartProcessView(APIView):
    def post(self, request):
        return Response({"message": "Cart processed successfully"})

class CartCountView(APIView):
    def get(self, request):
        # इथे DB logic येईल
        return Response({"count": 0})

class WeeksListView(APIView):
    def get(self, request):
        return Response({
            "weeks": [1, 2, 3, 4, 5]
        })

class AdlengthsListView(APIView):
    def get(self, request):
        return Response({
            "ad_lengths": [10, 15, 20, 30, 60]
        })

class MovieSliderListView(APIView):
    def get(self, request):
        return Response({
            "sliders": [
                {"id": 1, "title": "Movie 1", "image": "img1.jpg"},
                {"id": 2, "title": "Movie 2", "image": "img2.jpg"},
            ]
        })

class MovieSliderCreateView(APIView):
    def post(self, request):
        return Response({"message": "Movie slider created successfully"})

class MovieSliderDetailView(APIView):
    def get(self, request, id):
        return Response({"message": f"Movie slider detail for {id}"})

class MovieSliderUpdateView(APIView):
    def put(self, request, id):
        return Response({
            "message": f"Movie slider {id} updated successfully"
        })

class MovieSliderDeleteView(APIView):
    def delete(self, request, id):
        return Response({
            "message": f"Movie slider {id} deleted successfully"
        })

class CouponRequestListView(APIView):
    def get(self, request):
        return Response({"requests": []})

class CouponRequestCreateView(APIView):
    def post(self, request):
        return Response({"message": "Coupon request created successfully"})

class CouponRequestDetailView(APIView):
    def get(self, request, id):
        return Response({"message": f"Coupon request detail for {id}"})

class CouponRequestUpdateView(APIView):
    def put(self, request, id):
        return Response({
            "message": f"Coupon request {id} updated successfully"
        })

class CouponRequestDeleteView(APIView):
    def delete(self, request, id):
        return Response({
            "message": f"Coupon request {id} deleted successfully"
        })

class TopBrandsListView(APIView):
    def get(self, request):
        return Response({"brands": []})

class TopBrandsCreateView(APIView):
    def post(self, request):
        return Response({"message": "Top brand created successfully"})

class TopBrandDetailView(APIView):
    def get(self, request, id):
        return Response({"message": f"Top brand detail for {id}"})

class TopBrandUpdateView(APIView):
    def put(self, request, id):
        return Response({
            "message": f"Top brand {id} updated successfully"
        })  

class TopBrandDeleteView(APIView):
    def delete(self, request, id):
        return Response({
            "message": f"Top brand {id} deleted successfully"
        })

class PartnerListView(APIView):
    def get(self, request):
        return Response({"partners": []})

class PartnerCreateView(APIView):
    def post(self, request):
        return Response({"message": "Partner created successfully"})

class PartnerDetailView(APIView):
    def get(self, request, id):
        return Response({"message": f"Partner detail for {id}"})

class PartnerUpdateView(APIView):
    def put(self, request, id):
        return Response({
            "message": f"Partner {id} updated successfully"
        })

class PartnerDeleteView(APIView):
    def delete(self, request, id):
        return Response({
            "message": f"Partner {id} deleted successfully"
        })

class PartnerBankDetailsListView(APIView):
    def get(self, request):
        return Response({"bank_details": []})

class PartnerBankDetailsCreateView(APIView):
    def post(self, request):
        return Response({"message": "Partner bank details created successfully"})

class PartnerBankDetailsDetailView(APIView):
    def get(self, request, id):
        return Response({"message": f"Partner bank details detail for {id}"})

class PartnerBankDetailsUpdateView(APIView):
    def put(self, request, id):
        return Response({
            "message": f"Partner bank details {id} updated successfully"
        })

class PartnerBankDetailsDeleteView(APIView):
    def delete(self, request, id):
        return Response({
            "message": f"Partner bank details {id} deleted successfully"
        })


