from django.shortcuts import render

def wallet_view(request):
    # Представление для страницы кошелька
    return render(request, "wallet.html")