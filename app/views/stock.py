from flask import Blueprint, jsonify, request
from flask_login import login_required

from app.indicators.utils import get_price_history_df

from app.services.indicator_service import calculate_indicators
from app.services.stock_fetcher import fetch_and_store_stock_data
from app.utils.common import send_json_response
from app.utils.constants import HttpStatusCode

stock_bp = Blueprint("stock", __name__)


@login_required
def get_stock_history(symbol):
    df = get_price_history_df(symbol.upper())
    if df.empty:
        return send_json_response(response_status=False, message_key="Stock not found",
                                  http_status=HttpStatusCode.NOT_FOUND.value)

    data = df.to_dict(orient="records")
    return send_json_response(response_status=True, message_key="Details Fetched Successfully", data=data,
                              http_status=HttpStatusCode.OK.value)


@login_required
def get_indicators(symbol):
    try:
        rsi = request.args.get("rsi", "false").lower() == "true"
        macd = request.args.get("macd", "false").lower() == "true"
        sma = request.args.getlist("sma", type=int)  # ?sma=20&sma=50
        ema = request.args.getlist("ema", type=int)  # ?ema=12&ema=26

        indicators = {
            "rsi": rsi,
            "macd": macd,
            "sma": sma if sma else [],
            "ema": ema if ema else [],
        }

        result = calculate_indicators(symbol, indicators)

        if "error" in result:
            return send_json_response(response_status=False, message_key="Error occurred !", error=result,
                                      http_status=HttpStatusCode.NOT_FOUND.value)

        return send_json_response(response_status=True, message_key="Details Fetched Successfully", data=result,
                                  http_status=HttpStatusCode.OK.value)

    except Exception as e:
        return send_json_response(response_status=False, message_key="Error occurred !", error=str(e),
                                  http_status=HttpStatusCode.INTERNAL_SERVER_ERROR.value)


@login_required
def fetch_stock_data():
    symbol = request.json.get("symbol")
    if not symbol:
        return send_json_response(response_status=False, message_key="Missing symbol",
                                  http_status=HttpStatusCode.BAD_REQUEST.value)

    try:
        fetch_and_store_stock_data(symbol)
        return send_json_response(response_status=True, message_key=f"Data fetched and stored for {symbol}",
                                  http_status=HttpStatusCode.OK.value)
    except Exception as e:
        return send_json_response(response_status=False, message_key="Error occurred !", error=str(e),
                                  http_status=HttpStatusCode.INTERNAL_SERVER_ERROR.value)
