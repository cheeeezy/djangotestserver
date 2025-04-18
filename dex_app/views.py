import requests
import logging
from django.shortcuts import render
from django.core.cache import cache

logger = logging.getLogger(__name__)

SUPPORTED_CHAINS = ["Ethereum", "Arbitrum", "Solana", "Base", 'Sonic', 'Berachain', 'Aptos', 'Sui', 'BSC', 'All']


def get_dex_volume(chain):
    if chain not in SUPPORTED_CHAINS:
        raise ValueError(f"Unsupported chain: {chain}. Supported chains are: {SUPPORTED_CHAINS}")

    cache_key = f"dex_volume_{chain}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data

    url = f"https://api.llama.fi/overview/dexs/{chain}?excludeTotalDataChart=true&excludeTotalDataChartBreakdown=true&dataType=dailyVolume"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        total_24h = data.get("total24h", 0)
        total_30d = data.get("total30d", 0)
        result = (total_24h, total_30d)
        cache.set(cache_key, result, timeout=3600)  # Кэшируем на 1 час
        return result
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при запросе к API для {chain}: {e}")
        return None, None


def format_volume(value):
    """Форматирует значение объема в читаемый вид: $X.XXB или $X.XXM"""
    if value is None:
        return "Недоступно"
    if value >= 1_000_000_000:
        return f"${value / 1_000_000_000:.2f}B"
    else:
        return f"${value / 1_000_000:.2f}M"


def home(request):
    chain_data = {}
    for chain in SUPPORTED_CHAINS:
        total_24h, total_30d = get_dex_volume(chain=chain)
        chain_data[chain] = {
            "total_24h": format_volume(total_24h),
            "total_30d": format_volume(total_30d),
        }

    context = {
        "chain_data": chain_data,
    }
    return render(request, "home.html", context)