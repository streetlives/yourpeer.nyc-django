# In a file called [project root]/components/calendar/calendar.py
from django_components import component

@component.register("location_service")
class Calendar(component.Component):
    # Templates inside `[your apps]/components` dir and `[project root]/components` dir will be automatically found. To customize which template to use based on context
    # you can override def get_template_name() instead of specifying the below variable.
    template_name = "location_service/template.html"

    # This component takes one parameter, a service_info string to show in the template
    def get_context_data(self, service_info, name , icon):
        return {
            "service_info": service_info,
            "name": name,
            "icon": icon
        }

    # class Media:
        # css = "calendar/style.css"
        # js = "calendar/script.js"