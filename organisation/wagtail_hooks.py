from wagtail.contrib.modeladmin.options import(
    ModelAdmin, modeladmin_register
)

from organisation.models import Organisation

class OrganisationAdminModel(ModelAdmin):
    model = Organisation
    menu_label = 'Organisation'
    menu_icon = 'user'
    menu_order = 200
    add_to_settings_menu = False  
    exclude_from_explorer = False 
    list_display = ('name','description', 'website_url','facebook_url','twitter_url','linkedin_url')


modeladmin_register(OrganisationAdminModel)
