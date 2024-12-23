import uuid

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.response import Response
from sslcommerz_lib import SSLCOMMERZ

from course.models import CourseModel

from . import models, serializers


@method_decorator(csrf_exempt, name="dispatch")
class CheckViewset(viewsets.ModelViewSet):
    queryset = models.CheckOut.objects.all()
    serializer_class = serializers.PaymentSerializers

    def create(self, request, *args, **kwargs):
        user_id = request.data.get("user_id")
        course_id = request.data.get("course_id")
        price = request.data.get("price")
        user = User.objects.get(id=user_id)
        course = CourseModel.objects.get(id=course_id)

        # print(user.email, course.name)

        data_to_save = {"user_id": user_id, "course_id": course_id, "price": price}
        serializer = self.get_serializer(data=data_to_save)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        settings = {
            "store_id": "abc6614dbee40ed8",
            "store_pass": "abc6614dbee40ed8@ssl",
            "issandbox": True,
        }
        sslcz = SSLCOMMERZ(settings)
        post_body = {}
        post_body["total_amount"] = price
        post_body["currency"] = "BDT"
        post_body["tran_id"] = uuid.uuid4()
        post_body["success_url"] = f"https://quizzone-frontend.netlify.app/"
        post_body["fail_url"] = "your fail url"
        post_body["cancel_url"] = f"https://quizzone-frontend.netlify.app/"
        post_body["emi_option"] = 0
        post_body["cus_name"] = "name"
        post_body["cus_email"] = user.email
        post_body["cus_phone"] = "01713807932"
        post_body["cus_add1"] = "Bishwanath"
        post_body["cus_city"] = "Sylhet"
        post_body["cus_country"] = "Bangladesh"
        post_body["shipping_method"] = "NO"
        post_body["multi_card_name"] = ""
        post_body["num_of_item"] = 1
        post_body["product_name"] = course.name
        post_body["product_category"] = "Course"
        post_body["product_profile"] = "Education"

        response = sslcz.createSession(post_body)  # API response
        # print(response)

        # return Response({"user_id": user_id, "course_id":course_id, "price": price,})
        return JsonResponse({"GatewayPageURL": response["GatewayPageURL"]})

    def perform_create(self, serializer):
        serializer.save()
