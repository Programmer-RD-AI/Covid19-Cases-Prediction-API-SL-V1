from api import app
from updating import update
import threading
if __name__ == "__main__":
    print('g')
    threading.Thread(target=app.run(threaded=True, port=5000)).start()
    print('g')
    threading.Thread(target=update()).start()
