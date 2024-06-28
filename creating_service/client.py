import grpc
from data import data_pb2_grpc
from data import data_pb2
from train import train_pb2_grpc
from train import train_pb2
from testing import test_pb2_grpc
from testing import test_pb2



def run():
    cleaned_data = None
    model = None
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = data_pb2_grpc.DataServiceStub(channel)
        csv_file_path = './MSFT.US.csv'
        
        try:
            # Read CSV file content as bytes
            with open(csv_file_path, 'rb') as f:
                csv_content = f.read()

            # Create request with CSV content
            request = data_pb2.DataRequest(csv_content=csv_content)
            
            # Call the CleanData method
            response = stub.CleanData(request)

            if response.x_train and response.x_test and response.y_train and response.y_test and response.dates_train and response.dates_test:
                #print("x_trian:", response.x_train)
                #print("x_test:", response.x_test)
                #print("y_train:", response.y_train)
                #print("y_test:", response.y_test)
                #print("Dates Train:", response.dates_train)
                #print("Dates Test:", response.dates_test)
                cleaned_data = response
                #print("Data cleaned successfully. Training model...")

            else:
                print("No data returned or some fields are empty.")
        except grpc.RpcError as e:
            print(f"RPC failed: {e.code()} - {e.details()}")

    with grpc.insecure_channel('localhost:50052') as channel:
        stub = train_pb2_grpc.TrainingServiceStub(channel)
        try:
            x_train = cleaned_data.x_train
            y_train = cleaned_data.y_train
            response = stub.TrainModel(train_pb2.TrainRequest(x_train=x_train, y_train=y_train))

            if response.model:
                model = response.model
                print("Model trained successfully")
            else:
                print("Model not trained")
        except grpc.RpcError as e:
            print(f"RPC failed: {e.code()} - {e.details()}")

    with grpc.insecure_channel('localhost:50053') as channel:
        stub = test_pb2_grpc.TestingServiceStub(channel)
        try:
            x_test = cleaned_data.x_test
            y_test = cleaned_data.y_test
            dates_test = cleaned_data.dates_test
            response = stub.TestModel(test_pb2.TestRequest(model=model, x_test=x_test, y_test=y_test, dates_test=dates_test))

            if response.rmse:
                print(f"Model tested successfully. Root mean squared error: {response.rmse}")
            else:
                print("Model not tested")
        except grpc.RpcError as e:
            print(f"RPC failed: {e.code()} - {e.details()}")
        



if __name__ == '__main__':
    run()
