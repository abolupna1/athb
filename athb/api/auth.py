import string
import frappe
from frappe  import _
from datetime import datetime,timedelta
import random
from frappe.utils import  get_fullname,getdate

from frappe.utils.password import update_password as _update_password



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
	
		# 	roles = frappe.get_roles(usr) 
		# # is_std = frappe.has_role("Student")
		# print(roles)

# @frappe.whitelist( allow_guest=True )
# def logout(email:str):
# 	user = frappe.db.get("User", {"email":email })

# 	if user:
# 		frappe.local.login_manager.logout(user=user.name)
# 		frappe.db.commit()
# 		frappe.clear_messages()
# 		frappe.local.response["message"] = {
# 		"code":0,
# 		"message":"Authentication Error!",
# 		"data":user
# 		}
# 		return


@frappe.whitelist( allow_guest=True )
def sign_in(usr, pwd):
	try:
		login_manager = frappe.auth.LoginManager()
		login_manager.authenticate(user=usr, pwd=pwd)
		login_manager.post_login()
		api_generate = generate_keys(frappe.session.user)
		user = frappe.get_doc('User', frappe.session.user)
		roles = []
		roles = frappe.get_roles(usr) 
		student = roles.count("Student")
		teacher = roles.count("Teacher")

		role="Non"

		if student > 0:
			role="Student"
		if student == 0 and teacher > 0:
			role ="Teacher"
		frappe.response["message"] = {
		"code":1,
		"message":"Authentication Success",
		
		"data":{
			"id":user.name,
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
			"email":user.email,
			"role": role,
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


@frappe.whitelist( allow_guest=True )
def reset_password(usr):
	user = frappe.db.get("User", {"email":usr })
	if user:
		if user.enabled:
			send_verification_code(user)
			frappe.clear_messages()
			frappe.local.response["message"] =  {"code":1,"message":"Sent Verification Code Successfully"}
			return
		else:
			frappe.clear_messages()
			frappe.local.response["message"] =  {"code":0,"message":"Account closed"} 
			return
	else:
		frappe.clear_messages()
		frappe.local.response["message"] =  {"code":0,"message":"Email not found"} 
		return




	

	# sendmail(doc=user,recipients=[usr],title="Reset Password",msg="test",template=template)



def send_verification_code(user):
	code = ''.join(random.choices(string.digits, k=4))
	# Create a Verification Code record
	verification_code = frappe.new_doc("Verification Code")
	verification_code.user = user.name
	verification_code.code = code
	verification_code.expiry = datetime.now() + timedelta(hours=24)  # Set expiry time (e.g., 24 hours)
	verification_code.flags.ignore_permissions = True
	verification_code.save()
	context = {
        "recipient_name": get_fullname(user.name),
        "message_heading": "شكرا لتسجيلك في منصة عذب لعليم القران الكريم",
        "message_body": f"Your verification code is: {code}"
    }
	content = frappe.render_template("athb/templates/send_email.html", context)


	frappe.enqueue(method=	frappe.sendmail(
        recipients=[user.email],
		subject="Verification Code",
        content=content,
    ), queue='short', timeout=300)

	







@frappe.whitelist( allow_guest=True )
def verify_code(code):
	code_exists = frappe.db.exists("Verification Code", {"code": code})
	if code_exists:
		verification_code = frappe.get_doc("Verification Code", {"code": code})
		year =getdate(verification_code.expiry).year
		month =getdate(verification_code.expiry).month
		day = getdate(verification_code.expiry).day

		date = datetime(year, month, day) # Replace with whatever you want
		now = datetime.now() 
		if verification_code and date > now:
		# Code is valid and not expired
		
			verification_code.delete(ignore_permissions = True)
			frappe.db.commit()
			frappe.clear_messages()
			frappe.local.response["message"] =  {"code":1,"message":"Code OK"} 
			return
		else:
			frappe.clear_messages()
			frappe.local.response["message"] =  {"code":0,"message":"Code Erro"} 
			return
	else:
		frappe.clear_messages()
		frappe.local.response["message"] =  {"code":0,"message":"Code Erro"} 
		return
	


@frappe.whitelist(allow_guest=True)
def update_password(new_password:str,email:str):
	user_exists = frappe.db.exists("User", {"email": email})
	if user_exists:
		user = frappe.get_doc("User", {"email": email})
		# user.new_password = new_password
		# user.flags.ignore_permissions = True
		# user.flags.ignore_password_policy = True
		# user.db_update()
		if user.name not in ("Guest", "Administrator"):
			_update_password(email, new_password,logout_all_sessions=True)
			frappe.clear_messages()
			frappe.local.response["message"] =  {"code":1,"message":"Password update successfuly"}
		else:
			frappe.clear_messages()
			frappe.local.response["message"] =  {"code":0,"message":"User not found"} 
	else:
		frappe.clear_messages()
		frappe.local.response["message"] =  {"code":0,"message":"User not found"} 