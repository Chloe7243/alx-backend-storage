from pymongo import MongoClient


if __name__ == "__main__":
    """
    provides stats about nginx logs
    """
    nginx_collection = MongoClient("mongodb://127.0.0.1:27017").logs.nginx

    n_logs = nginx_collection.count_documents({})
    print(f"{n_logs} logs")

    print("Methods:")
    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        method_count = nginx_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {method_count}")

    status_check_count = nginx_collection.count_documents(
        {"method": "GET", "path": "/status"}
    )
    print(f"{status_check_count} status check")
