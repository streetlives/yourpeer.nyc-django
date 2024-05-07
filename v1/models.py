# Copyright (c) 2024 Streetlives, Inc.
# 
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.


from django.db import models
#from django.contrib.gis.db import models as gis_models



class Sequelizemeta(models.Model):
    name = models.CharField(primary_key=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'SequelizeMeta'


class Organizations(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__ (self):
        # return a lot of info but annotated with name before
        return f"name: {self.name} - description: {self.description} - id: {self.id} - created_at: {self.created_at} - updated_at: {self.updated_at}"

    class Meta:
        managed = False
        db_table = 'organizations'


class Services(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    interpretation_services = models.TextField(blank=True, null=True)
    fees = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    organization = models.ForeignKey(Organizations, models.DO_NOTHING)
    additional_info = models.TextField(blank=True, null=True)
    who_does_it_serve = models.TextField(blank=True, null=True)  # This field type is a guess.
    ages_served = models.TextField(blank=True, null=True)  # This field type is a guess.

    def __str__ (self):
        # return a lot of info
        return f"name: {self.name} - description: {self.description} - id: {self.id} - created_at: {self.created_at} - updated_at: {self.updated_at} - organization: {self.organization.name} - additional_info: {self.additional_info} - who_does_it_serve: {self.who_does_it_serve} - ages_served: {self.ages_served}"

    class Meta:
        managed = False
        db_table = 'services'


class Locations(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    transportation = models.TextField(blank=True, null=True)
    #position = gis_models.PointField(geography=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    organization = models.ForeignKey(Organizations, models.DO_NOTHING, blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)
    hidden_from_search = models.BooleanField(blank=True, null=True)
    slug = models.TextField()

    def __str__ (self):
        # return a lot of info but annotated with the field name before
        return f"name: {self.name} - description: {self.description} - id: {self.id} - created_at: {self.created_at} - updated_at: {self.updated_at} - organization: {self.organization.name} - additional_info: {self.additional_info} - hidden_from_search: {self.hidden_from_search}"

    class Meta:
        managed = False
        db_table = 'locations'


class ServicesAtLocations(models.Model):
    id = models.UUIDField(primary_key=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    location_id = models.UUIDField(Locations, blank=True, null=True)
    service_id = models.UUIDField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'services_at_locations'
        unique_together = (('location_id', 'service_id'),)


class AccessibilityForDisabilities(models.Model):
    id = models.UUIDField(primary_key=True)
    accessibility = models.TextField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    location = models.ForeignKey(Locations, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accessibility_for_disabilities'


class Comments(models.Model):
    id = models.UUIDField(primary_key=True)
    content = models.TextField(blank=True, null=True)
    posted_by = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    location = models.ForeignKey(Locations, models.DO_NOTHING, blank=True, null=True)
    service_at_location = models.ForeignKey(ServicesAtLocations, models.DO_NOTHING, blank=True, null=True)
    contact_info = models.TextField(blank=True, null=True)
    reply_to_id = models.UUIDField(blank=True, null=True)
    hidden = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comments'


class DocumentsInfos(models.Model):
    id = models.UUIDField(primary_key=True)
    recertification_time = models.TextField(blank=True, null=True)
    grace_period = models.TextField(blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    service = models.ForeignKey(Services, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'documents_infos'


class EligibilityParameters(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.TextField(unique=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'eligibility_parameters'


class Eligibility(models.Model):
    id = models.UUIDField(primary_key=True)
    eligible_values = models.JSONField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    parameter = models.ForeignKey(EligibilityParameters, models.DO_NOTHING, blank=True, null=True)
    service = models.ForeignKey(Services, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eligibility'
        unique_together = (('parameter', 'service'),)


class ErrorReports(models.Model):
    id = models.UUIDField(primary_key=True)
    general_location_error = models.BooleanField()
    services = models.TextField()  # This field type is a guess.
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    location = models.ForeignKey(Locations, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'error_reports'


class EventRelatedInfo(models.Model):
    id = models.UUIDField(primary_key=True)
    event = models.TextField()
    information = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    location = models.ForeignKey(Locations, models.DO_NOTHING, blank=True, null=True)
    service = models.ForeignKey(Services, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'event_related_info'
        unique_together = (('event', 'service', 'location'),)


class HolidaySchedules(models.Model):
    id = models.UUIDField(blank=True, null=False, primary_key=True)
    closed = models.BooleanField(blank=True, null=True)
    opens_at = models.TimeField(blank=True, null=True)
    closes_at = models.TimeField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    location_id = models.UUIDField(blank=True, null=True)
    service = models.ForeignKey(Services, models.DO_NOTHING, blank=True, null=True)
    service_at_location_id = models.UUIDField(blank=True, null=True)
    weekday = models.IntegerField(blank=True, null=True)
    occasion = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'holiday_schedules'


class HolidaySchedules20220827Backup(models.Model):
    id = models.UUIDField(blank=True, null=False, primary_key=True)
    closed = models.BooleanField(blank=True, null=True)
    opens_at = models.TimeField(blank=True, null=True)
    closes_at = models.TimeField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    location_id = models.UUIDField(blank=True, null=True)
    service_id = models.UUIDField(blank=True, null=True)
    service_at_location_id = models.UUIDField(blank=True, null=True)
    weekday = models.IntegerField(blank=True, null=True)
    occasion = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'holiday_schedules_20220827_backup'


class Languages(models.Model):
    id = models.UUIDField(primary_key=True)
    language = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'languages'


class LocationLanguages(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    language_id = models.UUIDField(primary_key=True)
    location = models.ForeignKey(Locations, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'location_languages'
        unique_together = (('language_id', 'location'),)


class LocationSuggestions(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    position = models.TextField(blank=True, null=True)  # This field type is a guess.
    taxonomy_ids = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'location_suggestions'


class Metadata(models.Model):
    id = models.UUIDField(primary_key=True)
    resource_id = models.UUIDField()
    resource_table = models.TextField()
    last_action_date = models.DateTimeField()
    last_action_type = models.TextField()  # This field type is a guess.
    field_name = models.TextField(blank=True, null=True)
    previous_value = models.TextField(blank=True, null=True)
    replacement_value = models.TextField(blank=True, null=True)
    updated_by = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    source = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'metadata'


class PaymentsAccepted(models.Model):
    id = models.UUIDField(primary_key=True)
    payment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    service = models.ForeignKey(Services, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'payments_accepted'


class Phones(models.Model):
    id = models.UUIDField(primary_key=True)
    number = models.TextField()
    extension = models.IntegerField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    language = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    location = models.ForeignKey(Locations, models.DO_NOTHING, blank=True, null=True)
    organization = models.ForeignKey(Organizations, models.DO_NOTHING, blank=True, null=True)
    service = models.ForeignKey(Services, models.DO_NOTHING, blank=True, null=True)
    service_at_location = models.ForeignKey(ServicesAtLocations, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'phones'


class PhysicalAddresses(models.Model):
    id = models.UUIDField(primary_key=True)
    address_1 = models.TextField()
    city = models.TextField()
    region = models.TextField(blank=True, null=True)
    state_province = models.TextField()
    postal_code = models.TextField()
    country = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    location_suggestion = models.ForeignKey(LocationSuggestions, models.DO_NOTHING, blank=True, null=True)
    location = models.ForeignKey(Locations, models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
    
        return f"address_1: {self.address_1} - city: {self.city} - region: {self.region} - state_province: {self.state_province} - postal_code: {self.postal_code} - country: {self.country} - updated_at: {self.updated_at} - location_suggestion: {self.location_suggestion} - location.name: {self.location.name}"

    class Meta:
        managed = False
        db_table = 'physical_addresses'


class Taxonomies(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.TextField()
    parent_name = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'taxonomies'


class TaxonomySpecificAttributes(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.TextField(unique=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    taxonomy = models.ForeignKey(Taxonomies, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'taxonomy_specific_attributes'


class ServiceTaxonomySpecificAttributes(models.Model):
    id = models.UUIDField(primary_key=True)
    values = models.JSONField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    attribute = models.ForeignKey(TaxonomySpecificAttributes, models.DO_NOTHING, blank=True, null=True)
    service = models.ForeignKey(Services, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'service_taxonomy_specific_attributes'
        unique_together = (('attribute', 'service'),)


class ServiceTaxonomy(models.Model):
    id = models.UUIDField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    service = models.ForeignKey(Services, models.DO_NOTHING, blank=True, null=True)
    taxonomy = models.ForeignKey(Taxonomies, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'service_taxonomy'
        unique_together = (('service', 'taxonomy'),)


class ServiceLanguages(models.Model):
    id = models.UUIDField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    language = models.ForeignKey(Languages, models.DO_NOTHING, blank=True, null=True)
    service = models.ForeignKey(Services, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'service_languages'
        unique_together = (('language', 'service'),)


class ServiceAtLocations(models.Model):
    id = models.UUIDField(primary_key=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    location = models.ForeignKey(Locations, models.DO_NOTHING, blank=True, null=True)
    service = models.ForeignKey(Services, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'service_at_locations'
        unique_together = (('location', 'service'),)


class RegularSchedules(models.Model):
    id = models.UUIDField(primary_key=True)
    weekday = models.IntegerField()
    opens_at = models.TimeField(blank=True, null=True)
    closes_at = models.TimeField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    location = models.ForeignKey(Locations, models.DO_NOTHING, blank=True, null=True)
    service = models.ForeignKey(Services, models.DO_NOTHING, blank=True, null=True)
    service_at_location = models.ForeignKey(ServiceAtLocations, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'regular_schedules'


class RequiredDocuments(models.Model):
    id = models.UUIDField(primary_key=True)
    document = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    service = models.ForeignKey(Services, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'required_documents'


class ServiceAreas(models.Model):
    id = models.UUIDField(primary_key=True)
    postal_codes = models.TextField()  # This field type is a guess.
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    service = models.ForeignKey(Services, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'service_areas'


class SpatialRefSys(models.Model):
    srid = models.IntegerField(primary_key=True)
    auth_name = models.CharField(max_length=256, blank=True, null=True)
    auth_srid = models.IntegerField(blank=True, null=True)
    srtext = models.CharField(max_length=2048, blank=True, null=True)
    proj4text = models.CharField(max_length=2048, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'spatial_ref_sys'


class VwOrgsFood(models.Model):
    organization_name = models.TextField(blank=True, null=True)
    address_1 = models.TextField()
    service_name = models.TextField(blank=True, null=True)
    category_parent_name = models.TextField(blank=True, null=True)
    subcategory_name = models.TextField(blank=True, null=True)
    taxonomy_parent_id = models.UUIDField(blank=True, null=True)
    service_id = models.UUIDField(blank=True, null=True)
    service_description = models.TextField(blank=True, null=True)
    id = models.UUIDField(primary_key=True, blank=True)
    organization_description = models.TextField(blank=True, null=True)
    organization_email = models.TextField(blank=True, null=True)
    organization_url = models.TextField(blank=True, null=True)
    org_created_at = models.DateTimeField(blank=True, null=True)
    org_updated_at = models.DateTimeField(blank=True, null=True)
    service_url = models.TextField(blank=True, null=True)
    service_email = models.TextField(blank=True, null=True)
    interpretation_services = models.TextField(blank=True, null=True)
    fees = models.TextField(blank=True, null=True)
    srv_created_at = models.DateTimeField(blank=True, null=True)
    srv_updated_at = models.DateTimeField(blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)
    location_id = models.UUIDField(blank=True, null=True)
    location_name = models.TextField(blank=True, null=True)
    position = models.TextField(blank=True, null=True)  # This field type is a guess.
    physical_location_id = models.UUIDField(blank=True, null=True)
    city = models.TextField()
    postal_code = models.TextField()
    state_province = models.TextField()
    country = models.TextField()

    class Meta:
        managed = False 
        db_table = 'vw_orgs_food'


class VwOrgsAccommodations(models.Model):
    organization_name = models.TextField(blank=True, null=True)
    address_1 = models.TextField()
    service_name = models.TextField(blank=True, null=True)
    category_parent_name = models.TextField(blank=True, null=True)
    subcategory_name = models.TextField(blank=True, null=True)
    taxonomy_parent_id = models.UUIDField(blank=True, null=True)
    service_id = models.UUIDField(blank=True, null=True)
    service_description = models.TextField(blank=True, null=True)
    id = models.UUIDField(primary_key=True, blank=True)
    organization_description = models.TextField(blank=True, null=True)
    organization_email = models.TextField(blank=True, null=True)
    organization_url = models.TextField(blank=True, null=True)
    org_created_at = models.DateTimeField(blank=True, null=True)
    org_updated_at = models.DateTimeField(blank=True, null=True)
    service_url = models.TextField(blank=True, null=True)
    service_email = models.TextField(blank=True, null=True)
    interpretation_services = models.TextField(blank=True, null=True)
    fees = models.TextField(blank=True, null=True)
    srv_created_at = models.DateTimeField(blank=True, null=True)
    srv_updated_at = models.DateTimeField(blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)
    location_id = models.UUIDField(blank=True, null=True)
    location_name = models.TextField(blank=True, null=True)
    position = models.TextField(blank=True, null=True)  # This field type is a guess.
    physical_location_id = models.UUIDField(blank=True, null=True)
    city = models.TextField()
    postal_code = models.TextField()
    state_province = models.TextField()
    country = models.TextField()

    class Meta:
        managed = False 
        db_table = 'vw_orgs_accommodations'


class VwOrgsClothing(models.Model):
    organization_name = models.TextField(blank=True, null=True)
    address_1 = models.TextField()
    service_name = models.TextField(blank=True, null=True)
    category_parent_name = models.TextField(blank=True, null=True)
    subcategory_name = models.TextField(blank=True, null=True)
    taxonomy_parent_id = models.UUIDField(blank=True, null=True)
    service_id = models.UUIDField(blank=True, null=True)
    service_description = models.TextField(blank=True, null=True)
    id = models.UUIDField(primary_key=True, blank=True)
    organization_description = models.TextField(blank=True, null=True)
    organization_email = models.TextField(blank=True, null=True)
    organization_url = models.TextField(blank=True, null=True)
    org_created_at = models.DateTimeField(blank=True, null=True)
    org_updated_at = models.DateTimeField(blank=True, null=True)
    service_url = models.TextField(blank=True, null=True)
    service_email = models.TextField(blank=True, null=True)
    interpretation_services = models.TextField(blank=True, null=True)
    fees = models.TextField(blank=True, null=True)
    srv_created_at = models.DateTimeField(blank=True, null=True)
    srv_updated_at = models.DateTimeField(blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)
    location_id = models.UUIDField(blank=True, null=True)
    location_name = models.TextField(blank=True, null=True)
    position = models.TextField(blank=True, null=True)  # This field type is a guess.
    physical_location_id = models.UUIDField(blank=True, null=True)
    city = models.TextField()
    postal_code = models.TextField()
    state_province = models.TextField()
    country = models.TextField()

    class Meta:
        managed = False 
        db_table = 'vw_orgs_clothing'


class VwOrgsOtherServices(models.Model):
    organization_name = models.TextField(blank=True, null=True)
    address_1 = models.TextField()
    service_name = models.TextField(blank=True, null=True)
    category_parent_name = models.TextField(blank=True, null=True)
    subcategory_name = models.TextField(blank=True, null=True)
    taxonomy_parent_id = models.UUIDField(blank=True, null=True)
    service_id = models.UUIDField(blank=True, null=True)
    service_description = models.TextField(blank=True, null=True)
    id = models.UUIDField(primary_key=True, blank=True)
    organization_description = models.TextField(blank=True, null=True)
    organization_email = models.TextField(blank=True, null=True)
    organization_url = models.TextField(blank=True, null=True)
    org_created_at = models.DateTimeField(blank=True, null=True)
    org_updated_at = models.DateTimeField(blank=True, null=True)
    service_url = models.TextField(blank=True, null=True)
    service_email = models.TextField(blank=True, null=True)
    interpretation_services = models.TextField(blank=True, null=True)
    fees = models.TextField(blank=True, null=True)
    srv_created_at = models.DateTimeField(blank=True, null=True)
    srv_updated_at = models.DateTimeField(blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)
    location_id = models.UUIDField(blank=True, null=True)
    location_name = models.TextField(blank=True, null=True)
    position = models.TextField(blank=True, null=True)  # This field type is a guess.
    physical_location_id = models.UUIDField(blank=True, null=True)
    city = models.TextField()
    postal_code = models.TextField()
    state_province = models.TextField()
    country = models.TextField()

    class Meta:
        managed = False 
        db_table = 'vw_orgs_other_services'


class VwOrgsPersonalCare(models.Model):
    organization_name = models.TextField(blank=True, null=True)
    address_1 = models.TextField()
    service_name = models.TextField(blank=True, null=True)
    category_parent_name = models.TextField(blank=True, null=True)
    subcategory_name = models.TextField(blank=True, null=True)
    taxonomy_parent_id = models.UUIDField(blank=True, null=True)
    service_id = models.UUIDField(blank=True, null=True)
    service_description = models.TextField(blank=True, null=True)
    id = models.UUIDField(primary_key=True, blank=True)
    organization_description = models.TextField(blank=True, null=True)
    organization_email = models.TextField(blank=True, null=True)
    organization_url = models.TextField(blank=True, null=True)
    org_created_at = models.DateTimeField(blank=True, null=True)
    org_updated_at = models.DateTimeField(blank=True, null=True)
    service_url = models.TextField(blank=True, null=True)
    service_email = models.TextField(blank=True, null=True)
    interpretation_services = models.TextField(blank=True, null=True)
    fees = models.TextField(blank=True, null=True)
    srv_created_at = models.DateTimeField(blank=True, null=True)
    srv_updated_at = models.DateTimeField(blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)
    location_id = models.UUIDField(blank=True, null=True)
    location_name = models.TextField(blank=True, null=True)
    position = models.TextField(blank=True, null=True)  # This field type is a guess.
    physical_location_id = models.UUIDField(blank=True, null=True)
    city = models.TextField()
    postal_code = models.TextField()
    state_province = models.TextField()
    country = models.TextField()

    class Meta:
        managed = False 
        db_table = 'vw_orgs_personal_care'


class VwOrgsHealth(models.Model):
    organization_name = models.TextField(blank=True, null=True)
    address_1 = models.TextField()
    service_name = models.TextField(blank=True, null=True)
    category_parent_name = models.TextField(blank=True, null=True)
    subcategory_name = models.TextField(blank=True, null=True)
    taxonomy_parent_id = models.UUIDField(blank=True, null=True)
    service_id = models.UUIDField(blank=True, null=True)
    service_description = models.TextField(blank=True, null=True)
    id = models.UUIDField(primary_key=True, blank=True)
    organization_description = models.TextField(blank=True, null=True)
    organization_email = models.TextField(blank=True, null=True)
    organization_url = models.TextField(blank=True, null=True)
    org_created_at = models.DateTimeField(blank=True, null=True)
    org_updated_at = models.DateTimeField(blank=True, null=True)
    service_url = models.TextField(blank=True, null=True)
    service_email = models.TextField(blank=True, null=True)
    interpretation_services = models.TextField(blank=True, null=True)
    fees = models.TextField(blank=True, null=True)
    srv_created_at = models.DateTimeField(blank=True, null=True)
    srv_updated_at = models.DateTimeField(blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)
    location_id = models.UUIDField(blank=True, null=True)
    location_name = models.TextField(blank=True, null=True)
    position = models.TextField(blank=True, null=True)  # This field type is a guess.
    physical_location_id = models.UUIDField(blank=True, null=True)
    city = models.TextField()
    postal_code = models.TextField()
    state_province = models.TextField()
    country = models.TextField()

    class Meta:
        managed = False 
        db_table = 'vw_orgs_health'


class WebsiteData(models.Model):
    slug = models.TextField(primary_key=True)
    data = models.TextField()
    updated_at = models.DateTimeField()
    location = models.ForeignKey(Locations, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'website_data'

class Redirects(models.Model):
    old_slug = models.TextField(primary_key=True)
    new_slug = models.TextField()

    class Meta:
        managed = False
        db_table = 'redirects'

class LocationSlugRedirects(models.Model):
    slug = models.TextField(primary_key=True)
    location = models.ForeignKey(Locations, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'location_slug_redirects'

class NycNeighborhoods(models.Model):
    zip_code = models.TextField(primary_key=True)
    neighborhood_name = models.TextField()

    class Meta:
        managed = False
        db_table = 'nyc_neighborhoods'
