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
    """
        Get historical stock price data
        ---
        tags:
          - Stock
        parameters:
          - name: symbol
            in: path
            required: true
            schema:
              type: string
            description: Ticker symbol of the stock (e.g., AAPL, TSLA)
        responses:
          200:
            description: Historical price data fetched successfully
            schema:
              type: object
              properties:
                status:
                  type: boolean
                  example: true
                message:
                  type: string
                  example: "Details Fetched Successfully"
                data:
                  type: array
                  items:
                    type: object
                    properties:
                      date:
                        type: string
                        example: "Fri, 03 May 2024 00:00:00 GMT"
                      open:
                        type: number
                        format: float
                        example: 185.7727942523785
                      high:
                        type: number
                        format: float
                        example: 186.12115543095717
                      low:
                        type: number
                        format: float
                        example: 181.80155578938326
                      close:
                        type: number
                        format: float
                        example: 182.51817321777344
                      volume:
                        type: integer
                        example: 163224100
          404:
            description: Stock not found
            schema:
              type: object
              properties:
                status:
                  type: boolean
                  example: false
                message:
                  type: string
                  example: "Stock not found"
        """
    df = get_price_history_df(symbol.upper())
    if df.empty:
        return send_json_response(response_status=False, message_key="Stock not found",
                                  http_status=HttpStatusCode.NOT_FOUND.value)

    data = df.to_dict(orient="records")
    return send_json_response(response_status=True, message_key="Details Fetched Successfully", data=data,
                              http_status=HttpStatusCode.OK.value)


@login_required
def get_indicators(symbol):
    """
        Get technical indicators for a stock
        ---
        tags:
          - Stock
        parameters:
          - name: symbol
            in: path
            required: true
            schema:
              type: string
            description: Ticker symbol of the stock (e.g., AAPL, TSLA)
          - name: rsi
            in: query
            required: false
            schema:
              type: boolean
            description: Include RSI indicator (true/false)
          - name: macd
            in: query
            required: false
            schema:
              type: boolean
            description: Include MACD indicator (true/false)
          - name: sma
            in: query
            required: false
            schema:
              type: array
              items:
                type: integer
            description: List of SMA periods (e.g., ?sma=20&sma=50)
          - name: ema
            in: query
            required: false
            schema:
              type: array
              items:
                type: integer
            description: List of EMA periods (e.g., ?ema=12&ema=26)
        responses:
          200:
            description: Indicators calculated successfully
            schema:
              type: object
              properties:
                status:
                  type: boolean
                  example: true
                message:
                  type: string
                  example: "Details Fetched Successfully"
                data:
                  type: object
                  properties:
                    rsi:
                      type: object
                      properties:
                        x:
                          type: array
                          items:
                            type: string
                            format: date
                          example: ["2024-05-03", "2024-05-06", "2024-05-07"]
                        y:
                          type: array
                          items:
                            type: number
                            format: float
                          example: [59.11, 69.35, 68.38]
                    # Other indicators (macd, sma, ema) will follow a similar structure
          404:
            description: Indicator calculation error
            schema:
              type: object
              properties:
                status:
                  type: boolean
                  example: false
                message:
                  type: string
                  example: "Error occurred !"
                error:
                  type: object
                  example: {"error": "Invalid symbol"}
          500:
            description: Internal server error
            schema:
              type: object
              properties:
                status:
                  type: boolean
                  example: false
                message:
                  type: string
                  example: "Error occurred !"
                error:
                  type: string
                  example: "Unexpected error"
        """
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
    """
        Fetch and store stock data for a given symbol
        ---
        tags:
          - Stock
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                required:
                  - symbol
                properties:
                  symbol:
                    type: string
                    example: "NVDA"
        responses:
          200:
            description: Data fetched and stored successfully
            schema:
              type: object
              properties:
                status:
                  type: boolean
                  example: true
                message:
                  type: string
                  example: "Data fetched and stored for NVDA"
          400:
            description: Missing symbol in request body
            schema:
              type: object
              properties:
                status:
                  type: boolean
                  example: false
                message:
                  type: string
                  example: "Missing symbol"
          500:
            description: Server error during data fetch
            schema:
              type: object
              properties:
                status:
                  type: boolean
                  example: false
                message:
                  type: string
                  example: "Error occurred !"
                error:
                  type: string
                  example: "Something went wrong while fetching data."
        """
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
