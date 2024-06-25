import grpc
import data_pb2_grpc
import data_pb2

def run():
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

            if response.previous_close and response.close and response.dates:
                print("Previous Close:", response.previous_close)
                print("Close:", response.close)
                print("Dates:", response.dates)
            else:
                print("No data returned or some fields are empty.")
        except grpc.RpcError as e:
            print(f"RPC failed: {e.code()} - {e.details()}")

if __name__ == '__main__':
    run()
