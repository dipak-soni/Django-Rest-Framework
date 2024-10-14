from rest_framework import serializers
from ..models import CarList,ShowRoomList,Review
import decimal

def alphanumeric(value):     # another way to use validators in the program for the field
    if not str(value).isalnum():
        raise serializers.ValidationError("car number must contain only alphanumeric characters")

# serializer converts model complex data structure into python dictionary objects in order to better handling of data
class CarSerializer(serializers.Serializer):
    # if we use model serializer then we do not need to write these details
    id=serializers.IntegerField(read_only=True)
    name=serializers.CharField()
    description=serializers.CharField()
    active=serializers.BooleanField(read_only=True)
    carnumber=serializers.CharField(validators=[alphanumeric])
    price=serializers.DecimalField(max_digits=9,decimal_places=2)
    
    def create(self, validated_data):
       return CarList.objects.create(**validated_data)
   
    
    def update(self, instance, validated_data):
        instance.name=validated_data.get('name','instance.name')
        instance.description=validated_data.get('description','instance.description')
        instance.active=validated_data.get('active','instance.active')
        instance.carnumber=validated_data.get('carnumber','instance.carnumber')
        instance.price=validated_data.get('price','instance.price')
        instance.save()
        return instance
    
    def validate_price(self,value):    # field level validation
        if value<=20000:
            raise serializers.ValidationError("price must be greater than 20000")
        return value
    
    def validate(self,data):             # object level validation 
        if data['name']==data['description']:
            raise serializers.ValidationError("Name and description must not be same")
        return data

class ReviewSerializer(serializers.ModelSerializer):
    apiuser=serializers.StringRelatedField(read_only=True)
    class Meta:
        model=Review
        fields="__all__"


class CarSerializerUsingModel(serializers.ModelSerializer):     
    #  if we are using model serializer then automatically two methods are created that are create(post) and update(put) method 
    #  create custom fields in the model
    #  if we are using model serializer then it automatically generates fiels according to the model attributes 
    discounted_price=serializers.SerializerMethodField()  
    # this name Reviews should be mathched with ralated_name in models.py
    Reviews=ReviewSerializer(many=True,read_only=True) 
    class Meta:
        model=CarList
        fields="__all__"
        # exclude=['carnumber']     # if we want to exclude such fields
    
    # we have created discounted price field so we gonna generate values for it
    def get_discounted_price(self,object):
        print(type(object.price))
        return object.price-5000 if type(object.price)==decimal.Decimal else None
    
    def validate_price(self,value):    # field level validation
        if value<=20000:
            raise serializers.ValidationError("price must be greater than 20000")
        return value
    
    def validate(self,data):             # object level validation 
        if data['name']==data['description']:
            raise serializers.ValidationError("Name and description must not be same")
        return data  
    

class ShowRoomSerializer(serializers.ModelSerializer):
    # showrooms=CarSerializer(many=True,read_only=True)
    # showrooms=serializers.StringRelatedField(many=True)
    # this is a custom field that generates links for all the cars availble in the showroom
    showrooms=serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='car_detail'
    )
    class Meta:
        model=ShowRoomList
        fields="__all__"
          


    
       