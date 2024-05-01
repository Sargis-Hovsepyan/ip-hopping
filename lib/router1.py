from router import Router


if __name__ == "__main__":
    router = Router('127.0.0.1', 7001, '127.0.0.1')

    address = {'source': '127.0.0.1:5555', 'destination': '127.0.0.1:5556'}
    router.routing_table.append(address)

    router.start()
