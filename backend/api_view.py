from django.http import JsonResponse, Http404
from rest_framework import status, permissions
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from .models import *
from .serializers import *
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.hashers import make_password
import os
import base64
import mimetypes
from django.core.mail import EmailMessage, send_mail
from django.db import transaction
from django.db import IntegrityError
from django.db.models import Q
from django.conf import settings
from datetime import datetime, timedelta
import jwt
from .models import Settings
from django.contrib.auth.hashers import check_password, make_password
from django.utils.timezone import now
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status, permissions
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from rest_framework.decorators import api_view
from backend.authentication import CustomJWTAuthentication
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from django.http import FileResponse, HttpResponse
from rest_framework.authentication import SessionAuthentication
import logging
logger = logging.getLogger(__name__)
import threading
import base64 

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Number to words conversion for Indian currency
def number_to_words_indian(amount):
    """Convert amount to words in Indian currency format"""

    ones = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
    teens = ["Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
    tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]

    def convert_below_hundred(n):
        if n < 10:
            return ones[n]
        elif n < 20:
            return teens[n - 10]
        else:
            return tens[n // 10] + (" " + ones[n % 10] if n % 10 != 0 else "")

    def convert_below_thousand(n):
        if n < 100:
            return convert_below_hundred(n)
        else:
            return ones[n // 100] + " Hundred" + (" " + convert_below_hundred(n % 100) if n % 100 != 0 else "")

    try:
        amount = float(amount)
        rupees = int(amount)
        paise = int(round((amount - rupees) * 100))

        if rupees == 0 and paise == 0:
            return "Zero Rupees Only"

        result = ""

        # Crore
        if rupees >= 10000000:
            crore = rupees // 10000000
            result += convert_below_thousand(crore) + " Crore "
            rupees %= 10000000

        # Lakh
        if rupees >= 100000:
            lakh = rupees // 100000
            result += convert_below_thousand(lakh) + " Lakh "
            rupees %= 100000

        # Thousand
        if rupees >= 1000:
            thousand = rupees // 1000
            result += convert_below_thousand(thousand) + " Thousand "
            rupees %= 1000

        # Hundred
        if rupees > 0:
            result += convert_below_thousand(rupees) + " "

        result = "Rupees " + result.strip()

        if paise > 0:
            result += " and Paise " + convert_below_hundred(paise)

        return result + " Only"

    except:
        return "Amount conversion error"

# def generate_quotation_pdf(book_campaign, cart_items, calculation):
#     buffer = io.BytesIO()
#     doc = SimpleDocTemplate(buffer, pagesize=letter)
#     styles = getSampleStyleSheet()
#     elements = []

#     elements.append(Paragraph("AdBajao Campaign Quotation", styles['Title']))
#     elements.append(Spacer(1, 12))

#     elements.append(Paragraph(f"Campaign Code: {book_campaign.campaign_code}", styles['Normal']))
#     elements.append(Paragraph(f"Customer ID: {book_campaign.customer_id}", styles['Normal']))
#     elements.append(Paragraph(f"Ad Length: {book_campaign.ad_length} sec", styles['Normal']))
#     elements.append(Paragraph(f"Weeks: {book_campaign.weeks}", styles['Normal']))
#     elements.append(Paragraph(f"Rate Type: {book_campaign.rate_type}", styles['Normal']))
#     elements.append(Paragraph(f"Ad Position: {book_campaign.ad_position}", styles['Normal']))
#     elements.append(Spacer(1, 12))

#     # Cart Items
#     data = [['Theater Name', 'City', 'State', 'Rate']]
#     for item in cart_items:
#         data.append([item.media_name, item.city, item.state, item.rate])
#     table = Table(data)
#     table.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.grey),
#                                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
#                                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
#                                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
#                                ('BOTTOMPADDING', (0,0), (-1,0), 12),
#                                ('BACKGROUND', (0,1), (-1,-1), colors.beige),
#                                ('GRID', (0,0), (-1,-1), 1, colors.black)]))
#     elements.append(table)
#     elements.append(Spacer(1, 12))

#     elements.append(Paragraph(f"Gross Total: ₹{calculation['gross_total']}", styles['Normal']))
#     elements.append(Paragraph(f"Discount: ₹{calculation['total_discount_perc']}", styles['Normal']))
#     elements.append(Paragraph(f"Coupon Discount: ₹{calculation['coupon_discount']}", styles['Normal']))
#     elements.append(Paragraph(f"Taxable Amount: ₹{calculation['taxable_amount']}", styles['Normal']))
#     elements.append(Paragraph(f"GST: ₹{calculation['gst']}", styles['Normal']))
#     elements.append(Paragraph(f"Total Payable: ₹{calculation['total_payable']}", styles['Normal']))

#     doc.build(elements)
#     buffer.seek(0)
#     return buffer

# def generate_receipt_pdf(book_campaign, cart_items, calculation):
#     # Similar to quotation, but for receipt
#     buffer = io.BytesIO()
#     doc = SimpleDocTemplate(buffer, pagesize=letter)
#     styles = getSampleStyleSheet()
#     elements = []

#     elements.append(Paragraph("AdBajao Campaign Receipt", styles['Title']))
#     elements.append(Spacer(1, 12))

#     elements.append(Paragraph(f"Campaign Code: {book_campaign.campaign_code}", styles['Normal']))
#     elements.append(Paragraph(f"Status: Confirmed", styles['Normal']))
#     elements.append(Paragraph(f"Payment Date: {timezone.now().date()}", styles['Normal']))
#     # Add payment details if any
#     elements.append(Spacer(1, 12))

#     # Same table
#     data = [['Theater Name', 'City', 'State', 'Rate']]
#     for item in cart_items:
#         data.append([item.media_name, item.city, item.state, item.rate])
#     table = Table(data)
#     table.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.grey),
#                                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
#                                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
#                                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
#                                ('BOTTOMPADDING', (0,0), (-1,0), 12),
#                                ('BACKGROUND', (0,1), (-1,-1), colors.beige),
#                                ('GRID', (0,0), (-1,-1), 1, colors.black)]))
#     elements.append(table)
#     elements.append(Spacer(1, 12))

#     elements.append(Paragraph(f"Total Paid: ₹{book_campaign.final_amount}", styles['Normal']))

#     doc.build(elements)
#     buffer.seek(0)
#     return buffer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username

        return token
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    """Custom token refresh view that handles Users model properly"""

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"error": "Token refresh failed", "detail": str(e)},
                status=status.HTTP_401_UNAUTHORIZED
            )


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def getRoutes(request):
    routes = [
        '/api/token',
        '/api/token/refresh',
    ]

    return Response(routes)


class CredentialsProvidedPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method != "POST":
            return False
        username = request.data.get("username")
        password = request.data.get("password")
        return bool(username and password)

 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            username_input = request.data.get("username")
            password_input = request.data.get("password")

            # ============================
            # STEP 1: Check user exists
            # ============================
            user = Users.objects.filter(username=username_input).first()
            if not user:
                return Response({"error": "User not found"}, status=401)

            # ============================
            # STEP 2: Check password
            # ============================
            if not check_password(password_input, user.password):
                return Response({"error": "Invalid password"}, status=401)

            # ============================
            # STEP 3: Get user type
            # ============================
            user_type_obj = Usertype.objects.filter(id=user.usertype_id).first()
            if not user_type_obj:
                return Response({"error": "Invalid user type"}, status=400)

            user_type = user_type_obj.usertype_name.lower()

            # ============================
            # STEP 4: Generate JWT
            # ============================
            refresh = RefreshToken.for_user(user)

            response_data = {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "role": user_type,
                "user_id": user.user_id,
            }

            # ============================
            # STEP 5: ROLE BASED DATA
            # ============================

            if user_type == "admin":
                employee = Employee.objects.filter(employee_code=user.employee_code).first()

                if employee:
                    company_code_value = (
                        employee.company_code.company_code
                        if hasattr(employee.company_code, 'company_code')
                        else employee.company_code
                    )

                    response_data.update({
                        "username": employee.employee_firstname + " " + employee.employee_lastname,
                        "employee_code": employee.employee_code,
                        "company_code": company_code_value,
                    })
                else:
                    response_data.update({
                        "username": user.username,
                        "employee_code": None,
                        "company_code": str(user.company_code) if user.company_code else None,
                    })

            elif user_type == "associate":
                associate = Associates.objects.filter(associate_code=user.associate_code).first()

                if not associate:
                    return Response({"error": "Associate not found"}, status=404)

                response_data.update({
                    "username": associate.name,
                    "associate_code": associate.associate_code,
                })

            elif user_type == "partner":
                partner = Partner.objects.filter(partner_code=user.partner_code).first()

                if not partner:
                    return Response({"error": "Partner not found"}, status=404)

                response_data.update({
                    "username": partner.name,
                    "partner_code": partner.partner_code,
                    "company_code": str(user.company_code) if user.company_code else None,
                })

            elif user_type == "customer":
                customer = Customer.objects.filter(customer_code=user.customer_code).first()

                if not customer:
                    return Response({"error": "Customer not found"}, status=404)

                response_data.update({
                    "username": customer.name,
                    "customer_code": customer.customer_code,
                    "company_code": str(customer.company_code) if customer.company_code else None,
                    "city_code": customer.city_code,
                    "state": customer.state,
                    "gstin": customer.gstin,
                })

            # ============================
            # STEP 6: Update last visit
            # ============================
            user.lastvisiton = timezone.now()
            user.save()

            # ============================
            # STEP 7: Modules (permissions)
            # ============================
            permissions = Permissions.objects.filter(
                usertype_id=user.usertype_id,
                e_read='Yes'
            )

            module_ids = [perm.module_id for perm in permissions]

            modules = EngineModule.objects.filter(
                id__in=module_ids,
                status=1
            ).order_by('sequence')

            modules_data = []
            for module in modules:
                modules_data.append({
                    "id": module.id,
                    "modulename": module.modulename,
                    "url": module.url,
                    "icon": module.icon,
                    "sequence": module.sequence,
                })

            response_data["modules"] = modules_data

            # ============================
            # STEP 8: SAVE SESSION
            # ============================
            request.session["user_data"] = response_data
            request.session["is_logged_in"] = True

            # ============================
            # STEP 9: PRINT SESSION (DEBUG)
            # ============================
            print("SESSION FULL:", dict(request.session))
            print("USER SESSION:", request.session.get("user_data"))

            return Response(response_data, status=200)

        except Exception as e:
            import traceback
            print("LOGIN ERROR:", str(e))
            traceback.print_exc()
            return Response({"error": str(e)}, status=500)
 


class RequestOTPView(APIView):
    permission_classes = [AllowAny] # This allows the email request without a token
    def post(self, request):
        email = request.data.get("email")
        try:
            user = Users.objects.get(email=email, status=1)
            otp = str(random.randint(100000, 999999))
            
            # Save to your new model fields
            user.otp_code = otp
            user.otp_expiry = timezone.now() + timedelta(minutes=5)
            user.save()

            # Using your Hostinger settings from settings.py
            send_mail(
                'Your AdBajao Password Reset Code',
                f'Your OTP is: {otp}. It expires in 5 minutes.',
                'hr@sanpurnam.in', 
                [email],
                fail_silently=False,
            )
            return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)
        except Users.DoesNotExist:
            # Security: return 200 so hackers don't know if email exists
            return Response({"message": "If this email exists, an OTP has been sent."}, status=status.HTTP_200_OK)

class ResetPasswordView(APIView):
    permission_classes = [AllowAny] # This allows password change without a token
    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")
        new_password = request.data.get("new_password")

        try:
            # Validate user by email and otp_code
            user = Users.objects.get(email=email, otp_code=otp, status=1)
            
            # Check if OTP is expired
            if user.otp_expiry < timezone.now():
                return Response({"error": "OTP has expired"}, status=status.HTTP_400_BAD_REQUEST)

            # Update Password & Clear OTP fields
            user.password = make_password(new_password)
            user.otp_code = None
            user.otp_expiry = None
            user.save()

            # Auto-Login: Generate JWT immediately
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Password updated successfully",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "username": user.username
            }, status=status.HTTP_200_OK)

        except Users.DoesNotExist:
            return Response({"error": "Invalid OTP or Email"}, status=status.HTTP_400_BAD_REQUEST)

from django.db.models import Max
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(APIView):
    permission_classes = [CredentialsProvidedPermission]

    def post(self, request):
        # Extract data dynamically from request
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")
        
        # Get optional fields if they exist in the request, otherwise None
        employee_code = request.data.get("employee_code", None)
        usertype_id = request.data.get("usertype_id", 1) # Default to 1 or None

        if not username or not password:
            return Response({"error": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST)

        if Users.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        # AUTO-INCREMENT LOGIC
        max_id = Users.objects.aggregate(Max('user_id'))['user_id__max']
        next_user_id = (max_id or 0) + 1 

        try:
            user = Users.objects.create(
                user_id=next_user_id,
                username=username,
                password=make_password(password),
                email=email,
                status=1,
                superuser=0,
                usertype_id=usertype_id, 
                employee_code=employee_code, # This will be NULL if not provided
            )

            refresh = RefreshToken.for_user(user)

            return Response({
                "message": "User registered successfully",
                "user_id": user.user_id,
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SettingsListView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, format=None):
        settings = Settings.objects.all()
        serializer = SettingsSerializer(settings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SettingsDetailView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, setting_id, format=None):
        setting = get_object_or_404(Settings, setting_id=setting_id)
        serializer = SettingsSerializer(setting)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SettingsCreateView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        data = request.data.copy()

        # 1. Clean data: Convert empty strings to None (null) for the database
        for field in ['module_code', 'submodule_code', 'activity_code']:
            if data.get(field) == "":
                data[field] = None

        # 2. Duplicate Check with improved logic
        if Settings.objects.filter(
            setting_name=data.get('setting_name'),
            module_code=data.get('module_code'),
            submodule_code=data.get('submodule_code'),
            activity_code=data.get('activity_code')
        ).exists():
            return Response({"error": "This configuration already exists"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = SettingsSerializer(data=data)
        if serializer.is_valid():
            # 3. Use request.user.id for tracking
            serializer.save(
                created_by=request.user.id,
                updated_by=request.user.id,
                created_on=timezone.now(),
                updated_on=timezone.now()
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # If serializer fails, it returns why (e.g., "This field is required")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SettingsUpdateView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, setting_id, format=None):
        setting = get_object_or_404(Settings, setting_id=setting_id)
        serializer = SettingsSerializer(setting)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def put(self, request, setting_id, format=None):
        setting = get_object_or_404(Settings, setting_id=setting_id)
        data = request.data.copy()

        serializer = SettingsSerializer(setting, data=data, partial=True)
        if serializer.is_valid():
            serializer.save(
                updated_by=request.user.id,
                updated_on=timezone.now()
            )
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SettingsDeleteView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, setting_id, format=None):
        setting = get_object_or_404(Settings, setting_id=setting_id)
        serializer = SettingsSerializer(setting)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def delete(self, request, setting_id, format=None):
        setting = get_object_or_404(Settings, setting_id=setting_id)
        setting.delete()
        return Response({"message": "Setting deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



# # Engine
# class EngineModuleCreateView(APIView):
#     authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#     def post(self, request):
#         try:
#             serializer = EngineModuleSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save(
#                     created_by=request.user.id,
#                     created_on=timezone.now(),
#                 )
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response(
#                 {"error": str(e)},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )
 
# class EngineModuleListView(APIView):
#     authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#     def get(self, request):
#         try:
#             data = EngineModule.objects.all().order_by('module_code')
#             serializer = EngineModuleSerializer(data, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response(
#                 {"error": str(e)},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )
 
# class EngineModuleDetailView(APIView):
#     authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#     def get(self, request, module_code, format=None):
#         module = get_object_or_404(EngineModule, module_code=module_code)
#         serializer = EngineModuleSerializer(module)
 
#         return Response(serializer.data, status=status.HTTP_200_OK)
 
# class EngineModuleUpdateView(APIView):
#     authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#     def put(self, request, module_code):
#         try:
#             obj = get_object_or_404(EngineModule, module_code=module_code)
#             serializer = EngineModuleSerializer(obj, data=request.data, partial=True)
#             if serializer.is_valid():
#                 serializer.save(
#                     updated_by=request.user.id,
#                     updated_on=timezone.now()
#                 )
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response(
#                 {"error": str(e)},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )
 
# class EngineModuleDeleteView(APIView):
#     authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#     def delete(self, request, module_code):
#         try:
#             module = get_object_or_404(EngineModule, module_code=module_code)
#             module.delete()
    
#             return Response(
#                 {"message": "Engine Module deleted successfully"},
#                 status=status.HTTP_204_NO_CONTENT
#             )
#         except Exception as e:
#             return Response(
#                 {"error": str(e)},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )
 
 
# Engine Submodule
class EngineSubmoduleCreateView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            data = request.data.copy()
            permissions_data = data.pop("permissions", {})

            # Save submodule first
            serializer = EngineSubmoduleSerializer(data=data)

            if serializer.is_valid():
                submodule = serializer.save()

                # Save permissions
                for usertype_id, perms in permissions_data.items():
                    Permissions.objects.create(
                        submodule_id=submodule.id,
                        usertype_id=usertype_id,
                        e_read="Yes" if perms.get("read") else "No",
                        e_write="Yes" if perms.get("write") else "No",
                        e_update="Yes" if perms.get("update") else "No",
                    )

                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
class EngineSubmoduleListView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            submodules = EngineSubmodule.objects.all().order_by('id')
            result = []

            for submodule in submodules:
                submodule_data = EngineSubmoduleSerializer(submodule).data

                # Fetch permissions for this submodule
                perms = Permissions.objects.filter(submodule_id=submodule.id)
                permissions_dict = {}

                for perm in perms:
                    permissions_dict[str(perm.usertype_id)] = {
                        "read": perm.e_read == "Yes",
                        "write": perm.e_write == "Yes",
                        "update": perm.e_update == "Yes"
                    }

                submodule_data['permissions'] = permissions_dict
                result.append(submodule_data)

            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
 
class EngineSubmoduleDetailView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id, format=None):
        submodule = get_object_or_404(EngineSubmodule, id=id)
        submodule_data = EngineSubmoduleSerializer(submodule).data

        # Fetch permissions for this submodule
        perms = Permissions.objects.filter(submodule_id=submodule.id)
        permissions_dict = {}

        for perm in perms:
            permissions_dict[str(perm.usertype_id)] = {
                "read": perm.e_read == "Yes",
                "write": perm.e_write == "Yes",
                "update": perm.e_update == "Yes"
            }

        submodule_data['permissions'] = permissions_dict
        return Response(submodule_data, status=status.HTTP_200_OK)
 
class EngineSubmoduleUpdateView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, id):
        try:
            submodule = get_object_or_404(EngineSubmodule, id=id)

            data = request.data.copy()
            permissions_data = data.pop("permissions", {})

            serializer = EngineSubmoduleSerializer(submodule, data=data, partial=True)

            if serializer.is_valid():
                serializer.save()

                # Delete old permissions
                Permissions.objects.filter(submodule_id=submodule.id).delete()

                # Create new permissions
                for usertype_id, perms in permissions_data.items():
                    Permissions.objects.create(
                        submodule_id=submodule.id,
                        usertype_id=usertype_id,
                        e_read="Yes" if perms.get("read") else "No",
                        e_write="Yes" if perms.get("write") else "No",
                        e_update="Yes" if perms.get("update") else "No",
                    )

                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
 
class EngineSubmoduleDeleteView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, pk):
        try:
            obj = get_object_or_404(EngineSubmodule, pk=pk)
            obj.delete()
     
            return Response(
                {"message": "Engine Submodule deleted successfully"},
                status=status.HTTP_204_NO_CONTENT
            )
        except Http404:
            return Response({"error": "Submodule not found"}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError:
            return Response({"error": "Cannot delete submodule with existing activities"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) 
 
# Engine Activity
class EngineActivityCreateView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            data = request.data.copy()
            permissions_data = data.pop("permissions", {})

            # Save activity first
            serializer = EngineActivitySerializer(data=data)

            if serializer.is_valid():
                activity = serializer.save()

                # Save permissions
                for usertype_id, perms in permissions_data.items():
                    Permissions.objects.create(
                        activity_id=activity.id,
                        usertype_id=usertype_id,
                        e_read="Yes" if perms.get("read") else "No",
                        e_write="Yes" if perms.get("write") else "No",
                        e_update="Yes" if perms.get("update") else "No",
                    )

                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
class EngineActivityListView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            activities = EngineActivity.objects.all().order_by('id')
            result = []

            for activity in activities:
                activity_data = EngineActivitySerializer(activity).data

                # Fetch permissions for this activity
                perms = Permissions.objects.filter(activity_id=activity.id)
                permissions_dict = {}

                for perm in perms:
                    permissions_dict[str(perm.usertype_id)] = {
                        "read": perm.e_read == "Yes",
                        "write": perm.e_write == "Yes",
                        "update": perm.e_update == "Yes"
                    }

                activity_data['permissions'] = permissions_dict
                result.append(activity_data)

            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
 
class EngineActivityDetailView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id, format=None):
        activity = get_object_or_404(EngineActivity, id=id)
        activity_data = EngineActivitySerializer(activity).data

        # Fetch permissions for this activity
        perms = Permissions.objects.filter(activity_id=activity.id)
        permissions_dict = {}

        for perm in perms:
            permissions_dict[str(perm.usertype_id)] = {
                "read": perm.e_read == "Yes",
                "write": perm.e_write == "Yes",
                "update": perm.e_update == "Yes"
            }

        activity_data['permissions'] = permissions_dict
        return Response(activity_data, status=status.HTTP_200_OK)
 
class EngineActivityUpdateView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, id):
        try:
            activity = get_object_or_404(EngineActivity, id=id)

            data = request.data.copy()
            permissions_data = data.pop("permissions", {})

            serializer = EngineActivitySerializer(activity, data=data, partial=True)

            if serializer.is_valid():
                serializer.save()

                # Delete old permissions
                Permissions.objects.filter(activity_id=activity.id).delete()

                # Create new permissions
                for usertype_id, perms in permissions_data.items():
                    Permissions.objects.create(
                        activity_id=activity.id,
                        usertype_id=usertype_id,
                        e_read="Yes" if perms.get("read") else "No",
                        e_write="Yes" if perms.get("write") else "No",
                        e_update="Yes" if perms.get("update") else "No",
                    )

                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
class EngineActivityDeleteView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, id):
        try:
            obj = get_object_or_404(EngineActivity, id=id)
            obj.delete()
    
            return Response(
                {"message": "Engine Activity deleted successfully"},
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

      
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.authentication import SessionAuthentication
 
from .models import EngineModule
from .serializers import EngineModuleSerializer
from .authentication import CustomJWTAuthentication
 
 
class EngineModuleCreateView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            data = request.data.copy()
            permissions_data = data.pop("permissions", {})

            # Save module first
            serializer = EngineModuleSerializer(data=data)

            if serializer.is_valid():
                module = serializer.save(created_by=request.user.id)

                # 🔥 SAVE PERMISSIONS
                for usertype_id, perms in permissions_data.items():
                    Permissions.objects.create(
                        module_id=module.id,
                        usertype_id=usertype_id,
                        e_read="Yes" if perms.get("read") else "No",
                        e_write="Yes" if perms.get("write") else "No",
                        e_update="Yes" if perms.get("update") else "No",
                    )

                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
class EngineModuleListView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            modules = EngineModule.objects.all().order_by('sequence')
            result = []

            for module in modules:
                module_data = EngineModuleSerializer(module).data

                # Fetch permissions for this module
                perms = Permissions.objects.filter(module_id=module.id)
                permissions_dict = {}

                for perm in perms:
                    permissions_dict[str(perm.usertype_id)] = {
                        "read": perm.e_read == "Yes",
                        "write": perm.e_write == "Yes",
                        "update": perm.e_update == "Yes"
                    }

                module_data['permissions'] = permissions_dict
                result.append(module_data)

            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
       
class EngineModuleDetailView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id, format=None):
        module = get_object_or_404(EngineModule, id=id)
        module_data = EngineModuleSerializer(module).data

        # Fetch permissions for this module
        perms = Permissions.objects.filter(module_id=module.id)
        permissions_dict = {}

        for perm in perms:
            permissions_dict[str(perm.usertype_id)] = {
                "read": perm.e_read == "Yes",
                "write": perm.e_write == "Yes",
                "update": perm.e_update == "Yes"
            }

        module_data['permissions'] = permissions_dict
        return Response(module_data, status=status.HTTP_200_OK)
class EngineModuleUpdateView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, id):
        try:
            module = get_object_or_404(EngineModule, id=id)

            data = request.data.copy()
            permissions_data = data.pop("permissions", {})

            serializer = EngineModuleSerializer(module, data=data, partial=True)

            if serializer.is_valid():
                serializer.save(
                    updated_by=request.user.id,
                    updated_on=timezone.now()
                )

                # 🔥 DELETE OLD PERMISSIONS
                Permissions.objects.filter(module_id=module.id).delete()

                # 🔥 CREATE NEW PERMISSIONS
                for usertype_id, perms in permissions_data.items():
                    Permissions.objects.create(
                        module_id=module.id,
                        usertype_id=usertype_id,
                        e_read="Yes" if perms.get("read") else "No",
                        e_write="Yes" if perms.get("write") else "No",
                        e_update="Yes" if perms.get("update") else "No",
                    )

                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class EngineModuleDeleteView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
 
    def delete(self, request, pk):
        try:
            module = get_object_or_404(EngineModule, pk=pk)
            module.delete()
 
            return Response(
                {"message": "Engine Module deleted successfully"},
                status=status.HTTP_204_NO_CONTENT
            )
 
        except Http404:
            return Response({"error": "Module not found"}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError:
            return Response({"error": "Cannot delete module with existing submodules or activities"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SidebarMenuView(APIView):
    """
    Returns hierarchical sidebar menu structure from database.
    Modules -> Submodules -> Activities (if any)
    Filtered based on user's permissions.
    """
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            # Get the authenticated user
            user = request.user

            # Get user's usertype_id
            if hasattr(user, 'usertype_id'):
                usertype_id = user.usertype_id
            else:
                # Fallback: try to get from Users model
                try:
                    user_obj = Users.objects.get(username=user.username)
                    usertype_id = user_obj.usertype_id
                except Users.DoesNotExist:
                    return Response({"error": "User type not found"}, status=status.HTTP_400_BAD_REQUEST)

            # Get all permissions for this user type (where e_read = 'Yes')
            permissions_qs = Permissions.objects.filter(usertype_id=usertype_id, e_read='Yes')

            # Get permitted IDs
            permitted_module_ids = [perm.module_id for perm in permissions_qs if perm.module_id]
            permitted_submodule_ids = [perm.submodule_id for perm in permissions_qs if perm.submodule_id]
            permitted_activity_ids = [perm.activity_id for perm in permissions_qs if perm.activity_id]

            # Get only permitted active modules ordered by sequence
            modules = EngineModule.objects.filter(
                id__in=permitted_module_ids,
                status=1
            ).order_by('sequence', 'id')

            sidebar_data = []

            for module in modules:
                module_data = {
                    'id': module.id,
                    'title': module.modulename,
                    'url': module.url,
                    'icon': module.icon or 'Settings',
                    'children': []
                }

                # Get submodules for this module that user has permission to read
                submodules = EngineSubmodule.objects.filter(
                    module_id=module.id,
                    id__in=permitted_submodule_ids,
                    status=1
                ).order_by('id')

                for submodule in submodules:
                    submodule_data = {
                        'id': submodule.id,
                        'title': submodule.submodule_name,
                        'url': submodule.url,
                        'icon': submodule.icon or 'Layers',
                        'children': []
                    }

                    # Get activities for this submodule that user has permission to read
                    activities = EngineActivity.objects.filter(
                        submodule_id=submodule.id,
                        id__in=permitted_activity_ids,
                        status=1
                    ).order_by('id')

                    for activity in activities:
                        activity_data = {
                            'id': activity.id,
                            'title': activity.activity_name,
                            'url': activity.url,
                        }
                        submodule_data['children'].append(activity_data)

                    # Add submodule to module's children
                    module_data['children'].append(submodule_data)

                # Add module to sidebar
                sidebar_data.append(module_data)

            return Response(sidebar_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
 
class UserTypeListView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        usertypes = Usertype.objects.all()
        data = [
            {
                "usertype_id": u.usertype_id,
                "usertype_name": u.usertype_name
            }
            for u in usertypes
        ]
        return Response(data)
    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from .models import Customer, Users
from .serializers import CustomerSerializer
from .authentication import CustomJWTAuthentication
from rest_framework.authentication import SessionAuthentication

class ClientCreateView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            data = request.data.copy()

            # ============================
            # GET USER FROM TOKEN (JWT)
            # ============================
            user = request.user

            partner_code = getattr(user, "partner_code", None)
            associate_code = getattr(user, "associate_code", None)

            # ============================
            # PASSWORD HASH
            # ============================
            raw_password = data.get('password')
            if raw_password:
                data['password'] = make_password(raw_password)

            # ============================
            # REMOVE SYSTEM FIELDS FROM INPUT
            # ============================
            data.pop('partner_code', None)
            data.pop('associate_code', None)

            # ============================
            # SERIALIZER
            # ============================
            serializer = CustomerSerializer(data=data)

            if serializer.is_valid():

                customer = serializer.save(
                    createdby=user,   # assuming FK to Users
                    createdon=timezone.now(),
                    partner_code=partner_code,
                    associate_code=associate_code
                )

                # ============================
                # POST SAVE FIXES
                # ============================
                if not customer.customer_code:
                    customer.customer_code = str(customer.id)

                if not customer.company_code and hasattr(user, 'company_code'):
                    customer.company_code = user.company_code

                customer.save()

                # ============================
                # EMAIL CHECK
                # ============================
                if Users.objects.filter(email=customer.email_id).exists():
                    return Response(
                        {"error": "User already exists with this email"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # ============================
                # CREATE USER ENTRY
                # ============================
                new_user = Users.objects.create(
                    username=customer.contact_number[:20],
                    password=customer.password,
                    email=customer.email_id,
                    status=1,
                    superuser=0,
                    usertype_id=2,
                    customer_code=customer.customer_code,
                    company_code=customer.company_code,
                    partner_code=partner_code,
                    associate_code=associate_code,
                    createdon=timezone.now()
                )

                new_user.user_id = new_user.id
                new_user.save()

                return Response({
                    "message": "Client created successfully",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)

            return Response({
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class ClientListView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            # ============================
            # TRY SESSION FIRST
            # ============================
            session_data = request.session.get("user_data", {})

            partner_code = session_data.get("partner_code")
            associate_code = session_data.get("associate_code")

            # ============================
            # FALLBACK TO JWT (IMPORTANT)
            # ============================
            if not partner_code and not associate_code:
                user = request.user
                partner_code = getattr(user, "partner_code", None)
                associate_code = getattr(user, "associate_code", None)

            # ============================
            # FILTERING
            # ============================
            if partner_code:
                customers = Customer.objects.filter(partner_code=partner_code)

            elif associate_code:
                customers = Customer.objects.filter(associate_code=associate_code)

            else:
                customers = Customer.objects.all()

            customers = customers.order_by('-createdon')

            serializer = CustomerSerializer(customers, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ClientDetailView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, customer_code):
        try:
            usertype_id = request.session.get("UserType")
            partner_code = request.session.get("PartnerCode")
            associate_code = request.session.get("Associate_code")

            # Get customer
            customer = Customer.objects.get(customer_code=customer_code)

            # 🔒 ACCESS CONTROL (CORE LOGIC)

            # Partner → only his clients
            if usertype_id in ["Partner", "partner"]:
                if not customer.partner_code or customer.partner_code != partner_code:
                    return Response(
                        {"error": "You are not authorized to view this client"},
                        status=status.HTTP_403_FORBIDDEN
                    )

            # Associate → only his clients
            elif usertype_id in ["Associate", "associate"]:
                if not customer.associate_code or customer.associate_code != associate_code:
                    return Response(
                        {"error": "You are not authorized to view this client"},
                        status=status.HTTP_403_FORBIDDEN
                    )

            # Admin → no restriction (can view all)

            serializer = CustomerSerializer(customer)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Customer.DoesNotExist:
            return Response(
                {"error": "Client not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ClientUpdateView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, customer_code):
        try:
            usertype_id = request.session.get("UserType")
            partner_code = request.session.get("PartnerCode")
            associate_code = request.session.get("Associate_code")
            user_id = request.session.get("user_id")

            customer = get_object_or_404(Customer, customer_code=customer_code)

            # ACCESS CONTROL
            if usertype_id in ["Partner", "partner"]:
                if customer.partner_code != partner_code:
                    return Response({"error": "Unauthorized"}, status=403)

            elif usertype_id in ["Associate", "associate"]:
                if customer.associate_code != associate_code:
                    return Response({"error": "Unauthorized"}, status=403)

            data = request.data.copy()
            raw_password = data.get('password')

            if raw_password:
                data['password'] = make_password(raw_password)

            serializer = CustomerSerializer(customer, data=data, partial=True)

            if serializer.is_valid():
                updated_customer = serializer.save()

                updated_customer.updatedby = user_id
                updated_customer.updatedon = timezone.now()
                updated_customer.save()

                user = Users.objects.filter(customer_code=customer_code).first()

                if user:
                    if 'email' in data:
                        user.email = data['email']

                    if raw_password:
                        user.password = updated_customer.password

                    if 'contact_number' in data:
                        user.username = data['contact_number'][:20]

                    user.updatedon = timezone.now()
                    user.save()

                return Response({
                    "message": "Customer updated successfully",
                    "data": serializer.data
                }, status=200)

            return Response(serializer.errors, status=400)

        except Exception as e:
            return Response({"error": str(e)}, status=500)


class ClientDeleteView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, customer_code):
        try:
            usertype_id = request.session.get("UserType")
            partner_code = request.session.get("PartnerCode")
            associate_code = request.session.get("Associate_code")

            try:
                customer = Customer.objects.get(pk=int(customer_code))
            except:
                customer = get_object_or_404(Customer, customer_code=customer_code)

            # ACCESS CONTROL
            if usertype_id in ["Partner", "partner"]:
                if customer.partner_code != partner_code:
                    return Response({"error": "Unauthorized"}, status=403)

            elif usertype_id in ["Associate", "associate"]:
                if customer.associate_code != associate_code:
                    return Response({"error": "Unauthorized"}, status=403)

            Users.objects.filter(customer_code=customer.customer_code).delete()
            customer.delete()

            return Response(
                {"message": "Client deleted successfully"},
                status=204
            )

        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
        
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.authentication import SessionAuthentication

from .models import Countries
from .serializers import CountrySerializer 
from .authentication import CustomJWTAuthentication

class CountryCreateView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            serializer = CountrySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(
                    createdby=request.user,
                    createdon=timezone.now()
                )
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CountryListView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            countries = Countries.objects.all().order_by('country_name')
            serializer = CountrySerializer(countries, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CountryDetailView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, country_code):
        country = get_object_or_404(Countries, country_code=country_code)
        serializer = CountrySerializer(country)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CountryUpdateView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, country_code):
        try:
            country = get_object_or_404(Countries, country_code=country_code)
            serializer = CountrySerializer(country, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save(
                    updatedby=request.user,
                    updatedon=timezone.now()
                )
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CountryDeleteView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, country_code):
        try:
            country = get_object_or_404(Countries, country_code=country_code)
            country.delete()
            return Response(
                {"message": "Country deleted successfully"},
                status=status.HTTP_204_NO_CONTENT
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.authentication import SessionAuthentication

from .models import Cities
from .serializers import CitySerializer
from .authentication import CustomJWTAuthentication

class CityCreateView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            serializer = CitySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(
                    createdby=request.user.user_id,  # INTEGER FIELD
                    createdon=timezone.now()
                )
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class CityListView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            cities = Cities.objects.all().order_by('city_name')
            serializer = CitySerializer(cities, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class CityByStateView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, state_code):
        try:
            cities = Cities.objects.filter(state_code=state_code).order_by('city_name')
            serializer = CitySerializer(cities, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class CityDetailView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, city_code):
        city = get_object_or_404(Cities, city_code=city_code)
        serializer = CitySerializer(city)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CityUpdateView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, city_code):
        try:
            city = get_object_or_404(Cities, city_code=city_code)
            serializer = CitySerializer(city, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save(
                    updatedby=request.user.user_id,  # INTEGER FIELD
                    updatedon=timezone.now()
                )
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class CityDeleteView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, city_code):
        try:
            city = get_object_or_404(Cities, city_code=city_code)
            city.delete()
            return Response(
                {"message": "City deleted successfully"},
                status=status.HTTP_204_NO_CONTENT
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.authentication import SessionAuthentication

from .models import States
from .serializers import StateSerializer
from .authentication import CustomJWTAuthentication

class StateCreateView(APIView):
        authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
        permission_classes = [permissions.IsAuthenticated]

        def post(self, request):
            try:
                serializer = StateSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(
                        createdby=request.user.user_id,  # INTEGER FIELD
                        createdon=timezone.now()
                    )
                    return Response(serializer.data, status=status.HTTP_201_CREATED)

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
class StateListView(APIView):
        authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
        permission_classes = [permissions.IsAuthenticated]

        def get(self, request):
            try:
                states = States.objects.all().order_by('state_name')
                serializer = StateSerializer(states, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
class StateByCountryView(APIView):
        authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
        permission_classes = [permissions.IsAuthenticated]

        def get(self, request, country_code):
            try:
                states = States.objects.filter(country_code=country_code).order_by('state_name')
                serializer = StateSerializer(states, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
class StateDetailView(APIView):
        authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
        permission_classes = [permissions.IsAuthenticated]

        def get(self, request, state_code):
            state = get_object_or_404(States, state_code=state_code)
            serializer = StateSerializer(state)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
class StateUpdateView(APIView):
        authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
        permission_classes = [permissions.IsAuthenticated]

        def put(self, request, state_code):
            try:
                state = get_object_or_404(States, state_code=state_code)
                serializer = StateSerializer(state, data=request.data, partial=True)

                if serializer.is_valid():
                    serializer.save(
                        updatedby=request.user.user_id,  # INTEGER FIELD
                        updatedon=timezone.now()
                    )
                    return Response(serializer.data, status=status.HTTP_200_OK)

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
class StateDeleteView(APIView):
        authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
        permission_classes = [permissions.IsAuthenticated]

        def delete(self, request, state_code):
            try:
                state = get_object_or_404(States, state_code=state_code)
                state.delete()
                return Response(
                    {"message": "State deleted successfully"},
                    status=status.HTTP_204_NO_CONTENT
                )

            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                ) 


class ModuleDropdownView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            modules = EngineModule.objects.filter(status=1).values('id', 'modulename')
            return Response(modules, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UrlDropdownView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Providing a set of common URLs as requested for dynamic call
        urls = [
            "/masters/module",
            "/masters/submodule", 
            "/masters/activity", 
            "clients", 
            "countries",
            "states",
            "cities",
        ]
        return Response(urls, status=status.HTTP_200_OK) 
    
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, serializers
from rest_framework.authentication import SessionAuthentication
from .models import Customer, CustomerFollowup
from .serializers import CustomerFollowupSerializer 
from .authentication import CustomJWTAuthentication
import datetime

class ClientFollowupCreateView(APIView):
    """Handles creation, fixes time format, and ensures fresh client data is saved."""
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated] 

    def post(self, request): 
        try:
            # 1. Get Session/User Data for Partner/Associate
            session_data = request.session.get("user_data", {})
            partner_code = session_data.get("partner_code") or getattr(request.user, "partner_code", None)
            associate_code = session_data.get("associate_code") or getattr(request.user, "associate_code", None)

            # 2. Prepare and Clean Data
            data = request.data.copy()
            
            # --- FIX FOR THE TIME ERROR ---
            time_val = data.get('time')
            if time_val:
                try:
                    if 'T' in str(time_val):
                        data['time'] = time_val.split('T')[1][:8]
                except Exception:
                    data['time'] = timezone.now().strftime('%H:%M:%S')
            else:
                data['time'] = timezone.now().strftime('%H:%M:%S')

            # 3. Inject current user codes into data dictionary
            if partner_code: data['partner_code'] = partner_code
            if associate_code: data['associate_code'] = associate_code

            serializer = CustomerFollowupSerializer(data=data) 
            
            if serializer.is_valid():
                # 4. Save with EXPLICIT fields from the request
                # This ensures the selected client's code and contact number are used
                serializer.save(
                    createdby=request.user,
                    createdon=timezone.now(),
                    partner_code=partner_code,
                    associate_code=associate_code,
                    # We pull these directly from data to ensure they aren't missed
                    customer_code=data.get('customer_code'), 
                    contact_no=data.get('contact_no'),
                    type=data.get('type'),
                    visit_for=data.get('visit_for'),
                    follow_up_type=data.get('follow_up_type')
                )
                return Response(serializer.data, status=status.HTTP_201_CREATED) 
            
            print("Serializer Errors:", serializer.errors) 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ClientFollowupListView(APIView):
    """Fetches client follow-ups with session-first filtering logic."""
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            # ============================
            # TRY SESSION FIRST
            # ============================
            session_data = request.session.get("user_data", {})
            partner_code = session_data.get("partner_code")
            associate_code = session_data.get("associate_code")

            # ============================
            # FALLBACK TO JWT (IMPORTANT)
            # ============================
            if not partner_code and not associate_code:
                user = request.user
                partner_code = getattr(user, "partner_code", None)
                associate_code = getattr(user, "associate_code", None)

            # Ordering by createdon descending to show newest follow-ups first
            # FILTERING
            if partner_code:
                followups = CustomerFollowup.objects.filter(partner_code=partner_code).order_by('-createdon')
            elif associate_code:
                followups = CustomerFollowup.objects.filter(associate_code=associate_code).order_by('-createdon')
            else:
                followups = CustomerFollowup.objects.all().order_by('-createdon')
            serializer = CustomerFollowupSerializer(followups, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ClientFollowupDetailView(APIView):
    """Retrieves a single follow-up via its ID."""
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated] 

    def get(self, request, id):
        try:
            followup = get_object_or_404(CustomerFollowup, pk=id)
            serializer = CustomerFollowupSerializer(followup)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ClientFollowupUpdateView(APIView):
    """Updates follow-up details using partial updates."""
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, id):
        try:
            followup = get_object_or_404(CustomerFollowup, pk=id)
            
            # Partial=True allows the React page to send only modified fields
            serializer = CustomerFollowupSerializer(followup, data=request.data, partial=True)

            if serializer.is_valid(): 
                serializer.save(
                    updatedby=request.user,
                    updatedon=timezone.now()
                )
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ClientFollowupDeleteView(APIView):
    """Deletes a follow-up record."""
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication] 
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, id):
        try:
            followup = get_object_or_404(CustomerFollowup, pk=id)
            followup.delete()
            return Response(
                {"message": "Client Follow-up deleted successfully"},
                status=status.HTTP_204_NO_CONTENT
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Users, Usertype, Employee
from .serializers import UserSerializer

class UserListCreateView(APIView):
    def get(self, request):
        users = Users.objects.all().order_by('-id')
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        
        # Look up foreign key objects if IDs are provided in request
        # This prevents the "Cannot add or update a child row" error
        usertype_id = data.get('usertype')
        employee_code = data.get('employee_code')

        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            # Save the user instance
            user = serializer.save(
                createdon=timezone.now(),
                superuser=data.get('superuser', 0),
                status=data.get('status', 1)
            )
            
            # Sync user_id with primary key id if it's blank
            if not user.user_id:
                user.user_id = user.id
                user.save()
                
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
    def get(self, request, pk):
        user = get_object_or_404(Users, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = get_object_or_404(Users, pk=pk)
        # partial=True allows you to update just the email or just the status
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(updatedon=timezone.now())
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = get_object_or_404(Users, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
        
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.authentication import SessionAuthentication
import traceback # Added for debugging

from .models import Associates, Cities 
from .serializers import AssociateSerializer 
from .authentication import CustomJWTAuthentication

from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status, permissions
from django.utils import timezone 
from django.db import transaction  # Crucial for dual-table saving
import traceback

from .models import Associates, Users, Usertype, Company # Ensure Company/Usertype exist
from .serializers import AssociateSerializer
from .authentication import CustomJWTAuthentication

class AssociateListCreateView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            month = request.query_params.get('month')
            queryset = Associates.objects.all()
            if month:
                queryset = queryset.filter(month=month)
            
            associates = queryset.order_by('-id')
            serializer = AssociateSerializer(associates, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        data = request.data.copy()

        # 1. Handle City code mapping
        if 'city_code' in data:
            data['city'] = data.pop('city_code')

        # 2. Auto-generate Associate Code
        if not data.get('associate_code'):
            last_assoc = Associates.objects.all().order_by('-associate_code').first()
            data['associate_code'] = (last_assoc.associate_code + 1) if last_assoc else 1001

        # 3. Map status to database values
        status_mapping = {"Active": 1, "Inactive": 0}
        if 'status' in data:
            data['status'] = status_mapping.get(data['status'], data['status'])

        # --- START ATOMIC TRANSACTION ---
        try:
            with transaction.atomic():
                serializer = AssociateSerializer(data=data)
                if serializer.is_valid():
                    # A. Save to Associates Table
                    associate_inst = serializer.save(
                        createdby=request.user, 
                        createdon=timezone.now()
                    )

                    # B. Fetch Master Data for Users (Dynamic Lookup)
                    # Adjust 'Associate' to match your specific Usertype record name
                    m_usertype = Usertype.objects.filter(usertype_name__iexact="Associate").first()
                    
                    # C. Save to Users Table
                    # We sync fields from the Associate instance to the User instance
                    new_user = Users.objects.create(
                        username=associate_inst.username or data.get('username'),
                        password=make_password(associate_inst.password), # Note: Consider hashing if required
                        email=associate_inst.email,
                        superuser=0,  # Default per your model requirement
                        status=1,     # Default Active
                        usertype=m_usertype,
                        associate_code=associate_inst.associate_code,
                        company_code=data.get('company_code'),
                        createdon=timezone.now()
                    )

                    # D. Final ID Sync
                    # If user_id must match the auto-generated ID
                    new_user.user_id = new_user.id
                    new_user.save()

                    # Update the Associate record with the newly created user_id
                    associate_inst.user_id = new_user.id
                    associate_inst.save()

                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(traceback.format_exc())
            return Response(
                {"error": f"Failed to save data to both tables: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CityListView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication] 
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            # Fetches city_code and city_name dynamically
            cities = Cities.objects.all().values('city_code', 'city_name') 
            return Response(list(cities), status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Note: Ensure AssociateDetailView is its own class and NOT nested inside another
class AssociateDetailView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated] 

    def get(self, request, id):
        associate = get_object_or_404(Associates, pk=id)
        serializer = AssociateSerializer(associate)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        associate = get_object_or_404(Associates, pk=id) 
        data = request.data.copy()
        
        # Map status to database values
        status_mapping = {"Active": 1, "Inactive": 0}
        if 'status' in data:
            data['status'] = status_mapping.get(data['status'], data['status'])
        
        serializer = AssociateSerializer(associate, data=data, partial=True)
        if serializer.is_valid(): 
            serializer.save(updatedby=request.user, updatedon=timezone.now())
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        associate = get_object_or_404(Associates, pk=id)
        associate.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authentication import SessionAuthentication
from django.shortcuts import get_object_or_404
# Ensure you import your custom auth here
# from your_auth_path import CustomJWTAuthentication 

from .models import CinemaList
from .serializers import CinemaListSerializer

class CinemaCreateView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            serializer = CinemaListSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CinemaListView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            # Apply optional filters from query params
            qs = CinemaList.objects.all()
            state = request.GET.get("state")
            city = request.GET.get("city")
            if state:
                qs = qs.filter(state_code__iexact=state)
            if city:
                qs = qs.filter(city_code__iexact=city)

            data = qs.order_by('id')
            serializer = CinemaListSerializer(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CinemaDetailView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        obj = get_object_or_404(CinemaList, id=id)
        serializer = CinemaListSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CinemaUpdateView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, id):
        try:
            obj = get_object_or_404(CinemaList, id=id)
            # partial=True allows updating specific fields without sending the whole object 
            serializer = CinemaListSerializer(obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CinemaDeleteView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, id):
        try:
            obj = get_object_or_404(CinemaList, id=id)
            obj.delete()
            return Response({"message": "Cinema deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    # this view is of campaign page  
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import ScreenlistingNew
from .serializers import ScreenlistingNewSerializer

class CinemaListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            # Switched to ScreenlistingNew
            qs = ScreenlistingNew.objects.all()
            
            state = request.GET.get("state")
            city = request.GET.get("city")
            chain = request.GET.get("cinema_chain")
            ctype = request.GET.get("cinema_type")

            if state: qs = qs.filter(state__icontains=state)
            if city: qs = qs.filter(city__icontains=city)
            if chain: qs = qs.filter(cinema_chain__icontains=chain)
            if ctype: qs = qs.filter(cinema_type__icontains=ctype)

            # Ordered by id (or sr_no if id is not available in managed=False)
            serializer = ScreenlistingNewSerializer(qs.order_by('id'), many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CinemaFilterOptionsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            qs = ScreenlistingNew.objects.all()
            return Response({
                'states': list(qs.order_by('state').values_list('state', flat=True).distinct().exclude(state__isnull=True)),
                'cities': list(qs.order_by('city').values_list('city', flat=True).distinct().exclude(city__isnull=True)),
                'chains': list(qs.order_by('cinema_chain').values_list('cinema_chain', flat=True).distinct().exclude(cinema_chain__isnull=True)),
                'types': list(qs.order_by('cinema_type').values_list('cinema_type', flat=True).distinct().exclude(cinema_type__isnull=True)),
            })
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CinemaDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, id):
        obj = get_object_or_404(ScreenlistingNew, id=id)
        serializer = ScreenlistingNewSerializer(obj, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# from rest_framework.views import APIView 
# from rest_framework.response import Response
# from rest_framework import status, permissions
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from django.shortcuts import get_object_or_404
# from .models import MasterCinema
# from .serializers import MasterCinemaSerializer

# class CinemaListAPI(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         state = request.query_params.get('state')
#         city = request.query_params.get('city')
#         qs = MasterCinema.objects.all()
        
#         if state:
#             qs = qs.filter(state__iexact=state)
#         if city:
#             qs = qs.filter(city__iexact=city)
            
#         serializer = MasterCinemaSerializer(qs, many=True, context={'request': request})
#         return Response(serializer.data)

# class CinemaDetailAPI(APIView): 
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [permissions.IsAuthenticated] 

#     def get(self, request, pk):
#         cinema = get_object_or_404(MasterCinema, id=pk)
#         serializer = MasterCinemaSerializer(cinema, context={'request': request})
#         return Response(serializer.data)

#     def post(self, request, pk):
#         # Logic for addToCart / removeFromCart goes here (as shown in previous response)
#         pass 

import os
import threading
import logging
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from django.core.mail import EmailMessage
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Contact
from .serializers import ContactSerializer

logger = logging.getLogger(__name__)

class ContactCreateView(APIView):
    # Set to AllowAny if guests should be able to contact you
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data
        
        with transaction.atomic():
            serializer = ContactSerializer(data=data)
            if serializer.is_valid():
                # 1. Save Contact to Database
                # created_by will be None if user is not logged in
                contact = serializer.save(
                    created_on=timezone.now(),
                    created_by=request.user.id if request.user.is_authenticated else None
                )
                
                # 2. Trigger Acknowledgement Email
                self.send_acknowledgement_email(contact)
                
                return Response({
                    "message": "Thank you for contacting us. We have received your message.",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)

            return Response({
                "error": "Validation failed",
                "details": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def send_acknowledgement_email(self, contact):
        def _send_async():
            try:
                customer_email = contact.email
                if not customer_email:
                    return

                customer_name = (contact.name or "Valued Customer").strip()
                subject = f"We've Received Your Inquiry: {contact.subject}"

                body_html = f"""
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <style>
                        /* mobile-responsive adjustments */
                        @media only screen and (max-width: 620px) {{
                            .container {{
                                padding: 10px !important;
                            }}
                            .content {{
                                padding: 15px !important;
                            }}
                            h1 {{
                                font-size: 20px !important;
                            }}
                        }}
                    </style>
                </head>
                <body style="margin:0;padding:0;background-color:#f4f6f8;font-family:Helvetica,Arial,sans-serif;">
                    <table width="100%" cellpadding="0" cellspacing="0">
                        <tr>
                            <td align="center" style="padding:20px 0;">
                                <table class="container" width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:8px;overflow:hidden;box-shadow:0 4px 12px rgba(0,0,0,0.1);">
                                    <!-- header -->
                                    <!-- <tr>
                                        <td style="background:#ffffff;padding:20px 30px;text-align:center;">
                                            <img src="AdBajao\Frontend\src\assets\logo.png.png" alt="Adbajao" width="120" style="display:block;margin:0 auto;" />
                                        </td>
                                    </tr> -->
                                    <tr>
                                        <td style="background:#d32f2f;padding:10px 30px;text-align:center;color:#ffffff;">
                                            <h1 style="margin:0;font-size:24px;">Thank You for Reaching Out!</h1>
                                        </td>
                                    </tr>

                                    <!-- body content -->
                                    <tr>
                                        <td class="content" style="padding:20px 30px;color:#333;">
                                            <p style="margin:0 0 15px;">Dear <strong>{customer_name}</strong>,</p>
                                            <p style="margin:0 0 15px;">Thank you for contacting <strong>Adbajao</strong>. We have successfully received your message regarding "<em>{contact.subject}</em>".</p>
                                            <p style="margin:0 0 20px;">Our team is currently reviewing your requirements and will get back to you shortly.</p>

                                            <div style="background:#f9f9f9;border-left:4px solid #d32f2f;padding:15px 20px;margin:20px 0;border-radius:4px;">
                                                <p style="margin:0;font-weight:600;color:#333;">Your Message Summary</p>
                                                <p style="margin:8px 0 0;font-style:italic;color:#555;">"{contact.message}"</p>
                                            </div>

                                            <p style="margin:0;">Best Regards,<br>
                                            <strong>Adbajao Team</strong></p>
                                        </td>
                                    </tr>

                                    <!-- footer -->
                                    <tr>
                                        <td style="background:#f1f1f1;padding:15px 30px;text-align:center;font-size:12px;color:#777;">
                                            <p style="margin:0;">This is an automated response. Please do not reply to this email.</p>
                                            <p style="margin:5px 0 0;">&copy; {timezone.now().year} Adbajao. All rights reserved.</p>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                    </table>
                </body>
                </html>
                """

                email = EmailMessage(
                    subject=subject,
                    body=body_html,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[customer_email],
                )
                email.content_subtype = "html"
                email.send(fail_silently=False)

            except Exception as e:
                logger.error(f"Contact Acknowledgement Email Failed: {str(e)}")

        threading.Thread(target=_send_async, daemon=True).start()

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db.models import Max, Sum
from django.utils import timezone
from decimal import Decimal, ROUND_HALF_UP
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authentication import SessionAuthentication
from django.utils import timezone
import uuid
from decimal import Decimal  # <--- Added for decimal conversion

from .models import (
    Cart, ScreenlistingNew, Customer, Coupens, 
    BookCampaign, CustomerCart, CustomerCartItem, MasterCinema,DiscountRates
)
from .serializers import CartSerializer

class CartAddView(APIView):
    # authentication_classes = [CustomJWTAuthentication, SessionAuthentication] # Keep your custom auth here
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            cinema_id = request.data.get('cinema_id')
            if not cinema_id:
                return Response({"error": "Cinema ID required"}, status=status.HTTP_400_BAD_REQUEST)
            
            customer_id = getattr(request.user, 'customer_code', None) or getattr(request.user, 'user_id', None) or getattr(request.user, 'id', None)
            if not customer_id:
                return Response({"error": "Unable to determine customer ID from authenticated user"}, status=status.HTTP_400_BAD_REQUEST)
            
            cinema = ScreenlistingNew.objects.filter(id=cinema_id).first() or MasterCinema.objects.filter(id=cinema_id).first()
            
            if not cinema:
                return Response({"error": "Cinema not found"}, status=status.HTTP_404_NOT_FOUND)
            
            customer_cart, created = CustomerCart.objects.get_or_create(
                customer_code=str(customer_id),
                defaults={
                    'cart_id': str(uuid.uuid4())[:45],
                    'createdon': timezone.now(),
                    'createdby': request.user.id
                }
            )

            # --- DECIMAL CONVERSION FIX START ---
            current_rate = Decimal(getattr(cinema, 'base_rate_per_seconds_perweeks', '0') or '0')
            current_bb_rate = Decimal(getattr(cinema, 'bb_rate_per_seconds_perweeks', '0') or '0')
            
            # These are for the 10sec week columns
            base_10sec = Decimal(getattr(cinema, 'base_rate_10sec_week', '0') or '0')
            bb_10sec = Decimal(getattr(cinema, 'bb_rate_10sec_week', '0') or '0')
            # --- DECIMAL CONVERSION FIX END ---

            new_cart_item = CustomerCartItem.objects.create(
                customer_id=str(customer_id),
                cart_id=customer_cart.cart_id,
                screen_id=cinema.id,
                media_name=cinema.theatre_name,
                web_code=getattr(cinema, 'web_code', ''),
                city=cinema.city,
                district=getattr(cinema, 'district', ''),
                state=cinema.state,
                theatre_address=getattr(cinema, 'theatre_address', ''),
                img=getattr(cinema, 'image', '') or '',
                seats_number=getattr(cinema, 'seating_capacity', 0) or 0,
                projection=getattr(cinema, 'projection', '') or '',
                rate=current_rate,
                base_rate_10secweek=base_10sec,
                bb_rate_10secweek=bb_10sec,
                base_rate_10secweek_0=current_rate,
                bb_rate_10secweek_0=current_bb_rate,
                campaign_category='Cinema Ad',
                associate_code=getattr(request.user, 'associate_code', None),
                date=timezone.now().date(),
                createdon=timezone.now(),
                createdby=request.user.id
            )

            Cart.objects.create(
                p_id=getattr(cinema, 'web_code', cinema.id),
                web_code=getattr(cinema, 'web_code', ''),
                media_name=cinema.theatre_name,
                theatre_address=getattr(cinema, 'theatre_address', ''),
                img=getattr(cinema, 'image', '') or '',
                seats_number=str(getattr(cinema, 'seating_capacity', '0')),
                projection=getattr(cinema, 'projection', '') or '',
                rate=current_rate,
                customer_id=str(customer_id),
                date=timezone.now().date(),
                city=cinema.city,
                district=getattr(cinema, 'district', ''),
                state=cinema.state,
                campaign_category='Cinema Ad',
                associate_code=request.user.associate_code,
                base_rate_10secweek=current_rate,
                bb_rate_10secweek=current_bb_rate,
                base_rate_10secweek_0=current_rate,
                bb_rate_10secweek_0=current_bb_rate,
                rate_type=1
            )
            
            return Response({"message": "Added to cart"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
from decimal import Decimal, ROUND_HALF_UP
from django.db.models import Max
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

# Assuming these are your imports
from .models import (
    Cart, ScreenlistingNew, Coupens, 
    BookCampaign, CustomerCart, CustomerCartItem, DiscountRates
)
from .serializers import CartSerializer

class CartProcessView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data
        user = request.user
        
        if user.is_authenticated:
            customer_id = getattr(user, 'customer_code', None) or getattr(user, 'user_id', None) or getattr(user, 'id', None)
            if not customer_id:
                return Response({"error": "customer_id required"}, status=status.HTTP_400_BAD_REQUEST)
            customer_id = str(customer_id)
        else:
            customer_id = data.get('customer_id')
            if not customer_id:
                return Response({"error": "customer_id required"}, status=status.HTTP_400_BAD_REQUEST)
            customer_id = str(customer_id)

        rate_type_input = data.get('rateType', 'Base Rate')
        ad_length = int(data.get('adLength', 10))
        weeks = int(data.get('weeks', 1))
        ad_type = data.get('adType', 'Slide Ads')
        ad_position = data.get('adPosition', 'Before movie')
        coupon_code = data.get('couponCode', '')
        start_date = data.get('startDatePicker')
        manual_discount_perc = Decimal(str(data.get('discount_percentage', '0')))

        cart_items = Cart.objects.filter(customer_id=customer_id)
        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        total_base_rate = Decimal('0.00')
        total_seats = 0
        total_shows = weeks * 28 * cart_items.count()
        processed_items = []

        for item in cart_items:
            try:
                screen = ScreenlistingNew.objects.get(theatre_name=item.media_name, city=item.city, state=item.state)
                
                # Dynamic field selection based on model structure
                if rate_type_input == "Base Rate":
                    rate_value = getattr(screen, 'base_rate_per_seconds_perweeks', 0)
                elif rate_type_input == "Blockbuster Rate":
                    rate_value = getattr(screen, 'bb_rate_per_seconds_perweeks', 0)
                else:
                    rate_value = getattr(screen, 'base_rate_per_seconds_perweeks', 0)
                
                # Safe conversion for TextField values
                try:
                    clean_rate = Decimal(str(rate_value or 0))
                except:
                    clean_rate = Decimal('0')

                total_base_rate += clean_rate * ad_length * weeks
                total_seats += int(screen.seating_capacity or 0)

                item_data = CartSerializer(item).data
                item_data['rate'] = float(clean_rate) 
                processed_items.append(item_data)

            except ScreenlistingNew.DoesNotExist:
                processed_items.append(CartSerializer(item).data)
                continue

        if ad_position == 'Both':
            total_base_rate *= 2

        # --- DYNAMIC DISCOUNT LOGIC START ---
        count = cart_items.count()
        auto_discount_perc = Decimal('0')

        # Query database for matching range from your provided table
        discount_record = DiscountRates.objects.filter(
            screensfro__lte=count,
            screesto__gte=count,
            weeksfron__lte=weeks,
            weeksto__gte=weeks
        ).first()

        if discount_record:
            auto_discount_perc = Decimal(str(discount_record.discount))
        # --- DYNAMIC DISCOUNT LOGIC END ---

        coupon_discount_perc = Decimal('0')
        coupon_applied = False
        if coupon_code:
            try:
                coupon = Coupens.objects.get(coupen_code=coupon_code)
                if coupon.coupen_status.lower() == "unused":
                    coupon_discount_perc = Decimal(str(coupon.discount))
                    coupon_applied = True
            except Coupens.DoesNotExist:
                pass

        total_discount_perc = auto_discount_perc + coupon_discount_perc + manual_discount_perc
        gross_total = total_base_rate
        discount_amount = (gross_total * (total_discount_perc / Decimal('100'))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        discounted_total = gross_total - discount_amount
        
        certificate_charges = Decimal('6000.00') if (ad_type == "Video Ads" and data.get('question1') == "No" and data.get('question2') == "Yes") else Decimal('0.00')
        total_taxable = discounted_total + certificate_charges
        gst = (total_taxable * Decimal('0.18')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        total_payable = total_taxable + gst

        submit_type = data.get('submitType')
        if submit_type in ["bookWithoutPayment", "confirm"]:
            if submit_type == "bookWithoutPayment" and not start_date:
                return Response({"error": "Start date required"}, status=status.HTTP_400_BAD_REQUEST)

            max_code = BookCampaign.objects.aggregate(Max('campaign_code'))['campaign_code__max']
            new_campaign_code = f"CMP{int(max_code or 0) + 1:04d}"

            book_campaign = BookCampaign.objects.create(
                campaign_code=int(new_campaign_code.replace("CMP", "")),                        # Model is IntegerField
                customer_code=customer_id,                         # Changed from customer_id
                gross_total=int(gross_total),                      # Model is IntegerField
                discount=float(total_discount_perc),               # Model is FloatField
                discount_total=int(discount_amount),               # Added to match model
                gst=float(gst),                                    # Model is FloatField
                total_taxable_amount=float(total_taxable),         # Model is FloatField
                total_payable_amount=total_payable,                # Changed from final_amount
                ads_in_second=ad_length,                           # Changed from ad_length
                week=weeks,                                        # Changed from weeks
                campaign_status='Confirmed' if submit_type == "confirm" else 'Booked', # Changed from status
                campaign_start_date=start_date,                    # Mapping from form data
                booking_date=timezone.now().date(),                # Adding current date
                campaign_category='Cinema Ad',                     # Added
                createdon=timezone.now(),                          # Added
                createdby=user if user.is_authenticated else None, # Use user instance, not ID
            )

            if submit_type == "confirm":
                cart_items.delete()
                CustomerCartItem.objects.filter(customer_id=customer_id).delete()
                CustomerCart.objects.filter(customer_code=customer_id).delete()
                
                if coupon_applied:
                    Coupens.objects.filter(coupen_code=coupon_code).update(coupen_status="Used")

            return Response({"message": "Booking successful", "campaign_code": new_campaign_code})

        return Response({
            "calculation": {
                "gross_total": float(gross_total),
                "auto_discount": float(auto_discount_perc),
                "manual_discount": float(manual_discount_perc),
                "coupon_discount": float(coupon_discount_perc),
                "total_discount_perc": float(total_discount_perc),
                "taxable_amount": float(total_taxable),
                "gst": float(gst),
                "total_payable": float(total_payable),
                "total_seats": total_seats,
                "total_shows": total_shows,
                "coupon_applied": coupon_applied
            },
            "cart_items": processed_items 
        })
    
class WeeksListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        weeks = Weeks.objects.all().order_by('week_value')
        serializer = WeeksSerializer(weeks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AdlengthsListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        lengths = Adlengths.objects.all().order_by('length_value')
        serializer = AdlengthsSerializer(lengths, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CartCountView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        customer_id = (
            getattr(request.user, 'customer_code', None)
            or getattr(request.user, 'customer_id', None)
            or getattr(request.user, 'user_id', None)
            or getattr(request.user, 'id', None)
        )

        if not customer_id:
            return Response({"count": 0}, status=status.HTTP_200_OK)

        customer_id = str(customer_id)
        count = Cart.objects.filter(customer_id=customer_id).count()
        return Response({"count": count}, status=status.HTTP_200_OK)

class CartDeleteItemsView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        try:
            cart_ids = request.data.get('cartIds', [])
            if isinstance(cart_ids, str):
                try:
                    cart_ids = json.loads(cart_ids)
                except Exception:
                    cart_ids = [cart_ids]

            if not isinstance(cart_ids, list):
                return Response({"error": "cartIds must be a list"}, status=status.HTTP_400_BAD_REQUEST)

            if not cart_ids:
                return Response({"error": "No items specified"}, status=status.HTTP_400_BAD_REQUEST)

            customer_id = None
            if request.user and request.user.is_authenticated:
                customer_id = (
                    getattr(request.user, 'customer_code', None) 
                    or getattr(request.user, 'customer_id', None) 
                    or getattr(request.user, 'user_id', None) 
                    or getattr(request.user, 'id', None)
                )

            if not customer_id:
                return Response({"error": "Unable to determine customer ID"}, status=status.HTTP_400_BAD_REQUEST)

            customer_id = str(customer_id)

            # Collect cart items for this user for row-level deletion
            cart_items = list(Cart.objects.filter(id__in=cart_ids, customer_id=customer_id).values(
                'id', 'media_name', 'city', 'state', 'theatre_address'
            ))

            if not cart_items:
                return Response({"error": "No matching cart items found"}, status=status.HTTP_404_NOT_FOUND)

            # Delete Cart rows first
            deleted_cart_count, _ = Cart.objects.filter(id__in=[ci['id'] for ci in cart_items], customer_id=customer_id).delete()

            # Delete matching CustomerCartItem rows by keys (this ensures DB row cleanup)
            deleted_item_count = 0
            item_filter = None
            for item in cart_items:
                q = Q(
                    customer_id=customer_id,
                    media_name=item.get('media_name'),
                    city=item.get('city'),
                    state=item.get('state'),
                    theatre_address=item.get('theatre_address')
                )
                item_filter = q if item_filter is None else (item_filter | q)

            if item_filter is not None:
                deleted_item_count, _ = CustomerCartItem.objects.filter(item_filter).delete()

            # Delete cart parent if no items remain
            remaining_items = Cart.objects.filter(customer_id=customer_id).exists()
            if not remaining_items:
                CustomerCart.objects.filter(customer_code=customer_id).delete()

            return Response({
                "message": "Items deleted successfully",
                "deleted_cart_count": deleted_cart_count,
                "deleted_customer_cart_items": deleted_item_count
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.authentication import SessionAuthentication

from .models import Coupens, CoupenRequest, Customer
from .serializers import CouponSerializer
from .authentication import CustomJWTAuthentication

class CouponListView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            # For admin panel, show all coupons
            coupons = Coupens.objects.all().order_by('-id')
            serializer = CouponSerializer(coupons, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CouponCreateView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            coupen_code = data.get('coupen_code')

            # Logic: Check if Coupon Code already exists
            if Coupens.objects.filter(coupen_code=coupen_code).exists():
                return Response({"error": "Coupon Code already exists"}, status=status.HTTP_400_BAD_REQUEST)

            serializer = CouponSerializer(data=data)
            if serializer.is_valid():
                serializer.save(
                    coupen_status="0",
                    createdby_id=request.user.user_id, # Assuming user_id is the integer PK
                    createdon=timezone.now()
                )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CouponGenerateCodeView(APIView):
    """Port of your generate_coupon random logic"""
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        discount = request.data.get('discount', 0)
        random_code = random.randint(1000, 9999)
        coupon_code = f'DISCOUNT{discount}CODE{random_code}'
        return Response({'coupon_code': coupon_code, 'discount': discount}, status=status.HTTP_200_OK)

class CouponValidateView(APIView):
    """Validate coupon code and return discount"""
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, coupon_code):
        try:
            from datetime import date

            # Find the coupon
            coupon = Coupens.objects.filter(coupen_code=coupon_code).first()

            if not coupon:
                return Response({
                    "valid": False,
                    "message": "Invalid coupon code"
                }, status=status.HTTP_200_OK)

            # Check if coupon is already used
            if str(coupon.coupen_status).lower() in ['used', '1']:
                return Response({
                    "valid": False,
                    "message": "Coupon has already been used"
                }, status=status.HTTP_200_OK)

            # Check if coupon is expired
            if coupon.expire_date and coupon.expire_date < date.today():
                return Response({
                    "valid": False,
                    "message": "Coupon has expired"
                }, status=status.HTTP_200_OK)

            # Coupon is valid
            return Response({
                "valid": True,
                "discount": coupon.discount,
                "coupon_code": coupon.coupen_code
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CouponUpdateView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        try:
            coupon = get_object_or_404(Coupens, id=pk)
            serializer = CouponSerializer(coupon, data=request.data, partial=True)
            if serializer.is_valid():
                # Get the status from request data dynamically
                raw_status = request.data.get('coupen_status')
                
                # Logic: Map "Used" to 1 and "Unused" to 0 for the DB
                # This ensures the database stores integers while UI sends strings
                db_status = coupon.coupen_status  # Default to current value
                if raw_status == "Used":
                    db_status = 1
                elif raw_status == "Unused":
                    db_status = 0

                serializer.save(
                    coupen_status=db_status,
                    updatedby_id=request.user.user_id,
                    updatedon=timezone.now()
                )
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CouponDeleteView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        try:
            # Handles multiple delete logic from your getToDelete section
            ids = request.data.get('selectedIdsOfCoupens', [])
            if not ids:
                return Response({"error": "No IDs provided"}, status=status.HTTP_400_BAD_REQUEST)
            
            Coupens.objects.filter(id__in=ids).delete()
            return Response({"message": "Coupons deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": "Cannot delete selected Coupons"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
import base64
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.utils import timezone
from rest_framework.authentication import SessionAuthentication
# ADD THESE TWO IMPORTS
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser 
from .models import MoviesliderImage
from .serializers import MoviesliderImageSerializer
from .authentication import CustomJWTAuthentication

class MovieSliderListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            images = MoviesliderImage.objects.all().order_by('-id')
            serializer = MoviesliderImageSerializer(images, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MovieSliderCreateView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser] 

    def post(self, request):
        try:
            data = request.data
            name = data.get('name')
            image_file = request.FILES.get('image')
            
            print("DEBUG: request.data:", data)
            print("DEBUG: request.FILES:", request.FILES)
            print("DEBUG: name:", name)
            print("DEBUG: image_file:", image_file)
            
            # Validation Check
            if not name:
                return Response({"error": "Name field is required"}, status=status.HTTP_400_BAD_REQUEST)

            # Use your existing logic
            obj, created = MoviesliderImage.objects.get_or_create(name=name)
            
            obj.releasing_date = data.get('releasing_date')
            obj.createdby = request.user.user_id 
            obj.createdon = timezone.now()

            if image_file:
                obj.image = image_file.read()
            
            obj.save()
            
            serializer = MoviesliderImageSerializer(obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            # THIS LINE IS KEY: Look at your terminal/console to see the real error
            print(f"DEBUG ERROR: {str(e)}") 
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class MovieSliderUpdateView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    # ADD THIS LINE
    parser_classes = [MultiPartParser, FormParser] 

    def put(self, request, id):
        try:
            instance = MoviesliderImage.objects.get(pk=id)
            data = request.data
            image_file = request.FILES.get('image')

            instance.name = data.get('name', instance.name)
            instance.releasing_date = data.get('releasing_date', instance.releasing_date)
            instance.updatedby = request.user.user_id
            instance.updatedon = timezone.now()

            if image_file:
                instance.image = image_file.read()

            instance.save()
            serializer = MoviesliderImageSerializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class MovieSliderDeleteView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser]

    def delete(self, request):
        try:
            ids = request.data.get('selectedIds', [])
            if not ids:
                return Response({"error": "No IDs provided"}, status=status.HTTP_400_BAD_REQUEST)
            
            MoviesliderImage.objects.filter(id__in=ids).delete()
            return Response({"message": "Successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
       
class CouponRequestCreateView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            serializer = CouponRequestSerializer(data=request.data)

            if serializer.is_valid():
                instance = serializer.save(
                    createdby=request.user.id,
                    createdon=timezone.now()
                )

                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CouponRequestListView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            coupons = CoupenRequest.objects.all().order_by('-createdon')
            serializer = CouponRequestSerializer(coupons, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)     

class CouponRequestDetailView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        try:
            coupon = CoupenRequest.objects.get(id=id)
            serializer = CouponRequestSerializer(coupon)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except CoupenRequest.DoesNotExist:
            return Response({"error": "Coupon request not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CouponRequestUpdateView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, id):
        try:
            coupon = get_object_or_404(CoupenRequest, id=id)

            serializer = CouponRequestSerializer(coupon, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save(
                    updatedby=request.user.id,
                    updatedon=timezone.now()
                )

                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CouponRequestDeleteView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, id):
        try:
            coupon = get_object_or_404(CoupenRequest, id=id)

            coupon.delete()

            return Response(
                {"message": "Coupon request deleted successfully"},
                status=status.HTTP_204_NO_CONTENT
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TopBrandsListView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
 
    def get(self, request):
        brands = TopBrands.objects.all().order_by('-id')
        serializer = TopBrandsSerializer(brands, many=True)
        return Response(serializer.data)
 
class TopBrandsCreateView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
 
    def post(self, request):
        try:
            name = request.data.get("name")
            image_file = request.FILES.get("image")
 
            obj = TopBrands()
            obj.name = name
            obj.createdby = request.user.user_id
            obj.createdon = timezone.now()
 
            if image_file:
                obj.img = image_file.read()
 
            obj.save()
 
            serializer = TopBrandsSerializer(obj)
            return Response(serializer.data, status=201)
 
        except Exception as e:
            return Response({"error": str(e)}, status=400)
       
class TopBrandsUpdateView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
 
    def put(self, request, id):
        try:
            obj = TopBrands.objects.get(pk=id)
 
            obj.name = request.data.get("name", obj.name)
            image_file = request.FILES.get("image")
 
            if image_file:
                obj.img = image_file.read()
 
            obj.updatedby = request.user.user_id
            obj.updatedon = timezone.now()
 
            obj.save()
 
            serializer = TopBrandsSerializer(obj)
            return Response(serializer.data)
 
        except Exception as e:
            return Response({"error": str(e)}, status=400)
 
class TopBrandsDeleteView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
 
    def delete(self, request):
        ids = request.data.get("selectedIds", [])
 
        TopBrands.objects.filter(id__in=ids).delete()
 
        return Response({"message": "Deleted"}, status=204)
  

from django.utils import timezone
from django.shortcuts import get_object_or_404
 
from .models import Partner
from .serializers import PartnerSerializer
 
from rest_framework.authentication import SessionAuthentication
from .authentication import CustomJWTAuthentication
 
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
def generate_partner_code():
 
    last_partner = Partner.objects.order_by('-id').first()
 
    if not last_partner:
        return "P1001"
 
    last_code = last_partner.partner_code
 
    if last_code:
        number = int(last_code.replace("P", ""))
        new_number = number + 1
        return f"P{new_number}"
 
    return "P1001"


def sync_partner_user(partner, password=None, company_code=None, usertype_id=None, username=None):
    """Create or update the Users row for a Partner."""
    hashed_password = make_password(password) if password else None

    user = Users.objects.filter(partner_code=partner.partner_code).first()

    if user:
        if username:
            user.username = username
        user.email = partner.email or user.email

        if hashed_password:
            user.password = hashed_password

        if company_code is not None:
            user.company_code = company_code

        if usertype_id is not None:
            user.usertype_id = usertype_id

        user.updatedon = timezone.now()
        user.save()
        return user

    # Create new user only if username is provided
    if not username:
        return None

    max_user_id = Users.objects.aggregate(Max('user_id'))['user_id__max'] or 0
    user_password = hashed_password or make_password("")

    user = Users.objects.create(
        user_id=max_user_id + 1,
        username=username,
        email=partner.email,
        password=user_password,
        partner_code=partner.partner_code,
        status=1,
        superuser=0,
        company_code=company_code,
        usertype_id=usertype_id,
        createdon=timezone.now(),
        updatedon=timezone.now(),
    )

    # Ensure user_id is synced with model's id (id == user_id)
    if user.user_id != user.id:
        user.user_id = user.id
        user.save(update_fields=["user_id"])

    return user


class PartnerCreateView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    parser_classes = [MultiPartParser, FormParser, JSONParser]
 
    def post(self, request):
        try:
            # ============================
            # GET SESSION DATA
            # ============================
            session_data = request.session.get("user_data", {})
            session_partner_code = session_data.get("partner_code")

            # Fallback
            if not session_partner_code:
                user = request.user
                session_partner_code = getattr(user, "partner_code", None)

            # ============================
            # BLOCK PARTNER FROM CREATING
            # ============================
            if session_partner_code:
                return Response(
                    {"error": "Partners are not allowed to create partners"},
                    status=403
                )

            # ============================
            # YOUR EXISTING CODE (UNCHANGED)
            # ============================
            obj = Partner()

            obj.partner_code = generate_partner_code()
            obj.name = request.data.get("name")
            obj.gst_number = request.data.get("gst_number")
            obj.mobile_no = request.data.get("mobile_no")
            obj.email = request.data.get("email")
            obj.city = request.data.get("city")
            obj.state = request.data.get("state")
            obj.cin = request.data.get("cin")
            obj.pan = request.data.get("pan")
            obj.tan = request.data.get("tan")

            obj.address = request.data.get("address")
            obj.address1 = request.data.get("address1")
            obj.address2 = request.data.get("address2")
            obj.pin_code = request.data.get("pin_code")
            obj.country = request.data.get("country")

            obj.username = request.data.get("username")
            obj.password = request.data.get("password")

            image_file = request.FILES.get("logo")
            if image_file:
                obj.logo = image_file.read()

            obj.createdby = request.user.user_id
            obj.createdon = timezone.now()

            obj.save()

            # Sync to Users table
            company_code = request.session.get("CompanyCode") if hasattr(request, 'session') else None
            partner_usertype = Usertype.objects.filter(usertype_name__iexact='Partner').first()
            usertype_id = partner_usertype.id if partner_usertype else None

            sync_partner_user(
                partner=obj,
                password=request.data.get('password'),
                company_code=company_code,
                usertype_id=usertype_id,
                username=request.data.get('username')
            )

            return Response(PartnerSerializer(obj).data, status=201)

        except Exception as e:
            print("ERROR:", e)
            return Response({"error": str(e)}, status=400)
        
       
class PartnerListView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            session_data = request.session.get("user_data", {})

            role = session_data.get("role")
            partner_code = session_data.get("partner_code")

            # Fallback
            if not role:
                user = request.user
                role = getattr(user, "role", None)
                partner_code = getattr(user, "partner_code", None)

            # ============================
            # DYNAMIC ACCESS CONTROL
            # ============================
            queryset = Partner.objects.all()

            # If partner_code exists → restrict automatically
            if partner_code:
                queryset = queryset.filter(partner_code=partner_code)

            serializer = PartnerSerializer(queryset, many=True)
            return Response(serializer.data)

        except Exception as e:
            return Response({"error": str(e)}, status=400)
 
 
class PartnerDetailView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
 
    def get(self, request, id):
        try:
            partner = Partner.objects.get(id=id)
            serializer = PartnerSerializer(partner)
 
            return Response(serializer.data, status=status.HTTP_200_OK)
 
        except Partner.DoesNotExist:
            return Response({"error": "Partner not found"}, status=status.HTTP_404_NOT_FOUND)
 
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
class PartnerUpdateView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
 
    def put(self, request, id):
        try:
            # ============================
            # GET SESSION DATA
            # ============================
            session_data = request.session.get("user_data", {})
            partner_code = session_data.get("partner_code")

            # Fallback to JWT
            if not partner_code:
                user = request.user
                partner_code = getattr(user, "partner_code", None)

            print("SESSION PARTNER:", partner_code)

            # ============================
            # GET OBJECT
            # ============================
            obj = Partner.objects.get(pk=id)

            # ============================
            # ACCESS CONTROL (IMPORTANT)
            # ============================
            if partner_code and obj.partner_code != partner_code:
                return Response(
                    {"error": "You can only update your own record"},
                    status=403
                )

            # ============================
            # UPDATE FIELDS
            # ============================
            obj.partner_code = request.data.get("partner_code", obj.partner_code)
            # Partner table has 'name' field. If username is provided, use it to update name
            obj.name = request.data.get("username") or request.data.get("name", obj.name)
            obj.gst_number = request.data.get("gst_number", obj.gst_number)
            obj.mobile_no = request.data.get("mobile_no", obj.mobile_no)
            obj.email = request.data.get("email", obj.email)
            obj.city = request.data.get("city", obj.city)
            obj.state = request.data.get("state", obj.state)
            obj.cin = request.data.get("cin", obj.cin)
            obj.pan = request.data.get("pan", obj.pan)
            obj.tan = request.data.get("tan", obj.tan)
 
            obj.address = request.data.get("address", obj.address)
            obj.address1 = request.data.get("address1", obj.address1)
            obj.address2 = request.data.get("address2", obj.address2)
            obj.pin_code = request.data.get("pin_code", obj.pin_code)
            obj.country = request.data.get("country", obj.country)

            # ============================
            # HANDLE IMAGE
            # ============================
            image_file = request.FILES.get("logo")
            if image_file:
                obj.logo = image_file.read()
 
            obj.updatedby = request.user.user_id
            obj.updatedon = timezone.now()
 
            obj.save()

            # ============================
            # SYNC USERS TABLE
            # ============================
            company_code = request.session.get("CompanyCode") if hasattr(request, 'session') else None
            partner_usertype = Usertype.objects.filter(usertype_name__iexact='Partner').first()
            usertype_id = partner_usertype.id if partner_usertype else None

            sync_partner_user(
                partner=obj,
                password=request.data.get('password'),
                company_code=company_code,
                usertype_id=usertype_id,
                username=request.data.get('username')
            )
 
            serializer = PartnerSerializer(obj)
            return Response(serializer.data, status=200)
 
        except Partner.DoesNotExist:
            return Response({"error": "Partner not found"}, status=404)

        except Exception as e:
            print("ERROR:", e)
            return Response({"error": str(e)}, status=400)
       
class PartnerDeleteView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, id):
        try:
            # ============================
            # GET SESSION DATA
            # ============================
            session_data = request.session.get("user_data", {})
            partner_code = session_data.get("partner_code")

            # Fallback to JWT
            if not partner_code:
                user = request.user
                partner_code = getattr(user, "partner_code", None)

            print("SESSION PARTNER:", partner_code)

            # ============================
            # GET OBJECT
            # ============================
            obj = Partner.objects.get(pk=id)

            # ============================
            # ACCESS CONTROL (MAIN LOGIC)
            # ============================
            if partner_code and obj.partner_code != partner_code:
                return Response(
                    {"error": "You can only delete your own record"},
                    status=403
                )

            # ============================
            # DELETE OBJECT
            # ============================
            obj.delete()

            return Response(
                {"message": "Partner deleted successfully"},
                status=200
            )

        except Partner.DoesNotExist:
            return Response({"error": "Partner not found"}, status=404)

        except Exception as e:
            print("ERROR:", e)
            return Response({"error": str(e)}, status=400)
       
 
 
 
class PartnerBankDetailsListView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
 
    def get(self, request):
        try:
            partners = PartnerBankDetails.objects.all().order_by('-createdon')
            serializer = PartnerBankDetailsSerializer(partners, many=True)
 
            return Response(serializer.data, status=status.HTTP_200_OK)
 
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
 
class PartnerBankDetailsDetailView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
 
    def get(self, request, id):
        try:
            partner = PartnerBankDetails.objects.get(id=id)
            serializer = PartnerBankDetailsSerializer(partner)
 
            return Response(serializer.data, status=status.HTTP_200_OK)
 
        except PartnerBankDetails.DoesNotExist:
            return Response({"error": "Partner bank details not found"}, status=status.HTTP_404_NOT_FOUND)
 
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
 
class PartnerBankDetailsCreateView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
 
    def post(self, request):
        try:
            serializer = PartnerBankDetailsSerializer(data=request.data)
 
            if serializer.is_valid():
                serializer.save(
                    createdby=request.user.id,
                    createdon=timezone.now()
                )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
 
class PartnerBankDetailsUpdateView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
 
    def put(self, request, id):
        try:
            partner = get_object_or_404(PartnerBankDetails, id=id)
 
            serializer = PartnerBankDetailsSerializer(partner, data=request.data, partial=True)
 
            if serializer.is_valid():
                serializer.save(
                    updatedby=request.user.id,
                    updatedon=timezone.now()
                )
 
                return Response(serializer.data, status=status.HTTP_200_OK)
 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
 
class PartnerBankDetailsDeleteView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
 
    def delete(self, request, id):
        try:
            partner = get_object_or_404(PartnerBankDetails, id=id)
 
            partner.delete()
 
            return Response(
                {"message": "Partner bank details deleted successfully"},
                status=status.HTTP_204_NO_CONTENT
            )
 
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
from datetime import datetime
from django.utils import timezone
 
#client query views        
class CustomerQueryCreateView(APIView):
 
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
 
    def post(self, request):
 
        serializer = CustomerQuerySerializer(data=request.data)
 
        if serializer.is_valid():
 
            serializer.save(
                createdby=request.user.id,
                createdon=timezone.now(),
                date=datetime.now()
            )
 
            return Response(serializer.data, status=201)
 
        return Response(serializer.errors, status=400)
   
class CustomerQueryListView(APIView):
 
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
 
    def get(self, request):
 
        queries = Query.objects.all().order_by("-createdon")
 
        serializer = CustomerQuerySerializer(
            queries,
            many=True
        )
 
        return Response(serializer.data)
   
class CustomerQueryDetailView(APIView):
 
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
 
    def get(self, request, id):
 
        query = get_object_or_404(Query, id=id)
 
        serializer = CustomerQuerySerializer(query)
 
        return Response(serializer.data)
   
class CustomerQueryUpdateView(APIView):
 
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
 
    def put(self, request, id):
 
        query = get_object_or_404(Query, id=id)
 
        serializer = CustomerQuerySerializer(
            query,
            data=request.data,
            partial=True
        )
 
        if serializer.is_valid():
 
            serializer.save(
                updatedby=request.user.id,
                updatedon=timezone.now()
            )
 
            return Response(serializer.data)
 
        return Response(serializer.errors, status=400)
 
class CustomerQueryDeleteView(APIView):
 
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
 
    def delete(self, request, id):
 
        query = get_object_or_404(Query, id=id)
 
        query.delete()
 
        return Response(
            {"message": "Customer query deleted"},
            status=204
        )

 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
 
from .models import Cart, Customer, CustomerCartItem, Cities
 
 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_quotation_api(request):
    try:
        user = request.user
        data = request.data
 
        # -------------------------
        # CUSTOMER ID / CART ITEMS
        # -------------------------
        customer = None
        customer_id = None
 
        if user.is_authenticated:
            customer_id = str(
                getattr(user, 'customer_code', None)
                or getattr(user, 'customer_id', None)
                or getattr(user, 'user_id', None)
                or getattr(user, 'id', None)
            )
        else:
            customer_id = str(data.get('customer_id', '')).strip()
 
        if not customer_id:
            return HttpResponse("Customer not found", status=404)
 
        try:
            customer = Customer.objects.get(customer_code=customer_id)
        except Customer.DoesNotExist:
            # keep generating quotation with cart data; do not fail here if customer record is absent.
            customer = None
 
        cart_items = Cart.objects.filter(customer_id=customer_id)
        if not cart_items.exists():
            # fallback to CustomerCartItem if Cart record is missing (to cover CurrencyCartItem only usage)
            cart_items = CustomerCartItem.objects.filter(customer_id=customer_id)
 
        if not cart_items.exists():
            return HttpResponse("Cart is empty", status=400)
 
        # -------------------------
        # INPUT PARAMS
        # -------------------------
        weeks = int(data.get("weeks", 1))
        adLength = int(data.get("adLength", 1))
        adPosition = data.get("adPosition", "Before movie")
 
        multiplier = 2 if adPosition == "Both" else 1
 
        # -------------------------
        # CALCULATIONS
        # -------------------------
        total_values = []
        totalSeats = 0
        totalShowOffering = 0
        showOfferings = []
 
        spots_per_week = 28 * multiplier
        showOfferingSingle = weeks * spots_per_week
 
        for item in cart_items:
            total = item.rate * adLength * weeks * multiplier
            total_values.append(total)
 
            totalSeats += int(item.seats_number)
 
            showOfferings.append({
                "id": item.id,
                "offering": showOfferingSingle
            })
 
            totalShowOffering += showOfferingSingle
 
        gross_total = sum(total_values)
 
        # -------------------------
        # DISCOUNT + GST
        # -------------------------
        discount_rate = float(data.get("discount", 0))
        discount_amount = gross_total * discount_rate / 100
 
        discounted_total = gross_total - discount_amount
 
        gst = discounted_total * 0.18
        total_payable = discounted_total + gst
 
        # -------------------------
        # EXTRA CALCULATIONS
        # -------------------------
        campaign_time_seconds = adLength * totalShowOffering
 
        if campaign_time_seconds > 0:
            effective_cost = Decimal(discounted_total) / Decimal(campaign_time_seconds)
            effective_cost = effective_cost.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        else:
            effective_cost = Decimal("0.00")
 
        avgAudReach = round((showOfferingSingle * totalSeats) * 0.30)
 
        # -------------------------
        # REF NO GENERATION (no DB counter table needed)
        # -------------------------
        today = date.today()

        if today.month >= 4:
            start_year = today.year
            end_year = today.year + 1
        else:
            start_year = today.year - 1
            end_year = today.year

        financial_year = f"{start_year}/{str(end_year)[2:]}"
        refNo = f"QTN-{financial_year}-{int(datetime.now().timestamp()) % 100000:05d}"
 
        # -------------------------
        # CITY
        # -------------------------
        city = ""
        try:
            if customer and getattr(customer, 'city_code', None):
                city = Cities.objects.get(city_code=customer.city_code).city_name
        except Cities.DoesNotExist:
            city = ""
 
        # -------------------------
        # CONTEXT (IMPORTANT)
        # -------------------------
        # Generate logo - placeholder for now (user can add actual logo path)
        logo = ""
       
        quotation_with_totals = list(zip(cart_items, total_values))
        context = {
            'quotation': cart_items,
            'quotation_with_totals': quotation_with_totals,
            'customer': customer,
            'city': city,
            'refNo': refNo,
            'date': today.strftime('%d/%m/%Y'),
            'total_values': total_values,
            'totalSeats': totalSeats,
            'totalShowOffering': totalShowOffering,
            'showOfferings': showOfferings,
            'formatted_gross_total': "{:,.2f}".format(gross_total),
            'formatted_discount': "{:,.2f}".format(discount_amount),
            'formatted_discounted_total': "{:,.2f}".format(discounted_total),
            'formatted_total_taxable_amount': "{:,.2f}".format(discounted_total),
            'formatted_gst': "{:,.2f}".format(gst),
            'formatted_total_payable_amount': "{:,.2f}".format(total_payable),
            'effective_cost_per_show': "{:,.2f}".format(effective_cost),
            'avgAudReach': avgAudReach,
            'campaign_time_seconds': campaign_time_seconds,
            'discount_rate_numeric_coupen': float(discount_rate),
            'logo': logo,
            'quotation_data': {
                "weeks": weeks,
                "adLength": adLength,
                "adPosition": adPosition
            }
        }
 
        # -------------------------
        # Generate PDF using xhtml2pdf + quotation.html template
        # -------------------------
        html = render_to_string('quotation.html', context)
       
        # Encode to UTF-8 to ensure special characters (rupees symbol) render correctly
        html_bytes = html.encode('utf-8')
       
        # Generate PDF from HTML using xhtml2pdf/pisa
        result = io.BytesIO()
        pisa_status = pisa.CreatePDF(
            html_bytes,
            dest=result,
            encoding='utf-8'
        )
       
        if pisa_status.err:
            print(f"xhtml2pdf Error: {pisa_status.err}")
            return HttpResponse(f"PDF Error: {pisa_status.err}", status=500)
       
        result.seek(0)
        response = HttpResponse(result.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{refNo}.pdf"'
        return response
 
    except Exception as e:
        print("🔥 PDF TEMPLATE ERROR:", str(e))
        return HttpResponse(f"Error generating PDF: {str(e)}", status=500)


class PartnerCinemaListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            print("\n===== CINEMA LIST DEBUG START =====")

            print("QUERY PARAMS:", request.GET.dict())

            qs = ScreenlistingNew.objects.all()
            print("Initial Count:", qs.count())

            state = request.GET.get("state")
            city = request.GET.get("city")
            chain = request.GET.get("cinema_chain")
            ctype = request.GET.get("cinema_type")

            print("Filters →",
                  "state:", state,
                  "| city:", city,
                  "| chain:", chain,
                  "| type:", ctype)

            if state:
                qs = qs.filter(state__icontains=state)
                print("After state filter:", qs.count())

            if city:
                qs = qs.filter(city__icontains=city)
                print("After city filter:", qs.count())

            if chain:
                qs = qs.filter(cinema_chain__icontains=chain)
                print("After chain filter:", qs.count())

            if ctype:
                qs = qs.filter(cinema_type__icontains=ctype)
                print("After type filter:", qs.count())

            qs = qs.order_by('id')
            print("Final Count:", qs.count())

            # 🔍 Print sample record
            sample = qs.first()
            print("Sample Record:", sample)

            if sample:
                print("Sample Fields:", sample.__dict__)

                # 🔥 Check important fields
                print("base_rate_per_seconds_perweeks:",
                      getattr(sample, "base_rate_per_seconds_perweeks", "NOT FOUND"))

                print("base_rate_per_seconds_perweeks:",
                      getattr(sample, "base_rate_per_seconds_perweeks", "NOT FOUND"))

            serializer = PartnerScreenlistingSerializer(
                qs,
                many=True,
                context={'request': request}
            )

            print("Serialized Count:", len(serializer.data))
            print("===== CINEMA LIST DEBUG END =====\n")

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            print("🔥 ERROR in PartnerCinemaListView:", str(e))
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class PartnerCinemaFilterOptionsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            print("\n===== FILTER OPTIONS DEBUG START =====")

            qs = ScreenlistingNew.objects.all()
            print("Total Records:", qs.count())

            states = list(qs.values_list('state', flat=True).distinct())
            cities = list(qs.values_list('city', flat=True).distinct())
            chains = list(qs.values_list('cinema_chain', flat=True).distinct())
            types = list(qs.values_list('cinema_type', flat=True).distinct())

            print("States Count:", len(states))
            print("Cities Count:", len(cities))
            print("Chains Count:", len(chains))
            print("Types Count:", len(types))

            # 🔍 Print sample values
            print("Sample States:", states[:5])
            print("Sample Cities:", cities[:5])
            print("Sample Chains:", chains[:5])
            print("Sample Types:", types[:5])

            print("===== FILTER OPTIONS DEBUG END =====\n")

            return Response({
                'states': states,
                'cities': cities,
                'chains': chains,
                'types': types,
            })

        except Exception as e:
            print("🔥 ERROR in FilterOptions:", str(e))
            return Response({"error": str(e)}, status=500)
        
class PartnerCartAddView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            print("\n===== ADD TO CART DEBUG START =====")

            partner_code = request.user.partner_code

            print("partner_code:", partner_code)

            if not partner_code:
                return Response({"error": "Partner not found"}, status=400)

            cinema_id = request.data.get("cinema_id")
            cinema = ScreenlistingNew.objects.filter(id=cinema_id).first()

            if not cinema:
                return Response({"error": "Cinema not found"}, status=404)

            customer_code = request.data.get("customer_code")
            if not customer_code:
                return Response({"error": "Customer not selected"}, status=400)
            cart = PartnerCustomerCart.objects.filter(
                partner_code=partner_code,customer_code=customer_code,
            ).first()

            if not cart:
               
                last_cart = PartnerCustomerCart.objects.order_by('-id').first()

                if last_cart and last_cart.cart_id:
                    try:
                        last_number = int(last_cart.cart_id.split('-')[-1])
                        new_number = last_number + 1
                    except:
                        new_number = 1
                else:
                    new_number = 1

                
                cart = PartnerCustomerCart.objects.create(
                    cart_id=f"Cart-{new_number}",
                    partner_code=partner_code,
                    customer_code=customer_code,
                    createdon=timezone.now(),
                    createdby=request.user.id
                )

            # ✅ FIXED RATE
            base_rate = Decimal(cinema.base_rate_per_seconds_perweeks or 0)
            bb_rate = Decimal(cinema.bb_rate_per_seconds_perweeks or 0)

            item = PartnerCustomerCartItem.objects.create(
                partner_code=partner_code,
                customer_code=customer_code,
                cart_id=cart.cart_id,
                screen_id=cinema.id,
                media_name=cinema.theatre_name,
                web_code=cinema.webcode,
                city=cinema.city,
                district=cinema.district,
                state=cinema.state,
                theatre_address=cinema.theatre_address,
                projection=cinema.projection,
                seats_number=int(cinema.seating_capacity or 0),

                rate=base_rate,

                base_rate_10secweek=int(float(cinema.base_rate_10sec_week or 0)),
                bb_rate_10secweek=int(float(cinema.bb_rate_10sec_week or 0)),

                base_rate_10secweek_0=int(base_rate),
                bb_rate_10secweek_0=int(bb_rate),
                grand_total=0,
                discount="0",
                rate_type=1,
                campaign_category=cinema.cinema_category,
                date=timezone.now().date(),  
                createdon=timezone.now(),
                createdby=request.user.id
            )

            print("✅ SUCCESS ITEM:", item.id)

            return Response({"message": "Added to cart"}, status=201)

        except Exception as e:
            print("🔥 ERROR:", str(e))
            return Response({"error": str(e)}, status=500)
        
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from decimal import Decimal
from django.utils import timezone
from datetime import datetime
import uuid
from decimal import Decimal
from datetime import datetime
import uuid
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

class PartnerCartProcessView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def generate_campaign_code(self):
        last_code = BookCampaign.objects.aggregate(
            max_code=Max("campaign_code")
        )["max_code"]

        if last_code:
            return last_code + 1
        return 1
    def post(self, request):
        try:
            print("\n===== PROCESS CART DEBUG START =====")

            partner_code = request.user.partner_code
            data = request.data

            # ✅ Customer check
            customer_code = data.get("customer_code") or data.get("customer_id")
            if not customer_code:
                return Response({"error": "Please select a customer first"}, status=400)

            # ✅ Params
            rate_type = int(data.get("rateType", 0))
            ad_type = int(data.get("adType", 0))
            ad_position = int(data.get("adPosition", 0))
            ad_length = int(data.get("adLength", 10))
            weeks = int(data.get("weeks", 1))

            # ✅ Discount %
            discount_perc = Decimal(str(data.get("discount", 0)))

            # ✅ Cart items
            items = PartnerCustomerCartItem.objects.filter(
                partner_code=partner_code,
                customer_code=customer_code
            ).exclude(cart_id__contains="Booked")

            if not items.exists():
                return Response({"error": "Cart is empty"}, status=400)

            total = Decimal("0.00")
            partner_total = Decimal("0.00")
            processed = []

            for item in items:
                screen = ScreenlistingNew.objects.filter(id=item.screen_id).first()
                if not screen:
                    continue

                # ✅ Rate logic
                if rate_type == 0:
                    rate = Decimal(screen.base_rate_10sec_week or 0) / 10
                else:
                    rate = Decimal(screen.bb_rate_10sec_week or 0) / 10

                total += rate * ad_length * weeks

                # ✅ NEW (PARTNER RATE - REFERENCE ONLY)
                if rate_type == 0:
                    partner_rate = Decimal(getattr(screen, "partner_base_rate_10sec_week", 0)) / 10
                else:
                    partner_rate = Decimal(getattr(screen, "partner_bb_rate_10sec_week", 0)) / 10

                partner_total += partner_rate * ad_length * weeks

                processed.append({
                    "id": item.id,
                    "screen_id": item.screen_id,
                    "media_name": item.media_name,
                    "city": item.city,
                    "projection": item.projection,
                    "rate": float(rate),
                    "theatre_address": item.theatre_address,
                })

            # ✅ Ad position (Both)
            if ad_position == 2:
                total *= 2
                partner_total *= 2

            # ================= 💥 DISCOUNT LOGIC =================
            discount_amount = (total * discount_perc) / Decimal("100")
            discounted_total = total - discount_amount

            # ================= GST =================
            gst = discounted_total * Decimal("0.18")
            total_payable = discounted_total + gst

            # PARTNER (REFERENCE ONLY)
            partner_discount_amount = (partner_total * discount_perc) / Decimal("100")
            partner_discounted_total = partner_total - partner_discount_amount
            partner_gst = partner_discounted_total * Decimal("0.18")
            partner_total_payable = partner_discounted_total + partner_gst

            print("TOTAL:", total)
            print("DISCOUNT %:", discount_perc)
            print("DISCOUNT AMOUNT:", discount_amount)
            print("GST:", gst)
            print("TOTAL PAYABLE:", total_payable)

            submit_type = data.get("submitType")

            # ================= AUTO SAVE =================
            if submit_type == "autosave" or discount_perc > 0:

                cart = PartnerCustomerCart.objects.filter(
                    partner_code=partner_code,
                    customer_code=customer_code
                ).first()

                cart_id = cart.cart_id if cart else None

                start_date_str = data.get("startDatePicker")
                end_date_str = data.get("endDatePicker")

                start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date() if start_date_str else None
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date() if end_date_str else None

                # ✅ FIX: UPDATE OR CREATE (NO DELETE)
                obj, created = CustomerCartDetails.objects.update_or_create(
                    cart_id=cart_id,
                    customer_code=customer_code,
                    defaults={
                        "partner_id": str(partner_code),
                        "rate_type": rate_type,
                        "ad_length": str(ad_length),
                        "weeks": weeks,
                        "ad_position": ad_position,
                        "ad_type": ad_type,
                        "start_date": start_date,
                        "end_date": end_date,
                        "question1": data.get("question1", "No"),
                        "question2": data.get("question2", "No"),
                        "manual_discount_rate": float(discount_perc),
                        "manual_discount_amount": float(discount_amount),
                        "createdon": timezone.now(),
                        "createdby": request.user.id,
                    }
                )

                print("✅ SAVED (UPDATE_OR_CREATE)")
                print("Manual Discount %:", discount_perc)
                print("Manual Discount Amount:", discount_amount)

            # ================= BOOK =================
            if submit_type in ["confirm", "bookWithoutPayment"]:

                code = self.generate_campaign_code()

                # ✅ get dates (important)
                start_date_str = data.get("startDatePicker")
                end_date_str = data.get("endDatePicker")

                start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date() if start_date_str else None
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date() if end_date_str else None

                # ✅ LOOP THROUGH CART ITEMS
                for item in items:
                    screen = ScreenlistingNew.objects.filter(id=item.screen_id).first()

                    if rate_type == 0:
                        rate = Decimal(screen.base_rate_10sec_week or 0) / 10
                    else:
                        rate = Decimal(screen.bb_rate_10sec_week or 0) / 10
                        
                    BookCampaign.objects.create(
                        campaign_code=code,  # ✅ SAME for all rows

                        customer_code=customer_code,
                        partner_code=partner_code,

                        price=float(rate),  # ✅ SAVE THE PRICE HERE

                        # ✅ SCREEN DATA (NO MORE NULL)
                        screen_number=item.screen_id,
                        media_name=item.media_name,
                        projection=item.projection,
                        city_code=item.city,

                        number_seats=screen.seating_capacity if screen else None,
                        state_code=getattr(screen, "state", None),

                        # ✅ Campaign config
                        ad_type=str(ad_type),
                        ad_position=str(ad_position),
                        ads_in_second=ad_length,
                        week=weeks,

                        # ✅ Dates
                        date=timezone.now().date(),
                        campaign_start_date=start_date,
                        campaign_end_date=end_date,
                        booking_date=timezone.now().date(),
                        campaign_category=getattr(screen, "cinema_category", None),
                      

                        # ✅ Pricing (same for all)
                        gross_total=float(total),
                        discount_percentage=float(discount_perc),
                        discount_total=float(discount_amount),
                        total_taxable_amount=float(discounted_total),
                        gst=float(gst),
                        total_payable_amount=total_payable,

                        # ✅ Status
                        payment_status="Pending" if submit_type == "bookWithoutPayment" else "Paid",
                        campaign_status="Booked",

                        createdon=timezone.now(),
                        createdby=request.user
                    )

                print(f"✅ Campaign Saved for {items.count()} screens")

                # # ✅ Clear cart
                # items.delete()
                for item in items:
                    item.cart_id = f"{item.cart_id}-Booked"
                    item.save()

                return Response({
                    "message": "Booked successfully",
                    "campaign_code": code,
                    
                })
            print("===== PROCESS CART DEBUG END =====\n")

            return Response({
                "cart_items": processed,
                "calculation": {
                    "gross_total": float(total),
                    "discount_percentage": float(discount_perc),
                    "discount_amount": float(discount_amount),
                    "taxable_amount": float(discounted_total),
                    "gst": float(gst),
                    "total_payable": float(total_payable)
                },
                "partner_calculation": {
                    "gross_total": float(partner_total),
                    "discount_percentage": float(discount_perc),
                    "discount_amount": float(partner_discount_amount),
                    "taxable_amount": float(partner_discounted_total),
                    "gst": float(partner_gst),
                    "total_payable": float(partner_total_payable)
                }
            })

        except Exception as e:
            print("🔥 ERROR:", str(e))
            return Response({"error": str(e)}, status=500)
        
class PartnerCartDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        try:
            partner_code = request.user.partner_code
            cinema_id = request.data.get("cinema_id")
            customer_code = request.data.get("customer_code")

            if not cinema_id or not customer_code:
                return Response({"error": "Missing data"}, status=400)

            PartnerCustomerCartItem.objects.filter(
                partner_code=partner_code,
                customer_code=customer_code,
                screen_id=cinema_id   # ✅ KEY MATCH
            ).delete()

            return Response({"message": "Deleted"}, status=200)
          
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
class PartnerCartCountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        partner_code = request.user.partner_code
        customer_code = request.query_params.get("customer_code")

        if not customer_code:
            return Response({"count": 0})

        count = PartnerCustomerCartItem.objects.filter(
            partner_code=partner_code,
            customer_code=customer_code
        ).exclude(cart_id__contains="Booked").count()

        return Response({"count": count})

  
class PartnerCartItemsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        partner_code = request.user.partner_code
        customer_code = request.GET.get("customer_code")

        if not customer_code:
            return Response({"error": "Customer required"}, status=400)

        items = PartnerCustomerCartItem.objects.filter(
            partner_code=partner_code,
            customer_code=customer_code
        ).exclude(cart_id__contains="Booked")

        cinema_ids = items.values_list("screen_id", flat=True)
     
        return Response({"items": list(cinema_ids)})

from django.core.exceptions import ObjectDoesNotExist
from xhtml2pdf import pisa
from django.db import transaction
from datetime import date
import pdfkit
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_partner_quotation_api(request):
    try:
        user = request.user
        partner_code = user.partner_code
        data = request.data

        customer_code = data.get("customer_code")

        if not customer_code:
            return HttpResponse("Customer required", status=400)

        # ✅ Customer
        customer = Customer.objects.filter(customer_code=customer_code).first()

        # ✅ Partner
        partner = Partner.objects.filter(partner_code=partner_code).first()

        # ✅ Bank
        bank = PartnerBankDetails.objects.filter(
            partner_code=partner_code
        ).first()

        # ✅ Cart
        cart_items = PartnerCustomerCartItem.objects.filter(
            partner_code=partner_code,
            customer_code=customer_code
        ).exclude(cart_id__contains="Booked")

        if not cart_items.exists():
            return HttpResponse("Cart empty", status=400)

        # -------------------------
        # INPUT
        # -------------------------
        weeks = int(data.get("weeks", 1))
        adLength = int(data.get("adLength", 10))

        # ✅ Ad Position FIX
        adPosition_raw = data.get("adPosition", 0)

        if isinstance(adPosition_raw, str):
            mapping = {
                "Before movie": 0,
                "During interval": 1,
                "Both": 2
            }
            adPosition = mapping.get(adPosition_raw, 0)
        else:
            adPosition = int(adPosition_raw)

        # ✅ TEXT MAPPING (FINAL FIX)
        if adPosition == 0:
            adPositionText = "Before movie"
        elif adPosition == 1:
            adPositionText = "During interval"
        elif adPosition == 2:
            adPositionText = "Both (Before & Interval)"
        else:
            adPositionText = "-"

        multiplier = 2 if adPosition == 2 else 1

        # -------------------------
        # CALCULATION
        # -------------------------
        total_values = []
        totalSeats = 0
        totalShowOffering = 0
        showOfferings = []

        spots_per_week = 28 * multiplier
        showOfferingSingle = weeks * spots_per_week

        for item in cart_items:
            total = float(item.rate) * adLength * weeks * multiplier
            total_values.append(total)

            totalSeats += int(item.seats_number)

            showOfferings.append({
                "id": item.id,
                "offering": showOfferingSingle
            })

            totalShowOffering += showOfferingSingle

        gross_total = sum(total_values)

        # -------------------------
        # DISCOUNT (FROM CART - NO CHANGE)
        # -------------------------
        cart_details = CustomerCartDetails.objects.filter(
            customer_code=customer_code
        ).order_by('-createdon').first()

        if cart_details:
            discount = float(cart_details.manual_discount_rate or 0)
            discount_amount = float(cart_details.manual_discount_amount or 0)
        else:
            discount = 0
            discount_amount = 0

        discounted_total = gross_total - discount_amount
        gst = discounted_total * 0.18
        total_payable = discounted_total + gst

        # -------------------------
        # EXTRA
        # -------------------------
        campaign_time_seconds = adLength * totalShowOffering

        effective_cost = (
            discounted_total / campaign_time_seconds
            if campaign_time_seconds else 0
        )

        avgAudReach = round((showOfferingSingle * totalSeats) * 0.30)
        import base64

        logo_base64 = None

        if partner and partner.logo:
            try:
                logo_base64 = base64.b64encode(partner.logo).decode("utf-8")
            except Exception as e:
                print("Logo error:", e)
        # -------------------------
        # REF NO (FINANCIAL YEAR + COUNTER)
        # -------------------------
        
        today = date.today()

        # ✅ Financial Year Logic
        if today.month >= 4:
            start_year = today.year
            end_year = today.year + 1
        else:
            start_year = today.year - 1
            end_year = today.year

        financial_year = f"{start_year}/{str(end_year)[-2:]}"

        # ✅ Counter (PartnerQuotationCounter)
        with transaction.atomic():
            counter = PartnerQuotationCounter.objects.select_for_update().first()

            if not counter:
                counter = PartnerQuotationCounter.objects.create(count=1)
            else:
                counter.count = (counter.count or 0) + 1
                counter.save()

            counter_value = str(counter.count).zfill(5)

        # ✅ FINAL REF NO
        refNo = f"QTN-{financial_year}-{counter_value}"

        # -------------------------
        # CITY FIX (SAFE)
        # -------------------------
        city_value = "-"
        if customer:
            city_value = (
                getattr(customer, "city", None)
                or getattr(customer, "city_name", None)
                or getattr(customer, "city_code", None)
                or "-"
            )

        # -------------------------
        # CONTEXT
        # -------------------------
        quotation_with_totals = list(zip(cart_items, total_values))

        context = {
            "customer": customer,
            "city": city_value,

            # ✅ PARTNER DATA FIX
            "AssociateName": getattr(partner, "name", "-") if partner else "-",
            "AssociateContact": getattr(partner, "mobile_no", "-") if partner else "-",

            "partner": partner,
            "bank": bank,
            "logo": logo_base64,

            "quotation_with_totals": quotation_with_totals,
            "refNo": refNo,
            "date": today.strftime('%d/%m/%Y'),

            "totalSeats": totalSeats,
            "totalShowOffering": totalShowOffering,
            "showOfferings": showOfferings,

            "formatted_gross_total": "{:,.2f}".format(gross_total),
            "formatted_discount": "{:,.2f}".format(discount_amount),
            "formatted_discounted_total": "{:,.2f}".format(discounted_total),
            "formatted_total_taxable_amount": "{:,.2f}".format(discounted_total),
            "formatted_gst": "{:,.2f}".format(gst),
            "formatted_total_payable_amount": "{:,.2f}".format(total_payable),

            "effective_cost_per_show": "{:,.2f}".format(effective_cost),
            "avgAudReach": avgAudReach,
            "campaign_time_seconds": campaign_time_seconds,
            "discount_rate_numeric_coupen": discount,

            # ✅ FINAL FIX
            "quotation_data": {
                "weeks": weeks,
                "adLength": adLength,
                "adPosition": adPositionText
            }
        }

        # -------------------------
        # PDF GENERATION
        # -------------------------
        html = render_to_string("partner_quotation.html", context)

        result = io.BytesIO()
        pisa.CreatePDF(html.encode("utf-8"), dest=result)

        result.seek(0)

        response = HttpResponse(result.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{refNo}.pdf"'

        return response

    except Exception as e:
        print("🔥 PDF ERROR:", str(e))
        return HttpResponse(str(e), status=500)

		
		
import random
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.utils import timezone
from rest_framework.authentication import SessionAuthentication
from .models import Generateotp
from .authentication import CustomJWTAuthentication

class SendOTPView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request): 
        try:
            # Get customer and mobile from authenticated user (fallback to session)
            customer_code = (
                request.session.get('CustomerId')
                or getattr(request.user, 'customer_code', None)
                or getattr(request.user, 'user_id', None)
                or getattr(request.user, 'id', None)
            )

            # Prefer user.username as phone, then customer table contact_number
            phone_number = (
                request.session.get('username') 
                or getattr(request.user, 'username', None)
                or getattr(request.user, 'mobile_no', None)
            )

            if not phone_number and customer_code:
                from .models import Customer
                customer_obj = Customer.objects.filter(customer_code=customer_code).first()
                if customer_obj and customer_obj.contact_number:
                    phone_number = customer_obj.contact_number

            if not phone_number:
                return Response({"error": "Phone number not found"}, status=status.HTTP_400_BAD_REQUEST)

            otp_code = random.randint(100000, 999999)
            
            # Fast2SMS Dynamic Integration
            url = "https://www.fast2sms.com/dev/bulkV2"
            api_key = "TgxOvN2IdDUiMRJWAsByYw5ekca08Km97EbQfZhVtSHpGPrX6uDCG6fgcHzBW8KVTSwi0eM5FbPJdQ23" # Move to settings.py for best practice
            
            payload = {
                "authorization": api_key,
                "route": "dlt",
                "sender_id": "ADBJAO",
                "message": "172838", # Your DLT Template ID
                "variables_values": str(otp_code),
                "numbers": str(phone_number),
                "flash": "0"
            }
            
            response = requests.get(url, params=payload, timeout=10)
            api_res = response.json()

            if api_res.get('return'):
                expiry = timezone.now() + timezone.timedelta(minutes=5)
                Generateotp.objects.create(
                    customer_code=customer_code,
                    otp=otp_code,
                    created_at=timezone.now(),
                    expires_at=expiry,
                    is_deleted=0
                )
                return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)
            
            return Response({"error": "Failed to send SMS"}, status=status.HTTP_424_FAILED_DEPENDENCY)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VerifyOTPView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            otp_input = request.data.get('otp')
            customer_code = (
                request.session.get('CustomerId')
                or request.data.get('customer_id')
                or getattr(request.user, 'customer_code', None)
                or getattr(request.user, 'user_id', None)
                or getattr(request.user, 'id', None)
            )

            try:
                otp_val = int(otp_input)
            except (TypeError, ValueError):
                return Response({"error": "Invalid OTP format"}, status=status.HTTP_400_BAD_REQUEST)

            # Verify against DB
            otp_record = Generateotp.objects.filter(
                customer_code=customer_code,
                otp=otp_val,
                is_deleted=0
            ).last()

            if not otp_record:
                return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

            if otp_record.expires_at < timezone.now():
                return Response({"error": "OTP Expired"}, status=status.HTTP_400_BAD_REQUEST)

            # Mark as verified/deleted so it can't be reused
            otp_record.is_deleted = 1
            otp_record.save()
            
            request.session['otp_verified'] = True
            return Response({"success": True, "message": "Verified"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
import razorpay
from django.conf import settings
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authentication import SessionAuthentication
from .authentication import CustomJWTAuthentication

# Initialize Razorpay client
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

class InitiatePaymentView(APIView):
    """
    Handles the creation of a Razorpay Order.
    """
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            amount = request.data.get('amount')
            customer_id = request.data.get('customer_id')

            if not amount:
                return Response({"error": "Amount is required"}, status=status.HTTP_400_BAD_REQUEST)

            # Razorpay expects amount in PAISE (1 Rupee = 100 Paise)
            payment_data = {
                "amount": int(float(amount) * 100), 
                "currency": "INR",
                "payment_capture": "1"
            }

            # Create Order in Razorpay system
            razorpay_order = client.order.create(data=payment_data)
            
            # Return response matching your frontend expectations
            return Response({
                "razorpay_order_id": razorpay_order['id'],
                "razorpay_key": settings.RAZORPAY_KEY_ID,
                "amount": payment_data['amount'],
                "currency": "INR",
                "campaign_code": f"CPGN-{customer_id}"
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class VerifyPaymentView(APIView):
    """
    Handles signature verification after payment completion.
    """
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            # Placeholder for Razorpay Signature Verification logic
            # Typically involves: razorpay_payment_id, razorpay_order_id, razorpay_signature
            return Response(
                {"message": "Verification logic goes here"}, 
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
  
# ===== BOOK CAMPAIGN LIST & DETAIL VIEWS =====

# ============================
# IMPORTS
# ============================
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db.models import Q, Max
from django.shortcuts import get_object_or_404

from .models import BookCampaign, Customer
from .serializers import BookCampaignSerializer
from .authentication import CustomJWTAuthentication
from rest_framework.authentication import SessionAuthentication


class BookCampaignListView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            session_data = request.session.get("user_data", {})

            partner_code = session_data.get("partner_code")
            associate_code = session_data.get("associate_code")

            if not partner_code and not associate_code:
                user = request.user
                partner_code = getattr(user, "partner_code", None)
                associate_code = getattr(user, "associate_code", None)

            queryset = BookCampaign.objects.all()

            if partner_code:
                customer_codes = Customer.objects.filter(
                    partner_code=partner_code
                ).values_list('customer_code', flat=True)

                queryset = queryset.filter(customer_code__in=customer_codes)

            elif associate_code:
                queryset = queryset.filter(associate_code=associate_code)

            campaign_status = request.query_params.get('campaign_status')
            if campaign_status and campaign_status.lower() != 'all':
                queryset = queryset.filter(campaign_status__iexact=campaign_status)

            payment_status = request.query_params.get('payment_status')
            if payment_status and payment_status.lower() != 'all':
                queryset = queryset.filter(payment_status__iexact=payment_status)

            search = request.query_params.get('search', '').strip()

            if search:
                query = Q(campaign_name__icontains=search)

                if search.isdigit():
                    query |= Q(campaign_code=int(search))

                queryset = queryset.filter(query)

            latest_ids = (
                queryset
                .values('customer_code')
                .annotate(max_id=Max('id'))
                .values_list('max_id', flat=True)
            )

            queryset = queryset.filter(id__in=latest_ids).order_by('-booking_date')

            customer_codes = queryset.values_list('customer_code', flat=True)

            customers = Customer.objects.filter(
                customer_code__in=customer_codes
            )

            customer_map = {
                cust.customer_code: cust.name for cust in customers
            }

            serializer = BookCampaignSerializer(
                queryset,
                many=True,
                context={'customer_map': customer_map}
            )

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class BookCampaignDetailView(APIView):

    def get(self, request, id):
        try:
            # 1️⃣ clicked row
            campaign = BookCampaign.objects.filter(id=id).first()

            if not campaign:
                return Response({"error": "Campaign not found"}, status=404)

            # 2️⃣ SAME campaign_code चे सर्व records (screens)
            screens = BookCampaign.objects.filter(
                campaign_code=campaign.campaign_code
            )

            # 3️⃣ Calculate remaining_amount automatically
            from decimal import Decimal
            total_payable = Decimal(str(campaign.total_payable_amount or 0))
            paid_amount = Decimal(str(campaign.paid or 0))
            remaining_amount = total_payable - paid_amount

            # Convert numeric campaign_status to text labels
            status_map = {
                '0': 'Pending',
                '1': 'Approved',
                '2': 'Rejected',
                '3': 'Booked'
            }
            campaign_status_display = status_map.get(str(campaign.campaign_status), campaign.campaign_status)

            # Convert numeric payment_status to text labels
            payment_status_map = {
                '0': 'Paid',
                '1': 'Partially Paid',
                '2': 'Unpaid',
                '3': 'Pending'
            }
            payment_status_display = payment_status_map.get(str(campaign.payment_status), campaign.payment_status)

            # 4️⃣ response तयार कर
            data = {
                "campaign_code": campaign.campaign_code,
                "name": campaign.campaign_name,
                "booking_date": campaign.booking_date,
                "payment_mode": campaign.payment_mode,
                "campaign_status": campaign_status_display,
                "payment_status": payment_status_display,
                "total_payable_amount": str(total_payable),
                "remaining_amount": str(remaining_amount),
                "paid_amount": str(paid_amount),

                # Customization fields
                "ads_in_second": campaign.ads_in_second,
                "week": campaign.week,
                "ad_type": campaign.ad_type,
                "ad_position": campaign.ad_position,
                "campaign_start_date": campaign.campaign_start_date,
                "campaign_end_date": campaign.campaign_end_date,

                # Budget fields
                "gross_total": str(campaign.gross_total or 0),
                "discount": str(campaign.discount or 0),
                "discount_total": str(campaign.discount_total or 0),
                "censor_cc": str(campaign.censor_cc or 0),
                "total_taxable_amount": str(campaign.total_taxable_amount or 0),
                "gst": str(campaign.gst or 0),

                # 🔥 IMPORTANT PART
                "screens": [
                    {
                        "media_name": s.media_name,
                        "city": s.city_code,
                        "projection": s.projection,
                        "rate": s.price,
                        "seats_number": s.number_seats,
                    }
                    for s in screens
                ]
            }

            return Response(data, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def put(self, request, id):
        try:
            from decimal import Decimal

            print("\n===== APPROVE CAMPAIGN DEBUG =====")
            print("Request Data:", request.data)

            # Get the campaign by id
            campaign = BookCampaign.objects.filter(id=id).first()

            if not campaign:
                return Response({"error": "Campaign not found"}, status=404)

            # Get all campaigns with same campaign_code
            campaigns = BookCampaign.objects.filter(
                campaign_code=campaign.campaign_code,
                customer_code=campaign.customer_code
            )

            # Extract data from request
            payment_mode = request.data.get('payment_mode')
            payment_status = request.data.get('payment_status')
            transaction_id = request.data.get('transaction_id')
            paid_amount = request.data.get('paid_amount', 0)
            campaign_status = request.data.get('campaign_status')

            # Extract coupon data
            coupon_code = request.data.get('coupon_code')
            discount_percentage = request.data.get('discount_percentage')  # Only coupon %
            discount = request.data.get('discount')  # Combined discount %

            # Extract recalculated amounts from frontend
            gross_total = request.data.get('gross_total')
            total_payable_amount = request.data.get('total_payable_amount')

            # Convert campaign_status text to numeric
            status_map = {
                'Pending': '0',
                'Approved': '1',
                'Rejected': '2',
                'Booked': '3'
            }
            if campaign_status in status_map:
                campaign_status_db = status_map[campaign_status]
            else:
                campaign_status_db = campaign_status

            # Extract customization fields
            ads_in_second = request.data.get('ads_in_second')
            week = request.data.get('week')
            ad_type = request.data.get('ad_type')
            ad_position = request.data.get('ad_position')
            campaign_start_date = request.data.get('campaign_start_date')
            campaign_end_date = request.data.get('campaign_end_date')

            # Calculate remaining amount using recalculated total_payable if provided
            if total_payable_amount:
                total_payable = Decimal(str(total_payable_amount))
            else:
                total_payable = Decimal(str(campaign.total_payable_amount or 0))

            paid = Decimal(str(paid_amount or 0))

            # Determine payment status based on payment mode
            if payment_mode == "1":  # Online Payment
                remaining = Decimal("0.00")
                final_payment_status = "0"  # Paid
                paid = total_payable
            else:  # Offline Payment
                if paid >= total_payable:
                    remaining = Decimal("0.00")
                    final_payment_status = "0"  # Paid
                elif paid > 0:
                    remaining = total_payable - paid
                    final_payment_status = "1"  # Partially Paid
                else:
                    remaining = total_payable
                    final_payment_status = "2"  # Unpaid

            # Prepare update data
            update_data = {
                'campaign_status': campaign_status_db,
            }

            # Add payment fields if provided
            if payment_mode:
                update_data['payment_mode'] = payment_mode
                update_data['payment_status'] = final_payment_status
                update_data['paid'] = float(paid)
                update_data['remaining_amount'] = float(remaining)

                # Only add transaction_id if it's not empty
                if transaction_id:
                    update_data['transaction_id_check_no'] = transaction_id

            # Add customization fields if provided
            if ads_in_second:
                update_data['ads_in_second'] = ads_in_second
            if week:
                update_data['week'] = week
            if ad_type:
                update_data['ad_type'] = ad_type
            if ad_position:
                update_data['ad_position'] = ad_position
            if campaign_start_date:
                update_data['campaign_start_date'] = campaign_start_date
            if campaign_end_date:
                update_data['campaign_end_date'] = campaign_end_date

            # Add coupon data if provided
            if coupon_code:
                update_data['coupon_code'] = coupon_code
            if discount_percentage is not None:
                update_data['discount_percentage'] = discount_percentage  # Only coupon %
            if discount is not None:
                update_data['discount'] = discount  # Combined discount %

            # Add recalculated amounts if provided (when coupon is applied)
            if total_payable_amount:
                update_data['total_payable_amount'] = float(total_payable_amount)
            if gross_total:
                update_data['gross_total'] = float(gross_total)

            # Update all campaigns with same campaign_code
            campaigns.update(**update_data)

            # Mark coupon as used if coupon was applied
            if coupon_code:
                try:
                    coupon = Coupens.objects.filter(coupen_code=coupon_code).first()
                    if coupon:
                        coupon.coupen_status = '1'  # Mark as Used
                        coupon.save()
                except Exception as e:
                    print(f"Error updating coupon status: {e}")

            return Response({
                "message": f"Campaign {campaign_status.lower()} successfully",
                "campaign_code": campaign.campaign_code
            }, status=200)

        except Exception as e:
            print(f"ERROR in BookCampaignDetailView PUT: {str(e)}")
            import traceback
            traceback.print_exc()
            return Response({"error": str(e)}, status=500)

class UserProfileView(APIView):
    authentication_classes = [CustomJWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        role_map = {1: 'Admin', 2: 'Partner', 3: 'Associate', 4: 'Customer'}
        role = role_map.get(user.usertype_id, 'Unknown')
        
        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'usertype_id': user.usertype_id,
            'role': role,
            'partner_code': user.partner_code,
            'associate_code': user.associate_code,
            'customer_code': user.customer_code,
            'createdon': user.createdon,
            'lastvisiton': user.lastvisiton,
            'superuser': user.superuser,
            'status': user.status
        }
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        data = request.data
        
        username = data.get('username')
        email = data.get('email')
        
        if username:
            user.username = username
        if email:
            user.email = email
            
        user.save()
        return Response({'message': 'Profile updated successfully'}, status=status.HTTP_200_OK)

 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime, timedelta
from django.db.models import Sum, Count
from django.utils.timezone import now, make_aware
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum
from django.utils.timezone import now
from datetime import datetime
 
@api_view(['GET'])
def dashboard_stats(request):
 
    print("\n===== DASHBOARD JWT DEBUG =====")
 
    user = request.user
    print("USER:", user)
 
    # ================== USER SESSION ==================
    role = getattr(user, "role", None)
    partner_code = getattr(user, "partner_code", None)
    associate_code = getattr(user, "associate_code", None)
 
    print("ROLE:", role)
    print("PARTNER CODE:", partner_code)
    print("ASSOCIATE CODE:", associate_code)
 
    current_month = datetime.now().month
    current_year = datetime.now().year
 
    # ================== CUSTOMER FILTER ==================
    if role == "partner":
        customers_qs = Customer.objects.filter(partner_code=partner_code)
    elif role == "associate":
        customers_qs = Customer.objects.filter(associate_code=associate_code)
    else:  # admin
        customers_qs = Customer.objects.all()
 
    total_customers = customers_qs.count()
 
    # ================== BOOK CAMPAIGN BASE ==================
    bookCampaign = BookCampaign.objects.all()
    print("TOTAL CAMPAIGNS:", bookCampaign.count())
 
    if role == "partner":
        bookCampaign = bookCampaign.filter(partner_code=partner_code)
    elif role == "associate":
        bookCampaign = bookCampaign.filter(associate_code=associate_code)
 
    print("AFTER ROLE FILTER:", bookCampaign.count())
 
    # ================== MONTH DATA (CARDS) ==================
    monthly_base = bookCampaign.filter(
        createdon__year=current_year,
        createdon__month=current_month
    )
 
    print("MONTHLY COUNT:", monthly_base.count())
 
    monthly_campaigns = monthly_base.values(
        "campaign_code",
        "total_taxable_amount",
        "customer_code"
    ).distinct()
 
    campaigns = monthly_campaigns.count()
 
    revenue = monthly_campaigns.aggregate(
        total=Sum("total_taxable_amount")
    )["total"] or 0
 
    print("FINAL:", campaigns, revenue, total_customers)
 
    # ================== REPORTS (LAST 7 DAYS) ==================
    today = datetime.now().date()
 
    chart_labels = []
    sales_data = []
    revenue_data = []
    customers_data = []
 
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
 
        start = datetime.combine(day, datetime.min.time())
        end = datetime.combine(day, datetime.max.time())
 
        day_base = bookCampaign.filter(createdon__range=(start, end))
 
        day_campaigns = day_base.values(
            "campaign_code",
            "total_taxable_amount",
            "customer_code"
        ).distinct()
 
        chart_labels.append(day.strftime("%d %b"))
        sales_data.append(day_campaigns.count())
 
        day_revenue = day_campaigns.aggregate(
            total=Sum("total_taxable_amount")
        )["total"] or 0
        revenue_data.append(float(day_revenue))
 
        customers_data.append(
            day_campaigns.values("customer_code").distinct().count()
        )
 
    # ================== RECENT FOLLOW UPS ==================
    activity_filter = request.GET.get("activity_filter")
 
    followups = CustomerFollowup.objects.exclude(
        next_follow_up_date__isnull=True,
        time__isnull=True
    )
 
    if role == "partner":
        followups = followups.filter(partner_code=partner_code)
    elif role == "associate":
        followups = followups.filter(associate_code=associate_code)
 
    today_date = now().date()
 
    if activity_filter == "today":
        followups = followups.filter(next_follow_up_date=today_date)
    elif activity_filter == "month":
        followups = followups.filter(
            next_follow_up_date__year=today_date.year,
            next_follow_up_date__month=today_date.month
        )
    elif activity_filter == "year":
        followups = followups.filter(
            next_follow_up_date__year=today_date.year
        )
 
    followups = followups.order_by(
        "-next_follow_up_date", "-time"
    )[:6]
 
    # ================== CUSTOMER MAP ==================
    customers_map = {
        c.customer_code: c.name
        for c in customers_qs.only("customer_code", "name")
    }
 
    activities = []
 
    for f in followups:
        followup_dt = datetime.combine(f.next_follow_up_date, f.time)
        diff = now().replace(tzinfo=None) - followup_dt
 
        if diff.days < 0:
            label = f"In {abs(diff.days)} days"
            badge = "text-primary"
        elif diff.days == 0:
            hours = diff.seconds // 3600
            minutes = (diff.seconds % 3600) // 60
            label = f"{hours} hrs" if hours else f"{minutes} min"
            badge = "text-success"
        elif diff.days < 7:
            label = f"{diff.days} days"
            badge = "text-warning"
        elif diff.days < 30:
            label = f"{diff.days // 7} weeks"
            badge = "text-muted"
        else:
            label = f"{diff.days // 30} months"
            badge = "text-danger"
 
        customer_name = customers_map.get(
            f.customer_code, "Unknown Customer"
        )
 
        activities.append({
            "label": label,
            "badge": badge,
            "content": f"{customer_name} - {f.visit_for} - {f.customer_status} - {f.next_follow_up_date} - {f.type}"
        })
 
    # ================== RESPONSE ==================
    return Response({
        "campaigns": campaigns,
        "revenue": float(revenue),
        "customers": total_customers,
        "chart_labels": chart_labels,
        "sales_data": sales_data,
        "revenue_data": revenue_data,
        "customers_data": customers_data,
        "activities": activities,
        "role": role
    })
 


@api_view(['GET'])
def ro(request, campaign_code):
    try:
        if not campaign_code:
            return HttpResponse("Campaign code required", status=400)

        # Get BookCampaign data
        book_campaign = BookCampaign.objects.filter(campaign_code=campaign_code).first()

        if not book_campaign:
            return HttpResponse("Campaign not found", status=404)

        # Get Customer data
        customer = None
        if book_campaign.customer_code:
            customer = Customer.objects.filter(customer_code=book_campaign.customer_code).first()

        # Get Partner or Associate data
        partner = None
        associate = None
        company_name = "-"

        if book_campaign.partner_code:
            partner = Partner.objects.filter(partner_code=book_campaign.partner_code).first()
            if partner:
                company_name = partner.name or "-"
        elif book_campaign.associate_code:
            associate = Associates.objects.filter(id=book_campaign.associate_code).first()
            if associate:
                company_name = associate.name or "-"

        # Get Bank Details
        bank = None
        if book_campaign.partner_code:
            bank = PartnerBankDetails.objects.filter(partner_code=book_campaign.partner_code).first()

        # Logo encoding
        logo_base64 = None
        if partner and partner.logo:
            try:
                logo_base64 = base64.b64encode(partner.logo).decode("utf-8")
            except Exception as e:
                print("Logo error:", e)

        # Generate RO Number
    
        from datetime import date
        from django.db import transaction

        today = date.today()
        ro_date = today.strftime('%d/%m/%Y')

        # ==========================
        # ✅ FINANCIAL YEAR LOGIC
        # ==========================
        if today.month >= 4:
            start_year = today.year
            end_year = today.year + 1
        else:
            start_year = today.year - 1
            end_year = today.year

        financial_year = f"{start_year}/{str(end_year)[-2:]}"

        # ==========================
        # ✅ RO COUNTER (LOCK SAFE)
        # ==========================
        with transaction.atomic():
            counter = RoCounter.objects.select_for_update().first()

            if not counter:
                counter = RoCounter.objects.create(count=1)
            else:
                counter.count = (counter.count or 0) + 1
                counter.save()

            counter_value = str(counter.count).zfill(5)

        # ==========================
        # ✅ FINAL RO NUMBER
        # ==========================
        ro_number = f"RO-{financial_year}-{counter_value}"
         # -------------------------
        
        
       

        # Get all campaigns with same campaign_code for table rows
        campaign_items = BookCampaign.objects.filter(campaign_code=campaign_code)

        # Calculate totals
        total_spots = 0
        total_seats = 0
        grand_total = 0

        for item in campaign_items:
            spots = (item.week or 0) * 28  # Assuming 28 spots per week
            if item.ad_position and "Both" in str(item.ad_position):
                spots *= 2
            total_spots += spots
            total_seats += (item.number_seats or 0)
            grand_total += (item.price or item.total_sreen_rate or 0)

        # Financial calculations
        censor_charges = book_campaign.censor_cc or 0
        taxable_amount = grand_total + censor_charges
        gst_amount = taxable_amount * 0.18
        total_payable = taxable_amount + gst_amount

        context = {
            "customer": customer,
            "partner": partner,
            "associate": associate,
            "bank": bank,
            "logo": logo_base64,
            "company_name": company_name,
            "ro_number": ro_number,
            "ro_date": ro_date,
            "book_campaign": book_campaign,
            "campaign_items": campaign_items,
            "total_spots": total_spots,
            "total_seats": total_seats,
            "grand_total": "{:,.2f}".format(grand_total),
            "censor_charges": "{:,.2f}".format(censor_charges),
            "taxable_amount": "{:,.2f}".format(taxable_amount),
            "gst_amount": "{:,.2f}".format(gst_amount),
            "total_payable": "{:,.2f}".format(total_payable),
            "amount_in_words": number_to_words_indian(total_payable),
        }

        # Render HTML
        html = render_to_string("ro.html", context)

        # Generate PDF
        result = io.BytesIO()
        pisa.CreatePDF(html.encode("utf-8"), dest=result)
        result.seek(0)

        response = HttpResponse(result.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{ro_number}.pdf"'

        return response

    except Exception as e:
        print("🔥 RO PDF ERROR:", str(e))
        return HttpResponse(str(e), status=500)
