from time import sleep

# Import WebSocket from the unified_trading module.
from pybit.unified_trading import WebSocket

ws = WebSocket(
    testnet=True,
    channel_type="spot",
)


# Let's fetch the orderbook for BTCUSDT. First, we'll define a function.
def handle_orderbook(message):
    # I will be called every time there is new orderbook data!
    print(message)
    orderbook_data = message["data"]


# Now, we can subscribe to the orderbook stream and pass our arguments:
# our depth, symbol, and callback function.
ws.orderbook_stream(50, "BTCUSDT", handle_orderbook)

while True:
    # This while loop is required for the program to run.
    sleep(1)
