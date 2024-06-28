import grpc
from train import train_pb2_grpc
from train import train_pb2
from train.training_service import train_model
import logging
from concurrent import futures

class TrainingServiceServicer(train_pb2_grpc.TrainingServiceServicer):
    def TrainModel(self, request, context):
        try:
            # Train model
            model_binary = train_model(request.x_train, request.y_train)
            logging.info("Model trained successfully")
            
            return train_pb2.TrainResponse(
                model=model_binary
            )
        
        except Exception as e:
            logging.exception("Error training model")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            return train_pb2.TrainResponse()
        

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    train_pb2_grpc.add_TrainingServiceServicer_to_server(TrainingServiceServicer(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("Training service server started on port 50052.")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
