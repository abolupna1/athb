
frappe.ready(function() {
    // bind events here
    var preferred_language = frappe.get_cookie("preferred_language");
    if(preferred_language == "ar"){
      document.querySelector(".btn-next").innerHTML = "القادم";
      document.querySelector(".btn-previous").innerHTML = "السابق";
  
    }
  
  
    if(frappe.session.user == "Guest"){
      if(preferred_language != "ar"){
        document.cookie = `preferred_language=ar`;
      }
  
    lang = document.getElementsByTagName('html')[0].getAttribute('lang');
    if(lang == "ar" ){
      document.getElementsByTagName('html')[0].dir = "rtl";
    }
      
	// var msageAr = document.querySelector(".msgprint").innerText.replace("Mandatory fields required","يوجد بعض الحقول مطلوبة");
    // document.querySelector(".msgprint").innerHTML = msageAr;
  
    }
  
  
  
    
  
  })