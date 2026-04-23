from django.db import models

# Create your models here.

class Company(models.Model):
    company_code = models.CharField(unique=True, max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)
    company_name = models.CharField(max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)
    company_address = models.CharField(max_length=256, db_collation='latin1_swedish_ci', blank=True, null=True)
    company_email = models.CharField(max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)
    company_phone = models.CharField(max_length=15, db_collation='latin1_swedish_ci', blank=True, null=True)
    company_mobile = models.CharField(max_length=15, db_collation='latin1_swedish_ci', blank=True, null=True)
    company_fax = models.CharField(max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)
    company_contactperson = models.CharField(max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)
    company_country = models.CharField(max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)
    company_state = models.CharField(max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)
    company_currency = models.CharField(max_length=60, db_collation='latin1_swedish_ci', blank=True, null=True)
    company_registrationnumber = models.CharField(db_column='company_registrationNumber', max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    company_gstnumber = models.CharField(db_column='company_GSTNumber', unique=True, max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    company_timezone = models.CharField(max_length=60, db_collation='latin1_swedish_ci', blank=True, null=True)
    company_logo = models.CharField(max_length=60, db_collation='latin1_swedish_ci', blank=True, null=True)
    createdon = models.DateTimeField(blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    updatedon = models.DateTimeField(blank=True, null=True)
    updatedby = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company'
        
class Financialyear(models.Model):
    financialyear_id = models.IntegerField(unique=True, blank=True, null=True)
    financialyear_startyear = models.CharField(max_length=45, blank=True, null=True)
    financialyear_endyear = models.CharField(max_length=45, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'financialyear' 


class Users(models.Model):
    user_id = models.IntegerField(unique=True, blank=True, null=True)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    activkey = models.CharField(max_length=128, blank=True, null=True)
    superuser = models.IntegerField()
    status = models.IntegerField()
    usertype = models.ForeignKey('Usertype', models.DO_NOTHING, to_field='usertype_id', blank=True, null=True)
    employee_code = models.ForeignKey('Employee', models.DO_NOTHING, db_column='employee_code', to_field='employee_code', blank=True, null=True)
    customer_code = models.CharField(max_length=45, blank=True, null=True)
    company_code = models.CharField(max_length=45, blank=True, null=True)
    partner_code = models.CharField(max_length=45, blank=True, null=True)
    associate_code = models.IntegerField(blank=True, null=True)
    createdon = models.DateTimeField(blank=True, null=True)
    updatedon = models.DateTimeField(blank=True, null=True)
    lastvisiton = models.DateTimeField(blank=True, null=True)
    otp_code = models.CharField(max_length=6, blank=True, null=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
        
class Usertype(models.Model):
    usertype_id = models.IntegerField(unique=True, blank=True, null=True)
    usertype_name = models.CharField(max_length=45, blank=True, null=True)
    company_code = models.CharField(max_length=45, blank=True, null=True)
    createdon = models.DateTimeField(blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    updatedon = models.DateTimeField(blank=True, null=True)
    updatedby = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usertype'
        
 
class Employee(models.Model):
    employee_code = models.CharField(unique=True, max_length=45, blank=True, null=True)
    company_code = models.ForeignKey('Company', models.DO_NOTHING, db_column='company_code', to_field='company_code', blank=True, null=True)
    employee_firstname = models.CharField(max_length=45, blank=True, null=True)
    employee_middlename = models.CharField(max_length=45, blank=True, null=True)
    employee_lastname = models.CharField(max_length=45, blank=True, null=True)
    employee_joiningdate = models.DateField(blank=True, null=True)
    employee_qualification = models.CharField(max_length=45, blank=True, null=True)
    employee_totalexperiance = models.CharField(max_length=45, blank=True, null=True)
    financialyear_id = models.IntegerField(blank=True, null=True)
    department_code = models.CharField(max_length=45, blank=True, null=True)
    designation_id = models.IntegerField(blank=True, null=True)
    usertype_id = models.IntegerField(blank=True, null=True)
    division_code = models.CharField(max_length=45, blank=True, null=True)
    employee_dob = models.DateField(blank=True, null=True)
    employee_gender = models.CharField(max_length=10, blank=True, null=True, db_comment='1=>Male,2=>Female')
    employee_address1 = models.CharField(max_length=256, blank=True, null=True)
    employee_address2 = models.CharField(max_length=256, blank=True, null=True)
    employee_country = models.CharField(max_length=45, blank=True, null=True)
    employee_state = models.CharField(max_length=45, blank=True, null=True)
    employee_city = models.CharField(max_length=45, blank=True, null=True)
    employee_pincode = models.CharField(max_length=45, blank=True, null=True)
    employee_phone = models.CharField(max_length=15, blank=True, null=True)
    employee_mobile = models.CharField(max_length=15, blank=True, null=True)
    employee_email = models.CharField(max_length=45, blank=True, null=True)
    employee_photo = models.CharField(max_length=45, blank=True, null=True)
    employee_status = models.CharField(max_length=45, blank=True, null=True, db_comment='1=>existing,2=>resigned,3=>terminated')
    contact_id = models.IntegerField(blank=True, null=True)
    termination_date = models.DateField(blank=True, null=True)
    termination_reason = models.CharField(max_length=256, blank=True, null=True)
    createdon = models.DateTimeField(blank=True, null=True)
    createdby = models.ForeignKey('Users', models.DO_NOTHING, db_column='createdby', to_field='user_id', blank=True, null=True)
    updatedon = models.DateTimeField(blank=True, null=True)
    updatedby = models.ForeignKey('Users', models.DO_NOTHING, db_column='updatedby', to_field='user_id', related_name='employee_updatedby_set', blank=True, null=True)
 
    class Meta:
        managed = False
        db_table = 'employee'
 
 
class Permissions(models.Model):
    usertype_id = models.IntegerField(blank=True, null=True)
    module_id = models.IntegerField(blank=True, null=True)
    submodule_id = models.IntegerField(blank=True, null=True)
    activity_id = models.IntegerField(blank=True, null=True)
    e_read = models.CharField(max_length=10, blank=True, null=True)
    e_write = models.CharField(max_length=10, blank=True, null=True)
    e_update = models.CharField(max_length=10, blank=True, null=True)
 
    class Meta:
        managed = False
        db_table = 'permissions'
 
        
class Settings(models.Model):
    setting_id = models.IntegerField(blank=True, null=True)
    setting_name = models.CharField(max_length=100, blank=True, null=True)
    module_code = models.CharField(max_length=45, blank=True, null=True)
    submodule_code = models.CharField(max_length=45, blank=True, null=True)
    activity_code = models.CharField(max_length=45, blank=True, null=True)
    setting_value = models.CharField(max_length=45, blank=True, null=True)
    setting_value2 = models.CharField(max_length=255, blank=True, null=True)
    used_for = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'settings'
        
# class EngineModule(models.Model):
#     module_code = models.CharField(max_length=20)
#     module_name = models.CharField(max_length=60, blank=True, null=True)
#     url = models.CharField(max_length=60, blank=True, null=True)
#     icon = models.CharField(max_length=1000, blank=True, null=True)
#     status = models.IntegerField(blank=True, null=True)
#     created_on = models.DateTimeField(blank=True, null=True)
#     created_by = models.IntegerField(blank=True, null=True)
#     updated_on = models.DateTimeField(blank=True, null=True)
#     updated_by = models.IntegerField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'engine_module'


class EngineModule(models.Model):
    # id = models.IntegerField(primary_key=True)
    modulename = models.CharField(db_column='ModuleName', max_length=60, blank=True, null=True)  # Field name made lowercase.
    url = models.CharField(max_length=60, blank=True, null=True)
    icon = models.CharField(max_length=1000, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    sequence = models.CharField(max_length=45, blank=True, null=True)
 
    class Meta:
        managed = False
        db_table = 'engine_module'
 
        
class EngineSubmodule(models.Model):
    module_id = models.IntegerField(db_column='Module_Id', blank=True, null=True)
    submodule_name = models.CharField(db_column='SubModuleName', max_length=60, blank=True, null=True)
    url = models.CharField(max_length=60, blank=True, null=True)
    icon = models.CharField(max_length=600, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'engine_submodule'
        
        
class EngineActivity(models.Model):
    activity_name = models.CharField(db_column='ActivityName', max_length=60, blank=True, null=True)
    module_id = models.IntegerField(db_column='Module_Id', blank=True, null=True)
    submodule_id = models.IntegerField(db_column='SubModule_Id', blank=True, null=True)
    url = models.CharField(max_length=60, blank=True, null=True)
    icon = models.CharField(max_length=600, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'engine_activity'


class Customer(models.Model):
    customer_code = models.CharField(max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)
    associate_code = models.IntegerField(blank=True, null=True)
    partner_code = models.CharField(max_length=45, blank=True, null=True)
    company_code = models.CharField(max_length=45, blank=True, null=True)
    name = models.CharField(max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)
    email_id = models.CharField(max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)
    password = models.CharField(max_length=128, db_collation='utf8mb3_general_ci') 
    company_contactperson = models.CharField(max_length=45, blank=True, null=True)
    status = models.CharField(max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)
    contact_number = models.CharField(max_length=15, db_collation='latin1_swedish_ci', blank=True, null=True)
    address = models.CharField(max_length=256, db_collation='latin1_swedish_ci', blank=True, null=True)
    city_code = models.CharField(max_length=45, blank=True, null=True)
    state = models.CharField(max_length=45, blank=True, null=True)
    country_code = models.CharField(max_length=45, blank=True, null=True)
    gstin = models.CharField(max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)
    pincode = models.TextField(blank=True, null=True)
    referral_code = models.TextField(db_column='Referral_code', blank=True, null=True)  # Field name made lowercase.
    refferral_status = models.IntegerField(db_column='Refferral_status', blank=True, null=True)  # Field name made lowercase.
    desigation = models.TextField(blank=True, null=True)
    images = models.TextField(blank=True, null=True)
    createdon = models.DateTimeField(blank=True, null=True)
    createdby = models.ForeignKey('Users', models.DO_NOTHING, db_column='createdby', blank=True, null=True)
    updatedon = models.DateTimeField(blank=True, null=True) 
    updatedby = models.ForeignKey('Users', models.DO_NOTHING, db_column='updatedby', related_name='customer_updatedby_set', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer' 

class Countries(models.Model):
    country_code = models.CharField(unique=True, max_length=45, blank=True, null=True)
    country_name = models.CharField(max_length=255)
    createdon = models.DateTimeField(blank=True, null=True)
    createdby = models.ForeignKey('Users', models.DO_NOTHING, db_column='createdby', to_field='user_id', blank=True, null=True)
    updatedon = models.DateTimeField(blank=True, null=True)
    updatedby = models.ForeignKey('Users', models.DO_NOTHING, db_column='updatedby', to_field='user_id', related_name='countries_updatedby_set', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'countries' 

class Cities(models.Model):
    city_code = models.CharField(unique=True, max_length=45, blank=True, null=True)
    city_name = models.CharField(max_length=255)
    state_code = models.CharField(max_length=45)
    createdon = models.DateTimeField(blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True) 
    updatedon = models.DateTimeField(blank=True, null=True)
    updatedby = models.IntegerField(blank=True, null=True) 

    class Meta:
        managed = False
        db_table = 'cities'  

class States(models.Model):
    state_code = models.CharField(unique=True, max_length=45, blank=True, null=True)
    state_name = models.CharField(max_length=255)
    country_code = models.CharField(max_length=255)
    createdon = models.DateTimeField(blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    updatedon = models.DateTimeField(blank=True, null=True)
    updatedby = models.IntegerField(blank=True, null=True) 

    class Meta:
        managed = False
        db_table = 'states'

class CustomerFollowup(models.Model):
    follow_up_id = models.IntegerField(blank=True, null=True)
    associate_code = models.IntegerField(blank=True, null=True)
    customer_code = models.CharField(max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)
    contact_no = models.TextField(db_collation='utf8mb3_unicode_ci')
    visit_for = models.TextField(db_collation='utf8mb3_unicode_ci')
    follow_up_type = models.TextField(db_collation='utf8mb3_unicode_ci')
    customer_status = models.TextField(db_collation='utf8mb3_unicode_ci', blank=True, null=True)
    next_follow_up_date = models.DateField(blank=True, null=True)
    type = models.TextField(db_collation='utf8mb3_unicode_ci', blank=True, null=True)
    note = models.TextField(db_collation='utf8mb3_unicode_ci', blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    partner_code = models.CharField(max_length=45, blank=True, null=True)
    associate_name = models.CharField(max_length=255, blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    createdon = models.DateTimeField(blank=True, null=True)
    createdby = models.ForeignKey('Users', models.DO_NOTHING, db_column='createdby', blank=True, null=True)
    updatedon = models.DateTimeField(blank=True, null=True) 
    updatedby = models.ForeignKey('Users', models.DO_NOTHING, db_column='updatedby', related_name='customerfollowup_updatedby_set', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer_followup' 

#customer query page model / client query page model 
class Query(models.Model):
    customer_code = models.CharField(max_length=45, blank=True, null=True)      
    email = models.CharField(max_length=45, blank=True, null=True)
    contact_number = models.CharField(max_length=45, blank=True, null=True)    
    name = models.CharField(max_length=45, blank=True, null=True)
    query_type = models.CharField(max_length=45, blank=True, null=True)
    query_details = models.CharField(max_length=45, blank=True, null=True)      
    date = models.DateTimeField(blank=True, null=True)
    query_status = models.CharField(max_length=45, blank=True, null=True)      
    createdon = models.DateTimeField(blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    updatedon = models.DateTimeField(blank=True, null=True)
    updatedby = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'query'

class Associates(models.Model):
    associate_code = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(unique=True, max_length=255)
    date = models.DateField(blank=True, null=True)
    password = models.CharField(max_length=255)
    mobile_no = models.BigIntegerField(blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True) 
    status = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True) 
    user_id = models.IntegerField(blank=True, null=True)  
    createdon = models.DateTimeField(blank=True, null=True) 
    createdby = models.ForeignKey('Users', models.DO_NOTHING, db_column='createdby', blank=True, null=True)
    updatedon = models.DateTimeField(blank=True, null=True)
    updatedby = models.ForeignKey('Users', models.DO_NOTHING, db_column='updatedby', related_name='associates_updatedby_set', blank=True, null=True)
    username = models.CharField(max_length=20, blank=True, null=True)
    month = models.CharField(max_length=45, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'associates'


class CinemalistMysql(models.Model):
    sr_field = models.CharField(db_column='Sr#', max_length=255, db_collation='utf8mb3_general_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    web_code = models.CharField(db_column='Web_Code', max_length=255, db_collation='utf8mb3_general_ci', blank=True, null=True)  # Field name made lowercase.
    projection = models.CharField(db_column='Projection', max_length=255, db_collation='utf8mb3_general_ci', blank=True, null=True)  # Field name made lowercase.
    theater_name = models.CharField(db_column='Theater Name', max_length=255, db_collation='utf8mb3_general_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    theater_address = models.CharField(db_column='Theater Address', max_length=255, db_collation='utf8mb3_general_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    city = models.CharField(db_column='City', max_length=255, db_collation='utf8mb3_general_ci', blank=True, null=True)  # Field name made lowercase.
    district = models.CharField(db_column='District', max_length=255, db_collation='utf8mb3_general_ci', blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=255, db_collation='utf8mb3_general_ci', blank=True, null=True)  # Field name made lowercase.
    seating_capacity = models.FloatField(db_column='Seating_Capacity', blank=True, null=True)  # Field name made lowercase.
    cinema_category = models.CharField(db_column='Cinema_Category', max_length=255, db_collation='utf8mb3_general_ci', blank=True, null=True)  # Field name made lowercase.
    grade = models.CharField(db_column='Grade', max_length=255, db_collation='utf8mb3_general_ci', blank=True, null=True)  # Field name made lowercase.
    rate = models.FloatField(db_column='Rate', blank=True, null=True)  # Field name made lowercase.
    image = models.CharField(db_column='Image', max_length=255, db_collation='utf8mb3_general_ci', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cinemalist_mysql'


class CinemaList(models.Model):
    web_code = models.CharField(max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)
    projection = models.CharField(max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)
    theater_name = models.CharField(max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)
    theater_address = models.CharField(max_length=256, db_collation='latin1_swedish_ci', blank=True, null=True)
    city_code = models.CharField(max_length=45, blank=True, null=True)
    district_code = models.CharField(max_length=45, blank=True, null=True)
    state_code = models.CharField(max_length=45, blank=True, null=True) 
    seating_capacity = models.IntegerField(db_column='Seating_Capacity', blank=True, null=True)  # Field name made lowercase.
    cinema_type = models.CharField(max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)
    cinema_category = models.CharField(max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)
    rate = models.IntegerField(db_column='Rate', blank=True, null=True)  # Field name made lowercase.
    image = models.CharField(db_column='Image', max_length=255, blank=True, null=True)  # Field name made lowercase.
    createdon = models.DateTimeField(blank=True, null=True)
    createdby = models.ForeignKey('Users', models.DO_NOTHING, db_column='createdby', blank=True, null=True)
    updatedon = models.DateTimeField(blank=True, null=True)
    updatedby = models.ForeignKey('Users', models.DO_NOTHING, db_column='updatedby', related_name='cinemalist_updatedby_set', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cinema_list'




class MasterCinema(models.Model):
    web_code = models.TextField(blank=True, null=True)
    projection = models.CharField(max_length=100, blank=True, null=True)
    cinema_chain = models.CharField(max_length=200, blank=True, null=True)
    theatre_name = models.CharField(max_length=100, blank=True, null=True)
    theatre_address = models.CharField(max_length=500, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    district = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    seating_capacity = models.CharField(max_length=50, blank=True, null=True)
    cinema_type = models.CharField(max_length=20, blank=True, null=True)
    cinema_category = models.CharField(max_length=20, blank=True, null=True)
    image = models.CharField(db_column='Image', max_length=250, blank=True, null=True)  # Field name made lowercase.  
    rate_10sec_week = models.IntegerField(blank=True, null=True)
    rate_per_sec_per_week = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'master_cinema'


class Cart(models.Model):
    cart_id = models.IntegerField(unique=True, blank=True, null=True)
    p_id = models.CharField(max_length=45)
    web_code = models.CharField(max_length=45, blank=True, null=True)
    media_name = models.CharField(max_length=500)
    theatre_address = models.CharField(max_length=500)
    img = models.CharField(max_length=200)
    seats_number = models.CharField(max_length=45)
    projection = models.CharField(max_length=45)
    rate = models.FloatField() 
    customer_id = models.CharField(max_length=45)
    date = models.DateField() 
    city = models.CharField(max_length=45)
    district = models.CharField(max_length=45)
    state = models.CharField(max_length=45)
    campaign_category = models.CharField(max_length=45)
    associate_code = models.IntegerField(blank=True, null=True)
    base_rate_10secweek = models.IntegerField(blank=True, null=True)
    bb_rate_10secweek = models.IntegerField(blank=True, null=True)
    base_rate_10secweek_0 = models.IntegerField(blank=True, null=True)
    bb_rate_10secweek_0 = models.IntegerField(blank=True, null=True)
    rate_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cart' 


class Contact(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField()
    created_on = models.DateTimeField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contact'


class Coupens(models.Model):
    coupen_code = models.CharField(max_length=50, unique=True)
    discount = models.FloatField()
    expire_date = models.DateField(blank=True, null=True)
    coupen_status = models.CharField(max_length=20, default='unused')

    class Meta:
        managed = False
        db_table = 'coupens'

class BookCampaign(models.Model):
    campaign_code = models.IntegerField(blank=True, null=True)
    associate_code = models.IntegerField(blank=True, null=True)
    partner_code = models.CharField(max_length=45, blank=True, null=True)
    screen_number = models.IntegerField(blank=True, null=True)
    media_name = models.TextField(blank=True, null=True)
    projection = models.TextField(blank=True, null=True)
    number_seats = models.IntegerField(blank=True, null=True)
    city_code = models.CharField(max_length=45, blank=True, null=True)
    state_code = models.CharField(max_length=45, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    ads_in_second = models.IntegerField(blank=True, null=True)
    week = models.IntegerField(blank=True, null=True)
    ad_type = models.TextField(db_column='ad_Type', blank=True, null=True)  # Field name made lowercase.      
    ad_position = models.TextField(blank=True, null=True)
    total_sreen_rate = models.IntegerField(blank=True, null=True)
    gross_total = models.IntegerField(blank=True, null=True)
    discount = models.FloatField(blank=True, null=True)
    discount_total = models.IntegerField(blank=True, null=True)
    censor_certificate = models.TextField(blank=True, null=True)
    censor_cc = models.IntegerField(db_column='censor_CC', blank=True, null=True)  # Field name made lowercase.
    gst = models.FloatField(blank=True, null=True)
    total_taxable_amount = models.FloatField(blank=True, null=True)
    payment_mode = models.TextField(blank=True, null=True)
    payment_status = models.TextField(blank=True, null=True)
    coupon_code = models.TextField(blank=True, null=True)
    reference_code = models.TextField(blank=True, null=True)
    customize_id = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    campaign_status = models.TextField(blank=True, null=True)
    campaign_start_date = models.TextField(blank=True, null=True)
    campaign_end_date = models.TextField(blank=True, null=True)
    total_payable_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)        
    invoice = models.TextField(blank=True, null=True)
    remaining_amount = models.FloatField(blank=True, null=True)
    paid = models.CharField(max_length=45, blank=True, null=True)
    transaction_id_check_no = models.TextField(db_column='transaction_id/check_no', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    discount_percentage = models.IntegerField(blank=True, null=True)
    campaign_name = models.TextField(blank=True, null=True)
    booking_date = models.DateField(blank=True, null=True)
    customer_code = models.CharField(max_length=45, blank=True, null=True)
    campaign_category = models.TextField(blank=True, null=True)
    createdon = models.DateTimeField(blank=True, null=True)
    createdby = models.ForeignKey('Users', models.DO_NOTHING, db_column='createdby', blank=True, null=True)
    updatedon = models.DateTimeField(blank=True, null=True)
    updatedby = models.ForeignKey('Users', models.DO_NOTHING, db_column='updatedby', related_name='bookcampaign_updatedby_set', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'book_campaign'


class Coupens(models.Model):
    customer_code = models.CharField(max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)
    coupen_type = models.CharField(max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)
    coupen_code = models.CharField(max_length=45, blank=True, null=True)
    discount = models.FloatField(blank=True, null=True)
    expire_date = models.DateField(blank=True, null=True)
    coupen_status = models.CharField(max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)
    createdon = models.DateTimeField(blank=True, null=True)
    createdby = models.ForeignKey('Users', models.DO_NOTHING, db_column='createdby', blank=True, null=True)
    updatedon = models.DateTimeField(blank=True, null=True)
    updatedby = models.ForeignKey('Users', models.DO_NOTHING, db_column='updatedby', related_name='coupens_updatedby_set', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'coupens'

class CoupenRequest(models.Model):
    customer_code = models.CharField(max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)
    associate_code = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)
    contact_number = models.CharField(max_length=15, db_collation='latin1_swedish_ci', blank=True, null=True)
    coupen_discount = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    generate_coupen = models.CharField(max_length=15, db_collation='latin1_swedish_ci', blank=True, null=True)        
    createdon = models.DateTimeField(blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    updatedon = models.DateTimeField(blank=True, null=True)
    updatedby = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'coupen_request' 


class Customer(models.Model):
    customer_code = models.CharField(max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)
    associate_code = models.IntegerField(blank=True, null=True)
    partner_code = models.CharField(max_length=45, blank=True, null=True)
    company_code = models.CharField(max_length=45, blank=True, null=True)
    name = models.CharField(max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)
    email_id = models.CharField(max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)
    password = models.CharField(max_length=128, db_collation='utf8mb3_general_ci')
    company_contactperson = models.CharField(max_length=45, blank=True, null=True)
    status = models.CharField(max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)
    contact_number = models.CharField(max_length=15, db_collation='latin1_swedish_ci', blank=True, null=True)
    address = models.CharField(max_length=256, db_collation='latin1_swedish_ci', blank=True, null=True)
    city_code = models.CharField(max_length=45, blank=True, null=True)
    state = models.CharField(max_length=45, blank=True, null=True)
    country_code = models.CharField(max_length=45, blank=True, null=True)
    gstin = models.CharField(max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)
    pincode = models.TextField(blank=True, null=True)
    referral_code = models.TextField(db_column='Referral_code', blank=True, null=True)  # Field name made lowercase.  
    refferral_status = models.IntegerField(db_column='Refferral_status', blank=True, null=True)  # Field name made lowercase.
    desigation = models.TextField(blank=True, null=True)
    images = models.TextField(blank=True, null=True)
    createdon = models.DateTimeField(blank=True, null=True)
    createdby = models.ForeignKey('Users', models.DO_NOTHING, db_column='createdby', blank=True, null=True)
    updatedon = models.DateTimeField(blank=True, null=True)
    updatedby = models.ForeignKey('Users', models.DO_NOTHING, db_column='updatedby', related_name='customer_updatedby_set', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer'

class MoviesliderImage(models.Model):
    name = models.CharField(max_length=45, blank=True, null=True)
    image = models.BinaryField(blank=True, null=True)
    releasing_date = models.DateField(blank=True, null=True)
    createdon = models.DateTimeField(blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    updatedon = models.DateTimeField(blank=True, null=True)
    updatedby = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movieslider_image'

class CoupenRequest(models.Model):
    customer_code = models.CharField(max_length=45, db_collation='latin1_swedish_ci', blank=True, null=True)
    associate_code = models.IntegerField(blank=True, null=True)
    coupen_discount = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    generate_coupen = models.CharField(max_length=15, db_collation='latin1_swedish_ci', blank=True, null=True)
    createdon = models.DateTimeField(blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    updatedon = models.DateTimeField(blank=True, null=True)
    updatedby = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'coupen_request' 


class CustomerCart(models.Model):
    cart_id = models.CharField(db_column='cart_Id', max_length=45, blank=True, null=True) 
    customer_code = models.CharField(max_length=45, blank=True, null=True)
    createdon = models.DateTimeField(blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    updatedon = models.DateTimeField(blank=True, null=True)
    updatedby = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer_cart'

class CustomerCartItem(models.Model):
    customer_id = models.CharField(max_length=45, blank=True, null=True)
    cart_id = models.CharField(max_length=45, blank=True, null=True)
    screen_id = models.IntegerField(blank=True, null=True)
    media_name = models.CharField(max_length=500, blank=True, null=True)
    web_code = models.CharField(max_length=64, blank=True, null=True)
    city = models.CharField(max_length=45, blank=True, null=True)
    district = models.CharField(max_length=45, blank=True, null=True)
    state = models.CharField(max_length=45, blank=True, null=True)
    theatre_address = models.CharField(max_length=500, blank=True, null=True)
    img = models.CharField(max_length=200, blank=True, null=True)
    seats_number = models.IntegerField(blank=True, null=True)
    projection = models.CharField(max_length=45, blank=True, null=True)
    rate = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    base_rate_10secweek = models.IntegerField(blank=True, null=True)
    bb_rate_10secweek = models.IntegerField(blank=True, null=True)
    base_rate_10secweek_0 = models.IntegerField(blank=True, null=True)
    bb_rate_10secweek_0 = models.IntegerField(blank=True, null=True)
    grand_total = models.IntegerField(blank=True, null=True)
    discount = models.CharField(max_length=45, blank=True, null=True)
    rate_type = models.IntegerField(blank=True, null=True)
    campaign_category = models.CharField(max_length=45, blank=True, null=True)
    associate_code = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    createdon = models.DateTimeField(blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    updatedon = models.DateTimeField(blank=True, null=True)
    updatedby = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer_cart_item'
 
class TopBrands(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    img = models.BinaryField(blank=True, null=True)
    createdon = models.DateTimeField(blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    updatedon = models.DateTimeField(blank=True, null=True)
    updatedby = models.IntegerField(blank=True, null=True)
 
    class Meta:
        managed = False
        db_table = 'top_brands'
 
 
class Partner(models.Model):
    partner_code = models.CharField(unique=True, max_length=50)
    name = models.CharField(max_length=150)
    gst_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    address1 = models.CharField(max_length=100, blank=True, null=True)
    address2 = models.CharField(max_length=100, blank=True, null=True)
    pin_code = models.IntegerField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=150, blank=True, null=True)
    logo = models.BinaryField(blank=True, null=True)
    cin = models.CharField(max_length=50, blank=True, null=True)
    pan = models.CharField(max_length=20, blank=True, null=True)
    tan = models.CharField(max_length=20, blank=True, null=True)
    mobile_no = models.CharField(max_length=15, blank=True, null=True)
    createdon = models.DateTimeField(blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    updatedon = models.DateTimeField(blank=True, null=True)
    updatedby = models.IntegerField(blank=True, null=True)
 
    class Meta:
        managed = False
        db_table = 'partner'
 
class PartnerBankDetails(models.Model):
    partner_code = models.ForeignKey('Partner', models.DO_NOTHING, db_column='partner_code', to_field='partner_code')
    account_name = models.CharField(max_length=100)
    branch = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=30)
    ifsc = models.CharField(max_length=20)
    createdon = models.DateTimeField(blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    updatedon = models.DateTimeField(blank=True, null=True)
    updatedby = models.IntegerField(blank=True, null=True)
 
    class Meta:
        managed = False
        db_table = 'partner_bank_details'



class DiscountRates(models.Model):
    screensfro = models.IntegerField(blank=True, null=True)
    screesto = models.IntegerField(blank=True, null=True)
    weeksfron = models.IntegerField(blank=True, null=True)
    weeksto = models.IntegerField(blank=True, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'discount_rates'

class Weeks(models.Model):
    week_value = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'weeks'

class Adlengths(models.Model):
    length_value = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'adlengths'

class BookCampaign(models.Model):
    campaign_code = models.IntegerField(blank=True, null=True)
    associate_code = models.IntegerField(blank=True, null=True)
    partner_code = models.CharField(max_length=64, blank=True, null=True)
    screen_number = models.IntegerField(blank=True, null=True)
    media_name = models.TextField(blank=True, null=True)
    projection = models.TextField(blank=True, null=True)
    number_seats = models.IntegerField(blank=True, null=True)
    city_code = models.CharField(max_length=45, blank=True, null=True)
    state_code = models.CharField(max_length=45, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    ads_in_second = models.IntegerField(blank=True, null=True)
    week = models.IntegerField(blank=True, null=True)
    ad_type = models.TextField(db_column='ad_Type', blank=True, null=True)  # Field name made lowercase.
    ad_position = models.TextField(blank=True, null=True)
    total_sreen_rate = models.IntegerField(blank=True, null=True)
    gross_total = models.IntegerField(blank=True, null=True)
    discount = models.FloatField(blank=True, null=True)
    discount_total = models.IntegerField(blank=True, null=True)
    censor_certificate = models.TextField(blank=True, null=True)
    censor_cc = models.IntegerField(db_column='censor_CC', blank=True, null=True)  # Field name made lowercase.
    gst = models.FloatField(blank=True, null=True)
    total_taxable_amount = models.FloatField(blank=True, null=True)
    payment_mode = models.TextField(blank=True, null=True)
    payment_status = models.TextField(blank=True, null=True)
    coupon_code = models.TextField(blank=True, null=True)
    reference_code = models.TextField(blank=True, null=True)
    customize_id = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    campaign_status = models.TextField(blank=True, null=True)
    campaign_start_date = models.TextField(blank=True, null=True)
    campaign_end_date = models.TextField(blank=True, null=True)
    total_payable_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    invoice = models.TextField(blank=True, null=True)
    remaining_amount = models.FloatField(blank=True, null=True)
    paid = models.CharField(max_length=45, blank=True, null=True)
    transaction_id_check_no = models.TextField(db_column='transaction_id/check_no', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    discount_percentage = models.IntegerField(blank=True, null=True)
    campaign_name = models.TextField(blank=True, null=True)
    booking_date = models.DateField(blank=True, null=True)
    customer_code = models.CharField(max_length=45, blank=True, null=True)
    campaign_category = models.TextField(blank=True, null=True)
    createdon = models.DateTimeField(blank=True, null=True)
    createdby = models.ForeignKey('Users', models.DO_NOTHING, db_column='createdby', blank=True, null=True)
    updatedon = models.DateTimeField(blank=True, null=True)
    updatedby = models.ForeignKey('Users', models.DO_NOTHING, db_column='updatedby', related_name='bookcampaign_updatedby_set', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'book_campaign'


class Generateotp(models.Model):
    customer_code = models.CharField(max_length=45, blank=True, null=True)
    otp = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    is_deleted = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'generateotp'


class Permissions(models.Model):
    usertype_id = models.IntegerField(blank=True, null=True)
    module_id = models.IntegerField(blank=True, null=True)
    submodule_id = models.IntegerField(blank=True, null=True)
    activity_id = models.IntegerField(blank=True, null=True)
    e_read = models.CharField(max_length=10, blank=True, null=True)
    e_write = models.CharField(max_length=10, blank=True, null=True)
    e_update = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'permissions'

class ScreenlistingNew(models.Model):
    sr_no = models.TextField(blank=True, null=True)
    webcode = models.TextField(blank=True, null=True)
    projection = models.TextField(blank=True, null=True)
    cinema_chain = models.TextField(blank=True, null=True)
    theatre_name = models.TextField(blank=True, null=True)
    theatre_address = models.TextField(blank=True, null=True)
    pincode = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    district = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    seating_capacity = models.TextField(blank=True, null=True)
    cinema_type = models.TextField(blank=True, null=True)
    cinema_category = models.TextField(blank=True, null=True)
    base_rate_10sec_week = models.TextField(blank=True, null=True)
    base_rate_per_seconds_perweeks = models.TextField(blank=True, null=True)
    bb_rate_10sec_week = models.TextField(blank=True, null=True)
    bb_rate_per_seconds_perweeks = models.TextField(blank=True, null=True)
    partner_base_rate_10sec_week = models.TextField(blank=True, null=True)
    partner_bb_rate_10sec_week = models.TextField(blank=True, null=True)
    partner_base_rate_per_seconds_perweeks = models.TextField(blank=True, null=True)
    partner_bb_rate_per_seconds_perweeks = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'screenlisting_new'

class PartnerCustomerCartItem(models.Model):
    customer_code = models.CharField(max_length=45, blank=True, null=True)
    cart_id = models.CharField(max_length=45, blank=True, null=True)
    screen_id = models.IntegerField(blank=True, null=True)
    media_name = models.CharField(max_length=500, blank=True, null=True)
    web_code = models.CharField(max_length=64, blank=True, null=True)
    city = models.CharField(max_length=45, blank=True, null=True)
    district = models.CharField(max_length=45, blank=True, null=True)
    state = models.CharField(max_length=45, blank=True, null=True)
    theatre_address = models.CharField(max_length=500, blank=True, null=True)
    img = models.CharField(max_length=200, blank=True, null=True)
    seats_number = models.IntegerField(blank=True, null=True)
    projection = models.CharField(max_length=45, blank=True, null=True)
    rate = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    base_rate_10secweek = models.IntegerField(blank=True, null=True)
    bb_rate_10secweek = models.IntegerField(blank=True, null=True)
    base_rate_10secweek_0 = models.IntegerField(blank=True, null=True)
    bb_rate_10secweek_0 = models.IntegerField(blank=True, null=True)
    grand_total = models.IntegerField(blank=True, null=True)
    discount = models.CharField(max_length=45, blank=True, null=True)
    rate_type = models.IntegerField(blank=True, null=True)
    campaign_category = models.CharField(max_length=45, blank=True, null=True)
    partner_code = models.CharField(max_length=64, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    createdon = models.DateTimeField(blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    updatedon = models.DateTimeField(blank=True, null=True)
    updatedby = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'partner_customer_cart_item'

class PartnerCustomerCart(models.Model):
    cart_id = models.CharField(db_column='cart_Id', max_length=45, blank=True, null=True)  
    partner_code = models.CharField(max_length=64, blank=True, null=True)
    customer_code = models.CharField(max_length=45, blank=True, null=True)
    partner_customer_cartcol = models.CharField(max_length=45, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    createdon = models.DateTimeField(blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    updatedon = models.DateTimeField(blank=True, null=True)
    updatedby = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'partner_customer_cart'

class Generateotp(models.Model):
    customer_code = models.CharField(max_length=45, blank=True, null=True)
    otp = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    is_deleted = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'generateotp'
		
		
		
		
class CustomerCartDetails(models.Model):
    cart_id = models.CharField(max_length=45, blank=True, null=True)
    partner_id = models.CharField(max_length=45, blank=True, null=True)
    customer_code = models.CharField(max_length=45, blank=True, null=True)
    rate_type = models.CharField(max_length=50, blank=True, null=True)
    ad_length = models.CharField(max_length=45, blank=True, null=True)
    weeks = models.IntegerField(blank=True, null=True)
    ad_position = models.CharField(max_length=50, blank=True, null=True)
    ad_type = models.CharField(max_length=50, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    question1 = models.CharField(max_length=10, blank=True, null=True)
    question2 = models.CharField(max_length=10, blank=True, null=True)
    manual_discount_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    manual_discount_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    createdon = models.DateTimeField(blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    updatedon = models.DateTimeField(blank=True, null=True)
    updatedby = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer_cart_details'


class PartnerQuotationCounter(models.Model):
    id = models.BigAutoField(primary_key=True)
    count = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'partner_quotation_counter'


class RoCounter(models.Model):
    id = models.BigAutoField(primary_key=True)
    count = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ro_counter'


class UserProfileImages(models.Model):
    user_id = models.IntegerField(unique=True, blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    createdon = models.DateTimeField(blank=True, null=True)
    createdby = models.IntegerField(blank=True, null=True)
    updatedon = models.DateTimeField(blank=True, null=True)
    updatedby = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_profile_images'