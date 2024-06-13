import frappe
from frappe  import _
from datetime import datetime, timedelta
from frappe import auth
#http://127.0.0.1:8000/api/method/athb.api.auth.sign_up?email=edom@email.com&full_name=edom
#1996d8cd8631a4d43dda7cbcf47ff3ee1147abde5bfee69dda43a49442b008c8
@frappe.whitelist(allow_guest=True)
def sign_up(**data):
	user = frappe.db.get("User", {"email":data.get("email") })
	if user:
		if user.enabled:
			frappe.clear_messages()
			frappe.local.response["message"] =  {"code":0,"message":"Email Already Registered","data":{}}
			return
		
		else:
			frappe.local.response["message"] =  {"code":0,"message":"Email Already Registered but disabled","data":{}} 
			return
	mobile = frappe.db.get("User", {"mobile_no":data.get("mobile_no") })
	if mobile:
		frappe.local.response["message"] =  {"code":0,"message":"Mobile Already Registered","data":{}} 
		return


	else:
		full_name = "{} {} {}".format(data.get("first_name"),data.get("middle_name") ,data.get("last_name") )
		user = frappe.get_doc(
			{
				"doctype": "User",
				"email": data.get("email") ,
				"first_name": data.get("first_name"),
				"middle_name":data.get("middle_name"),
				"last_name":data.get("last_name"),
				"full_name":full_name,
				'birth_date':data.get("birth_date"),
				"gender":"Male",
				"mobile_no":data.get("mobile_no"),
				"enabled": 1,
				"new_password": data.get("password"),
				"user_type": "Website User",
				"send_welcome_email":0,
				"custom_online":1
			}
		)

		user.flags.ignore_permissions = True
		user.flags.ignore_password_policy = True

		user.insert()

		student = frappe.get_doc(
			{
				"doctype": "Student",
				"email": data.get("email") ,
				"first_name": data.get("first_name"),
				"middle_name":data.get("middle_name"),
				"last_name":data.get("last_name"),
				"full_name":full_name,
				'birth_date':data.get("birth_date"),
				"gender":"Male",
				"mobile_no":data.get("mobile_no"),
				"enabled": 1,
				"online":1
			})

		student.flags.ignore_permissions = True

		student.insert()

		# set default signup role as per Portal Settings
		default_role = frappe.db.get_single_value("Portal Settings", "default_role")
		if default_role:
			user.add_roles(default_role)
			user.add_roles("Student")
		
		sign_in(usr=user.email,pwd=data.get("password"))

	# except :
	# 	frappe.clear_messages()
	# 	frappe.local.response["message"] = {
	# 	"code":0,
	# 	"message":"Register Error!"  ,
	# 	"data":{}
	# 	}
	# 	return
	



@frappe.whitelist( allow_guest=True )
def sign_in(usr, pwd):
	try:
		login_manager = frappe.auth.LoginManager()
		login_manager.authenticate(user=usr, pwd=pwd)
		login_manager.post_login()
		api_generate = generate_keys(frappe.session.user)
		user = frappe.get_doc('User', frappe.session.user)
		frappe.response["message"] = {
		"code":1,
		"message":"Authentication Success",
		"data":{
			"first_name":user.first_name,
			"middle_name":user.middle_name,
			"last_name":user.last_name,
			"birth_date":user.birth_date,
			"gender":user.gender,
			"mobile_no":user.mobile_no,
			"birth_date":user.birth_date,
			"custom_online":user.custom_online,
			"sid":frappe.session.sid,
			"api_key":user.api_key,
			"api_secret":api_generate,
			"email":user.email
			}
		}

	except frappe.exceptions.AuthenticationError:
		frappe.clear_messages()
		frappe.local.response["message"] = {
		"code":0,
		"message":"Authentication Error!",
		"data":{}
		}
		return

	

    # A1234@56789a athb.athb101@gmail.com  aqxy mvvl eyzm epai


    





def generate_keys(user):
	user_details = frappe.get_doc('User', user)
	api_secret = frappe.generate_hash(length=15)
	if not user_details.api_key:
		api_key = frappe.generate_hash(length=15)
		user_details.api_key = api_key
	user_details.api_secret = api_secret
	user_details.save(ignore_permissions=True)
	user_details.db_update()
	return api_secret


