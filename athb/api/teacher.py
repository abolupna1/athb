
import frappe
from frappe.utils.data import ceil
no_cache = 1

#http://127.0.0.1:8000/api/method/athb.api.teacher.getFavoritTeachers
@frappe.whitelist()
def getFavoritTeachers(user_name:str):
    try:
        teachers =  frappe.db.get_list('Teacher',filters={'enabled': True},
                                    fields=["name","full_name","online","rating","image"],ignore_permissions=True)
        check = frappe.db.exists('Student',{"user": user_name})
        teachers_return = []
        if check:
            student = frappe.get_doc('Student', {"user":user_name})
            for teacher in teachers:
                teacher_app = teacher
                is_favorite = frappe.db.exists('Favorite Teachers',{"parent": student.name,"teacher":teacher.name})
                if is_favorite:
                    teacher_app['favorite'] = True
                else:
                    teacher_app['favorite'] = False
                teacher_app['rating'] = ceil(((teacher_app.rating * 100) / 2 ) /10) 
                teachers_return.append(teacher_app)
        else:
            for teacher in teachers:
                teacher_app = teacher
                teacher_app["favorite"] =  False
                teacher_app['rating'] = ceil(((teacher_app.rating * 100) / 2 ) /10) 
                teachers_return.append(teacher_app)
        frappe.clear_messages()
        frappe.local.response["message"] = {
        "code":1,
        "message":"Success",
        "teacher_list":teachers_return
        }
        return
    except:
            frappe.clear_messages()
            frappe.local.response["message"] = {
            "code":0,
            "message":"Server Error!",
            }
            return

