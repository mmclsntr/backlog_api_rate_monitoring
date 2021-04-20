import datetime
import time
import json
import os

import cw_metric
import backlog_api


CW_METRIC_NAMESPACE = "BacklogApiRate"


def main(event, context):
    # Backlogのパラメータ
    backlog_space_key = os.environ.get("backlog_space_key")
    backlog_api_key_list = os.environ.get("backlog_api_key_list")
    monitoring_period = int(os.environ.get("monitoring_period"))
    monitoring_count = int(os.environ.get("monitoring_count"))

    backlog_api_keys = backlog_api_key_list.split(",")

    for i in range(monitoring_count):
        print("Check count: {}".format(i + 1))
        start_time = datetime.datetime.now().timestamp()
        print("Start time: {}".format(start_time))
        for backlog_api_key in backlog_api_keys:
            res = backlog_api.get_ratelimit(backlog_space_key,
                                            backlog_api_key)
            print("API Key: {}".format(backlog_api_key[:5]))
            for api_type, info in res["rateLimit"].items():
                limit = info["limit"]
                remaining = info["remaining"]
                usage = limit - remaining
                print("{}: Limit: {} Remaining: {} Usage: {}".format(api_type, limit, remaining, usage))
                dim = {
                    "ApiKey": backlog_api_key[:5],
                    "ApiType": api_type
                }
                cw_metric.put_metric(
                    CW_METRIC_NAMESPACE,
                    "Limit",
                    dim,
                    limit
                )
                cw_metric.put_metric(
                    CW_METRIC_NAMESPACE,
                    "Remaining",
                    dim,
                    remaining
                )
                cw_metric.put_metric(
                    CW_METRIC_NAMESPACE,
                    "Usage",
                    dim,
                    usage
                )
        end_time = datetime.datetime.now().timestamp()
        elapsed = end_time - start_time
        print("End time: {}".format(end_time))
        print("Elapsed time: {}".format(elapsed))
        diff = monitoring_period - elapsed
        sleep_time = diff if diff > 0 else 0
        print("Sleep: {}".format(sleep_time))
        time.sleep(sleep_time)
