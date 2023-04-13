from rest_framework import viewsets
from rest_framework.permissions import  BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication

from ride_app.models import Ride
from ride_app.serializer.ride import RideSerializer


class RidesPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST']:
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in ['PATCH', 'PUT', 'DELETE']:
            return request.user.is_authenticated and request.user.id == obj.user_id
        return True


class RidesViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [RidesPermissions]
    serializer_class = RideSerializer

    def create(self, request, *args, **kwargs):
        # Set the user field to the current user based on the JWT token
        request.data['user'] = request.user.id

    #     # Call the default create method with the modified data
        return super().create(request, *args, **kwargs)

    def get_ride(self):
        qs = self.queryset
        print(qs)
        if 'user' in self.request.query_params:
            qs = qs.filter(user=self.request.query_params['user'])
        if 'from_location' in self.request.query_params:
            qs = qs.filter(from_location=self.request.query_params['from_location'])
        if 'to_location' in self.request.query_params:
            qs = qs.filter(to_location=self.request.query_params['to_location'])
        if 'datetime' in self.request.query_params:
            qs = qs.filter(datetime=self.request.query_params['datetime'])
        if 'is_request' in self.request.query_params:
            qs = qs.filter(is_request=self.request.query_params['is_request'])
        if 'price' in self.request.query_params:
            qs = qs.filter(price=self.request.query_params['price'])
        if 'status' in self.request.query_params:
            qs = qs.filter(status=self.request.query_params['status'])

        return qs
