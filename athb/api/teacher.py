
import frappe

#http://127.0.0.1:8000/api/method/athb.api.teacher.getFavoritTeachers
@frappe.whitelist(allow_guest=True)
def getFavoritTeachers(user_name:str):
    teachers =  frappe.db.get_list('Teacher',filters={'enabled': True},
                                   fields=["name","full_name","online","rating","image"],
                                   )
    
    check = frappe.db.exists('Student',{"user": user_name})

    if check:
        student = frappe.get_doc('Student', {"user":user_name})

    

    
    return teachers,check,student.favorite_teachers

