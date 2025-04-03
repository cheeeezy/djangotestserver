import requests
from django.shortcuts import render

def get_dex_volume(chain="Base"):
    url = f"https://api.llama.fi/overview/dexs/{chain}?excludeTotalDataChart=true&excludeTotalDataChartBreakdown=true&dataType=dailyVolume"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на ошибки HTTP
        data = response.json()
        total_24h = data.get("total24h", 0)  # Объем за 24 часа
        total_30d = data.get("total30d", 0)  # Объем за 30 дней
        return total_24h, total_30d
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return None, None

def home(request):
    # Получаем объемы торгов для Base
    total_24h, total_30d = get_dex_volume(chain="Base")

    # Форматируем значения для отображения
    if total_24h is not None and total_30d is not None:
        # Форматируем total_24h
        if total_24h >= 1_000_000_000:
            total_24h_formatted = f"${total_24h / 1_000_000_000:.2f}B"
        else:
            total_24h_formatted = f"${total_24h / 1_000_000:.2f}M"

        # Форматируем total_30d
        if total_30d >= 1_000_000_000:
            total_30d_formatted = f"${total_30d / 1_000_000_000:.2f}B"
        else:
            total_30d_formatted = f"${total_30d / 1_000_000:.2f}M"
    else:
        total_24h_formatted = "Недоступно"
        total_30d_formatted = "Недоступно"

    context = {
        "chain": "Base",
        "total_24h": total_24h_formatted,
        "total_30d": total_30d_formatted,
    }
    return render(request, "home.html", context)