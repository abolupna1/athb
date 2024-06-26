// Copyright (c) 2024, edom ibrahim and contributors
// For license information, please see license.txt

frappe.ui.form.on("Teacher", {
	refresh(frm) {
        
        frm.set_query("user", function(){
            return {
                filters: {
                    "ignore_user_type": 1
                }
            }
        });

	},
});
