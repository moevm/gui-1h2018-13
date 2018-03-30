from threading import Thread


def makeRequest(function, *args, **kwargs):
    """
    Runs function in a new thread. easy peasy.
    make request async like without loop.
    """

    def newFunc(*args, **kwargs):
        def wrapper():
            function(*args, **kwargs)

        Thread(target=wrapper).start()

    return newFunc
