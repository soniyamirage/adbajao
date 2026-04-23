from .models import *
from rest_framework import serializers
from django.db import transaction
from django.contrib.auth.hashers import make_password 
import base64

from django.db.models import Max

class UserRegisterSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Users
        fields = ['username', 'password', 'email', 'user_id']

    def create(self, validated_data):
        # Calculate next user_id
        max_id = Users.objects.aggregate(Max('user_id'))['user_id__max']
        validated_data['user_id'] = (max_id or 0) + 1
        
        # Hash password and set status
        validated_data['password'] = make_password(validated_data['password'])
        validated_data['status'] = 1
        
        return super().create(validated_data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__' 
        
class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = '__all__'  
        
class EngineModuleSerializer(serializers.ModelSerializer):  
    class Meta:
        model = EngineModule
        fields = "__all__"

class EngineSubmoduleSerializer(serializers.ModelSerializer):  
    class Meta:
        model = EngineSubmodule
        fields = "__all__"

class EngineActivitySerializer(serializers.ModelSerializer):  
    class Meta:
        model = EngineActivity
        fields = "__all__"

class EngineModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngineModule
        fields = '__all__'

    def create(self, validated_data):
        # Remove created_by if present since the model doesn't have this field
        validated_data.pop('created_by', None)
        return super().create(validated_data)

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'id',
            'customer_code',  # include so frontend select valueKey works
            'name',
            'company_contactperson',
            'desigation',
            'email_id',
            'address',
            'country_code',
            'state',
            'city_code',
            'gstin',
            'referral_code',
            'contact_number',
            'password',
            'status',
            'company_code',
            'partner_code',      # 🔥 ADD THIS
            'associate_code'     # 🔥 ADD THIS
        ]

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Countries
        fields = '__all__' 

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Cities
        fields = '__all__'

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = States
        fields = '__all__' 

class CustomerFollowupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerFollowup
        fields = '__all__'  

class AssociateSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Associates
        fields = '__all__' 

class CinemaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CinemaList
        fields = '__all__'
        
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__' 

# class MasterCinemaSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MasterCinema
#         fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class CouponSerializer(serializers.ModelSerializer):
    # Ensure these always return strings to the frontend
    customer_name = serializers.SerializerMethodField()

    class Meta:
        model = Coupens
        fields = '__all__'

    def get_customer_name(self, obj):
        # Prevent "can't convert to string" by providing a fallback
        customer = Customer.objects.filter(customer_code=obj.customer_code).first()
        return str(customer.name) if customer else "No Customer"
    
class MoviesliderImageSerializer(serializers.ModelSerializer):
    image_src = serializers.SerializerMethodField()

    class Meta:
        model = MoviesliderImage
        fields = '__all__'

    def get_image_src(self, obj):
        try:
            if obj.image:
                binary_data = obj.image.tobytes() if hasattr(obj.image, 'tobytes') else obj.image
                b64 = base64.b64encode(binary_data).decode('utf-8')
                mime_type = getattr(obj, 'image_type', 'image/jpeg')  # Default to jpeg if no image_type
                return f"data:{mime_type};base64,{b64}"
        except Exception:
            return None
        return None
    
class CouponRequestSerializer(serializers.ModelSerializer):
    contact_number = serializers.SerializerMethodField()
    class Meta:
        model = CoupenRequest
        fields = "__all__"

    def get_contact_number(self, obj):
        try:
            customer = Customer.objects.get(customer_code=obj.customer_code)
            return customer.contact_number
        except:
            return None

import base64
from rest_framework import serializers
from .models import TopBrands
 
class TopBrandsSerializer(serializers.ModelSerializer):
 
    image_src = serializers.SerializerMethodField()
 
    class Meta:
        model = TopBrands
        fields = "__all__"
 
    def get_image_src(self, obj):
        try:
            if obj.img:
 
                binary_data = obj.img.tobytes() if hasattr(obj.img, "tobytes") else obj.img
 
                b64 = base64.b64encode(binary_data).decode("utf-8")
 
                return f"data:image/jpeg;base64,{b64}"
 
        except Exception as e:
            print("IMAGE ERROR:", e)
            return None
 
        return None
 
import base64
from rest_framework import serializers
from .models import Partner
 
class PartnerSerializer(serializers.ModelSerializer):
 
    logo_src = serializers.SerializerMethodField()
 
    class Meta:
        model = Partner
        fields = "__all__"
 
    def get_logo_src(self, obj):
        try:
            if obj.logo:
                b64 = base64.b64encode(obj.logo).decode("utf-8")
                return f"data:image/jpeg;base64,{b64}"
        except Exception as e:
            print("LOGO ERROR:", e)
 
        return None
   

class PartnerBankDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnerBankDetails
        fields = '__all__'

class CustomerQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Query
        fields = '__all__'

class ScreenlistingNewSerializer(serializers.ModelSerializer):
    # Add this field
    rate_per_show = serializers.SerializerMethodField()

    class Meta:
        model = ScreenlistingNew
        fields = '__all__' 

    def get_rate_per_show(self, obj):
        # Logic: Base Rate / 28
        if obj.base_rate_per_seconds_perweeks:
            try:
                # Dividing the value and rounding to 2 decimal places
                return round(float(obj.base_rate_per_seconds_perweeks) / 28, 2)
            except (ValueError, TypeError):
                return 0
        return 0
    
class WeeksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weeks
        fields = ['id', 'week_value']

class AdlengthsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adlengths
        fields = ['id', 'length_value']

class UsertypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usertype
        fields = '__all__'

class PartnerScreenlistingSerializer(serializers.ModelSerializer):
    rate_per_show = serializers.SerializerMethodField()

    class Meta:
        model = ScreenlistingNew
        fields = '__all__'

    def get_rate_per_show(self, obj):
        if obj.base_rate_per_seconds_perweeks:
            try:
                return round(float(obj.base_rate_per_seconds_perweeks) / 28, 2)
            except (ValueError, TypeError):
                return 0
        return 0
    
class PartnerCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnerCustomerCartItem
        fields = "__all__"

class GenerateOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = Generateotp
        fields = '__all__' 

from rest_framework import serializers
from .models import BookCampaign


class BookCampaignSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    campaign_status = serializers.SerializerMethodField()
    payment_status = serializers.SerializerMethodField()

    class Meta:
        model = BookCampaign
        fields = '__all__'

    def get_name(self, obj):
        customer_map = self.context.get('customer_map', {})
        return customer_map.get(obj.customer_code)

    def get_campaign_status(self, obj):
        # Convert numeric campaign_status to text labels
        status_map = {
            '0': 'Pending',
            '1': 'Approved',
            '2': 'Rejected',
            '3': 'Booked'
        }
        return status_map.get(str(obj.campaign_status), obj.campaign_status)

    def get_payment_status(self, obj):
        # Convert numeric payment_status to text labels
        payment_status_map = {
            '0': 'Paid',
            '1': 'Partially Paid',
            '2': 'Unpaid',
            '3': 'Pending'
        }
        return payment_status_map.get(str(obj.payment_status), obj.payment_status)


