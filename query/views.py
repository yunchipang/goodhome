from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.db import connection
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@require_http_methods(["POST"])
def execute_query(request):
    try:
        query = request.POST.get('query', '')
        # security consideration: Ensure the query is safe, consider allowing only select statements
        if not query.lower().startswith('select'):
            return HttpResponse("Unsupported query type.", status=400)

        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            return JsonResponse({"columns": columns, "rows": [dict(zip(columns, row)) for row in cursor.fetchall()]})
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=400)
