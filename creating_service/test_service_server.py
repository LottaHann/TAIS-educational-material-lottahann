import grpc
from testing import test_pb2_grpc
from testing import test_pb2
import logging
from testing.test_service import test_model
from concurrent import futures
import pickle

class TestingServiceServicer(test_pb2_grpc.TestingServiceServicer):
    def TestModel(self, request, context):
        try:
            #get the model from the bit string
            model_binary = request.model
            model = pickle.loads(model_binary)
            # Test model
            rmse = test_model(model, request.x_test, request.y_test, request.dates_test)
            logging.info("Model tested successfully")
            
            return test_pb2.TestResponse(
                rmse = rmse
            )
        
        except Exception as e:
            logging.exception("Error testing model")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            return test_pb2.TestResponse()
        
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    test_pb2_grpc.add_TestingServiceServicer_to_server(TestingServiceServicer(), server)
    server.add_insecure_port('[::]:50053')
    server.start()
    print("Testing service server started on port 50053.")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()