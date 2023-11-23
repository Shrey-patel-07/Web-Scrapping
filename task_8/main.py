import threading
from time import sleep

# Import WebSocket from the unified_trading module.
from pybit.unified_trading import WebSocket

# Create a new thread for the WebSocket communication
def websocket_thread():
    # Create a WebSocket instance
    ws = WebSocket(testnet=True, channel_type="spot")

    # Define the orderbook handler function
    def handle_orderbook(message):
        # Print the orderbook data
        print(message)
        orderbook_data = message["data"]

    # Subscribe to the orderbook stream
    ws.orderbook_stream(50, "BTCUSDT", handle_orderbook)

    # Keep the WebSocket connection alive
    while True:
        sleep(1)

# Start the WebSocket thread
websocket_thread_process = threading.Thread(target=websocket_thread)
websocket_thread_process.start()

# Keep the main thread alive
while True:
    sleep(1)
