import grpc
import data_pb2_grpc
import data_pb2




def run():
    cleaned_data = None
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
                print("x_trian:", response.x_train)
                print("x_test:", response.x_test)
                print("y_train:", response.y_train)
                print("y_test:", response.y_test)
                print("Dates Train:", response.dates_train)
                print("Dates Test:", response.dates_test)
            else:
                print("No data returned or some fields are empty.")
        except grpc.RpcError as e:
            print(f"RPC failed: {e.code()} - {e.details()}")


if __name__ == '__main__':
    run()
