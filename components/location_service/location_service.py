# In a file called [project root]/components/calendar/calendar.py
from django_components import component

@component.register("location_service")
class LocationService(component.Component):
    # Templates inside `[your apps]/components` dir and `[project root]/components` dir will be automatically found. To customize which template to use based on context
    # you can override def get_template_name() instead of specifying the below variable.
    template_name = "location_service/template.html"

    def get_context_data(self, service_info, name , icon, path, active_category):



        return {
            "service_info": service_info,
            "name": name,
            "icon": icon,
            "path": path,
            "active_category": active_category
        }

    # class Media:
        # css = "calendar/style.css"
        # js = "calendar/script.js"