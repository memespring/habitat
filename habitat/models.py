from mongoengine import StringField, PolygonField, DateTimeField, GeoPointField, StringField, DictField, DynamicDocument, Document, ObjectIdField
from mongoengine import signals
from mongoengine import DoesNotExist
import datetime
from habitat import tasks

class Event(DynamicDocument):
    guid = StringField(max_length=255, required=True, unique=True)
    source = StringField(max_length=25, required=True) 
    occured_at = DateTimeField()
    data = DictField(required=True)

    @staticmethod
    def guid_exists(guid):
        try:
            event = Event.objects.get(guid=guid)
            return True
        except DoesNotExist:
            return False

class Location(DynamicDocument):
    latlng = GeoPointField()
    event_id = ObjectIdField
    occured_at = DateTimeField()

    @classmethod
    def post_save(cls, sender, document, **kwargs):
        tasks.run_scenarios.delay()

class Setting(Document):
    key = StringField(max_length=25, required=True, unique=True)
    value = DictField(required=True)

class Fence(DynamicDocument):
    category = StringField(max_length=25, required=True)
    polygon = PolygonField()
  
signals.post_save.connect(Location.post_save, sender=Location)
