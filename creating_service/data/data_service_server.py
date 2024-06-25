# data_service_server.py

from concurrent import futures
import grpc
import data_pb2_grpc
import data_pb2
import pandas as pd
from data_service import clean_data
import os
import io
import logging

class DataServiceServicer(data_pb2_grpc.DataServiceServicer):
    def CleanData(self, request, context):
        try:
            # Read CSV content from the request
            csv_content = request.csv_content
            csv_file = io.BytesIO(csv_content)
            
            logging.info("Received CSV data, cleaning...")
            # Clean data
            previous_close, close, dates = clean_data(csv_file)
            logging.info("Data cleaned successfully")
            
            return data_pb2.DataResponse(
                previous_close=previous_close,
                close=close,
                dates=dates
            )
        except Exception as e:
            logging.exception("Error cleaning data")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            return data_pb2.DataResponse()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    data_pb2_grpc.add_DataServiceServicer_to_server(DataServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Data service server started on port 50051.")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
