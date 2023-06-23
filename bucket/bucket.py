def upload_file_to_s3(s3_client, bucket_name, filename):
    file_extension = filename.split(".")[-1]
    response = s3_client.upload_file(Filename=filename, Bucket=bucket_name, Key=f"{filename}")
    print("file uploaded")
    return response
