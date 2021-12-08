import ujson
from utility import log
from sys import print_exception


class HandleException:

    def __init__(self, mqtt):
        log("Initializing exception handler...")
        self.exceptionCount = 0
        self.mqtt = mqtt

    def handleException(self, exception, description, showDescription, showException, increaseExceptionCount, publishError):
        if showDescription:
            log("HandleException: "+description)

        if showException:
            print_exception(exception)

        if increaseExceptionCount:
            self.addToExceptionCount()

        if publishError:
            try:
                payload = ujson.dumps({"error":{"desc":str(description),"exp":str(exception)}})
                print(payload)
                self.mqtt.publishErrorEvent(payload)
            except Exception as ex:
                print_exception(ex)
                self.addToExceptionCount()

    def addToExceptionCount(self):
        self.exceptionCount = self.exceptionCount + 1

    def resetExceptionCount(self):
        self.exceptionCount = 0

    def getExceptionCount(self):
        return self.exceptionCount
