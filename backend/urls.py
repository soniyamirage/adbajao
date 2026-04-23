from django.urls import path
from django.views.generic import RedirectView
from .views import *
from .api_view import *

urlpatterns = [
    # root path serves as a simple redirect or health check; avoids 404 when hitting '/'
    path('', RedirectView.as_view(url='/api/', permanent=False)),

    path('api/', getRoutes), 
    
    path("api/admin-login/", LoginView.as_view(), name="admin-login"),
    path("api/admin-register/", RegisterView.as_view(), name="admin-register"),
    path('api/forgot-password/', RequestOTPView.as_view(), name='forgot-password'),
    path('api/reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    
    
    path('api/settings/', SettingsListView.as_view(), name='settings-list'),
    path('api/settings/create/', SettingsCreateView.as_view(), name='settings-create'),
    path('api/settings/<int:setting_id>/', SettingsDetailView.as_view(), name='settings-detail'),
    path('api/settings/update/<int:setting_id>/', SettingsUpdateView.as_view(), name='settings-update'),
    path('api/settings/delete/<int:setting_id>/', SettingsDeleteView.as_view(), name='settings-delete'),
    
    # path("api/engine-module/", EngineModuleListView.as_view()),
    # path("api/engine-module/create/", EngineModuleCreateView.as_view()),
    # path("api/engine-module/<str:module_code>/", EngineModuleDetailView.as_view()),
    # path("api/engine-module/update/<str:module_code>/", EngineModuleUpdateView.as_view()),
    # path("api/engine-module/delete/<str:module_code>/", EngineModuleDeleteView.as_view()),

    path("api/engine-submodule/", EngineSubmoduleListView.as_view()),
    path("api/engine-submodule/create/", EngineSubmoduleCreateView.as_view()),      
    path("api/engine-submodule/<int:id>/", EngineSubmoduleDetailView.as_view()),
    path("api/engine-submodule/update/<int:id>/", EngineSubmoduleUpdateView.as_view()),
    path("api/engine-submodule/delete/<int:pk>/", EngineSubmoduleDeleteView.as_view()),

    path("api/engine-activity/", EngineActivityListView.as_view()),
    path("api/engine-activity/create/", EngineActivityCreateView.as_view()),     
    path("api/engine-activity/<int:id>/", EngineActivityDetailView.as_view()),
    path("api/engine-activity/update/<int:id>/", EngineActivityUpdateView.as_view()),
    path("api/engine-activity/delete/<int:id>/", EngineActivityDeleteView.as_view()),

    path("api/engine-module/", EngineModuleListView.as_view()),
    path("api/engine-module/create/", EngineModuleCreateView.as_view()),
    path("api/engine-module/<int:id>/", EngineModuleDetailView.as_view()),
    path("api/engine-module/update/<int:id>/", EngineModuleUpdateView.as_view()),
    path("api/engine-module/delete/<int:pk>/", EngineModuleDeleteView.as_view()),

    # Dynamic Sidebar Menu
    path("api/sidebar-menu/", SidebarMenuView.as_view(), name='sidebar-menu'),
    path("api/usertypes/", UserTypeListView.as_view()),

    path('api/clients/', ClientListView.as_view(), name='client-list'),
    path('api/clients/create/', ClientCreateView.as_view(), name='client-create'),
    path('api/clients/<str:customer_code>/', ClientDetailView.as_view(), name='client-detail'),
    path('api/clients/update/<str:customer_code>/', ClientUpdateView.as_view(), name='client-update'),
    path('api/clients/delete/<str:customer_code>/', ClientDeleteView.as_view(), name='client-delete'),

    path('api/coupons/list/', CouponListView.as_view(), name='coupon-list'),
    path('api/coupons/create/', CouponCreateView.as_view(), name='coupon-create'),
    path('api/coupons/generate/', CouponGenerateCodeView.as_view(), name='coupon-generate'),
    path('api/coupons/validate/<str:coupon_code>/', CouponValidateView.as_view(), name='coupon-validate'),
    path('api/coupons/update/<int:pk>/', CouponUpdateView.as_view(), name='coupon-update'),
    path('api/coupons/delete/', CouponDeleteView.as_view(), name='coupon-delete'),

    path('api/countries/create/', CountryCreateView.as_view()),
    path('api/countries/', CountryListView.as_view()),
    path('api/countries/<str:country_code>/', CountryDetailView.as_view()), 
    path('api/countries/update/<str:country_code>/', CountryUpdateView.as_view()), 
    path('api/countries/delete/<str:country_code>/', CountryDeleteView.as_view()),  

    path('api/cities/create/', CityCreateView.as_view()),
    path('api/cities/', CityListView.as_view()),
    path('api/cities/state/<str:state_code>/', CityByStateView.as_view()),  # ⭐ IMPORTANT
    path('api/cities/<str:city_code>/', CityDetailView.as_view()),
    path('api/cities/update/<str:city_code>/', CityUpdateView.as_view()),
    path('api/cities/delete/<str:city_code>/', CityDeleteView.as_view()),

    path('api/states/create/', StateCreateView.as_view()),
    path('api/states/', StateListView.as_view()),
    path('api/states/country/<str:country_code>/', StateByCountryView.as_view()),  # ⭐
    path('api/states/<str:state_code>/', StateDetailView.as_view()),
    path('api/states/update/<str:state_code>/', StateUpdateView.as_view()),
    path('api/states/delete/<str:state_code>/', StateDeleteView.as_view()),

    path('api/dropdown/modules/', ModuleDropdownView.as_view(), name='dropdown-modules'),  
    path('api/dropdown/urls/', UrlDropdownView.as_view(), name='dropdown-urls'), 

    path('api/followups/', ClientFollowupListView.as_view(), name='followup-list'),
    path('api/followups/create/', ClientFollowupCreateView.as_view(), name='followup-create'),
    path('api/followups/<int:id>/', ClientFollowupDetailView.as_view(), name='followup-detail'),
    path('api/followups/update/<int:id>/', ClientFollowupUpdateView.as_view(), name='followup-update'),
    path('api/followups/delete/<int:id>/', ClientFollowupDeleteView.as_view(), name='followup-delete'),

    path('api/associates/', AssociateListCreateView.as_view(), name='associate-list-create'),
    path('api/associates/<int:id>/', AssociateDetailView.as_view(), name='associate-detail'),
    path('api/cities/', CityListView.as_view(), name='city-list'),

    path('api/users/', UserListCreateView.as_view(), name='user-list-create'),
    path('api/users/<int:pk>/', UserDetailView.as_view(), name='user-detail'), 
    path('api/profile/', UserProfileView.as_view(), name='user-profile'),

    path('api/cinema/create/', CinemaCreateView.as_view(), name='cinema-create'),
    path('api/cinema/mysql/list/', CinemaListView.as_view(), name='cinema-list'),
    path('api/cinema/mysql/details/<int:id>/', CinemaDetailView.as_view(), name='cinema-detail'), 
    path('api/cinema/update/<int:id>/', CinemaUpdateView.as_view(), name='cinema-update'),
    path('api/cinema/delete/<int:id>/', CinemaDeleteView.as_view(), name='cinema-delete'),
    path('api/cinema/mysql/list/', CinemaListView.as_view(), name='cinema-list'),
    path('api/cinema/mysql/filters/', CinemaFilterOptionsView.as_view(), name='cinema-filters'),
    path('api/cinema/mysql/<int:id>/', CinemaDetailView.as_view(), name='cinema-detail'),

    path('api/contact/', ContactCreateView.as_view(), name='contact-create'),

    # path('api/master-cinemas/', CinemaListAPI.as_view(), name='api_cinema_list'),
    # path('api/master-cinemas/<int:pk>/', CinemaDetailAPI.as_view(), name='api_cinema_detail'),

    path('api/cart/add/', CartAddView.as_view(), name='cart-add'),
    path('api/cart/process/', CartProcessView.as_view(), name='cart-process'),    
    path('api/cart/count/', CartCountView.as_view(), name='cart-count'),
    path('api/cart/delete/', CartDeleteItemsView.as_view(), name='cart-delete'),
    path('api/weeks/', WeeksListView.as_view(), name='weeks-list'),
    path('api/adlengths/', AdlengthsListView.as_view(), name='adlengths-list'),


    path('api/coupons/update/<int:pk>/',CouponUpdateView.as_view(), name='coupon-update'),
    path('api/coupons/delete/',CouponDeleteView.as_view(), name='coupon-delete'),
    path('api/coupons/list/', CouponListView.as_view(), name='coupon-list'),
    path('api/coupons/create/', CouponCreateView.as_view(), name='coupon-create'),
    path('api/coupons/generate/', CouponGenerateCodeView.as_view(), name='coupon-generate'),

    path('api/movieslider/', MovieSliderListView.as_view(), name='movieslider-list'),
    path('api/movieslider/create/', MovieSliderCreateView.as_view(), name='movieslider-create'),
    path('api/movieslider/update/<int:id>/', MovieSliderUpdateView.as_view(), name='movieslider-update'),
    path('api/movieslider/delete/', MovieSliderDeleteView.as_view(), name='movieslider-delete'),

    path('api/couponrequest/', CouponRequestListView.as_view()),
    path('api/couponrequest/create/', CouponRequestCreateView.as_view()),
    path('api/couponrequest/<int:id>/', CouponRequestDetailView.as_view()),
    path('api/couponrequest/update/<int:id>/', CouponRequestUpdateView.as_view()),
    path('api/couponrequest/delete/<int:id>/', CouponRequestDeleteView.as_view()),

    path('api/topbrands/', TopBrandsListView.as_view()),
    path('api/topbrands/create/', TopBrandsCreateView.as_view()),
    path('api/topbrands/update/<int:id>/', TopBrandsUpdateView.as_view()),
    path('api/topbrands/delete/', TopBrandsDeleteView.as_view()), 

    path('api/partner/', PartnerListView.as_view()),
    path('api/partner/create/', PartnerCreateView.as_view()),
    path('api/partner/<int:id>/', PartnerDetailView.as_view()),
    path('api/partner/update/<int:id>/', PartnerUpdateView.as_view()),
    path('api/partner/delete/<int:id>/', PartnerDeleteView.as_view()),

    path('api/partnerbankdetails/', PartnerBankDetailsListView.as_view()),

    # BookCampaign Routes
    path('api/BookCampaigns/', BookCampaignListView.as_view(), name='bookcampaign-list'),
    path('api/BookCampaigns/<int:id>/', BookCampaignDetailView.as_view(), name='bookcampaign-detail'),
    path('api/BookCampaigns/ro/<int:campaign_code>/download/', ro, name='download-ro'),
    
    path('api/partnerbankdetails/<int:id>/', PartnerBankDetailsDetailView.as_view()),
    path('api/partnerbankdetails/create/',PartnerBankDetailsCreateView.as_view()),
    path('api/partnerbankdetails/update/<int:id>/',PartnerBankDetailsUpdateView.as_view()),
    path('api/partnerbankdetails/delete/<int:id>/',PartnerBankDetailsDeleteView.as_view()),

    path("api/customerquery/", CustomerQueryListView.as_view()),
    path("api/customerquery/create/", CustomerQueryCreateView.as_view()),
    path("api/customerquery/<int:id>/", CustomerQueryDetailView.as_view()),
    path("api/customerquery/update/<int:id>/", CustomerQueryUpdateView.as_view()),
    path("api/customerquery/delete/<int:id>/", CustomerQueryDeleteView.as_view()),

    path("api/cart/quotation/", generate_quotation_api),
    path('api/p_plan_campaign/', PartnerCinemaListView.as_view(), name='partner-campaign'),
    path('api/p_plan_campaign/filters/', PartnerCinemaFilterOptionsView.as_view(), name='partner-filters'),
     
    path('api/partner-cart/add/', PartnerCartAddView.as_view()),
    path('api/partner-cart/process/', PartnerCartProcessView.as_view()),
    path('api/partner-cart/delete/', PartnerCartDeleteView.as_view()),
    path('api/partner-cart/count/', PartnerCartCountView.as_view()),
    path('api/partner-cart/items/', PartnerCartItemsView.as_view(), name="partner-cart-items"),

    path("api/partner-cart/quotation/", generate_partner_quotation_api),
    path('api/otp/send/', SendOTPView.as_view(), name='send-otp'),
    path('api/otp/verify/', VerifyOTPView.as_view(), name='verify-otp'),
    path('api/payment/initiate/', InitiatePaymentView.as_view(), name='initiate_payment'),
    path('api/payment/verify/', VerifyPaymentView.as_view(), name='api-payment-verify'),
    # path('api/payment-statuses/', PaymentStatusListView.as_view(), name='payment-statuses'),
    # path('api/offline-payment-modes/', OfflinePaymentModesListView.as_view(), name='offline-payment-modes'),
   
    path("BookCampaigns/<int:id>/", BookCampaignDetailView.as_view()),

    path('api/dashboard-stats/', dashboard_stats),
    
]






