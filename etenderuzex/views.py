import json

from rest_framework.response import Response
from rest_framework.views import APIView

import requests

from Etender.functions import query_to_data
from xariduzex.models import XariduzexCheck
from .models import *


class CategoryAPIView(APIView):
    @staticmethod
    def get(request):
        categories = Category.objects.all()
        data = query_to_data(categories, request)
        return data

    @staticmethod
    def post(request):
        data = request.data
        if not Category.objects.filter(category_id=data['category_id']).exists():
            Category.objects.create(
                category_id=data['category_id'],
                name=data['name']
            )
        return Response(status=201)


class ProductAPIView(APIView):
    @staticmethod
    def get(request):
        products = Product.objects.all()
        data = query_to_data(products, request)
        return data


class TenderAPIView(APIView):
    @staticmethod
    def get(request):
        tenders = Tender.objects.all()
        data = query_to_data(tenders, request, to_json=True)
        for i in data['data']:
            i["products"] = []
            for j in TenderProduct.objects.filter(tender_id=i['id']):
                i["products"].append(
                    {
                        "product_id": j.product.product_id,
                        "name": j.product.name,
                        "category": j.product.category.name,
                        "product_code": j.product.product_code
                    }
                )
        return Response(data, status=200)

    @staticmethod
    def post(request):
        data = {"TypeId": 2, "From": 1, "To": 260, "System_Id": 0}
        response = requests.post('https://apietender.uzex.uz/api/common/TradeList', json=data).json()
        checked_tenders = CheckedTender.objects.all()
        new_tenders = []
        for i in response:
            if not checked_tenders.filter(tender_id=i['id']).exists():
                new_tender = requests.get(f'https://apietender.uzex.uz/api/common/GetTrade/{i["id"]}/0').json()
                budget_products = json.loads(new_tender['budget_products'])
                if len(budget_products) == 0:
                    CheckedTender.objects.create(tender_id=i['id'], category_id=budget_products['Category_Id'])
                    continue

                categories = Category.objects.all()
                if not categories.filter(category_id=budget_products[0]['Category_Id']).exists():
                    CheckedTender.objects.create(tender_id=i['id'], category_id=budget_products[0]['Category_Id'])
                    continue

                for j in budget_products:
                    if not Product.objects.filter(product_id=j['Product_Id']).exists():
                        Product.objects.create(
                            product_id=j['Product_Id'],
                            name=j['Product_Name'],
                            category=Category.objects.get(category_id=budget_products[0]['Category_Id']),
                            product_code=j['Product_Code']
                        )

                tender = Tender.objects.create(
                    tender_id=i['id'], name=i['name'], display_number=i['display_no'], start_date=i['start_date'],
                    end_date=i['end_date'], clarific_date=i['clarific_date'], cost=i['cost'], currency=i['currency_id'],
                    seller_name=i['seller_name'], seller_tin=i['seller_tin'], region_name=i['region_name'],
                    district_name=i['district_name'], seller_id=i['seller_id'], category=Category.objects.get(
                        category_id=budget_products[0]['Category_Id']), type="1",
                    url=f'https://etender.uzex.uz/lot/{i["id"]}'
                )
                url=f'https://apietender.uzex.uz/api/common/GetTrade/{i["id"]}/0'
                data = requests.get(url).json()['budget_products']
                data = json.loads(data)
                for j in data:
                    TenderProduct.objects.create(
                        tender=tender,
                        product=Product.objects.get(product_id=j['Product_Id']) if Product.objects.filter(
                            product_id=j['Product_Id']).exists() else None
                    )

                new_tenders.append(
                    {
                        "tender_id": i['id'],
                        "name": i['name'],
                        "display_number": i['display_no'],
                        "start_date": i['start_date'],
                        "end_date": i['end_date'],
                        "clarific_date": i['clarific_date'],
                        "cost": i['cost'],
                        "currency": i['currency_id'],
                        "seller_name": i['seller_name'],
                        "seller_tin": i['seller_tin'],
                        "region_name": i['region_name'],
                        "district_name": i['district_name'],
                        "seller_id": i['seller_id'],
                        "category_id": budget_products[0]['Category_Id'],
                        "products": data
                    }
                )
                CheckedTender.objects.create(tender_id=i['id'], category_id=budget_products[0]['Category_Id'])
        return Response({
            "new_tenders": new_tenders
        })

    @staticmethod
    def put(request):
        data = {"TypeId": 1, "From": 1, "To": 1000, "System_Id": 0}
        response = requests.post('https://apietender.uzex.uz/api/common/TradeList', json=data).json()
        checked_tenders = CheckedTender.objects.all()
        new_tenders = []
        for i in response:
            if not checked_tenders.filter(tender_id=i['id']).exists():
                new_tender = requests.get(f'https://apietender.uzex.uz/api/common/GetTrade/{i["id"]}/0').json()
                budget_products = json.loads(new_tender['budget_products'])
                if len(budget_products) == 0:
                    CheckedTender.objects.create(tender_id=i['id'], category_id=budget_products['Category_Id'])
                    continue

                categories = Category.objects.all()
                if not categories.filter(category_id=budget_products[0]['Category_Id']).exists():
                    CheckedTender.objects.create(tender_id=i['id'], category_id=budget_products[0]['Category_Id'])
                    continue

                Tender.objects.create(
                    tender_id=i['id'], name=i['name'], display_number=i['display_no'], start_date=i['start_date'],
                    end_date=i['end_date'], clarific_date=i['clarific_date'], cost=i['cost'], currency=i['currency_id'],
                    seller_name=i['seller_name'], seller_tin=i['seller_tin'], region_name=i['region_name'],
                    district_name=i['district_name'], seller_id=i['seller_id'], category=Category.objects.get(
                        category_id=budget_products[0]['Category_Id']), type="2", url=f'https://etender.uzex.uz/lot/{i["id"]}'
                )
                for j in budget_products:
                    if not Product.objects.filter(product_id=j['Product_Id']).exists():
                        Product.objects.create(
                            product_id=j['Product_Id'],
                            name=j['Product_Name'],
                            category=Category.objects.get(category_id=budget_products[0]['Category_Id']),
                            product_code=j['Product_Code']
                        )
                    TenderProduct.objects.create(
                        tender=Tender.objects.get(tender_id=i['id']),
                        product=Product.objects.get(product_id=j['Product_Id'])
                    )
                new_tenders.append(
                    {
                        "tender_id": i['id'],
                        "name": i['name'],
                        "display_number": i['display_no'],
                        "start_date": i['start_date'],
                        "end_date": i['end_date'],
                        "clarific_date": i['clarific_date'],
                        "cost": i['cost'],
                        "currency": i['currency_id'],
                        "seller_name": i['seller_name'],
                        "seller_tin": i['seller_tin'],
                        "region_name": i['region_name'],
                        "district_name": i['district_name'],
                        "seller_id": i['seller_id'],
                        "category_id": budget_products[0]['Category_Id'],
                    }
                )
                CheckedTender.objects.create(tender_id=i['id'], category_id=budget_products[0]['Category_Id'])
        return Response({
            "new_auctions": new_tenders
        })


class CheckedTenderAPIView(APIView):
    @staticmethod
    def get(request):
        checked_tenders = CheckedTender.objects.all()
        tenders=[]
        for i in checked_tenders:
            if i.tender_id not in tenders:
                tenders.append(i.tender_id)
            else:
                checked_tenders.filter(tender_id=i.tender_id).delete()
        data = query_to_data(checked_tenders, request)
        return data


class XaridUzexAPIView(APIView):
    @staticmethod
    def get(request):
        f=1
        new_tenders=[]
        data = {"region_ids": [], "from": f, "to": f+20}
        response = requests.post('https://xarid-api-auction.uzex.uz/Common/GetMinimizedLotsList', json=data).json()
        while len(response) > 0:
            for i in response:
                if not XariduzexCheck.objects.filter(tender_id=i['id']).exists():
                    if Category.objects.filter(name=i['category_name']).exists():
                        new_data = requests.get(f'https://xarid-api-auction.uzex.uz/Common/GetLot/{i["id"]}').json()
                        if not Tender.objects.filter(tender_id=i['id']).exists():
                            Tender.objects.create(
                                tender_id=i['id'],
                                name="-",
                                category=Category.objects.get(name=i['category_name']),
                                type="2",
                                display_number=i['display_no'],
                                start_date=new_data['start_date'],
                                end_date=new_data['end_date'],
                                cost=i["start_cost"],
                                currency=i["currency_id"],
                                seller_name=new_data["customer_name"],
                                region_name=new_data["region_name"],
                                url=f"https://xarid.uzex.uz/auction/detail/{i['id']}"
                            )
                            new_tenders.append(
                                {
                                    "tender_id": i['id'],
                                    "name": "-",
                                    "display_number": i['display_no'],
                                    "start_date": i['start_date'],
                                    "end_date": new_data['end_date'],
                                    "clarific_date": None,
                                    "cost": i["start_cost"],
                                    "currency": i["currency_id"],
                                    "seller_name": new_data["customer_name"],
                                    "seller_tin": None,
                                    "region_name": new_data["region_name"],
                                    "district_name": None,
                                    "seller_id": None,
                                    "category_id": i['category_name']
                                }
                        )
                    XariduzexCheck.objects.create(tender_id=i['id'], category=i['category_name'])
            f += 20
            data = {"region_ids": [], "from": f, "to": f + 20}
            response = requests.post('https://xarid-api-auction.uzex.uz/Common/GetMinimizedLotsList', json=data).json()
        return Response({"new_auctions": new_tenders}, status=200)


class TelegramUserAPIView(APIView):
    @staticmethod
    def get(request):
        telegram_users = TelegramUser.objects.all()
        data = query_to_data(telegram_users, request)
        return data

    @staticmethod
    def post(request):
        data = request.data
        if not TelegramUser.objects.filter(user_id=data['user_id']).exists():
            TelegramUser.objects.create(
                user_id=data['user_id'],
                username=data['username'],
                first_name=data['first_name'],
                last_name=data['last_name']
            )
        return Response(status=201)

    @staticmethod
    def delete(request):
        data = request.data
        if TelegramUser.objects.filter(user_id=data['user_id']).exists():
            TelegramUser.objects.filter(user_id=data['user_id']).delete()
        return Response(status=204)

    @staticmethod
    def put(request):
        data = request.data
        if TelegramUser.objects.filter(user_id=data['user_id']).exists():
            TelegramUser.objects.filter(user_id=data['user_id']).update(
                username=data['username'],
                first_name=data['first_name'],
                last_name=data['last_name']
            )
        return Response(status=200)

