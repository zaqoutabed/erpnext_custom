import frappe


def execute():
    # Create a new department with a name of "BOM Department"
    for company in frappe.get_list("Company"):
        company = company.name
        if len(frappe.get_list("BOM", filters={"company": company})) == 0:
            continue

        departments_with_bom_name = frappe.db.sql(
            f"""
                SELECT name
                FROM `tabDepartment` 
                WHERE company='{company}' AND LOWER(department_name)='bom department'
            """,
            as_dict=True,
        )
        if len(departments_with_bom_name) > 0:
            department = departments_with_bom_name[0].name
        else:
            department = frappe.new_doc("Department")
            department.company = company
            department.department_name = "BOM Department 2"
            department.flags.ignore_mandatory = True
            department.insert()
            department = department.name
        frappe.db.sql(
            f"UPDATE `tabBOM` SET department = '{department}' WHERE company = '{company}'"
        )
