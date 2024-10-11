from django.db.models import QuerySet
from rest_framework.response import Response


# noinspection PyProtectedMember
def query_to_data(query: QuerySet, request, to_exel=False, to_json=False):
    """
        :param to_json:
        :param to_exel:
        :param request:
        :type query: object

    """
    # sort
    sort_field = request.GET.get('sort')
    if sort_field is not None:
        if sort_field[0] == "-":
            sort_field = sort_field[1:]
            query = query.order_by(f"-{sort_field}")
        else:
            query = query.order_by(sort_field)

    # filter
    for i in request.GET:
        if i.startswith("filter["):
            field = i[7:-1]
            try:
                new_query = query.none()
                for j in request.GET[i].split(","):
                    new_query = new_query | query.filter(**{field: j})
                query = new_query
            except Exception as e:
                if to_json:
                    return {
                        "error": str(e),
                        "status": 400
                    }
                return Response({
                    "error": str(e)
                }, status=400)

    # filter with date
    if "from" in request.GET and "until" in request.GET and "field" in request.GET:
        field = request.GET["field"]
        try:
            query = query.filter(**{f"{field}__gte": request.GET["from"], f"{field}__lte": request.GET["until"]})
        except Exception as e:
            return Response({
                "error": str(e)
            }, status=400)
    # search
    if "search" in request.GET:
        new_query = query.none()
        for field in query.model._meta.fields:
            remove_fields = ["ForeignKey", "DateTimeField", "DateField", "TimeField", "BooleanField"]
            if field.name == "id" or field.get_internal_type() in remove_fields:
                continue
            new_query = new_query | query.filter(**{f"{field.name}__icontains": request.GET["search"]})

        query = new_query

    # pagination
    all_foreign_keys = []
    for field in query.model._meta.fields:
        if field.get_internal_type() == "ForeignKey":
            all_foreign_keys.append(field.name)

    data = {"all_data": query.count()}
    page = int(request.GET.get('page', 1))
    if page < 1:
        page = 1
    per_page = int(request.GET.get('per_page', 10))
    if per_page < 1:
        per_page = 1
    data["page"] = page
    data["per_page"] = per_page*100 if to_exel else per_page
    data["data"] = []
    data["last_page"] = query.count() // per_page + 1
    data["next_page_url"] = ""
    data["prev_page_url"] = ""
    data["foreignKeys"] = all_foreign_keys
    data["from"] = (page - 1) * per_page + 1
    data["to"] = page * per_page
    if data["to"] > data["all_data"]:
        data["to"] = data["all_data"]
    if page > 1:
        data["prev_page_url"] = f"?page={page - 1}&per_page={per_page}"
    if page < data["last_page"]:
        data["next_page_url"] = f"?page={page + 1}&per_page={per_page}"
    query = query.values()[(page - 1) * per_page:page * per_page]

    # include
    if "include" in request.GET:
        new_data = []
        include = request.GET["include"].split(",")
        for i in query:
            for j in include:
                if j in all_foreign_keys:
                    i[j] = query.model._meta.get_field(j).related_model.objects.filter(
                        id=i[j + "_id"]).values()[0] if i[j + "_id"] is not None and query.model._meta.get_field(
                        j).related_model.objects.filter(id=i[j + "_id"]).exists() else None
            new_data.append(i)
        data["data"] = list(new_data)
        if to_json:
            return data
        return Response(data)

    data["data"] = list(query)

    if to_json:
        return data

    return Response(data)
